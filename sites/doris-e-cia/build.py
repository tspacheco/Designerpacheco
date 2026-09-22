#!/usr/bin/env python3
"""Doris & Cia Pet Shop (Vila Barros, Guarulhos) — demo Pacheco Studios.
Gera index.html a partir de index.src.html embutindo as fontes em base64 (site sem rede)."""
import base64, pathlib, re
HERE = pathlib.Path(__file__).parent
F = HERE.parent.parent / "propostas" / "doris-e-cia" / "fontes"
def face(fam, w, f):
    b = base64.b64encode((F / f).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;font-display:swap;src:url(data:font/woff2;base64,{b}) format('woff2')}}"
fonts = "\n".join([face("Fredoka",500,"Fredoka-500.woff2"),face("Fredoka",700,"Fredoka-700.woff2"),
                   face("Nunito",400,"Nunito-400.woff2"),face("Nunito",700,"Nunito-700.woff2"),face("Caveat",600,"Caveat-600.woff2")])
src = (HERE / "index.src.html").read_text(encoding="utf-8")
out = src.replace("/*FONTS*/", fonts)
(HERE / "index.html").write_text(out, encoding="utf-8")
print("index.html", len(out)//1024, "KB")
