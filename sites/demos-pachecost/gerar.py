#!/usr/bin/env python3
"""Junta o site pachecost.com e as demos num só zip (como o ro.pachecost.com).

Parte do zip mais recente do site da Pacheco Studios (ramo do thread dono,
claude/pacheco-studios-playbook-kztskg) e acrescenta demo/<curto>/ com index.html
(+ pt.html quando existe) e media/. O domínio demo.pachecost.com (alias no mesmo
projeto Netlify) é reescrito para /demo/, por isso demo.pachecost.com/la-gioia/
e pachecost.com/demo/la-gioia/ abrem a mesma página. Tudo com noindex.
Correr: python3 sites/demos-pachecost/gerar.py  ->  pachecost-com-e-demos-netlify.zip
"""
import os, re, shutil, subprocess, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SITES = os.path.dirname(AQUI)
OUT = os.path.join(AQUI, "_site")
RAMO_SITE = "claude/pacheco-studios-playbook-kztskg"
HOST = "https://demo.pachecost.com"

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
subprocess.run(["git", "fetch", "-q", "origin", RAMO_SITE], cwd=AQUI, check=True)
base = subprocess.run(["git", "show", f"origin/{RAMO_SITE}:sites/pacheco-studios/pacheco-studios-netlify.zip"],
                      cwd=AQUI, check=True, capture_output=True).stdout
base_zip = os.path.join(AQUI, "_base.zip")
with open(base_zip, "wb") as f:
    f.write(base)
with zipfile.ZipFile(base_zip) as z:
    z.extractall(OUT)
os.remove(base_zip)
assert os.path.exists(os.path.join(OUT, "index.html")) and not os.path.exists(os.path.join(OUT, "demo"))

regras = [f"{HOST}/    https://pachecost.com/    302!"]
for curto, pasta in DEMOS:
    src, dst = os.path.join(SITES, pasta), os.path.join(OUT, "demo", curto)
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
    regras.append(f"{HOST}/{curto}    {HOST}/{curto}/    301!")
    regras.append(f"/demo/{curto}    /demo/{curto}/    301")
regras.append(f"{HOST}/*    /demo/:splat    200!")

# entra antes da secção 3 do site; a primeira regra que bate ganha
rp = os.path.join(OUT, "_redirects")
with open(rp, encoding="utf-8") as f:
    r = f.read()
marca = "# 3)"
assert marca in r
r = r.replace(marca, "# 2b) demo.pachecost.com → /demo/ (sites/demos-pachecost/gerar.py)\n" + "\n".join(regras) + "\n" + marca, 1)
with open(rp, "w", encoding="utf-8") as f:
    f.write(r)
with open(os.path.join(OUT, "_headers"), "a", encoding="utf-8") as f:
    f.write("/demo/*\n  X-Robots-Tag: noindex, nofollow\n")
with open(os.path.join(OUT, "robots.txt"), encoding="utf-8") as f:
    rb = f.read()
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(rb.replace("Disallow: /p/\n", "Disallow: /p/\nDisallow: /demo/\n", 1))

zp = os.path.join(AQUI, "pachecost-com-e-demos-netlify.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for raiz, _, fs in os.walk(OUT):
        for f in sorted(fs):
            p = os.path.join(raiz, f)
            z.write(p, os.path.relpath(p, OUT))
print(f"site + {len(DEMOS)} demos -> {zp} ({os.path.getsize(zp)/1e6:.1f} MB)")
