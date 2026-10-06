#!/usr/bin/env python3
"""Monta index.html (RO, botão EN) e pt.html (a mesma página a abrir em PT, para o Tomás) a partir de:
- index.src.html  (estrutura + CSS; textos RO no HTML)
- index.src.js    (JS: dicionários en/pt, tosquia ao scroll, router #/, marcação WhatsApp)
- _fontes/fontes.css (Sigmar, Nunito, Caveat em base64, latin + latin-ext; gerado por ferramentas/fontes.py)
As fotografias ficam em media/*.webp (relativas, com onerror e fundo desenhado por baixo)."""
import os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open('index.src.html', encoding='utf-8').read()
js = open('index.src.js', encoding='utf-8').read().replace('</script', '<\\/script')
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read()).replace('/*__JS__*/', js)
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out)
pt = out.replace('<html lang="ro" data-lang="ro">', '<html lang="pt-PT" data-lang="pt" class="build-pt">', 1).replace("'sofiapets.lang'", "'sofiapets.lang.pt'")
pt = pt.replace('<title>Sofia Pets · Coafor canin și felin în Iași</title>', '<title>Sofia Pets · Tosquias de cães e gatos em Iași</title>', 1)
assert 'data-lang="pt"' in pt
open('pt.html', 'w', encoding='utf-8').write(pt)
print('index.html %.0f KB · pt.html %.0f KB' % (len(out.encode()) / 1024, len(pt.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
