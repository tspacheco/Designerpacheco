#!/usr/bin/env python3
"""Descarrega as fontes do Google Fonts, reduz-as a latin + latin-ext (ă â î ș ț) com fontTools,
converte para woff2 e gera _fontes/fontes.css com tudo em base64 (o site abre sem rede).
Uso: python3 ferramentas/fontes.py"""
import re, base64, urllib.request, os, sys, io
from fontTools.ttLib import TTFont
from fontTools import subset
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
PEDIDOS = {
  'aident-cabinet-stomatologic': 'https://fonts.googleapis.com/css2?family=Lunasima:wght@400;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap',
  'sabina-dent-cabinet': 'https://fonts.googleapis.com/css2?family=Judson:ital,wght@0,400;0,700;1,400&family=Karla:wght@400..700&display=swap',
  'dentama-by-dr': 'https://fonts.googleapis.com/css2?family=Ysabeau:ital,wght@0,400;0,500;0,700;0,800;1,400&family=Figtree:wght@400..700&display=swap',
}
UNI = 'U+0020-007E,U+00A0-00FF,U+0100-017F,U+0218-021B,U+2010-2015,U+2018-201E,U+2022,U+2026,U+2190-2193,U+00B7,U+2212,U+00D7,U+2713'
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA)).read()
faces = {}
for url in sys.argv[1:] or [PEDIDOS[os.path.basename(os.getcwd())]]:
    css = get(url).decode()
    for _, sub, bloco in re.findall(r'(/\* ([\w-]+) \*/\s*)?(@font-face \{.*?\})', css, re.S):
        if sub and sub not in ('latin', 'latin-ext'): continue
        src = re.search(r'url\((https://[^)]+)\)', bloco).group(1)
        fam = re.search(r"font-family: '([^']+)'", bloco).group(1)
        pw = [int(x) for x in re.search(r'font-weight: ([\d ]+);', bloco).group(1).split()]
        est = re.search(r'font-style: (\w+)', bloco).group(1)
        ur = re.search(r'unicode-range: ([^;]+);', bloco)
        k = (src, est)
        if k in faces: faces[k]['pesos'].extend(pw); continue
        faces[k] = dict(fam=fam, est=est, pesos=list(pw), ur=ur.group(1) if ur else '', src=src)
out = []
for d in faces.values():
    opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['*']; opts.notdef_outline = True
    f = TTFont(io.BytesIO(get(d['src'])))
    sb = subset.Subsetter(opts); sb.populate(unicodes=subset.parse_unicodes(UNI)); sb.subset(f)
    f.flavor = 'woff2'; b = io.BytesIO(); f.save(b)
    w = str(min(d['pesos'])) if min(d['pesos']) == max(d['pesos']) else '%d %d' % (min(d['pesos']), max(d['pesos']))
    out.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;%ssrc:url(data:font/woff2;base64,%s) format('woff2')}" % (d['fam'], d['est'], w, ('unicode-range:' + d['ur'] + ';') if d['ur'] else '', base64.b64encode(b.getvalue()).decode()))
open('_fontes/fontes.css', 'w').write('\n'.join(out))
print(len(out), 'faces ·', round(os.path.getsize('_fontes/fontes.css') / 1024), 'KB')
