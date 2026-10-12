#!/usr/bin/env python3
"""Gera index.html (um só ficheiro) a partir de src.html: fontes e fotos reais embutidas."""
import base64, io, pathlib, re, zipfile
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
MEDIA = AQUI.parent / "media"
FOTOS = {"cheie-toyota": 420, "cheie-vw-touran": 420, "card-renault-megane": 420, "cheie-opel": 420,
         "cheie-mercedes-vito": 420, "stand-magic-key": 160}


def data_uri(nome, w):
    im = Image.open(MEDIA / (nome + ".webp")).convert("RGB")
    im = im.resize((w, int(im.size[1] * w / im.size[0])), Image.LANCZOS)
    if nome.startswith("stand"):
        im = im.crop((0, 0, w, w))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=78)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


html = (AQUI / "src.html").read_text()
html = html.replace("{{FONTES}}", (AQUI.parent / "_fontes" / "fontes.css").read_text())
html = re.sub(r"\{\{IMG:([a-z0-9-]+)\}\}", lambda m: data_uri(m.group(1), FOTOS[m.group(1)]), html)
(AQUI / "index.html").write_text(html)
with zipfile.ZipFile(AQUI / "rececionista-magic-key-netlify.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.write(AQUI / "index.html", "index.html")
print("ok index.html", len(html) // 1024, "KB")
