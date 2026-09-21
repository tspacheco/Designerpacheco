#!/usr/bin/env python3
"""Compõe o herói de cada coleção (estação) a partir de três fotos de produto da própria loja.

Sem caras, sem imagens geradas: três peças da estação, em cartões inclinados sobre
um fundo de cor da estação. Grava media/colecoes/<estacao>.jpg (1800x1000).
Correr a partir de sites/toda-chic:  python3 ferramentas/colecoes.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
W, H = 1800, 1000

# três fotos por estação (nomes de media/produtos), da esquerda para a direita, e as cores do fundo
COLECOES = {
    'nova':    (['f087.jpg', 'f045.jpg', 'f043.jpg'], ((252, 236, 241), (232, 190, 205))),
    'inverno': (['f095.jpg', 'f079.jpg', 'f069.jpg'], ((242, 232, 234), (196, 176, 190))),
    'meia':    (['f033.jpg', 'f053.jpg', 'f030.jpg'], ((250, 240, 232), (222, 196, 172))),
    'verao':   (['f090.jpg', 'f019.jpg', 'f080.jpg'], ((253, 243, 232), (246, 205, 170))),
}


def fundo(c1, c2):
    im = Image.new('RGB', (W, H), c1)
    px = im.load()
    for x in range(W):
        t = x / (W - 1)
        col = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        for y in range(H): px[x, y] = col
    # um brilho suave no canto superior direito
    luz = Image.new('L', (W, H), 0)
    ImageDraw.Draw(luz).ellipse((W * 0.45, -H * 0.5, W * 1.3, H * 0.9), fill=110)
    luz = luz.filter(ImageFilter.GaussianBlur(160))
    im = Image.composite(Image.new('RGB', (W, H), (255, 250, 248)), im, luz)
    return im


def cartao(nome, largura, angulo):
    foto = Image.open('media/produtos/' + nome).convert('RGB')
    foto = foto.resize((largura, int(largura * 1.25)), Image.LANCZOS)
    borda = 14
    c = Image.new('RGB', (foto.width + borda * 2, foto.height + borda * 2), (255, 255, 255))
    c.paste(foto, (borda, borda))
    c = c.rotate(angulo, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
    mascara = Image.new('L', (foto.width + borda * 2, foto.height + borda * 2), 255).rotate(angulo, expand=True, resample=Image.BICUBIC)
    return c, mascara


def compoe(estacao):
    fotos, cores = COLECOES[estacao]
    im = fundo(*cores)
    # os cartões ocupam a metade direita: o texto do herói pousa à esquerda
    posicoes = [(int(W * 0.50), int(H * 0.16), 400, -6), (int(W * 0.66), int(H * 0.05), 450, 2), (int(W * 0.84), int(H * 0.20), 400, 7)]
    for nome, (x, y, larg, ang) in zip(fotos, posicoes):
        c, m = cartao(nome, larg, ang)
        sombra = Image.new('RGBA', (c.width + 120, c.height + 120), (0, 0, 0, 0))
        s = Image.new('L', m.size, 0); s.paste(m, (0, 0))
        sombra_m = Image.new('L', sombra.size, 0); sombra_m.paste(s, (60, 80))
        sombra_m = sombra_m.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.35))
        im.paste((60, 30, 40), (x - 60, y - 60, x - 60 + sombra.width, y - 60 + sombra.height), sombra_m)
        im.paste(c, (x, y), m)
    im.save('media/colecoes/%s.jpg' % estacao, 'JPEG', quality=84, optimize=True, progressive=True)
    return im


if __name__ == '__main__':
    os.makedirs('media/colecoes', exist_ok=True)
    for e in COLECOES: compoe(e); print('media/colecoes/%s.jpg' % e)
