#!/usr/bin/env python3
"""Monta index.html: injeta as fontes (base64) e a fotografia da montra do restaurante em index.src.html."""
import base64, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = open('index.src.html', encoding='utf-8').read()
foto = 'data:image/jpeg;base64,' + base64.b64encode(open('media/restaurante-montra.jpg', 'rb').read()).decode()
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read()).replace('__MONTRA__', foto)
assert '__' + 'FONTES' not in out and '__MONTRA__' not in out
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024))
