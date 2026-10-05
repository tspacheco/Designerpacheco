#!/usr/bin/env python3
"""Monta index.html a partir de index.src.html:
- /*__FONTES__*/ -> _fontes/fontes.css (Calistoga, Be Vietnam Pro e Caveat em base64, latin + latin-ext)
As fotografias ficam em media/*.webp (relativas, com onerror e desenho SVG por baixo).
A ementa (pratos e preços) está em index.src.html, no objeto EMENTA, transcrita dos PDF PT/EN da casa."""
import os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open('index.src.html', encoding='utf-8').read()
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
