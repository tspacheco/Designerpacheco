#!/usr/bin/env python3
"""Monta index.html a partir de index.src.html:
- /*__FONTES__*/  -> _fontes/fontes.css (fontes em base64, latin + latin-ext)
- __ESTRELAS__    -> 4,5 estrelas em SVG (4 cheias + 1 a 50 %)
As fotografias ficam em media/*.webp (relativas, com onerror e fundo desenhado por baixo)."""
import os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOTA = 4.5
P = 'M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z'
COR, VAZIO = '#E8A93A', '#8A938D'
def estrela(f, i):
    if f >= 1: return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="%s" fill="%s"/></svg>' % (P, COR)
    return ('<svg viewBox="0 0 24 24" aria-hidden="true"><defs><linearGradient id="e%d"><stop offset="%d%%" stop-color="%s"/>'
            '<stop offset="%d%%" stop-color="%s"/></linearGradient></defs><path d="%s" fill="url(#e%d)"/></svg>') % (i, f*100, COR, f*100, VAZIO, P, i)
src = open('index.src.html', encoding='utf-8').read()
n = [0]
def est(_):
    n[0] += 1
    return ''.join(estrela(min(1, max(0, NOTA - k)), n[0]) for k in range(5))
out = re.sub('__ESTRELAS__', est, src).replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
