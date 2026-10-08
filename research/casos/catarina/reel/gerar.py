#!/usr/bin/env python3
"""Reel 9:16 do caso Catarina, com o gerador do agente 4 (ramo claude/reels-demos-pjhcbh, social/reels-demos/).

  python3 research/casos/catarina/reel/gerar.py        (Playwright, ffmpeg, numpy)

Lê o gerador e o site da Catarina com git archive (não escreve em nenhum desses ramos) e troca só
o gancho: em vez de «Seria assim.» (demo), o caso abre com o resultado, «Agora tem.».
Quando a dona der os números, muda GANCHO_L2/GANCHO_L3 (ex.: «+8 reservas por semana.») e volta a correr.
Saída: saida/reel-catarina-9x16.mp4 e -capa.jpg (a legenda do caso está em ../LEIA-ME.md).
"""
import os, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = subprocess.run(["git", "-C", AQUI, "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RAMO_REELS = "claude/reels-demos-pjhcbh"
RAMO_SITE = "claude/catarina-alteracoes-657ynq"
GANCHO_L2 = "168 avaliações. Nenhum site."
GANCHO_L3 = "Agora tem."

R = {"slug": "catarina", "nome": "Pizzaria Catarina", "cidade": "Altura", "morada": "R. da Alagoa 84 · Altura",
     "lang": "pt", "nota": 4.4, "avaliacoes": 168, "musica": "quente", "instagram": "@pizzaria_catarina",
     "hashtags": "#algarve #altura #pizzaria #webdesign #pequenosnegocios"}


def arquivo(ramo, caminho, dst):
    subprocess.run(["git", "-C", RAIZ, "fetch", "-q", "origin", f"{ramo}:refs/remotes/origin/{ramo}"], check=True)
    a = subprocess.run(["git", "-C", RAIZ, "archive", f"origin/{ramo}", caminho], capture_output=True, check=True).stdout
    os.makedirs(dst, exist_ok=True)
    subprocess.run(["tar", "-x", "-C", dst, f"--strip-components={caminho.count('/') + 1}"], input=a, check=True)


trab = os.path.join(AQUI, "_trab"); shutil.rmtree(trab, ignore_errors=True)
ger = os.path.join(trab, "gerador"); arquivo(RAMO_REELS, "social/reels-demos", ger)
site = os.path.join(trab, "site"); arquivo(RAMO_SITE, "sites/pizzaria-catarina", site)

# o site carrega as fontes por <link> do Google Fonts; o gerador só lê @font-face, por isso embute-se o CSS
import re, urllib.request  # noqa: E402
idx = os.path.join(site, "index.html"); html = open(idx, encoding="utf-8").read()
for url in re.findall(r'href="(https://fonts\.googleapis\.com/css2[^"]+)"', html):
    req = urllib.request.Request(url.replace("&amp;", "&"), headers={"User-Agent": "Mozilla/5.0 Chrome/120"})
    html = html.replace("</head>", "<style>" + urllib.request.urlopen(req).read().decode() + "</style></head>", 1)
open(idx, "w", encoding="utf-8").write(html)

sys.path.insert(0, ger)
import gerar_reel as g  # noqa: E402

g.demo = lambda slug, t: site
g.TXT["pt"]["aval"] = lambda n: GANCHO_L2
g.TXT["pt"]["l3"] = GANCHO_L3
g.gerar(R)

saida = os.path.join(AQUI, "saida"); os.makedirs(saida, exist_ok=True)
for f in os.listdir(os.path.join(ger, "saida", "catarina")):
    shutil.copy(os.path.join(ger, "saida", "catarina", f), saida)
shutil.rmtree(trab, ignore_errors=True)
os.remove(os.path.join(saida, "legenda.md"))  # a legenda do gerador é de demo
print("ok", saida)
