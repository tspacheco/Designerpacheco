#!/usr/bin/env python3
"""Gera index.html (um só ficheiro, sem pedidos externos) a partir de src.html + zip Netlify."""
import base64, io, pathlib, re, zipfile
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
MEDIA = AQUI.parent / "media"


def data_uri(nome):
    im = Image.open(MEDIA / (nome + ".webp")).convert("RGB")
    w = 120 if nome.startswith("stand") else 360
    im = im.resize((w, int(im.size[1] * w / im.size[0])), Image.LANCZOS)
    if nome.startswith("stand"):
        im = im.crop((0, 0, w, w))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=76)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


html = (AQUI / "src.html").read_text()
html = html.replace("{{FONTES}}", (AQUI.parent / "_fontes" / "fontes.css").read_text())
html = re.sub(r"\{\{IMG:([a-z0-9-]+)\}\}", lambda m: data_uri(m.group(1)), html)
assert "{{" not in html
(AQUI / "index.html").write_text(html)
with zipfile.ZipFile(AQUI / "rececionista-livre-netlify.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.write(AQUI / "index.html", "index.html")
print("ok index.html", len(html) // 1024, "KB")
