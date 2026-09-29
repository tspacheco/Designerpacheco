#!/usr/bin/env python3
"""Monta index.html (ficheiro único) a partir de src/index.html, embutindo _fontes/fontes.css no marcador <!--@fontes-->.
    python3 ferramentas/build.py"""
import pathlib, sys
RAIZ = pathlib.Path(__file__).resolve().parent.parent
html = (RAIZ / "src" / "index.html").read_text(encoding="utf-8")
fontes = (RAIZ / "_fontes" / "fontes.css").read_text(encoding="utf-8")
if "<!--@fontes-->" not in html:
    sys.exit("src/index.html: falta o marcador <!--@fontes-->")
html = html.replace("<!--@fontes-->", "<style>\n" + fontes + "\n</style>")
destino = RAIZ / "index.html"
destino.write_text(html, encoding="utf-8")
print(f"{destino.name}: {destino.stat().st_size // 1024} KB")
