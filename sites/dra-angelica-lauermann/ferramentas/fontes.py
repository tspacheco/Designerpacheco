#!/usr/bin/env python3
"""Descarrega as fontes (só o subconjunto latin) do Google Fonts e gera _fontes/fontes.css com base64."""
import re, base64, urllib.request, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
PEDIDOS = [
  'https://fonts.googleapis.com/css2?family=Funnel+Display:wght@600;800&family=Funnel+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap',
  'https://fonts.googleapis.com/css2?family=Pinyon+Script&text=AL&display=swap',
]
out = []
for url in PEDIDOS:
    css = urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read().decode()
    blocos = re.findall(r'(/\* ([\w-]+) \*/\s*)?(@font-face \{.*?\})', css, re.S)
    for _, subset, bloco in blocos:
        if subset and subset != 'latin': continue
        src = re.search(r'url\((https://[^)]+)\)', bloco).group(1)
        dados = urllib.request.urlopen(urllib.request.Request(src, headers=UA)).read()
        fmt = 'woff2' if src.endswith('woff2') else 'truetype'
        out.append(re.sub(r'url\(https://[^)]+\) format\(\'[^\']+\'\)', "url(data:font/%s;base64,%s) format('%s')" % (fmt, base64.b64encode(dados).decode(), fmt), bloco))
open('_fontes/fontes.css', 'w').write('\n'.join(out))
print(len(out), 'faces ·', round(os.path.getsize('_fontes/fontes.css') / 1024), 'KB')
