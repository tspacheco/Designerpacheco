#!/usr/bin/env python3
"""Monta index.html (RO, botão EN) e pt.html (a mesma página a abrir em PT, para o Tomás) a partir de:
- index.src.html  (estrutura + CSS; textos RO no HTML)
- index.src.js    (JS: dicionários en/pt, borboleta de unhas, configurador de unhas, router #/, WhatsApp)
- _fontes/fontes.css (Viaoda Libre, Urbanist, Red Hat Mono em base64, latin + latin-ext; gerado por ferramentas/fontes.py)
As fotografias ficam em media/*.webp (relativas, com onerror e fundo desenhado por baixo)."""
import os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open('index.src.html', encoding='utf-8').read()
js = open('index.src.js', encoding='utf-8').read().replace('</script', '<\\/script')
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read()).replace('/*__JS__*/', js)
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
# fotos que o dono ainda não mandou: o <img> sai (fica só o desenho por baixo, sem erros 404 na consola)
out = re.sub(r'<img src="media/([\w.-]+\.webp)"[^>]*>', lambda m: m.group(0) if os.path.exists('media/' + m.group(1)) else '', out)
import json
lucrari = sorted(f for f in os.listdir('media') if re.match(r'lucrare-\d+\.webp$', f)) if os.path.isdir('media') else []
out = out.replace('/*__LUCRARI__*/[]', json.dumps(lucrari))
open('index.html', 'w', encoding='utf-8').write(out)
pt = out.replace('<html lang="ro" data-lang="ro">', '<html lang="pt-PT" data-lang="pt" class="build-pt">', 1).replace("'butterfly.lang'", "'butterfly.lang.pt'")
pt = pt.replace('<title>Salon Butterfly · Manichiură în Moara de Foc, Iași</title>', '<title>Salon Butterfly · Manicure em Moara de Foc, Iași</title>', 1)
assert 'data-lang="pt"' in pt
open('pt.html', 'w', encoding='utf-8').write(pt)
print(('lucrari: %d · ' % len(lucrari)) + 'index.html %.0f KB · pt.html %.0f KB' % (len(out.encode()) / 1024, len(pt.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
