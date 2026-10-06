#!/usr/bin/env python3
"""Monta o site a partir de index.src.html:
- /*__FONTES__*/  -> _fontes/fontes.css (Forum, Manrope, Caveat Brush em base64, latin + latin-ext)
- /*__T__*/       -> dicionário ro/en/pt de ferramentas/textos.py (para o botão de língua)
- elementos vazios com data-t="chave" e atributos "@@chave" -> texto na língua do ficheiro
Saídas: index.html (RO, botão RO/EN) e pt.html (a mesma página a abrir em PT, para o Tomás rever)."""
import json, os, re, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, 'ferramentas')
from textos import T

src = open('index.src.html', encoding='utf-8').read()
src = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
src = src.replace('/*__T__*/', 'var T=' + json.dumps(T, ensure_ascii=False, separators=(',', ':')) + ';')

PAR = re.compile(r'(<(?P<tag>[a-z0-9]+)\b(?P<at>[^>]*?)\sdata-t="(?P<k>[\w.-]+)"(?P<at2>[^>]*)>)</(?P=tag)>')

def montar(html, i):
    falta = set()
    def el(m):
        k = m.group('k')
        if k not in T: falta.add(k); return m.group(0)
        return m.group(1) + (T[k][i] or T[k][0]) + '</%s>' % m.group('tag')
    html = PAR.sub(el, html)
    def at(m):
        k = m.group(1)
        if k not in T: falta.add(k); return m.group(0)
        return (T[k][i] or T[k][0]).replace('"', '&quot;')
    html = re.sub(r'@@([\w.-]+)', at, html)
    if falta: raise SystemExit('faltam textos: ' + ', '.join(sorted(falta)))
    vazios = re.findall(r'data-t="([\w.-]+)"[^>]*></', html)
    return html

ro = montar(src, 0)
pt = montar(src, 2)
pt = pt.replace('<html lang="ro" data-lang="ro">', '<html lang="pt-PT" data-lang="pt" data-pt="1">', 1)
pt = pt.replace("'bz.lang'", "'bz.lang.pt'")
assert 'data-lang="pt"' in pt
open('index.html', 'w', encoding='utf-8').write(ro)
open('pt.html', 'w', encoding='utf-8').write(pt)
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.(?:webp|mp4|webm))', ro) if not os.path.exists('media/' + m)})
print('index.html %.0f KB · pt.html %.0f KB' % (len(ro.encode()) / 1024, len(pt.encode()) / 1024)
      + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
