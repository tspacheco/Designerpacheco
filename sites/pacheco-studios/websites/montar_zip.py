#!/usr/bin/env python3
"""Junta a página /websites a um ZIP do site já pronto para o Netlify.

Uso: python3 montar_zip.py <zip-do-site-atual> <zip-novo>
Não toca em mais nada do site: só acrescenta /websites/, /en/websites/ e as linhas noindex no _headers.
Confirma no fim que a página continua escondida (sem link no site, fora do sitemap e do robots.txt).
"""
import os, re, shutil, subprocess, sys, tempfile, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
CAB = """
# Página escondida de portefólio (websites/gerar_websites.py): nunca indexar.
/websites
  X-Robots-Tag: noindex, nofollow, noarchive
/websites/*
  X-Robots-Tag: noindex, nofollow, noarchive
/en/websites
  X-Robots-Tag: noindex, nofollow, noarchive
/en/websites/*
  X-Robots-Tag: noindex, nofollow, noarchive
"""

def main():
    base, novo = sys.argv[1], sys.argv[2]
    with tempfile.TemporaryDirectory() as t:
        site = os.path.join(t, "site"); zipfile.ZipFile(base).extractall(site)
        for p in ("websites", os.path.join("en", "websites")):
            shutil.rmtree(os.path.join(site, p), ignore_errors=True)
        ger = os.path.join(t, "ger")
        subprocess.run([sys.executable, os.path.join(AQUI, "gerar_websites.py"), ger], check=True)
        shutil.copytree(os.path.join(ger, "websites"), os.path.join(site, "websites"))
        shutil.copytree(os.path.join(ger, "en", "websites"), os.path.join(site, "en", "websites"))
        h = os.path.join(site, "_headers")
        txt = open(h, encoding="utf-8").read() if os.path.exists(h) else ""
        txt = re.sub(r"\n# Página escondida de portefólio.*?(?=\n#|\Z)", "", txt, flags=re.S).rstrip("\n") + "\n" + CAB
        open(h, "w", encoding="utf-8").write(txt)
        # verificação: escondida
        erros = []
        for raiz, _, fs in os.walk(site):
            for f in fs:
                cam = os.path.join(raiz, f); rel = os.path.relpath(cam, site).replace(os.sep, "/")
                if rel.startswith(("websites/", "en/websites/")) or not f.endswith((".html", ".xml", ".txt", ".json", ".js")):
                    continue
                if re.search(r"""["'(/]websites(/|["')])""", open(cam, encoding="utf-8", errors="ignore").read()):
                    erros.append(rel)
        for l in ("websites/index.html", "en/websites/index.html"):
            if "noindex" not in open(os.path.join(site, l), encoding="utf-8").read():
                erros.append(l + " sem noindex")
        if erros:
            sys.exit("ERRO, a página não ficou escondida: " + ", ".join(erros))
        if os.path.exists(novo):
            os.remove(novo)
        with zipfile.ZipFile(novo, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for raiz, _, fs in sorted(os.walk(site)):
                for f in sorted(fs):
                    cam = os.path.join(raiz, f); z.write(cam, os.path.relpath(cam, site))
    print("ok:", novo, os.path.getsize(novo) // 1024, "KB; página escondida confirmada")

if __name__ == "__main__":
    main()
