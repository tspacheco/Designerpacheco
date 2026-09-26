#!/usr/bin/env python3
"""Monta a página do QR do cartão (ro.pachecost.com) em romeno, mais a versão portuguesa para revisão.

    python3 gerar.py

Lê: index.src.html · conteudo/ro.json · conteudo/pt.json · portfolio.json · ../../marca/dados.json (contactos)
Escreve em dist/ (não vai para o git):
  index.html            página em romeno (3 vistas: proiecte / automatizari / servicii + contacto)
  pt/index.html         a mesma página em português, para rever (ligação discreta no rodapé)
  404.html · _redirects (QR /c) · _headers · netlify.toml · media/og.png
  p/<slug>/             cópia de cada site do portefólio, com <meta noindex> e o botão «Înapoi la proiecte» injetados
  ../pacheco-studios-netlify.zip   tudo isto, pronto a arrastar para o Netlify
Copia ainda index.html, pt/index.html, 404.html, _redirects, _headers e netlify.toml para esta pasta
(para se abrirem na app e para o git ter sempre a versão atual).
Depois corre verificar.cjs (HTML, acessibilidade, separadores, ligações dos quadrados, botão «Înapoi», 404).
"""
import base64
import html
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from urllib.parse import quote

from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MARCA = os.path.join(RAIZ, "marca")
SITES = os.path.join(RAIZ, "sites")
DIST = os.path.join(AQUI, "dist")
NODE_ENV = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
FONTES = [("Archivo Black", 400, "archivo-black-ro.woff2"), ("Space Mono", 700, "space-mono-700-ro.woff2"),
          ("Inter", 400, "inter-400-ro.woff2"), ("Inter", 600, "inter-600-ro.woff2")]

I = {
    "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
    "telefone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "email": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><path d="M22 6l-10 7L2 6"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/></svg>',
    "site": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "seta": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "baixo": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>',
}


def e(s):
    return html.escape(str(s), quote=True)


def fontes_css():
    out = []
    for fam, peso, fich in FONTES:
        b64 = base64.b64encode(open(os.path.join(MARCA, "fontes", fich), "rb").read()).decode()
        out.append(f'@font-face{{font-family:"{fam}";font-weight:{peso};font-style:normal;font-display:swap;'
                   f'src:url(data:font/woff2;base64,{b64}) format("woff2")}}')
    return "\n".join(out)


def glifos_em_falta(texto):
    """Letras do conteúdo que não existem em nenhuma das fontes embutidas (o Ș e o Ț do romeno, por exemplo)."""
    cmap = set()
    for _, _, fich in FONTES:
        cmap |= set(TTFont(os.path.join(MARCA, "fontes", fich)).getBestCmap())
    return sorted({ch for ch in texto if not ch.isspace() and ord(ch) not in cmap})


def textos_de(obj):
    if isinstance(obj, dict):
        return "".join(textos_de(v) for k, v in obj.items() if not k.startswith("_"))
    if isinstance(obj, list):
        return "".join(textos_de(v) for v in obj)
    return str(obj) if isinstance(obj, str) else ""


# ——— vistas ———
def contraste(a, b):
    def lum(h):
        h = h.lstrip("#")
        r, g, bl = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(bl)
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def quadrado(item, rot, i):
    nome = item["nome"]
    fs = 1 if len(nome) <= 10 else 0.86 if len(nome) <= 16 else 0.72
    # site real do cliente → separador novo (a página fica aberta por baixo); cliente sem site publicado → cópia em /p/ com «Înapoi»
    href = item["url"] if item.get("url") else f"/p/{item['slug']}/"
    externo = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    estilo = (f"--bg:{item['bg']};--ink:{item['ink']};--ac:{item['accent']};--f:'{item['fonte']}';--w:{item['peso']};--fs:{fs}"
              + (";font-style:italic" if item.get("italico") else ""))
    info = rot["itens"].get(item["slug"], {})
    tip, oras = info.get("tip", ""), info.get("oras", "")
    # tipo e cidade em partes: na fila de destaque, no telemóvel, só cabe a cidade
    meta = "".join((f'<span class="q-tip">{e(tip)}</span>' if tip else "",
                    '<span class="q-sep">&nbsp;· </span>' if tip and oras else "",  # o ponto fica com o tipo; a cidade é que muda de linha
                    f'<span class="q-oras">{e(oras)}</span>' if oras else ""))
    return (f'<li class="rv{" dest" if item.get("destaque") else ""}" style="--i:{i}"><a class="q{" neutro" if item.get("neutro") else ""}" href="{e(href)}" style="{estilo}"{externo}>'
            f'<span class="q-nome">{e(nome)}</span><span class="q-meta">{meta}</span></a></li>')


def ativos(portfolio):
    """Os quadrados, por ordem: primeiro os três em destaque (primeira fila), depois os outros pela ordem do ficheiro."""
    itens = [x for x in portfolio["itens"] if x.get("ativo") and not x.get("demo") and (x.get("pasta") or x.get("url"))]
    return sorted(itens, key=lambda x: not x.get("destaque"))


def fontes_google(portfolio):
    """Pedido ao Google Fonts só com as fontes dos quadrados que aparecem (as da marca vão embutidas)."""
    marca = {"Space Mono", "Archivo Black", "Inter"}
    fam = []
    for x in ativos(portfolio):
        if x["fonte"] in marca:
            continue
        nome = x["fonte"].replace(" ", "+")
        peso = int(x.get("peso", 400))
        spec = f"{nome}:ital,wght@1,{peso}" if x.get("italico") else (f"{nome}:wght@{peso}" if peso != 400 else nome)
        if spec not in fam:
            fam.append(spec)
    return "&".join(f"family={f}" for f in fam)


def vista_proiecte(c, portfolio, teu):
    p = c["proiecte"]
    itens = ativos(portfolio)
    dest = [x["slug"] for x in itens if x.get("destaque")]
    if len(dest) != 3:
        raise SystemExit(f"portfolio.json: a primeira fila leva 3 quadrados em destaque, há {len(dest)}: {dest}")
    lis = "\n".join(quadrado(x, p, i) for i, x in enumerate(itens))
    lis += (f'\n<li class="rv" style="--i:{len(itens)}"><a class="q teu" href="#contact" style="--fs:.8">'
            f'<span class="q-nome">{e(teu)}</span></a></li>')
    m = c["metoda"]
    passos = "\n".join(f'<li class="passo rv" style="--i:{i}"><h3>{e(s["t"])}</h3><p>{e(s["d"])}</p></li>' for i, s in enumerate(m["pasi"]))
    return f"""<section id="proiecte" class="vista" aria-labelledby="t-proiecte">
  <div class="envolver seccao">
    <p class="eyebrow">{e(p["eyebrow"])}</p>
    <h2 id="t-proiecte" class="afirmacao">{e(p["titlu"])}</h2>
    <p class="lead">{e(p["intro"])}</p>
    <ul class="grelha">
{lis}
    </ul>
    <p class="nota-grelha">{e(p["nota"])}</p>
  </div>
  <div class="claro">
    <div class="envolver seccao">
      <p class="eyebrow">{e(m["eyebrow"])}</p>
      <h2 class="afirmacao">{e(m["titlu"])}</h2>
      <ol class="passos">
{passos}
      </ol>
    </div>
  </div>
</section>"""


def no_html(n):
    """Um passo do fluxo: declanșator (âmbar), automático (escuro), pessoa (verde) ou decisão (tracejado) com ramos."""
    cls = n.get("tip", "auto") if n.get("tip") in ("gatilho", "pessoa", "decizie") else "auto"
    inner = f"<b>{e(n['t'])}</b>" + (f"<small>{e(n['d'])}</small>" if n.get("d") else "")
    if n.get("ramuri"):
        inner += '<div class="ramuri">' + "".join(
            f'<div class="no {"pessoa" if r.get("tip") == "pessoa" else "ramo"}"><b>{e(r["t"])}</b><small>{e(r["d"])}</small></div>'
            for r in n["ramuri"]) + "</div>"
    return f'<li><div class="no {cls}">{inner}</div></li>'


def vista_automatizari(c, digitos):
    a = c["automatizari"]
    lab = a["labels"]
    por_id = {x["id"]: x for x in a["itens"]}
    legenda = ('<div class="legenda">' + "".join(f'<span><i class="l-{k}"></i>{e(v)}</span>' for k, v in lab["legenda"].items()) + "</div>")
    cards = []
    for i, x in enumerate(a["itens"]):
        fluxo = "\n".join(no_html(n) for n in x["fluxo"])
        reguli = "\n".join(f"<li>{e(r)}</li>" for r in x["reguli"])
        decide = "".join(f'<div><b>{e(lab[k])}</b><span>{e(x["decide"][k])}</span></div>' for k in ("tu", "masina", "noi"))
        chat = "".join(f'<div class="msg {e(m["cine"])}"><small>{e(lab["client"] if m["cine"] == "client" else lab["asistent"] if m["cine"] == "asistent" else lab["tu_msg"])}</small>{e(m["t"])}</div>'
                       for m in x["exemplu"])
        chips = " ".join(f'<a class="chip" href="#a-{e(k)}">{e(por_id[k]["scurt"])}</a>' for k in x["leaga"] if k in por_id)
        wa_demo = f"https://wa.me/351{digitos}?text={quote(lab['demo_msg'] + x['titlu'])}"
        cards.append(f"""<details class="auto rv" name="auto" id="a-{e(x["id"])}" style="--i:{i}">
  <summary>
    <h3>{e(x["titlu"])}</h3>
    <span class="durere"><span class="eyebrow">{e(lab["durere"])}</span><q>{e(x["durere"])}</q></span>
    <span class="vezi" aria-hidden="true"><span class="abre">{e(lab["vezi"])}</span><span class="fecha">{e(lab["inchide"])}</span>{I["baixo"]}</span>
  </summary>
  <div class="corpo">
    <div><h4 class="rotulo">{e(lab["montata"])}</h4>{legenda}<ol class="bp">
{fluxo}
    </ol></div>
    <div class="obtii"><h4 class="rotulo">{e(lab["obtii"])}</h4>{e(x["obtii"])}</div>
    <div><h4 class="rotulo">{e(lab["reguli"])}</h4><ul class="reguli">
{reguli}
    </ul></div>
    <div><h4 class="rotulo">{e(lab["decide"])}</h4><div class="decide">{decide}</div></div>
    <div><h4 class="rotulo">{e(lab["vede"])}</h4><div class="chat">{chat}</div></div>
    <div class="nevoie"><h4 class="rotulo">{e(lab["nevoie"])}</h4><p>{e(x["nevoie"])}</p></div>
    <div><h4 class="rotulo">{e(lab["leaga"])}</h4><div class="chips">{chips}</div></div>
    <div class="demo"><p>{e(lab["demo_t"])}</p><a class="botao secundario" href="{e(wa_demo)}">{I["chat"]}{e(lab["demo_cta"])}</a></div>
  </div>
</details>""")
    cb = a["combos"]
    drumuri = []
    for d in cb["itens"]:
        elos = [f'<a class="chip" href="#a-{e(k)}">{e(por_id[k]["scurt"])}</a>' for k in d["ids"] if k in por_id]
        # seta + chip seguintes ficam juntos: a seta nunca fica sozinha no fim de uma linha
        cadeia = elos[0] + "".join(f'<span class="dc">{I["seta"]}{x}</span>' for x in elos[1:])
        drumuri.append(f'<li class="drum"><span class="drum-t">{e(d["t"])}</span><span class="drum-c">{cadeia}</span></li>')
    ai = "".join(f"<li>{e(f)}</li>" for f in lab["ai"])
    return f"""<section id="automatizari" class="vista" aria-labelledby="t-automatizari">
  <div class="envolver seccao">
    <div class="autos-grelha">
      <div class="cab">
        <p class="eyebrow">{e(a["eyebrow"])}</p>
        <h2 id="t-automatizari" class="afirmacao">{e(a["titlu"])}</h2>
        <p class="lead">{e(a["intro"])}</p>
        <p class="lead intro-2">{e(a["intro_extra"])}</p>
        <details class="ai">
          <summary><span><span class="eyebrow ai-e">{e(lab["ai_e"])}</span>{e(lab["ai_t"])}</span>{I["baixo"]}</summary>
          <ol>{ai}</ol>
        </details>
      </div>
      <div class="autos">
{chr(10).join(cards)}
      </div>
    </div>
    <div class="combos">
      <p class="eyebrow">{e(cb["eyebrow"])}</p>
      <h3 class="afirmacao">{e(cb["titlu"])}</h3>
      <p class="lead">{e(cb["intro"])}</p>
      <ul class="drumuri">
{chr(10).join(drumuri)}
      </ul>
    </div>
  </div>
</section>"""


def vista_servicii(c, portfolio):
    s = c["servicii"]
    ligacao = {x["slug"]: (x["url"] if x.get("url") else f"/p/{x['slug']}/") for x in ativos(portfolio)}
    cards = []
    for i, x in enumerate(s["itens"]):
        ex = ""
        if x.get("exemplu") and x["exemplu"] not in ligacao:
            raise SystemExit(f"servicii «{x['id']}»: o exemplo «{x['exemplu']}» não está nos quadrados (só clientes reais)")
        if x.get("exemplu") in ligacao:
            u = ligacao[x["exemplu"]]
            ex = f'<a class="link-ex" href="{e(u)}"{" target=_blank rel=noopener" if u.startswith("http") else ""}>{e(s["exemplu"])}{I["seta"]}</a>'
        cards.append(f'<li class="svc rv" style="--i:{i}"><h3>{e(x["titlu"])}</h3><p>{e(x["ce"])}</p><p class="de-ce">{e(x["de_ce"])}</p>{ex}</li>')
    return f"""<section id="servicii" class="vista claro" aria-labelledby="t-servicii">
  <div class="envolver seccao">
    <p class="eyebrow">{e(s["eyebrow"])}</p>
    <h2 id="t-servicii" class="afirmacao">{e(s["titlu"])}</h2>
    <p class="lead">{e(s["intro"])}</p>
    <ul class="svcs">
{chr(10).join(cards)}
    </ul>
  </div>
</section>"""


def contacto(c, d, wa, tel_legivel, digitos):
    k = c["contact"]
    lab = k["labels"]
    ig = d["instagram"].lstrip("@")
    site = d["site_principal"]
    linhas = [(lab["whatsapp"], tel_legivel, wa, "chat"), (lab["telefon"], tel_legivel, f"tel:+351{digitos}", "telefone"),
              (lab["email"], d["email"], f"mailto:{d['email']}", "email"),
              (lab["instagram"], f"@{ig}", f"https://www.instagram.com/{ig}/", "instagram"),
              (lab["site"], site, f"https://{site}/", "site")]
    lis = "\n".join(f'<li><a href="{e(u)}"{" rel=noopener" if u.startswith("http") else ""}>{I[i]}'
                    f'<span class="txt"><span class="qual">{e(q)}</span><span class="valor">{e(v)}</span></span></a></li>'
                    for q, v, u, i in linhas)
    return f"""<section id="contact" class="seccao" aria-labelledby="t-contact">
  <div class="envolver">
    <p class="eyebrow">{e(k["eyebrow"])}</p>
    <h2 id="t-contact" class="afirmacao">{e(k["titlu"])}</h2>
    <p class="lead">{e(k["text"])}</p>
    <a class="botao primario grande" href="{e(wa)}">{I["chat"]}{e(k["cta"])}</a>
    <ul class="contactos">
{lis}
    </ul>
  </div>
</section>"""


def rodape(c, d, outra_lingua):
    r = c["rodape"]
    extra = f'\n    <p><a href="{e(outra_lingua[1])}">{e(outra_lingua[0])}</a></p>' if outra_lingua else ""
    return f"""<footer class="rodape">
  <div class="envolver">
    <p>{e(r["linha"])}</p>
    <p><a href="https://www.livroreclamacoes.pt/inicio" rel="noopener">{e(r["legal"])}</a></p>
    <p>{e(r["nota"])}</p>{extra}
  </div>
</footer>"""


def montar(src, valores):
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: valores[m.group(1)], src)


# ——— validação ———
class Verificador(HTMLParser):
    VAZIOS = {"meta", "link", "img", "br", "hr", "input", "source", "area", "base", "col", "embed", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.pilha, self.erros, self.svg = [], [], 0

    def handle_starttag(self, t, a):
        if t == "svg":
            self.svg += 1
        if t not in self.VAZIOS and not self.svg:
            self.pilha.append(t)

    def handle_endtag(self, t):
        if t == "svg":
            self.svg -= 1
            return
        if self.svg:
            return
        if self.pilha and self.pilha[-1] == t:
            self.pilha.pop()
        else:
            self.erros.append(t)


def validar(nome, h):
    p = Verificador()
    p.feed(h)
    ok = not p.pilha and not p.erros
    falta = len(re.findall(r"\{\{[A-Z_]+\}\}", h))
    estado = "HTML-OK" if ok else "ERRO " + str(p.pilha[-3:]) + str(p.erros[-3:])
    lang = re.search(r'lang="([^"]+)"', h).group(1)
    legal = "legal" if "livroreclamacoes" in h else "SEM-LEGAL"
    print(f"  {nome}: {estado} | h1:{h.count('<h1')} | lang:{lang} | {legal} | U+FFFD:{h.count(chr(0xFFFD))} | por preencher:{falta}")
    return ok and h.count("<h1") == 1 and "livroreclamacoes" in h and chr(0xFFFD) not in h and not falta


# ——— cópias dos sites com o botão «Înapoi» ———
def pilula(texto):
    return (f'\n<a id="ps-inapoi" href="/#proiecte" lang="ro" style="position:fixed;left:12px;bottom:calc(12px + env(safe-area-inset-bottom));'
            'z-index:2147483647;display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:10px 16px 10px 12px;border-radius:999px;'
            'background:#141210;color:#EFEAE3;border:2px solid #E8622C;font:700 14px/1 system-ui,-apple-system,\'Segoe UI\',Roboto,sans-serif;'
            'letter-spacing:.02em;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.35)">'
            '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" style="flex:none;fill:none;stroke:#E8622C;stroke-width:2.5;'
            f'stroke-linecap:round;stroke-linejoin:round"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>{e(texto)}</a>\n'
            "<script>(function(){var a=document.getElementById('ps-inapoi');a.addEventListener('click',function(ev){try{"
            "if(document.referrer&&new URL(document.referrer).host===location.host&&history.length>1){ev.preventDefault();history.back();}"
            "}catch(e){}});})();</script>\n")


def copiar_sites(portfolio, texto_inapoi):
    n = 0
    for it in portfolio["itens"]:
        if not (it.get("ativo") and it.get("pasta")) or it.get("url") or it.get("demo"):
            continue  # com site real publicado, a cópia não é precisa; apresentações nunca vão
        origem = os.path.join(SITES, it["pasta"])
        destino = os.path.join(DIST, "p", it["slug"])
        os.makedirs(destino, exist_ok=True)
        h = open(os.path.join(origem, "index.html"), encoding="utf-8").read()
        if "</body>" not in h:
            raise SystemExit(f"{it['pasta']}/index.html sem </body>")
        h = re.sub(r"(<meta charset=[^>]*>)", r'\1\n<meta name="robots" content="noindex,nofollow">', h, count=1)
        h = h.replace("</body>", pilula(texto_inapoi) + "</body>", 1)
        open(os.path.join(destino, "index.html"), "w", encoding="utf-8").write(h)
        media = os.path.join(origem, "media")
        if os.path.isdir(media):
            shutil.copytree(media, os.path.join(destino, "media"), dirs_exist_ok=True)
        n += 1
    return n


def og_png(fontes, slogan, proposito, regiao):
    def frase(l):
        t = e(l.strip("*"))
        if t.endswith("."):
            t = t[:-1] + '<span class="pf"></span>'
        return f'<span{" class=o" if l.startswith("*") else ""}>{t}</span>'
    og = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{fontes}
    body{{margin:0;width:1200px;height:630px;background:#141210;color:#EFEAE3;position:relative;overflow:hidden}}
    .m{{position:absolute;left:84px;top:72px;display:flex;align-items:center;gap:18px;font:700 24px/1 "Space Mono";letter-spacing:.24em}}
    .m i{{width:18px;height:18px;border-radius:50%;background:#E8622C}}
    .r{{position:absolute;right:84px;top:72px;font:700 24px/1 "Space Mono";letter-spacing:.24em;color:#A5A19B}}
    h1{{position:absolute;left:80px;top:150px;margin:0;font:400 90px/.93 "Archivo Black";text-transform:uppercase}}
    h1 span{{display:block}} .o{{color:#E8622C}}
    .pf{{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:#E8622C;margin-left:.06em}}
    .s{{position:absolute;left:84px;bottom:60px;font:700 24px/1 "Space Mono";letter-spacing:.12em;color:#A5A19B;text-transform:uppercase}}
    </style></head><body><p class="m"><i></i>PACHECO STUDIOS</p><p class="r">{e(regiao.upper())}</p>
    <h1>{"".join(frase(l) for l in slogan)}</h1><p class="s">{e(proposito)}</p></body></html>"""
    tmp = os.path.join(AQUI, ".og.html")
    open(tmp, "w", encoding="utf-8").write(og)
    os.makedirs(os.path.join(DIST, "media"), exist_ok=True)
    subprocess.run(["node", "-e", """
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + process.argv[1]); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: process.argv[2] }); await b.close(); })();
""", tmp, os.path.join(DIST, "media", "og.png")], check=True, env=NODE_ENV)
    os.remove(tmp)


def main():
    d = json.load(open(os.path.join(MARCA, "dados.json"), encoding="utf-8"))
    portfolio = json.load(open(os.path.join(AQUI, "portfolio.json"), encoding="utf-8"))
    linguas = {k: json.load(open(os.path.join(AQUI, "conteudo", f"{k}.json"), encoding="utf-8")) for k in ("ro", "pt")}
    dominio = d["dominio"].strip().lower()
    url_site = f"https://{dominio}/"
    digitos = re.sub(r"\D", "", d["telefone"])
    digitos = digitos[3:] if digitos.startswith("351") and len(digitos) == 12 else digitos
    if len(digitos) != 9:
        raise SystemExit("marca/dados.json: telefone tem de ter 9 dígitos")
    tel_legivel = f"+351 {digitos[:3]} {digitos[3:6]} {digitos[6:]}"
    fontes = fontes_css()
    src = open(os.path.join(AQUI, "index.src.html"), encoding="utf-8").read()

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "pt"))

    ok = True
    print("CONTEÚDO")
    paginas = {}
    for lang, c in linguas.items():
        falta = glifos_em_falta(textos_de(c))
        print(f"  {lang}: {'todas as letras existem nas fontes' if not falta else '✗ letras sem glifo: ' + ''.join(falta)}")
        ok &= not falta
        wa = f"https://wa.me/351{digitos}?text={quote(c['contact']['mensagem_wa'])}"
        outra = ("Versiunea în română →", "/") if lang == "pt" else None
        url_pagina = url_site if lang == "ro" else url_site + "pt/"
        jsonld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Pacheco Studios", "url": url_pagina,
                  "image": url_site + "media/og.png", "description": c["meta"]["description"], "telephone": tel_legivel,
                  "email": d["email"], "areaServed": {"@type": "Country", "name": "Romania"},
                  "sameAs": [f"https://www.instagram.com/{d['instagram'].lstrip('@')}/", f"https://{d['site_principal']}/"],
                  "founder": {"@type": "Person", "name": d["nome"]}}
        valores = {
            "LINGUA": c["lingua"], "TITLE": e(c["meta"]["title"]), "DESCRIPTION": e(c["meta"]["description"]),
            "OG_TITLE": e(c["meta"]["og_title"]), "OG_LOCALE": "ro_RO" if lang == "ro" else "pt_PT",
            "URL_SITE": url_site, "URL_PAGINA": url_pagina, "FONTES": fontes, "FONTES_GOOGLE": fontes_google(portfolio),
            "JSONLD": json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/"),
            "SALTAR": "Sari la conținut" if lang == "ro" else "Saltar para o conteúdo",
            "NAV_LABEL": "Secțiuni" if lang == "ro" else "Secções",
            "REGIAO": e(c["topo"]["regiao"].upper()), "TAB_PROIECTE": e(c["topo"]["tabs"]["proiecte"]),
            "TAB_AUTOMATIZARI": e(c["topo"]["tabs"]["automatizari"]), "TAB_SERVICII": e(c["topo"]["tabs"]["servicii"]),
            "VISTA_AUTOMATIZARI": vista_automatizari(c, digitos), "VISTA_SERVICII": vista_servicii(c, portfolio),
            "VISTA_PROIECTE": vista_proiecte(c, portfolio, "Afacerea ta?" if lang == "ro" else "O teu negócio?"),
            "CONTACT": contacto(c, d, wa, tel_legivel, digitos), "RODAPE": rodape(c, d, outra),
            "WA_URL": e(wa), "ICONE_CHAT": I["chat"], "CTA": e(c["contact"]["cta"]),
        }
        pagina = montar(src, valores)
        paginas[lang] = pagina
        destino = os.path.join(DIST, "index.html") if lang == "ro" else os.path.join(DIST, "pt", "index.html")
        open(destino, "w", encoding="utf-8").write(pagina)

    # 404 em romeno, com o mesmo estilo
    ro = linguas["ro"]
    estilo = re.search(r"<style>.*?</style>", paginas["ro"], re.S).group(0)
    p404 = f"""<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(ro["p404"]["titlu"])} — Pacheco Studios</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#141210">
{estilo}
</head>
<body>
<header class="envolver topo">
  <h1 class="marca"><span class="ponto" aria-hidden="true"></span>Pacheco Studios</h1>
  <span class="regiao">{e(ro["topo"]["regiao"].upper())}</span>
</header>
<main id="conteudo" class="envolver seccao">
  <p class="eyebrow">404</p>
  <h2 class="afirmacao">{e(ro["p404"]["titlu"])}</h2>
  <p class="lead">{e(ro["p404"]["text"])}</p>
  <a class="botao primario grande" href="/#proiecte">{I["seta"]}{e(ro["p404"]["cta"])}</a>
</main>
<footer class="rodape">
  <div class="envolver">
    <p>{e(ro["rodape"]["linha"])}</p>
    <p><a href="https://www.livroreclamacoes.pt/inicio" rel="noopener">{e(ro["rodape"]["legal"])}</a></p>
  </div>
</footer>
</body>
</html>
"""
    open(os.path.join(DIST, "404.html"), "w", encoding="utf-8").write(p404)

    # Netlify: o QR aponta para /c — o destino muda em marca/dados.json, sem reimprimir cartões
    caminho = d.get("caminho_qr", "c").strip("/").lower()
    destino_qr = d.get("destino_qr", "/?origem=cartao").strip()
    curtos = {k: v for k, v in d.get("enderecos_curtos", {}).items() if not k.startswith("_") and v}
    red = ["# Gerado por gerar.py a partir de marca/dados.json — não editar à mão.",
           f"# QR do cartão (https://{dominio}/{caminho.upper()}) → marca/dados.json: destino_qr.",
           f"/{caminho}    {destino_qr}    302", f"/{caminho.upper()}    {destino_qr}    302",
           "# Endereços curtos (marca/dados.json → enderecos_curtos)"]
    for slug, dest in sorted(curtos.items()):
        red.append(f"/{re.sub(r'[^a-z0-9-]', '', slug.lower())}    {dest}    302")
    open(os.path.join(DIST, "_redirects"), "w", encoding="utf-8").write("\n".join(red) + "\n")
    # Cabeçalhos em _headers (e não no netlify.toml): o Netlify lê _headers e _redirects também quando o zip é
    # arrastado à mão; o netlify.toml só é garantido em builds. Um sítio só, para não se duplicarem.
    open(os.path.join(DIST, "_headers"), "w", encoding="utf-8").write(
        "# Gerado por gerar.py — não editar à mão.\n/*\n  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n/p/*\n  X-Robots-Tag: noindex, nofollow\n"
        "/media/*\n  Cache-Control: public, max-age=604800\n")
    open(os.path.join(DIST, "netlify.toml"), "w", encoding="utf-8").write(
        '# Gerado por gerar.py. Redirecionamentos em _redirects e cabeçalhos em _headers.\n[build]\npublish = "."\n')

    n = copiar_sites(portfolio, ro["inapoi"])
    og_png(fontes, d["cartao"]["slogan"], d["cartao"]["proposito"], ro["topo"]["regiao"])

    for f in ("index.html", "404.html", "_redirects", "_headers", "netlify.toml"):
        shutil.copy(os.path.join(DIST, f), os.path.join(AQUI, f))
    os.makedirs(os.path.join(AQUI, "pt"), exist_ok=True)
    shutil.copy(os.path.join(DIST, "pt", "index.html"), os.path.join(AQUI, "pt", "index.html"))

    print("\nVALIDAÇÃO")
    ok &= validar("index.html (ro)", paginas["ro"]) & validar("pt/index.html", paginas["pt"]) & validar("404.html", p404)
    print(f"  index.html: {len(paginas['ro'].encode()) / 1024:.0f} KB · {n} sites copiados para /p/")
    regras = open(os.path.join(DIST, "_redirects"), encoding="utf-8").read().splitlines()
    qr_ok = all(any(r.split()[:3] == [f"/{c}", destino_qr, "302"] for r in regras if not r.startswith("#"))
                for c in (caminho, caminho.upper()))
    cab_ok = "X-Robots-Tag: noindex" in open(os.path.join(DIST, "_headers"), encoding="utf-8").read()
    ok &= qr_ok and cab_ok
    print(f"  {'✓' if qr_ok else '✗'} _redirects: /{caminho} e /{caminho.upper()} → {destino_qr} (o QR impresso)"
          f" · {'✓' if cab_ok else '✗'} _headers: /p/* com noindex")

    zipp = os.path.join(AQUI, "pacheco-studios-netlify.zip")
    with zipfile.ZipFile(zipp, "w", zipfile.ZIP_DEFLATED) as z:
        for raiz, _, fichs in os.walk(DIST):
            for f in sorted(fichs):
                caminho_f = os.path.join(raiz, f)
                z.write(caminho_f, os.path.relpath(caminho_f, DIST))
    print(f"  zip Netlify: {os.path.getsize(zipp) / 1024 / 1024:.1f} MB")

    r = subprocess.run(["node", os.path.join(AQUI, "verificar.cjs"), DIST, *sys.argv[1:]], env=NODE_ENV)
    sys.exit(0 if ok and r.returncode == 0 else 1)


if __name__ == "__main__":
    main()
