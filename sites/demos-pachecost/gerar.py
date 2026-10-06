#!/usr/bin/env python3
"""Junta as demos num só site Netlify (demo.pachecost.com/<curto>/).

Cada demo fica numa pasta com index.html (+ pt.html quando existe) e media/.
Tudo leva noindex: são apresentações para o dono ver, não sites públicos.
Correr: python3 sites/demos-pachecost/gerar.py  ->  demos-pachecost-netlify.zip
"""
import os, re, shutil, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SITES = os.path.dirname(AQUI)
OUT = os.path.join(AQUI, "_site")

DEMOS = [  # (endereço curto, pasta em sites/)
    ("la-gioia", "la-gioia-di-giovanni"),
    ("laurinda", "cofetaria-laurinda"),
    ("sir-johns", "sir-johns-barbershop"),
    ("sofia-pets", "sofia-pets"),
    ("elenor", "floraria-elenor"),
    ("beauty-zone", "beauty-zone"),
    ("butterfly", "salon-butterfly"),
    ("croitoria-dan", "croitoria-dan"),
    ("auto-spa", "auto-spa-detailing"),
    ("la-punct", "service-auto-la-punct"),
    ("tasquinha-do-bruno", "tasquinha-do-bruno"),
    ("tasca-do-to", "tasca-do-to"),
    ("o-antonio", "o-antonio"),
    ("colibri", "restaurante-colibri"),
    ("barbers-touch", "barbers-touch"),
    ("sr-bonifacio", "barbearia-sr-bonifacio"),
    ("flor-mimosa", "flor-mimosa"),
    ("faisca-henriques", "faisca-henriques"),
    ("sos-car", "sos-car"),
    ("mb-cakes", "mb-cakes"),
]
NOINDEX = '<meta name="robots" content="noindex, nofollow">'


def com_noindex(html):
    if 'name="robots"' in html:
        return re.sub(r'<meta name="robots"[^>]*>', NOINDEX, html, count=1)
    return re.sub(r"(<head[^>]*>)", r"\1" + NOINDEX, html, count=1)


shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
redirects = []
for curto, pasta in DEMOS:
    src, dst = os.path.join(SITES, pasta), os.path.join(OUT, curto)
    os.makedirs(os.path.join(dst, "media"))
    for nome in ("index.html", "pt.html"):
        p = os.path.join(src, nome)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                html = com_noindex(f.read())
            with open(os.path.join(dst, nome), "w", encoding="utf-8") as f:
                f.write(html)
    for f in os.listdir(os.path.join(src, "media")):
        p = os.path.join(src, "media", f)
        if os.path.isfile(p) and f != "LEIA-ME.txt":
            shutil.copy2(p, os.path.join(dst, "media", f))
    # sem a barra final os caminhos relativos (media/...) partiam-se
    redirects.append(f"/{curto} /{curto}/ 301")

with open(os.path.join(OUT, "_redirects"), "w") as f:
    f.write("\n".join(redirects) + "\n/ https://pachecost.com 302\n")
with open(os.path.join(OUT, "netlify.toml"), "w") as f:
    f.write('[[headers]]\n  for = "/*"\n  [headers.values]\n    X-Robots-Tag = "noindex, nofollow"\n')
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write("User-agent: *\nDisallow: /\n")

zp = os.path.join(AQUI, "demos-pachecost-netlify.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for raiz, _, fs in os.walk(OUT):
        for f in sorted(fs):
            p = os.path.join(raiz, f)
            z.write(p, os.path.relpath(p, OUT))
print(f"{len(DEMOS)} demos -> {zp} ({os.path.getsize(zp)/1e6:.1f} MB)")
