#!/usr/bin/env python3
"""Descarrega as fontes do Google Fonts (subconjuntos latin + latin-ext, por causa do ș ț ă â î do romeno)
e gera _fontes/fontes.css com as fontes em base64 (o site abre sem rede)."""
import re, base64, urllib.request, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
PEDIDOS = sys.argv[1:] or [
  'https://fonts.googleapis.com/css2?family=Brygada+1918:ital,wght@0,500;0,600;1,500&family=Albert+Sans:wght@400;500;600&display=swap',
]
SUBSETS = {'latin', 'latin-ext'}
out, vistos = [], {}
for url in PEDIDOS:
    css = urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read().decode()
    blocos = re.findall(r'(/\* ([\w-]+) \*/\s*)?(@font-face \{.*?\})', css, re.S)
    for _, subset, bloco in blocos:
        if subset and subset not in SUBSETS: continue
        src = re.search(r'url\((https://[^)]+)\)', bloco).group(1)
        peso = re.search(r'font-weight: (\d+)', bloco).group(1)
        if src in vistos:  # fonte variável: o Google repete o mesmo ficheiro por peso -> uma só face com intervalo de pesos
            i, pesos = vistos[src]; pesos.append(int(peso))
            out[i] = re.sub(r'font-weight: [\d ]+;', 'font-weight: %d %d;' % (min(pesos), max(pesos)), out[i]); continue
        dados = urllib.request.urlopen(urllib.request.Request(src, headers=UA)).read()
        fmt = 'woff2' if 'woff2' in bloco else 'truetype'
        vistos[src] = (len(out), [int(peso)])
        out.append(re.sub(r"url\(https://[^)]+\) format\('[^']+'\)", "url(data:font/%s;base64,%s) format('%s')" % (fmt, base64.b64encode(dados).decode(), fmt), bloco))
open('_fontes/fontes.css', 'w').write('\n'.join(out))
print(len(out), 'faces ·', round(os.path.getsize('_fontes/fontes.css') / 1024), 'KB')
