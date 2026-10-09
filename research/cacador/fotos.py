#!/usr/bin/env python3
"""Gera pedidos «imagem» da ponte a partir de ponte/<prefixo>fotos-<nome>.imagens.txt (fotosmaps).
  python3 research/cacador/fotos.py <slug do site>=<ficheiro imagens.txt> ... > .github/ponte.txt
Até 10 fotos distintas por negócio, a 1600 px, em sites/<slug>/media/g/NN.webp."""
import re, sys
print("# caçador — fotos para as demos")
for arg in sys.argv[1:]:
    slug, f = arg.split("=", 1)
    vistos, n = set(), 0
    for u in open(f, encoding="utf-8").read().split():
        m = re.match(r"(https://lh\d\.googleusercontent\.com/(?:gps-cs-s|p)/[A-Za-z0-9_-]+)", u)
        if not m or m.group(1) in vistos:
            continue
        vistos.add(m.group(1)); n += 1
        print(f'imagem sites/{slug}/media/g/{n:02d}.webp "{m.group(1)}=w1600"')
        if n == 10:
            break
