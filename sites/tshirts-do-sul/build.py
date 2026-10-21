#!/usr/bin/env python3
"""Tshirts do Sul · injeta os logótipos SVG no index.src.html e gera index.html (site) e preview.html (Artifact, imagens embutidas)."""
import base64, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = (HERE / 'index.src.html').read_text('utf-8')
logo = (HERE / 'marca/logos/logo-1.svg').read_text('utf-8')
badge = (HERE / 'marca/logos/logo-2.svg').read_text('utf-8')
html = src.replace('{{LOGO}}', logo).replace('{{BADGE}}', badge)
(HERE / 'index.html').write_text(html, 'utf-8')

# versão para pré-visualização num só ficheiro (Artifact): media/*.webp → data URI
def inline(m):
    p = HERE / 'media' / m.group(1)
    if not p.exists():
        return m.group(0)
    return 'data:image/webp;base64,' + base64.b64encode(p.read_bytes()).decode()
prev = re.sub(r'media/([\w\-]+\.webp)', inline, html)
assert 'data:image/webp' in prev, 'media não embutida'
# o Artifact acrescenta o seu próprio esqueleto: retirar doctype/html/head/body
prev = re.sub(r'<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*', '', prev)
prev = prev.replace('</head>\n<body>', '').replace('</body>\n</html>', '')
(HERE / 'preview.html').write_text(prev, 'utf-8')
print('index.html', len(html) // 1024, 'KB · preview.html', len(prev) // 1024, 'KB')
