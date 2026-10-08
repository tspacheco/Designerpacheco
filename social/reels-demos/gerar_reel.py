#!/usr/bin/env python3
"""Reel 9:16 a partir de uma demo de pachecost.com/demo/<slug>/ (agente 4: um reel por demo).

  python3 gerar_reel.py <slug> [<slug> ...]     (Playwright, ffmpeg, numpy)

Os dados de cada reel vêm do reels.json (nota e n.º de avaliações Google confirmados, morada,
língua, estilo de música). A demo é tirada do ramo das demos (claude/dez-negocios-dez-websites-7gevwu)
com git archive: este script só lê esse ramo, nunca escreve nele.

Estrutura (10 compassos, a música manda no corte):
  2 compassos  gancho: «4,9★ pe Google · 82 de recenzii. Niciun site. Așa ar arăta.» (já no 1.º fotograma)
               por baixo, o herói da demo a fazer a entrada
  7 compassos  nome do negócio + morada; o site desce uma secção por compasso
  1 compasso   «Ai o afacere? Meriți un site ca acesta.»
  3 s          ecrã final: ro.pachecost.com / pachecost.com + «Portugal based · Acting worldwide»
A identidade (fonte de título, cor de destaque, fundo) é a da própria demo, por isso cada reel
sai diferente sem trabalho manual.

Saída: saida/<slug>/reel-<slug>-9x16.mp4, -capa.jpg e legenda.md (legenda + mensagem ao dono).
"""
import asyncio, json, os, re, shutil, subprocess, sys
from playwright.async_api import async_playwright
from captar import captar, CHROME, FPS

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
RAMO_DEMOS = "origin/claude/dez-negocios-dez-websites-7gevwu"
FAIXA, FECHO = 470, 3.0
BPM = {"urbano": 92, "quente": 86, "energia": 116}

TXT = {
    "ro": dict(sub="pe Google", aval=lambda n: f"{n} {'de ' if n % 100 >= 20 or n % 100 == 0 else ''}recenzii. Niciun site.",
               l3="Așa ar arăta.", credito="Site creat de Pacheco Studios", f1="Ai o afacere?",
               f2="Meriți un site ca acesta.", url="ro.pachecost.com"),
    "pt": dict(sub="no Google", aval=lambda n: f"{n} avaliações. Nenhum site.", l3="Seria assim.",
               credito="Site feito pela Pacheco Studios", f1="Tem um negócio?", f2="Merece um site assim.",
               url="pachecost.com"),
    "en": dict(sub="on Google", aval=lambda n: f"{n} reviews. No website.", l3="Here's how it could look.",
               credito="Website by Pacheco Studios", f1="Business owner?", f2="You deserve a website like this.",
               url="pachecost.com"),
}


def sh(*a, **k):
    return subprocess.run(a, check=True, **k)


def demo(slug, trab):
    """Extrai a pasta da demo do ramo das demos (mapa slug → pasta no gerar.py desse ramo)."""
    sh("git", "-C", RAIZ, "fetch", "-q", "origin", f"{RAMO_DEMOS.split('/', 1)[1]}:refs/remotes/{RAMO_DEMOS}")
    g = subprocess.run(["git", "-C", RAIZ, "show", f"{RAMO_DEMOS}:sites/demos-pachecost/gerar.py"],
                       capture_output=True, text=True, check=True).stdout
    mapa = dict(re.findall(r'\("([^"]+)",\s*"([^"]+)"\)', g))
    pasta = mapa.get(slug, slug)
    dst = os.path.join(trab, "demo")
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)
    arq = subprocess.run(["git", "-C", RAIZ, "archive", RAMO_DEMOS, f"sites/{pasta}/index.html", f"sites/{pasta}/media"],
                         capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", dst, "--strip-components=2"], input=arq, check=True)
    return dst


async def titulos(cfg, fontes_css, trab, tempos):
    """Fotogramas transparentes do texto, só nos momentos em que algo mexe (o resto fica parado)."""
    d = os.path.join(trab, "tit"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    total = cfg["T"]["fim"] + FECHO
    ts = set()
    for a, z in tempos:
        ts |= {round(a + i / FPS, 4) for i in range(int(round((z - a) * FPS)) + 1)}
    ts = sorted(t for t in ts if 0 <= t < total)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME)
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto(f"file://{AQUI}/titulos.html")
        await pg.add_style_tag(path=fontes_css)
        await pg.evaluate("document.fonts.ready.then(()=>1)")
        await pg.evaluate("cfg => init(cfg)", cfg)
        await pg.evaluate("document.fonts.ready.then(()=>1)")
        linhas = []
        for i, t in enumerate(ts):
            await pg.evaluate(f"setT({t})")
            await pg.screenshot(path=f"{d}/{i:05d}.png", omit_background=True)
            nxt = ts[i + 1] if i + 1 < len(ts) else total
            linhas.append(f"file '{d}/{i:05d}.png'\nduration {nxt - t:.4f}\n")
        linhas.append(f"file '{d}/{len(ts) - 1:05d}.png'\n")
        open(f"{d}/lista.txt", "w").write("".join(linhas))
        await b.close()
    return f"{d}/lista.txt"


def legenda(r, saida):
    """Legenda do Instagram (máx. 5 hashtags) e a mensagem de pedido ao dono, com a versão PT para o Tomás."""
    L = r["lang"]
    nota, n = r["nota"], r["avaliacoes"]
    tpl = json.load(open(os.path.join(AQUI, "textos.json"), encoding="utf-8"))
    nota = f"{nota:.1f}".replace(".", "," if L in ("ro", "pt") else ".")
    sub = dict(nome=r["nome"], cidade=r["cidade"], nota=nota, n=n, hashtags=r["hashtags"], link=f"https://pachecost.com/demo/{r['slug']}/",
               ig=r.get("instagram") or "@… (a confirmar)", tag=r.get("instagram") or r["nome"])
    f = lambda s: s.format(**sub)
    md = [f"# Reel · {r['nome']} ({r['cidade']})\n",
          f"Vídeo: `reel-{r['slug']}-9x16.mp4` · capa: `reel-{r['slug']}-capa.jpg` · demo: {sub['link']}\n",
          f"Instagram do negócio: {sub['ig']}\n",
          "## 1. Mensagem ao dono (WhatsApp, com o vídeo anexado)\n",
          f"**{L.upper()}**\n\n" + f(tpl["pedido"][L]) + "\n",
          "**PT (para ti)**\n\n" + f(tpl["pedido"]["pt"]) + "\n" if L != "pt" else "",
          "## 2. Se disser que sim: resposta\n",
          f"**{L.upper()}**\n\n" + f(tpl["sim"][L]) + "\n",
          "**PT (para ti)**\n\n" + f(tpl["sim"]["pt"]) + "\n" if L != "pt" else "",
          "## 3. Legenda do Instagram (só depois do «sim»; publicar como Colaboração com o negócio)\n",
          f(tpl["legenda"][L]) + "\n",
          "**PT (para ti)**\n\n" + f(tpl["legenda"]["pt"]) + "\n" if L != "pt" else ""]
    open(os.path.join(saida, "legenda.md"), "w", encoding="utf-8").write("\n".join(x for x in md if x))


def gerar(r):
    slug, L = r["slug"], r["lang"]
    trab = os.path.join(AQUI, "_trab", slug); os.makedirs(trab, exist_ok=True)
    saida = os.path.join(AQUI, "saida", slug); os.makedirs(saida, exist_ok=True)
    pasta = demo(slug, trab)
    html = open(os.path.join(pasta, "index.html"), encoding="utf-8").read()
    fontes = os.path.join(trab, "fontes.css")
    open(fontes, "w").write("\n".join(re.findall(r"@font-face\s*\{[^}]*\}", html)))

    bpm = r.get("bpm") or BPM[r["musica"]]
    bar = 4 * 60 / bpm
    T = {"gancho": 2 * bar, "nome": 2 * bar, "frase": 9 * bar, "fim": 10 * bar}
    dur = T["fim"]
    print(slug, f"{bpm} BPM, {dur:.1f} s + {FECHO} s", flush=True)

    ident = asyncio.run(captar(pasta, os.path.join(trab, "site"), dur, ini=T["nome"], periodo=bar, n_paragens=7))
    t = TXT[L]
    nota = f"{r['nota']:.1f}".replace(".", "," if L in ("ro", "pt") else ".")
    cfg = {
        "fundo": r.get("fundo") or ident["fundo"], "cor": r.get("cor") or ident["cor"],
        "acento": r.get("acento") or ident["acento"], "ft": ident["titulo"], "fx": ident["texto"],
        "gancho": {"nota": nota, "sub": t["sub"], "l2": t["aval"](r["avaliacoes"]), "l3": t["l3"]} if r.get("nota") else None,
        "nome": r["nome"], "morada": r["morada"], "credito": t["credito"], "f1": t["f1"], "f2": t["f2"],
        "url": t["url"], "T": T,
    }
    lista = asyncio.run(titulos(cfg, fontes, trab, [
        (0, 2.2), (T["gancho"] - 1.5, T["gancho"] - .5), (T["nome"] - .4, T["nome"] + 1.3),
        (T["frase"] - .4, T["frase"] + 1.1), (T["fim"] - .2, T["fim"] + 1.1)]))

    total = dur + FECHO
    mj = os.path.join(trab, "musica.json")
    json.dump({"style": r["musica"], "bpm": bpm, "dur": total, "end": dur, "seed": slug}, open(mj, "w"))
    sh("python3", os.path.join(AQUI, "som-demos.py"), mj, os.path.join(trab, "musica.wav"))

    out = os.path.join(saida, f"reel-{slug}-9x16.mp4")
    fc = (f"color=c=black:s=1080x1920:r={FPS}:d={total:.3f}[c];"
          f"[0:v]fps={FPS}[s];[c][s]overlay=0:{FAIXA}:eof_action=repeat[bg];"
          f"[1:v]fps={FPS},format=rgba[o];[bg][o]overlay=0:0:eof_action=repeat:format=auto,format=yuv420p[v]")
    sh("ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{trab}/site/%05d.png",
       "-f", "concat", "-safe", "0", "-i", lista, "-i", f"{trab}/musica.wav",
       "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{total:.2f}",
       "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "8M", "-bufsize", "16M", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out)
    sh("ffmpeg", "-v", "error", "-y", "-ss", f"{T['gancho'] - .3:.2f}", "-i", out, "-frames:v", "1", "-q:v", "3",
       os.path.join(saida, f"reel-{slug}-capa.jpg"))
    legenda(r, saida)
    print("ok", out, f"{os.path.getsize(out) / 1e6:.1f} MB", flush=True)


if __name__ == "__main__":
    reels = {r["slug"]: r for r in json.load(open(os.path.join(AQUI, "reels.json"), encoding="utf-8"))["reels"]}
    for s in sys.argv[1:] or list(reels):
        gerar(reels[s])
