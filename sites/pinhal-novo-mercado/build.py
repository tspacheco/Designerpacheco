#!/usr/bin/env python3
"""Monta index.html: injeta as fontes (base64) e a fotografia da fachada em index.src.html."""
import base64, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src=open('index.src.html',encoding='utf-8').read()
fontes=open('_fontes/fontes.css',encoding='utf-8').read()
foto='data:image/jpeg;base64,'+base64.b64encode(open('media/restaurante-fachada.jpg','rb').read()).decode()
out=src.replace('/*__FONTES__*/',fontes).replace('__FOTO_FACHADA__',foto)
assert '__FONTES__' not in out and '__FOTO_FACHADA__' not in out
open('index.html','w',encoding='utf-8').write(out)
print('index.html %.0f KB'%(len(out.encode())/1024))
