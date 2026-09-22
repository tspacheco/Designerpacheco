#!/usr/bin/env python3
"""Monta index.html a partir de index.src.html + catalogo.json + fontes.css.

Correr a partir de sites/toda-chic:  python3 ferramentas/build.py
(Depois de mudar fotos, correr primeiro ferramentas/fotos.py.)
"""
import json, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

src = open('index.src.html', encoding='utf-8').read()
fontes = open('ferramentas/fontes.css', encoding='utf-8').read()
cat = json.load(open('catalogo.json', encoding='utf-8'))
cat.pop('_nota', None)

# cada referência de foto passa a ser o nome do ficheiro em media/produtos/
def ficheiro(ref):
    if isinstance(ref, dict): return 'f%03d-c%d.jpg' % (ref['ficha'], ref['cel'])
    return 'f%03d.jpg' % ref

for p in cat['pecas']:
    for c in p['cores']:
        if c.get('foto') is not None: c['foto'] = ficheiro(c['foto'])
    if p.get('fotos'): p['fotos'] = [ficheiro(f) for f in p['fotos']]
    for f in [c.get('foto') for c in p['cores']] + p.get('fotos', []):
        if f and not os.path.exists('media/produtos/' + f):
            raise SystemExit('falta media/produtos/' + f + ' (peça ' + p['id'] + ') — corre ferramentas/fotos.py')

dados = json.dumps(cat, ensure_ascii=False, separators=(',', ':'))
out = src.replace('/*__FONTES__*/', fontes).replace('__CATALOGO__', dados)
assert '__CATALOGO__' not in out and '/*__FONTES__*/' not in out
open('index.html', 'w', encoding='utf-8').write(out)
painel = open('painel.src.html', encoding='utf-8').read().replace('/*__FONTES__*/', fontes)
open('painel.html', 'w', encoding='utf-8').write(painel)
print('index.html: %.0f KB · %d peças · %d fotos' % (len(out.encode()) / 1024, len(cat['pecas']),
      len(os.listdir('media/produtos'))))
