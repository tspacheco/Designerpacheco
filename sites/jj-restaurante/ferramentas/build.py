#!/usr/bin/env python3
"""Monta index.html a partir de index.src.html:
- /*__FONTES__*/  -> _fontes/fontes.css (Corben, Atkinson Hyperlegible e Caveat em base64, latin + latin-ext)
- __ESTRELAS__    -> 4,2 estrelas em SVG (4 cheias + 1 a 20 %)
As fotografias ficam em media/*.webp (relativas, com onerror e fundo desenhado por baixo)."""
import os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = 'M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z'
def estrela(f, i):
    if f >= 1: return '<svg viewBox="0 0 24 24"><path d="%s" fill="#E0A426"/></svg>' % P
    return ('<svg viewBox="0 0 24 24"><defs><linearGradient id="e%d"><stop offset="%d%%" stop-color="#E0A426"/>'
            '<stop offset="%d%%" stop-color="#D6D2C8"/></linearGradient></defs><path d="%s" fill="url(#e%d)"/></svg>') % (i, f*100, f*100, P, i)
src = open('index.src.html', encoding='utf-8').read()
n = [0]
def est(_):
    n[0] += 1
    return ''.join(estrela(1 if k < 4 else .2, n[0]) for k in range(5))
out = re.sub('__ESTRELAS__', est, src).replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
