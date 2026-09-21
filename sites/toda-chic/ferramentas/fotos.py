#!/usr/bin/env python3
"""Prepara as fotos de produto da Toda Chic para a web.

Lê catalogo.json, descobre que fotos são usadas, e para cada uma:
  1. corta a faixa "Toda chic" do topo (deteção por desvio-padrão por linha)
  2. apaga os rótulos, preços e ícones sobrepostos (inpainting)
  3. recorta a 4:5 e grava em media/produtos/ a 880px de largura

Correr a partir de sites/toda-chic:  python3 ferramentas/fotos.py
"""
import json, os, sys
import numpy as np
import cv2
from PIL import Image, ImageStat

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
LARGURA = 880
QUALIDADE = 80

indice = [l.rstrip('\n') for l in open('fotos/indice-novas.txt', encoding='utf-8')]


def caminho(n):
    return indice[n - 1]


def fim_da_faixa(im):
    """A faixa "Toda chic" é texto preto: linhas com muitas transições claro/escuro.
    O título grosso tem 14-60 transições e >35% de pixels escuros; a linha
    pequena repetida tem >80 transições. Uma peça de roupa escura tem poucas."""
    g = np.array(im.convert('L')); H, W = g.shape
    escuro = g < 100
    linhas = []
    for y in range(int(H * 0.24)):
        r = escuro[y]; frac = r.mean(); trans = np.count_nonzero(r[1:] != r[:-1])
        linhas.append((frac > 0.3 and 14 <= trans <= 70) or trans > 80)
    inicio = next((y for y in range(int(H * 0.15)) if linhas[y]), None)
    if inicio is None: return 0
    fim = inicio; folga = int(H * 0.04)
    y = inicio
    while y < len(linhas):
        if linhas[y]: fim = y; y += 1
        elif y - fim > folga: break
        else: y += 1
    return min(fim + int(H * 0.012), int(H * 0.24))


def componentes(bin_):
    n, lab, stats, _ = cv2.connectedComponentsWithStats(bin_.astype(np.uint8), 8)
    return [(i, *stats[i]) for i in range(1, n)], lab


def mascara_sobreposicoes(arr):
    """Marca caixas brancas com texto, preços soltos, ícone de som e crachá 1/2."""
    H, W = arr.shape[:2]
    g = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    sat = arr.max(axis=2).astype(int) - arr.min(axis=2).astype(int)
    m = np.zeros((H, W), np.uint8)

    # 1. caixas brancas retangulares com texto dentro (rótulos "Top rosa Barbie 12.50€")
    branco = (arr.min(axis=2) > 238)
    for i, x, y, w, h, a in componentes(branco)[0]:
        if 0.10 * W < w < 0.85 * W and 0.025 * H < h < 0.30 * H and y > 0.05 * H:
            texto = (g[y:y + h, x:x + w] < 160).mean()
            # caixa quadrada com pouco texto, ou balões de fala (cantos redondos) cheios de texto
            if (a > 0.62 * w * h and texto > 0.004) or (a > 0.45 * w * h and texto > 0.08):
                m[max(0, y - 3):y + h + 3, max(0, x - 3):x + w + 3] = 255

    # 2. texto escuro ou vermelho solto no terço de baixo (preços "12.50€", "Tam-34")
    escuro = (g < 118) | ((arr[..., 0] > 150) & (arr[..., 1] < 90) & (arr[..., 2] < 90))
    comps, lab = componentes(escuro)
    pequenos = np.zeros((H, W), np.uint8)
    for i, x, y, w, h, a in comps:
        if y > 0.66 * H and h < 0.12 * H and w < 0.45 * W and a > 6:
            pequenos[lab == i] = 1
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (max(3, int(W * 0.035)), max(3, int(H * 0.012))))
    grupos = cv2.morphologyEx(pequenos, cv2.MORPH_CLOSE, k)
    for i, x, y, w, h, a in componentes(grupos)[0]:
        if h < 0.16 * H and w < 0.7 * W and a > 40:
            m[max(0, y - 4):y + h + 4, max(0, x - 4):x + w + 4] = 255

    # 3. ícone de som (círculo cinzento) no canto inferior direito
    cinza = (g > 95) & (g < 200) & (sat < 22)
    cinza[: int(H * 0.84)] = False; cinza[:, : int(W * 0.78)] = False
    for i, x, y, w, h, a in componentes(cinza)[0]:
        if 0.02 * W < w < 0.08 * W and 0.6 < w / max(h, 1) < 1.6:
            m[max(0, y - 4):y + h + 4, max(0, x - 4):x + w + 4] = 255

    # 4. crachá "1/2" no canto superior direito
    cracha = (g > 50) & (g < 125) & (sat < 30)
    cracha[int(H * 0.09):] = False; cracha[:, : int(W * 0.78)] = False
    for i, x, y, w, h, a in componentes(cracha)[0]:
        if 0.03 * W < w < 0.12 * W and 0.015 * H < h < 0.06 * H and a > 0.5 * w * h:
            m[max(0, y - 4):y + h + 4, max(0, x - 4):x + w + 4] = 255

    return cv2.dilate(m, np.ones((5, 5), np.uint8))


def limpa(im):
    arr = np.array(im.convert('RGB'))
    m = mascara_sobreposicoes(arr)
    if m.any():
        arr = cv2.inpaint(arr, m, 7, cv2.INPAINT_TELEA)
    return Image.fromarray(arr), (m > 0).mean()


def recorta_4_5(im, foco):
    w, h = im.size
    alvo = 1.25
    if h / w > alvo:
        nh = int(w * alvo)
        if foco == 'topo': y0 = 0
        elif foco == 'fundo': y0 = h - nh
        else: y0 = (h - nh) // 2
        im = im.crop((0, y0, w, y0 + nh))
    elif h / w < alvo:
        nw = int(h / alvo)
        x0 = (w - nw) // 2
        im = im.crop((x0, 0, x0 + nw, h))
    return im


def grava(im, dest):
    if im.width > LARGURA:
        im = im.resize((LARGURA, int(im.height * LARGURA / im.width)), Image.LANCZOS)
    im.save(dest, 'JPEG', quality=QUALIDADE, optimize=True, progressive=True)


def celula(ficha, cel):
    im = Image.open(caminho(ficha)).convert('RGB')
    w, h = im.size
    cw, ch = w / 2, h / 3
    c, r = (cel - 1) % 2, (cel - 1) // 2
    return im.crop((int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch)))


# fotos em que o rótulo está por cima da peça: cortar por baixo antes de tudo (fração da altura)
AJUSTES = {60: 0.66, 70: 0.64,
           # manequins com o rótulo por baixo da peça: corta em vez de pintar
           39: .78, 40: .80, 41: .74, 42: .74, 44: .76, 45: .75, 59: .78, 81: .72, 85: .72,
           91: .84, 93: .85, 95: .80, 72: .82}

FOCO_POR_CAT = {'calcas': 'centro', 'vestidos': 'centro', 'conjuntos': 'centro', 'saias': 'centro',
                'acessorios': 'centro'}


def main():
    cat = json.load(open('catalogo.json', encoding='utf-8'))
    os.makedirs('media/produtos', exist_ok=True)
    feitas = {}
    relatorio = []
    for p in cat['pecas']:
        refs = [c.get('foto') for c in p['cores'] if c.get('foto') is not None] + p.get('fotos', [])
        foco = FOCO_POR_CAT.get(p['cat'], 'topo')
        for ref in refs:
            if isinstance(ref, dict):
                nome = 'f%03d-c%d.jpg' % (ref['ficha'], ref['cel'])
                if nome in feitas: continue
                im = celula(ref['ficha'], ref['cel'])
                im, cob = limpa(im)
                im = recorta_4_5(im, 'centro')
                grava(im, 'media/produtos/' + nome)
                feitas[nome] = cob
                relatorio.append((nome, im.size, round(cob * 100, 1), 'célula'))
            else:
                nome = 'f%03d.jpg' % ref
                if nome in feitas: continue
                im = Image.open(caminho(ref)).convert('RGB')
                if ref in AJUSTES: im = im.crop((0, 0, im.width, int(im.height * AJUSTES[ref])))
                corte = fim_da_faixa(im)
                im, cob = limpa(im)
                if corte: im = im.crop((0, corte, im.width, im.height))
                im = recorta_4_5(im, foco)
                grava(im, 'media/produtos/' + nome)
                feitas[nome] = cob
                relatorio.append((nome, im.size, round(cob * 100, 1), 'faixa %dpx' % corte))
    # herói: a dona, fotografia 24
    heroi = Image.open(caminho(24)).convert('RGB')
    heroi.save('media/heroi.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
    for r in relatorio: print('%-14s %-11s %5s%%  %s' % (r[0], '%dx%d' % r[1], r[2], r[3]))
    print(len(relatorio), 'fotos preparadas +', 'heroi.jpg')


if __name__ == '__main__':
    main()
