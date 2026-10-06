#!/usr/bin/env python3
"""Monta index.html (RO, botão EN) e pt.html (a mesma página a abrir em PT, para o Tomás rever)
a partir de index.src.html:
- /*__FONTES__*/ -> _fontes/fontes.css (Agbalumo, Rethink Sans, Martian Mono em base64, latin + latin-ext)
As fotografias ficam em media/*.webp (relativas, com onerror e fundo desenhado por baixo)."""
import os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open('index.src.html', encoding='utf-8').read()
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
fotos = set(re.findall(r'media/([\w.-]+\.webp)', out)) | {m + '.webp' for m in re.findall(r"img:'([\w-]+)'", out)}
faltam = sorted(f for f in fotos if not os.path.exists('media/' + f))
open('index.html', 'w', encoding='utf-8').write(out)
pt = out.replace('<html lang="ro" data-lang="ro">', '<html lang="pt-PT" data-lang="pt">', 1)
pt = pt.replace('<title>La Gioia di Giovanni · Pizzerie în centrul Iașului</title>', '<title>La Gioia di Giovanni · Pizzaria no centro de Iași</title>', 1)
assert 'data-lang="pt"' in pt
open('pt.html', 'w', encoding='utf-8').write(pt)
print('index.html %.0f KB · pt.html' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
