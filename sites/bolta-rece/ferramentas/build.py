#!/usr/bin/env python3
"""Monta as páginas finais (ficheiro único cada, CSS/JS/fontes embutidos) a partir de src/.

    python3 ferramentas/build.py

src/pages/*.html   → <nome>.html na raiz do site. Cada página tem o seu <title>, meta e conteúdo.
src/site.css       → CSS partilhado.   src/site.js → JS partilhado (nav, reveal, tilt, parallax).
src/nav.html, src/footer.html, src/intro.html (só index)   src/bolta.js (só index; precisa do three.min.js).
_fontes/fontes.css → fontes em base64 (gerado por ferramentas/fontes.py).
ferramentas/three.min.js → Three.js UMD (npm pack three@0.152.2 → package/build/three.min.js).
Marcadores nas páginas: <!--@head-->  <!--@nav-->  <!--@footer-->  <!--@scripts-->  e, no index, <!--@intro--> <!--@bolta-->.
"""
import pathlib, re, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SRC = RAIZ / "src"
ler = lambda p: pathlib.Path(p).read_text(encoding="utf-8")

fontes = ler(RAIZ / "_fontes" / "fontes.css")
css = ler(SRC / "site.css")
js = ler(SRC / "site.js")
nav = ler(SRC / "nav.html")
footer = ler(SRC / "footer.html")
intro = ler(SRC / "intro.html")
bolta = ler(SRC / "bolta.js")
three_path = RAIZ / "ferramentas" / "three.min.js"
three = ler(three_path).replace("</script>", "<\\/script>") if three_path.exists() else ""
if not three:
    print("AVISO: ferramentas/three.min.js em falta — a bolta 3D cai para a fotografia.")

estado = "<script>(function(d){d.className=d.className.replace('no-js','js');if(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches)d.className+=' rm'})(document.documentElement)</script>"
head = f"{estado}\n<style>\n{fontes}\n</style>\n<style>\n{css}\n</style>"
scripts = f"<script>\n{js}\n</script>"

for pagina in sorted((SRC / "pages").glob("*.html")):
    html = ler(pagina)
    atual = pagina.stem
    nav_p = re.sub(r'href="(%s)\.html"' % atual, r'href="\1.html" aria-current="page"', nav)
    html = html.replace("<!--@head-->", head).replace("<!--@nav-->", nav_p).replace("<!--@footer-->", footer)
    if atual == "index":
        html = html.replace("<!--@intro-->", intro)
        bloco = (f"<script>\n{three}\n</script>\n" if three else "") + f"<script>\n{bolta}\n</script>"
        html = html.replace("<!--@bolta-->", bloco)
    html = html.replace("<!--@scripts-->", scripts)
    resto = re.findall(r"<!--@\w+-->", html)
    if resto:
        sys.exit(f"{pagina.name}: marcadores por substituir: {resto}")
    destino = RAIZ / f"{atual}.html"
    destino.write_text(html, encoding="utf-8")
    print(f"{destino.name}: {destino.stat().st_size // 1024} KB")
