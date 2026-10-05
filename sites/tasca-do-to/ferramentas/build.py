#!/usr/bin/env python3
"""Monta index.html a partir de index.src.html:
- /*__FONTES__*/  -> _fontes/fontes.css (Kufam, Public Sans e DM Mono em base64, latin + latin-ext)
- __ESTRELAS__    -> 4,5 estrelas em SVG (4 cheias + 1 a 50 %)
- __TELHADOS__    -> a linha de casas de Tavira com telhados de tesoura (SVG gerado, sempre igual)
As fotografias ficam em media/*.webp (relativas, com onerror e fundo desenhado por baixo)."""
import os, re, random
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOTA = 4.5
P = 'M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z'
COR, VAZIO = '#E8A93A', '#8A938D'
def estrela(f, i):
    if f >= 1: return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="%s" fill="%s"/></svg>' % (P, COR)
    return ('<svg viewBox="0 0 24 24" aria-hidden="true"><defs><linearGradient id="e%d"><stop offset="%d%%" stop-color="%s"/>'
            '<stop offset="%d%%" stop-color="%s"/></linearGradient></defs><path d="%s" fill="url(#e%d)"/></svg>') % (i, f*100, COR, f*100, VAZIO, P, i)

def telhados(largura=1440, base=250, semente=7):
    """Casas caiadas com telhados de tesoura (várias pirâmides lado a lado), janelas que acendem e portas.
    Devolve o interior de um <svg viewBox="0 0 largura 260">."""
    r = random.Random(semente)
    paredes = ['#F4F1E8', '#EFEADC', '#F7F4EC', '#ECE6D6']
    barras = [None, '#D9A441', None, '#3E6E9E', None, '#D9A441']
    x, casas, linha, janelas, n = -20, [], [], [], 0
    while x < largura + 20:
        w = r.choice([130, 150, 170, 190, 220, 250])
        h = r.choice([96, 112, 128, 144])
        topo = base - h
        npir = max(1, min(3, round(w / 85)))
        pw = w / npir
        g = ['<g class="casa">']
        g.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, topo, w, h + 12, r.choice(paredes)))
        b = r.choice(barras)
        if b: g.append('<rect x="%d" y="%d" width="%d" height="14" fill="%s"/>' % (x, base - 4, w, b))
        g.append('<rect x="%d" y="%d" width="%d" height="5" fill="#FFFFFF" opacity=".9"/>' % (x - 4, topo - 3, w + 8))
        for k in range(npir):
            x0 = x + k * pw; x1 = x0 + pw; xm = (x0 + x1) / 2
            ap = topo - 3 - pw * r.choice([.42, .46, .5])
            g.append('<path class="tl" d="M%.1f %.1fL%.1f %.1fL%.1f %.1fz" fill="#D0643A"/>' % (x0 - 2, topo - 3, xm, ap, xm, topo - 3))
            g.append('<path class="tl" d="M%.1f %.1fL%.1f %.1fL%.1f %.1fz" fill="#A8451F"/>' % (xm, topo - 3, xm, ap, x1 + 2, topo - 3))
            for f in (.33, .66):
                yy = ap + (topo - 3 - ap) * f
                dx = (pw / 2 + 2) * f
                g.append('<path d="M%.1f %.1fH%.1f" stroke="#8A3716" stroke-opacity=".35" stroke-width="1.2"/>' % (xm - dx, yy, xm + dx))
            linha.append((x0 - 2, topo - 3)); linha.append((xm, ap)); linha.append((x1 + 2, topo - 3))
        # chaminé algarvia numa casa sim, noutra não
        if r.random() < .35:
            cx = x + w * r.choice([.2, .75])
            g.append('<rect x="%.1f" y="%d" width="14" height="30" fill="#F7F4EC"/><rect x="%.1f" y="%d" width="20" height="5" fill="#FFFFFF"/>' % (cx, topo - 30, cx - 3, topo - 34))
            g.append('<path d="M%.1f %dh2v6h-2zM%.1f %dh2v6h-2z" fill="#B9AE98"/>' % (cx + 3, topo - 24, cx + 9, topo - 24))
        # janelas e porta
        nj = max(1, int(w // 62))
        esp = w / nj
        porta = r.randrange(nj)
        for j in range(nj):
            jx = x + esp * j + esp / 2
            if j == porta:
                g.append('<rect x="%.1f" y="%d" width="26" height="46" rx="2" fill="#1F4B3F"/>' % (jx - 13, base - 46))
                g.append('<rect class="jan" style="--i:%d" x="%.1f" y="%d" width="18" height="10" fill="#2A3442"/>' % (n, jx - 9, base - 60)); n += 1
            else:
                g.append('<rect x="%.1f" y="%d" width="26" height="36" fill="#D9CFB8"/>' % (jx - 13, base - 62))
                g.append('<rect class="jan" style="--i:%d" x="%.1f" y="%d" width="18" height="28" fill="#2A3442"/>' % (n, jx - 9, base - 58)); n += 1
            if h >= 128:
                g.append('<rect x="%.1f" y="%d" width="24" height="30" fill="#D9CFB8"/>' % (jx - 12, topo + 18))
                g.append('<rect class="jan" style="--i:%d" x="%.1f" y="%d" width="16" height="22" fill="#2A3442"/>' % (n, jx - 8, topo + 22)); n += 1
        g.append('</g>')
        casas.append(''.join(g))
        x += w + r.choice([0, 0, 6, 10])
    d = 'M' + ' L'.join('%.1f %.1f' % p for p in linha)
    return ('<g class="casas">' + ''.join(casas) + '</g>'
            '<path class="linha-telhados" d="%s" pathLength="1"/>' % d
            + '<rect x="-40" y="%d" width="%d" height="40" fill="#C9BFA8"/>' % (base + 8, largura + 80))

src = open('index.src.html', encoding='utf-8').read()
n = [0]
def est(_):
    n[0] += 1
    return ''.join(estrela(min(1, max(0, NOTA - k)), n[0]) for k in range(5))
out = re.sub('__ESTRELAS__', est, src)
out = out.replace('__TELHADOS__', telhados())
out = out.replace('__TELHADOS_RODAPE__', telhados(semente=23))
out = out.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
