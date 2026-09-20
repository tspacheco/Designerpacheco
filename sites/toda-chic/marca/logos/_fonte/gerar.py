# -*- coding: utf-8 -*-
"""Gera as 3 propostas de logotipo da Toda Chic em SVG puro (letras em curvas)."""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texto2svg import texto_path_puro
from fontTools.ttLib import TTFont

D = os.path.dirname(os.path.abspath(__file__))
ITA, J5, J4, PAR = [os.path.join(D,f) for f in ('italiana.ttf','jost-500.ttf','jost-400.ttf','parisienne.ttf')]

TINTA  = '#2B1D21'
ROSA   = '#C25C77'
ROSAE  = '#8E3A52'
BLUSH  = '#F8EFEA'

def cap_height(ttf, tamanho):
    f = TTFont(ttf); upem = f['head'].unitsPerEm
    try:
        ch = f['OS/2'].sCapHeight
        if ch: return ch / upem * tamanho
    except Exception: pass
    return 0.70 * tamanho

def svg(w, h, corpo, fundo=None):
    bg = '<rect width="%g" height="%g" fill="%s"/>' % (w, h, fundo) if fundo else ''
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" width="%g" height="%g" '
            'role="img" aria-label="Toda Chic">%s%s</svg>' % (w, h, w, h, bg, corpo))

def grav(nome, conteudo):
    io.open(os.path.join(D, nome), 'w', encoding='utf-8').write(conteudo)
    return nome

# ---------------------------------------------------------------- A: PEROLA
def A_principal():
    S = 120; TR = 0.20
    ch = cap_height(ITA, S)
    d_t,  w_t  = texto_path_puro(ITA, 'T',      S, TR)
    d_da, w_da = texto_path_puro(ITA, 'DA',     S, TR)
    d_ch, w_ch = texto_path_puro(ITA, 'CHIC',   S, TR)
    r = ch/2 * 0.96
    sw = S*0.038
    gap_anel = S*0.085
    espaco   = S*0.34
    largura = w_t + gap_anel + 2*r + gap_anel + w_da + espaco + w_ch
    M = 70; W = largura + 2*M
    base = 180
    x = M
    p = []
    p.append('<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_t, TINTA, x, base))
    x += w_t + gap_anel + r
    p.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f"/>'
             % (x, base - ch/2, r, ROSA, sw))
    x += r + gap_anel
    p.append('<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_da, TINTA, x, base))
    x += w_da + espaco
    p.append('<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_ch, TINTA, x, base))
    # assinatura
    ST = 20; STR = 0.34
    d_s, w_s = texto_path_puro(J4, 'EMBELEZA-TE CONNOSCO', ST, STR)
    sx = (W - w_s)/2; sy = base + 60
    p.append('<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_s, ROSAE, sx, sy))
    lr = 46
    p.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.4"/>'
             % (sx - lr - 18, sy - ST*0.34, sx - 18, sy - ST*0.34, ROSA))
    p.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.4"/>'
             % (sx + w_s + 18, sy - ST*0.34, sx + w_s + 18 + lr, sy - ST*0.34, ROSA))
    return svg(W, 250, ''.join(p))

def A_monograma():
    B = 100; c = B/2
    r = 40; sw = 3.4
    S = 34
    d_tc, w_tc = texto_path_puro(ITA, 'TC', S, 0.10)
    ch = cap_height(ITA, S)
    p = ['<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="%g"/>' % (c, c, r, ROSA, sw),
         '<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_tc, TINTA, c - w_tc/2, c + ch/2)]
    return svg(B, B, ''.join(p))

# ------------------------------------------------------------ B: ASSINATURA
def B_principal():
    S = 92; TR = 0.26
    d_toda, w_toda = texto_path_puro(J5, 'TODA', S, TR)
    SC = 150
    d_chic, w_chic = texto_path_puro(PAR, 'Chic', SC, 0.0)
    M = 70
    desloc = w_toda * 0.40            # o script arranca a 40% do TODA
    esq = 0.0
    dir = max(w_toda, desloc + w_chic)
    largura = dir - esq
    W = largura + 2*M
    base_toda = 150
    x_toda = M + (largura - w_toda)/2 * 0.0   # ancorado a esquerda do bloco
    x_chic = M + desloc
    # centra o bloco inteiro
    bloco_esq = min(x_toda, x_chic)
    bloco_dir = max(x_toda + w_toda, x_chic + w_chic)
    ajuste = (W - (bloco_dir - bloco_esq))/2 - bloco_esq
    x_toda += ajuste; x_chic += ajuste
    base_chic = base_toda + 92
    p = ['<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_toda, TINTA, x_toda, base_toda),
         '<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_chic, ROSA, x_chic, base_chic)]
    ST = 19; STR = 0.36
    d_s, w_s = texto_path_puro(J4, 'EMBELEZA-TE CONNOSCO', ST, STR)
    sx = (W - w_s)/2; sy = base_chic + 74
    p.append('<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_s, ROSAE, sx, sy))
    lr = 44
    for x1, x2 in ((sx-lr-18, sx-18), (sx+w_s+18, sx+w_s+18+lr)):
        p.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.4"/>'
                 % (x1, sy - ST*0.34, x2, sy - ST*0.34, ROSA))
    return svg(W, 370, ''.join(p))

def B_monograma():
    B = 100
    d_t, w_t = texto_path_puro(J5, 'T', 62, 0)
    d_c, w_c = texto_path_puro(PAR, 'C', 92, 0)
    p = ['<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_t, TINTA, 20, 62),
         '<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_c, ROSA, 36, 84)]
    return svg(B, B, ''.join(p))

# ----------------------------------------------------------------- C: LACO
def laco(cor_laco, cor_no, sw=5.0, tails=True):
    p = []
    p.append('<path d="M50 46 C 40 27, 13 25, 9 38 C 6 49, 30 57, 50 46 Z" fill="none" stroke="%s" '
             'stroke-width="%g" stroke-linejoin="round"/>' % (cor_laco, sw))
    p.append('<path d="M50 46 C 60 27, 87 25, 91 38 C 94 49, 70 57, 50 46 Z" fill="none" stroke="%s" '
             'stroke-width="%g" stroke-linejoin="round"/>' % (cor_laco, sw))
    if tails:
        p.append('<path d="M44 52 C 41 63, 37 70, 32 77" fill="none" stroke="%s" stroke-width="%g" '
                 'stroke-linecap="round"/>' % (cor_laco, sw))
        p.append('<path d="M56 52 C 59 63, 63 70, 68 77" fill="none" stroke="%s" stroke-width="%g" '
                 'stroke-linecap="round"/>' % (cor_laco, sw))
    p.append('<circle cx="50" cy="47" r="6.4" fill="%s"/>' % cor_no)
    return ''.join(p)

def C_principal():
    S = 76; TR = 0.34
    d_w, w_w = texto_path_puro(J5, 'TODA CHIC', S, TR)
    M = 70
    W = max(w_w, 200) + 2*M
    marca = 156
    mx = (W - marca)/2
    p = ['<g transform="translate(%.2f 14) scale(%.4f)">%s</g>' % (mx, marca/100.0, laco(ROSA, ROSAE, 5.2)),
         '<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_w, TINTA, (W - w_w)/2, 238)]
    ST = 18; STR = 0.36
    d_s, w_s = texto_path_puro(J4, 'EMBELEZA-TE CONNOSCO', ST, STR)
    sx = (W - w_s)/2; sy = 282
    p.append('<path d="%s" fill="%s" transform="translate(%.2f %.2f)"/>' % (d_s, ROSAE, sx, sy))
    return svg(W, 300, ''.join(p))

def C_monograma():
    return svg(100, 100, laco(ROSA, ROSAE, 5.6))

ficheiros = {
 'A-perola-principal.svg': A_principal(),
 'A-perola-monograma.svg': A_monograma(),
 'B-assinatura-principal.svg': B_principal(),
 'B-assinatura-monograma.svg': B_monograma(),
 'C-laco-principal.svg': C_principal(),
 'C-laco-monograma.svg': C_monograma(),
}
for n, c in ficheiros.items():
    grav(n, c); print('%-32s %6d bytes' % (n, len(c)))
