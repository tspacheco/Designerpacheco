#!/usr/bin/env python3
"""Descarrega as fontes do Google Fonts (subconjuntos latin + latin-ext, diacríticos romenos ă â î ș ț)
e gera _fontes/fontes.css com as fontes em base64 (o site abre sem rede).
Uso: python3 ferramentas/fontes.py  (os pedidos estão em PEDIDOS, por site)."""
import re, base64, urllib.request, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
PEDIDOS = {
  'dulce-de-acasa': 'https://fonts.googleapis.com/css2?family=Playpen+Sans:wght@500;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap',
}
SUBSETS = {'latin', 'latin-ext'}
out, vistos = [], {}
for url in sys.argv[1:] or [PEDIDOS[os.path.basename(os.getcwd())]]:
    css = urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read().decode()
    for _, subset, bloco in re.findall(r'(/\* ([\w-]+) \*/\s*)?(@font-face \{.*?\})', css, re.S):
        if subset not in SUBSETS: continue
        src = re.search(r'url\((https://[^)]+)\)', bloco).group(1)
        peso = re.search(r'font-weight: ([\d ]+);', bloco).group(1)
        chave = (src, re.search(r'font-style: (\w+)', bloco).group(1))
        if chave in vistos:
            i, pesos = vistos[chave]; pesos.extend(int(p) for p in peso.split())
            out[i] = re.sub(r'font-weight: [\d ]+;', 'font-weight: %d %d;' % (min(pesos), max(pesos)), out[i]); continue
        dados = urllib.request.urlopen(urllib.request.Request(src, headers=UA)).read()
        if 'Playpen' in bloco:  # a Playpen é grande: cortar ao latim básico + romeno (ă â î ș ț) + tipografia
            import io
            from fontTools import subset
            from fontTools.ttLib import TTFont
            fo = TTFont(io.BytesIO(dados)); op = subset.Options(); op.flavor = 'woff2'; op.layout_features = ['*']
            sb = subset.Subsetter(op); sb.populate(unicodes=list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + [0x102, 0x103, 0x218, 0x219, 0x21A, 0x21B, 0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E, 0x2026, 0x2022, 0x20AC, 0x2192, 0x2190, 0x2715, 0x2713])
            sb.subset(fo); b = io.BytesIO(); fo.save(b); dados = b.getvalue()
        fmt = 'woff2' if 'woff2' in bloco else 'truetype'
        vistos[chave] = (len(out), [int(p) for p in peso.split()])
        out.append(re.sub(r"url\(https://[^)]+\) format\('[^']+'\)", "url(data:font/%s;base64,%s) format('%s')" % (fmt, base64.b64encode(dados).decode(), fmt), bloco))
open('_fontes/fontes.css', 'w').write('\n'.join(out))
print(len(out), 'faces ·', round(os.path.getsize('_fontes/fontes.css') / 1024), 'KB')
