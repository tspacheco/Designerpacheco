#!/usr/bin/env python3
"""Monta index.html: injeta fontes (base64) e as três fotografias da fachada em index.src.html."""
import base64, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = open('index.src.html', encoding='utf-8').read()
def b64(p): return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
out = (src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
          .replace('__HEROI__', b64('media/heroi.jpg')).replace('__MONTRA__', b64('media/montra.jpg')).replace('__LETREIRO__', b64('media/letreiro.jpg')))
assert '__' + 'FONTES' not in out and '__HEROI__' not in out
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024))
