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
    ("gemino-barbershop", "gemino-barbershop"),
    ("frame-art", "frame-art"),
    ("bonvino", "bonvino"),
    ("cosi-buono", "cosi-buono"),
    ("shaorma-pacurari", "shaorma-pacurari"),
    ("carmangerie-spinu", "carmangerie-spinu"),
    ("bistro-felix", "bistro-felix"),
    ("extensii-gene-pacurari", "extensii-gene-pacurari"),
    ("yssa-beauty", "yssa-beauty"),
    ("andreea-lash", "andreea-lash"),
    ("odaia-neagra", "odaia-neagra"),
    ("magic-pets-house", "magic-pets-house"),
    ("fevila-pet-spa", "fevila-pet-spa"),
    ("star-service-auto", "star-service-auto"),
    ("service-auto-paul-ion", "service-auto-paul-ion"),
    ("service-la-pici", "service-la-pici"),
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
    # caçador 2026-10-09
    ("atractiv-barber", "atractiv-barber"),
    ("frizeria-magnific", "frizeria-magnific"),
    ("salon-manier", "salon-manier"),
    ("lisnic-barbershop", "lisnic-barbershop"),
    ("ego-hair-studio", "ego-hair-studio"),
    ("beauty-wow", "beauty-wow"),
    ("salon-michelle", "salon-michelle"),
    ("salon-venus", "salon-venus"),
    ("origins-coffee", "origins-coffee"),
    ("petale-coffee", "petale-coffee"),
    ("kinetomobil", "kinetomobil"),
    ("ambiental-covoare", "ambiental-covoare"),
    ("vulcanizare-miroslava", "vulcanizare-miroslava"),
    ("anton-giovani", "anton-giovani"),
    ("vfishing", "vfishing"),
    ("dulce-de-acasa", "dulce-de-acasa"),
    ("reparatii-termopane", "reparatii-termopane"),
    ("ami-salon", "ami-salon"),
    ("svl-salon", "svl-salon"),
    ("identity-marius-timofte", "identity-marius-timofte"),
    ("such-salon", "such-salon"),
    ("fade-society", "fade-society"),
    ("la-detaliu", "la-detaliu"),
    ("tapiterie-auto-iasi", "tapiterie-auto-iasi"),
    ("spaauto", "spaauto"),
    ("idalia", "idalia"),
    ("atelier-madi", "atelier-madi"),
    ("pescaria-galata", "pescaria-galata"),
    ("pescaria-noastra", "pescaria-noastra"),
    ("piscicola", "piscicola"),
    ("dynamite-pacurari", "dynamite-pacurari"),
    ("roxette", "roxette"),
    ("vogue-pacurari", "vogue-pacurari"),
    ("cosmetica-pacurari", "cosmetica-pacurari"),
    ("mop-vet", "mop-vet"),
    ("vet-point-of-care", "vet-point-of-care"),
    ("pethealth", "pethealth"),
    ("total-fauna", "total-fauna"),
    ("be3concept", "be3concept"),
    ("elephant-car-wash", "elephant-car-wash"),
    ("crys-grill", "crys-grill"),
    ("beer-house", "beer-house"),
    ("pilates-fusion", "pilates-fusion"),
    ("swallow-pilates", "swallow-pilates"),
    ("status-coffee", "status-coffee"),
    ("fresco-jugo", "fresco-jugo"),
]
NOINDEX = '<meta name="robots" content="noindex, nofollow">'
# Contador de aberturas (tracker das demos, ramo claude/tracker-demos-kx5ukf): só no index.html,
# com o caminho fixo /demo/<curto>/ para contar igual em pachecost.com/demo/, demo.pachecost.com
# e pachecost-demos.netlify.app. Sem cookies e sem script externo (um pedido de imagem ao GoatCounter).
# Não conta navegadores automáticos (ponte, testes) nem quem abriu um link com #nao-contar
# (o Tomás faz isso uma vez em cada telemóvel/PC para não contar as próprias visitas).
CONTADOR = ('<script>(function(c){try{var L=localStorage;if(location.hash=="#nao-contar")'
            '{L.setItem("skipgc","t");return}if(L.getItem("skipgc")=="t")return}catch(e){}'
            'if(navigator.webdriver)return;'
            # quem chega das páginas por nicho (/site-uri/, /sites/) não é o dono: conta à parte, em /nisa-demo/
            'var b=/\\/(site-uri|sites)\\//.test(document.referrer)?"/nisa-demo/":"/demo/";'
            'var q="p="+encodeURIComponent(b+c+"/")+"&t="+'
            'encodeURIComponent(document.title)+"&r="+encodeURIComponent(document.referrer)+'
            '"&rnd="+Math.random().toString(36).slice(2);'
            '(new Image).src="https://pachecost.goatcounter.com/count?"+q})("%s")</script>')

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
        if "index.html" in htmls:
            htmls["index.html"] = htmls["index.html"].replace("</body>", CONTADOR % curto + "</body>", 1)
        for nome, html in htmls.items():
            with open(os.path.join(dst, nome), "w", encoding="utf-8") as f:
                f.write(html)
        for f in os.listdir(os.path.join(src, "media")):
            p = os.path.join(src, "media", f)
            if os.path.isfile(p) and f != "LEIA-ME.txt":
                shutil.copy2(p, os.path.join(dst, "media", f))
    # páginas por nicho e cidade (sites/paginas-nicho): indexáveis, servidas pelo pachecost.com e pelo
    # ro.pachecost.com através das regras de gerar_site(); refazem-se a cada push, com as demos novas
    # Se falharem, as demos publicam-se na mesma (são os links que já foram enviados aos donos).
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("paginas_nicho", os.path.join(SITES, "paginas-nicho", "gerar.py"))
        paginas_nicho = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(paginas_nicho)
        paginas_nicho.gerar(SITES, os.path.abspath(__file__), out)
    except Exception as erro:  # noqa: BLE001
        print("AVISO: páginas por nicho não geradas:", repr(erro))
    with open(os.path.join(out, "_redirects"), "w", encoding="utf-8") as f:
        f.write("/    https://pachecost.com/    302\n")
    with open(os.path.join(out, "_headers"), "w", encoding="utf-8") as f:
        # noindex só nas demos (as páginas por nicho têm de ser indexadas)
        f.writelines(f"/{curto}/*\n  X-Robots-Tag: noindex, nofollow\n" for curto, _ in DEMOS)
        f.write("/*/media/*\n  Cache-Control: public, max-age=604800\n")
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
              f"/demo/*    {DEMOS_URL}/:splat    200!",
              # páginas por nicho e cidade (vivem no projeto das demos, que se publica a cada push)
              "https://ro.pachecost.com/sites/*    https://pachecost.com/sites/:splat    301!",
              "https://pachecost.com/site-uri/*    https://ro.pachecost.com/site-uri/:splat    301!",
              f"https://ro.pachecost.com/site-uri/*    {DEMOS_URL}/site-uri/:splat    200!",
              f"/sites/*    {DEMOS_URL}/sites/:splat    200!",
              f"/sitemap-nichos.xml    {DEMOS_URL}/sitemap-nichos.xml    200!"]
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
        rb = rb.replace("Disallow: /p/\n", "Disallow: /p/\nDisallow: /demo/\n", 1)
        f.write(rb.rstrip("\n") + "\nSitemap: https://pachecost.com/sitemap-nichos.xml\n")
    zp = os.path.join(AQUI, "pachecost-com-netlify.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for raiz, _, fs in os.walk(out):
            for f in sorted(fs):
                p = os.path.join(raiz, f)
                z.write(p, os.path.relpath(p, out))
    print(f"site + regras das demos -> {zp} ({os.path.getsize(zp)/1e6:.1f} MB)")


if __name__ == "__main__":
    gerar_demos() if "--so-demos" in sys.argv else gerar_site()
