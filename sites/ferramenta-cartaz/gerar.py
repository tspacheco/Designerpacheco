#!/usr/bin/env python3
"""Ferramenta grátis «Cartaz de avaliações Google» (ideia 9 dos agentes de leads).

Lê: src.html · textos.json · logo.svg · vendor/qrcode.min.js · ../../marca/fontes/*.woff2 · ../../marca/dados.json
Escreve em dist/ (para juntar ao site pachecost.com, ver LEIA-ME.md):
  cartaz.html        PT  → pachecost.com/cartaz
  ro/afis.html       RO  → ro.pachecost.com/afis
  en/poster.html     EN  → pachecost.com/en/poster
  previa-pt.html · previa-ro.html   as mesmas páginas sem GoatCounter, para as pré-visualizações (Artifact)

Uso: python3 gerar.py
"""
import base64, html, json, os, re, sys
from urllib.parse import quote

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
DIST = os.path.join(AQUI, "dist")
FONTES = [("Archivo Black", 400, "archivo-black-ro.woff2"), ("Space Mono", 700, "space-mono-700-ro.woff2"),
          ("Inter", 400, "inter-400-ro.woff2"), ("Inter", 600, "inter-600-ro.woff2")]
ESTRELA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6-4.9-4.6 6.6-.8z"/></svg>'
CORES_TEMA = {"carvao": "#141210", "papel": "#F4EFE6", "floresta": "#18352A", "vinho": "#4A1622"}
ORDEM = ["pt", "en", "ro"]


def ler(*p, modo="r"):
    with open(os.path.join(*p), modo, **({} if "b" in modo else {"encoding": "utf-8"})) as f:
        return f.read()


def e(s):
    return html.escape(str(s), quote=True)


def fontes_css():
    out = []
    for fam, peso, fich in FONTES:
        b64 = base64.b64encode(ler(RAIZ, "marca", "fontes", fich, modo="rb")).decode()
        out.append(f'@font-face{{font-family:"{fam}";font-weight:{peso};font-style:normal;font-display:swap;'
                   f'src:url(data:font/woff2;base64,{b64}) format("woff2")}}')
    return "\n".join(out)


def pagina(src, T, cod, previa, goat_url):
    t = T[cod]
    sem_cartaz = {k: v for k, v in t.items() if k != "cartaz"}
    linguas = "".join(
        f'<a href="{e(T[c]["url"])}" hreflang="{T[c]["lang"]}"' + (' aria-current="page"' if c == cod else "") + f'>{c.upper()}</a>'
        for c in ORDEM)
    hreflang = "\n".join(f'<link rel="alternate" hreflang="{T[c]["lang"]}" href="{e(T[c]["url"])}">' for c in ORDEM)
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "WebApplication", "name": t["titulo_pagina"], "url": t["url"],
        "description": t["descricao"], "applicationCategory": "BusinessApplication", "operatingSystem": "Web", "inLanguage": t["lang"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "provider": {"@type": "Organization", "name": "Pacheco Studios", "url": "https://pachecost.com/"}},
        ensure_ascii=False).replace("</", "<\\/")
    goat = "" if previa else (
        '<script>window.goatcounter = { path: function (p) { return location.host + p; } };</script>\n'
        f'<script data-goatcounter="{e(goat_url)}" async src="https://gc.zgo.at/count.js"></script>')
    rec = ('<a href="https://www.livroreclamacoes.pt/" target="_blank" rel="noopener">Livro de Reclamações</a>'
           if t.get("reclamacoes") else "")
    temas = "".join(f'<label><input type="radio" name="tema" value="{k}"><span><i style="background:{CORES_TEMA[k]}"></i>{e(v)}</span></label>'
                    for k, v in t["temas"].items())
    blocos = {
        "FONTES": fontes_css(), "LOGO": ler(AQUI, "logo.svg").replace("<svg ", '<svg aria-hidden="true" ', 1),
        "FAVICON": quote(ler(AQUI, "logo.svg").strip()), "ESTRELAS": ESTRELA * 5, "LINGUAS": linguas, "HREFLANG": hreflang,
        "JSONLD": jsonld, "GOAT": goat, "RECLAMACOES": rec, "TEMAS": temas,
        "AJUDA": "".join(f"<li>{e(x)}</li>" for x in t["ajuda"]),
        "UI": json.dumps(sem_cartaz, ensure_ascii=False).replace("</", "<\\/"),
        "CARTAZES": json.dumps({c: T[c]["cartaz"] for c in T}, ensure_ascii=False).replace("</", "<\\/"),
        "CODIGO": cod, "QR_JS": ler(AQUI, "vendor", "qrcode.min.js"),
    }
    out = src
    for k, v in blocos.items():
        out = out.replace("{{" + k + "}}", v)
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: e(t[m.group(1)]), out)
    return out


def validar(nome, h):
    erros = []
    if h.count("<h1") != 1: erros.append("um só <h1>")
    if "{{" in h: erros.append("marcadores por preencher: " + ", ".join(sorted(set(re.findall(r"\{\{\w+\}\}", h)))))
    if "prefers-reduced-motion" not in h: erros.append("prefers-reduced-motion")
    if ":focus-visible" not in h: erros.append(":focus-visible")
    if 'application/ld+json' not in h: erros.append("JSON-LD")
    for url in re.findall(r'(?:src|href)="(https?://[^"]+)"', h):
        if not re.match(r"https://(pachecost\.com|ro\.pachecost\.com|gc\.zgo\.at|wa\.me|www\.livroreclamacoes\.pt)", url):
            erros.append("dependência externa: " + url)
    if erros:
        sys.exit(f"✗ {nome}: " + "; ".join(erros))
    print(f"✓ {nome}  {len(h.encode()) / 1024:.0f} KB")


def main():
    T = json.loads(ler(AQUI, "textos.json"))
    src = ler(AQUI, "src.html")
    goat_url = json.loads(ler(RAIZ, "marca", "dados.json")).get("medicao", {}).get("goatcounter") or "https://pachecost.goatcounter.com/count"
    for cod in ORDEM:
        destino = os.path.join(DIST, T[cod]["ficheiro"])
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        h = pagina(src, T, cod, False, goat_url)
        validar(T[cod]["ficheiro"], h)
        with open(destino, "w", encoding="utf-8") as f:
            f.write(h)
    for cod in ("pt", "ro"):
        with open(os.path.join(DIST, f"previa-{cod}.html"), "w", encoding="utf-8") as f:
            h = pagina(src, T, cod, True, goat_url)
            # a pré-visualização (Artifact) já vem embrulhada no esqueleto: tira-se o nosso
            h = re.sub(r"<!doctype html>\s*|</?html[^>]*>\s*|</?head>\s*|</?body>\s*", "", h, flags=re.I)
            h = re.sub(r"<title>[^<]*</title>", "<title>" + {"pt": "Cartaz de avaliações", "ro": "Afiș pentru recenzii"}[cod] + "</title>", h)
            f.write(h)


if __name__ == "__main__":
    main()
