#!/usr/bin/env python3
"""Demos dos clientes num projeto Netlify próprio, ligado ao GitHub, e o pachecost.com leve.

Desde 07/10/2026 as demos já não vão dentro do zip do pachecost.com (com 30 demos passava
dos 77 MB e o Netlify recusou-o). Ficam no projeto Netlify «pachecost-demos», que se
publica sozinho a partir deste ramo do GitHub (sem zip nem limite de tamanho), e o
pachecost.com só reencaminha: pachecost.com/demo/<curto>/ e demo.pachecost.com/<curto>/
mostram a página do projeto das demos sem mudar o endereço.

  python3 gerar.py --so-demos   ->  _demos/<curto>/  (é o que o Netlify corre; ver netlify.toml)
  python3 gerar.py              ->  pachecost-com-netlify.zip (site da Pacheco Studios + regras)

O site da Pacheco Studios vem do zip mais recente do ramo do thread dono
(claude/pacheco-studios-playbook-kztskg). Tudo o que é demo leva noindex.
Para juntar uma demo: acrescentar uma linha a DEMOS e fazer push.
"""
import os, re, shutil, subprocess, sys, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SITES = os.path.dirname(AQUI)
RAMO_SITE = "claude/pacheco-studios-playbook-kztskg"
HOST = "https://demo.pachecost.com"
DEMOS_URL = "https://pachecost-demos.netlify.app"  # nome do projeto Netlify das demos

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
    ("fika", "fika-iasi"),
    ("petit-bijou", "petit-bijou"),
    ("vulcanizare", "vulcanizare-service-roti"),
    ("pumbavet", "pumbavet"),
    ("unghii-gel", "unghii-gel"),
    ("geange", "cizmarie-geange"),
    ("dubai-shaworma", "dubai-shaworma"),
    ("trend-barbershop", "trend-barbershop"),
    ("atelier-croitorie", "atelier-croitorie-la-comanda"),
    ("tapiterie", "tapiterie-david-macris"),
    # lote 3 de Iași (07/10)
    ("arca-pet", "arca-pet"),
    ("noir-barbershop", "noir-barbershop"),
    ("motiv-key", "motiv-key"),
    ("peony-beauty", "peony-beauty"),
    ("brutaria-rustica", "brutaria-rustica"),
    ("weekend-salon", "weekend-salon"),
    ("optimum-auto", "optimum-auto"),
    ("bike-4-ride", "bike-4-ride"),
    ("reparatii-tv-alex-conrad", "reparatii-tv-alex-conrad"),
    ("meat-concept-store", "meat-concept-store"),
    ("tattoo-alice", "tattoo-alice"),
    ("ceasornicarie-nicolina", "ceasornicarie-nicolina"),
    ("estetica-new-shape", "estetica-new-shape"),
    ("exclusive-laundry", "exclusive-laundry"),
    ("inkhaus-tattoo", "inkhaus-tattoo"),
    # lote 4 de Iași (08/10)
    ("pro-masaj-domiciliu", "pro-masaj-domiciliu"),
    ("acm-masaj", "acm-masaj"),
    ("kineos-massage", "kineos-massage"),
    ("croitorie-grand-siraj", "croitorie-grand-siraj"),
    ("interventii-rapide", "interventii-rapide"),
    ("chei-targu-cucu", "chei-targu-cucu"),
    ("magic-key", "magic-key"),
    ("dubitec", "dubitec"),
    ("city-wash", "city-wash"),
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
FONTE = re.compile(r"@font-face\s*\{[^}]*?url\(['\"]?data:[^}]*\}")


# Sem a barra final os caminhos relativos (media/...) partiam-se. Não se resolve no
# _redirects: o Netlify ignora a barra final ao comparar regras, e /x → /x/ 301! fazia
# um ciclo infinito (06/10). Por isso a página acrescenta a barra antes de carregar.
BARRA = ('<script>(function(l){if(!/\\/$|\\.html$/.test(l.pathname))'
         'l.replace(l.pathname+"/"+l.search+l.hash)})(location)</script>')


def com_noindex(html):
    html = re.sub(r"(<head[^>]*>)", r"\1" + BARRA.replace("\\", "\\\\"), html, count=1)
    if 'name="robots"' in html:
        return re.sub(r'<meta name="robots"[^>]*>', NOINDEX, html, count=1)
    return re.sub(r"(<head[^>]*>)", r"\1" + NOINDEX, html, count=1)


def gerar_demos():
    out = os.path.join(AQUI, "_demos")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    for curto, pasta in DEMOS:
        src, dst = os.path.join(SITES, pasta), os.path.join(out, curto)
        os.makedirs(os.path.join(dst, "media"))
        htmls = {}
        for nome in ("index.html", "pt.html"):
            p = os.path.join(src, nome)
            if os.path.exists(p):
                with open(p, encoding="utf-8") as f:
                    htmls[nome] = com_noindex(f.read())
        # index.html e pt.html levam as mesmas fontes em base64: passam a um fontes.css comum
        blocos = {n: FONTE.findall(h) for n, h in htmls.items()}
        if len(htmls) == 2 and blocos["index.html"] and blocos["index.html"] == blocos["pt.html"]:
            with open(os.path.join(dst, "fontes.css"), "w", encoding="utf-8") as f:
                f.write("\n".join(blocos["index.html"]))
            for n in htmls:
                h = FONTE.sub("", htmls[n])
                htmls[n] = re.sub(r"(<head[^>]*>)", r'\1<link rel="stylesheet" href="fontes.css">', h, count=1)
        for nome, html in htmls.items():
            with open(os.path.join(dst, nome), "w", encoding="utf-8") as f:
                f.write(html)
        for f in os.listdir(os.path.join(src, "media")):
            p = os.path.join(src, "media", f)
            if os.path.isfile(p) and f != "LEIA-ME.txt":
                shutil.copy2(p, os.path.join(dst, "media", f))
    with open(os.path.join(out, "_redirects"), "w", encoding="utf-8") as f:
        f.write("/    https://pachecost.com/    302\n")
    with open(os.path.join(out, "_headers"), "w", encoding="utf-8") as f:
        f.write("/*\n  X-Robots-Tag: noindex, nofollow\n/*/media/*\n  Cache-Control: public, max-age=604800\n")
    with open(os.path.join(out, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nDisallow: /\n")
    tam = sum(os.path.getsize(os.path.join(r, x)) for r, _, fs in os.walk(out) for x in fs)
    print(f"{len(DEMOS)} demos -> {out} ({tam/1e6:.1f} MB)")


def gerar_site():
    out = os.path.join(AQUI, "_site")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    subprocess.run(["git", "fetch", "-q", "origin", RAMO_SITE], cwd=AQUI, check=True)
    base = subprocess.run(["git", "show", f"origin/{RAMO_SITE}:sites/pacheco-studios/pacheco-studios-netlify.zip"],
                          cwd=AQUI, check=True, capture_output=True).stdout
    base_zip = os.path.join(AQUI, "_base.zip")
    with open(base_zip, "wb") as f:
        f.write(base)
    with zipfile.ZipFile(base_zip) as z:
        z.extractall(out)
    os.remove(base_zip)
    assert os.path.exists(os.path.join(out, "index.html")) and not os.path.exists(os.path.join(out, "demo"))
    regras = [f"{HOST}/    https://pachecost.com/    302!",
              f"{HOST}/*    {DEMOS_URL}/:splat    200!",
              f"/demo/*    {DEMOS_URL}/:splat    200!"]
    # entra antes da secção 3 do site; a primeira regra que bate ganha
    rp = os.path.join(out, "_redirects")
    with open(rp, encoding="utf-8") as f:
        r = f.read()
    marca = "# 3)"
    assert marca in r
    r = r.replace(marca, "# 2b) demos → projeto Netlify das demos (sites/demos-pachecost/gerar.py)\n"
                  + "\n".join(regras) + "\n" + marca, 1)
    with open(rp, "w", encoding="utf-8") as f:
        f.write(r)
    with open(os.path.join(out, "_headers"), "a", encoding="utf-8") as f:
        f.write("/demo/*\n  X-Robots-Tag: noindex, nofollow\n")
    with open(os.path.join(out, "robots.txt"), encoding="utf-8") as f:
        rb = f.read()
    with open(os.path.join(out, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(rb.replace("Disallow: /p/\n", "Disallow: /p/\nDisallow: /demo/\n", 1))
    zp = os.path.join(AQUI, "pachecost-com-netlify.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for raiz, _, fs in os.walk(out):
            for f in sorted(fs):
                p = os.path.join(raiz, f)
                z.write(p, os.path.relpath(p, out))
    print(f"site + regras das demos -> {zp} ({os.path.getsize(zp)/1e6:.1f} MB)")


if __name__ == "__main__":
    gerar_demos() if "--so-demos" in sys.argv else gerar_site()
