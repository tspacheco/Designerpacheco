#!/usr/bin/env python3
"""Limpa em lote capturas de ecrã do Instagram: corta a faixa cinzenta à esquerda, apaga os botões < > (por correspondência de padrão)
e os pontos do carrossel (blobs alinhados na base), grava JPG numerado. Uso: limpa-lote.py PASTA_ORIGEM PASTA_DESTINO [N_INICIAL] [excluir.png,outro.png]"""
import cv2, numpy as np, glob, os, sys
SRC = sys.argv[1]; DST = sys.argv[2]; INICIO = int(sys.argv[3]) if len(sys.argv) > 3 else 1
EXCLUIR = set(sys.argv[4].split(',')) if len(sys.argv) > 4 else set()
os.makedirs(DST, exist_ok=True)
AQUI = os.path.dirname(os.path.abspath(__file__))
TB = np.load(os.path.join(AQUI, 'tpl_botao.npy')); TBF = cv2.flip(TB, 1); R = TB.shape[0] // 2
TD = np.load(os.path.join(AQUI, 'tpl_ponto.npy')); RDY, RDX = TD.shape[0] // 2, TD.shape[1] // 2

def borda_esq(img):
    lum = img.mean(axis=2); cm = lum.mean(axis=0); cs = lum.std(axis=0); n = 0
    for k in range(min(40, img.shape[1])):
        if cs[k] < 12 and cm[k] < 95: n += 1
        else: break
    return n

def botoes(g):
    H, W = g.shape; out = []
    for lado, tpl in (('E', TBF), ('D', TB)):
        x0, x1 = (0, 120) if lado == 'E' else (W - 120, W); y0, y1 = H//2 - 130, H//2 + 130
        r = cv2.matchTemplate(g[y0:y1, x0:x1], tpl, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(r)
        cx, cy = loc[0] + x0 + R, loc[1] + y0 + R
        margem = cx if lado == 'E' else W - cx
        posicao_ok = 15 <= margem <= 62 and abs(cy - H//2) <= 45
        if (posicao_ok and mx >= 0.5) or mx >= 0.85: out.append((cx, cy, round(float(mx), 2)))
    return out

def pontos(g):
    """pontos do carrossel: correspondência com um ponto real, depois só grupos alinhados, espaçados e centrados."""
    H, W = g.shape; y0 = H - 46; x0 = W//2 - 150
    band = g[y0:H, x0:W//2 + 150]
    r = cv2.matchTemplate(band, TD, cv2.TM_CCOEFF_NORMED)
    ys, xs = np.where(r > 0.45); cand = []
    for y, x in sorted(zip(ys, xs), key=lambda p: -r[p[0], p[1]]):
        if all(abs(x - px) > 8 or abs(y - py) > 6 for px, py in cand): cand.append((int(x), int(y)))
    cand = [(x + x0 + RDX, y + y0 + RDY) for x, y in cand]
    melhor = []
    for p in cand:  # cadeia: a partir de cada candidato, avançar para a direita com espaçamento de ponto (10–24 px)
        cadeia = [p]
        while True:
            seg = [q for q in cand if abs(q[1] - cadeia[-1][1]) <= 3 and 10 <= q[0] - cadeia[-1][0] <= 24]
            if not seg: break
            cadeia.append(min(seg, key=lambda q: q[0]))
        if len(cadeia) >= 2 and abs((cadeia[0][0] + cadeia[-1][0]) / 2 - W/2) <= 45 and len(cadeia) > len(melhor): melhor = cadeia
    return melhor

fs = sorted(glob.glob(os.path.join(SRC, '*.png'))); n = INICIO; ver = []
for f in fs:
    nome = os.path.basename(f)
    if nome in EXCLUIR: continue
    img = cv2.imread(f)
    if img is None or img.shape[1] < 200: print('ignorado', nome); continue
    e = borda_esq(img); img = img[:-40, e:]  # os pontos do carrossel vivem sempre nos últimos ~30 px: cortar é mais seguro do que apagar
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); h, w = g.shape
    bs = botoes(g); ps = []
    mask = np.zeros((h, w), np.uint8)
    for (cx, cy, _) in bs: cv2.circle(mask, (cx, cy), R + 2, 255, -1)
    for (cx, cy) in ps: cv2.circle(mask, (cx, cy), 9, 255, -1)
    out = img
    if mask.any():
        out = cv2.inpaint(img, mask, 9, cv2.INPAINT_TELEA)
        soft = cv2.GaussianBlur(out, (0, 0), 2.5)
        mm = cv2.GaussianBlur(cv2.dilate(mask, np.ones((5, 5), np.uint8)), (0, 0), 3).astype(np.float32) / 255.0
        out = (out * (1 - mm[..., None]) + soft * mm[..., None]).astype(np.uint8)
    cv2.imwrite(os.path.join(DST, f'{n:02d}.jpg'), out, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(f'{n:02d}', nome[-10:], 'borda', e, 'botoes', bs, 'pontos', len(ps))
    cy = h // 2
    L = cv2.resize(out[cy-60:cy+60, 0:90], (180, 240)); Rr = cv2.resize(out[cy-60:cy+60, w-90:w], (180, 240)); B = cv2.resize(out[h-50:h, w//2-130:w//2+130], (520, 240))
    t = np.hstack([L, np.full((240, 4, 3), 255, np.uint8), Rr, np.full((240, 4, 3), 255, np.uint8), B]); cv2.putText(t, f'{n:02d}', (6, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2); ver.append(t)
    n += 1
for i in range(0, len(ver), 7):
    cv2.imwrite(os.path.join(DST, '..', f'verificacao_{i//7}.png'), np.vstack(ver[i:i+7]))
