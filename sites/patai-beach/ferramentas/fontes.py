#!/usr/bin/env python3
"""Descarrega as fontes do site (latin + latin-ext: ñ ¿ ¡ á é í ó ú ü ß) e escreve _fontes/fontes.css com @font-face em base64.
Correr uma vez: python3 ferramentas/fontes.py. O build.py embute o CSS na página."""
import re, base64, urllib.request, pathlib
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
FAMILIAS = ["Rufina:wght@400;700", "Figtree:ital,wght@0,400;0,500;0,600;1,400"]
saida = pathlib.Path(__file__).resolve().parent.parent / "_fontes" / "fontes.css"
partes, total = [], 0
for fam in FAMILIAS:
    req = urllib.request.Request("https://fonts.googleapis.com/css2?family=" + fam + "&display=swap", headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    for sub, corpo in re.findall(r"/\* (\S+) \*/\s*@font-face \{(.*?)\}", css, re.S):
        if sub not in ("latin", "latin-ext"):
            continue
        url = re.search(r"url\((https://[^)]+\.woff2)\)", corpo).group(1)
        dados = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()
        total += len(dados)
        corpo = re.sub(r"src: url\([^)]+\) format\('woff2'\)", "src: url(data:font/woff2;base64," + base64.b64encode(dados).decode() + ") format('woff2')", corpo)
        partes.append(f"/* {fam.split(':')[0].replace('+', ' ')} {sub} */\n@font-face {{{corpo}}}")
saida.write_text("\n".join(partes), encoding="utf-8")
print(f"{saida.name}: {len(partes)} faces, {total // 1024} KB woff2, {saida.stat().st_size // 1024} KB css")
