#!/usr/bin/env python3
"""Monta demo/ — painel (index.html) + loja (loja.html) com o servidor simulado dentro do browser (loja/demo-shim.js).
Correr depois de build.py, a partir de sites/toda-chic:  python3 ferramentas/demo.py"""
import json, os, re
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(RAIZ)
cat = json.load(open('catalogo.json', encoding='utf-8')); cat.pop('_nota', None)
def ficheiro(ref): return 'f%03d-c%d.jpg' % (ref['ficha'], ref['cel']) if isinstance(ref, dict) else 'f%03d.jpg' % ref
for p in cat['pecas']:
    for c in p['cores']:
        if c.get('foto') is not None: c['foto'] = ficheiro(c['foto'])
    if p.get('fotos'): p['fotos'] = [ficheiro(f) for f in p['fotos']]
shim = open('loja/demo-shim.js', encoding='utf-8').read().replace('__CATALOGO__', json.dumps(cat, ensure_ascii=False, separators=(',', ':')))
shim = '<script>' + shim.replace('</script', '<\\/script') + '</script>'
os.makedirs('demo', exist_ok=True)
BARRA = ('<style>.demo-barra{background:#2B1E22;color:#F6E7E9;font:600 12px/1.4 Jost,system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;'
         'padding:.55rem 1rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}.demo-barra a{color:#F5C2CC;text-decoration:underline;text-underline-offset:3px}.demo-barra b{color:#fff}</style>'
         '<div class="demo-barra"><span>Demonstração · palavra-passe do painel <b>123</b> · MB WAY simulado</span>%s<a href="#" onclick="__demoRepor();return false">Repor dados</a></div>')
painel = open('painel.html', encoding='utf-8').read()
painel = painel.replace('</head>', shim + '</head>', 1).replace('<body>', '<body>' + BARRA % '<a href="loja.html">Abrir a loja</a>', 1)
painel = painel.replace('<p>Painel da loja. Só para ti.</p>', '<p>Painel da loja. Só para ti.</p><p style="margin-top:-.4rem;font-size:13px;opacity:.75">Demonstração: a palavra-passe é <b>123</b>.</p>', 1)
open('demo/index.html', 'w', encoding='utf-8').write(painel)
loja = open('index.html', encoding='utf-8').read()
loja = loja.replace('</head>', shim + '</head>', 1).replace('<body>', '<body>' + BARRA % '<a href="./">Abrir o painel</a>', 1)
open('demo/loja.html', 'w', encoding='utf-8').write(loja)
print('demo/index.html %.0f KB · demo/loja.html %.0f KB' % (len(painel.encode()) / 1024, len(loja.encode()) / 1024))
