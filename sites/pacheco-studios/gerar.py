#!/usr/bin/env python3
"""Monta o site da Pacheco Studios em três línguas, para um só projeto Netlify com dois domínios.

    python3 gerar.py [pasta-para-capturas]

    pachecost.com         português (a página principal)
    pachecost.com/en/     inglês
    ro.pachecost.com      romeno: é para onde aponta o QR do cartão (HTTPS://RO.PACHECOST.COM/C → /?origem=cartao)

Lê: index.src.html · conteudo/{pt,en,ro}.json · portfolio.json · ../../marca/dados.json (contactos, domínios, medição)
Escreve em dist/ (não vai para o git):
  index.html · en/index.html · ro/index.html      as três versões (proiecte / automatizari / servicii + contacto)
  404.html · en/404.html · ro/404.html            404 em cada língua
  privacidade.html · privacy.html · confidentialitate.html
  _redirects (QR /c primeiro, ro.pachecost.com → /ro/) · _headers · netlify.toml · robots.txt · sitemap.xml
  media/og-{pt,en,ro}.png · media/intro-{1,2,3}.webp (os três carros da intro) · p/<slug>/ (clientes sem site
  publicado: index.html romeno, pt.html, en.html)
  ../pacheco-studios-netlify.zip   tudo isto, pronto a arrastar para o projeto Netlify do pachecost.com
Copia ainda as páginas e os ficheiros do Netlify para esta pasta (para o git ter sempre a versão atual).
Depois corre verificar.cjs, que serve dist/ como o Netlify serviria os dois domínios (lê o _redirects).
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
LINGUAS = {}  # preenchido por configurar_linguas() a partir de marca/dados.json
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
    "fora": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>',
}

# ícones das caixas do esquema (traço, 24×24), no estilo dos Feather Icons (MIT)
ICONES_ESQUEMA = {
    "telefone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mensagem": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    "lista": '<path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
    "agenda": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "agenda-ok": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M9 16l2 2 4-4"/>',
    "contactos": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "grafico": '<path d="M18 20V10M12 20V4M6 20v-6M3 20h18"/>',
    "relogio": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "ok": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/>',
    "repetir": '<path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>',
    "pessoa": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "estrela": '<path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/>',
    "pausa": '<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>',
    "entrada": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "camara": '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    "documento": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    "pasta": '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    "email": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><path d="m22 6-10 7L2 6"/>',
    "presente": '<path d="M20 12v10H4V12M2 7h20v5H2zM12 22V7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/>',
    "stop": '<path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="m15 9-6 6M9 9l6 6"/>',
    "dados": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
    "alerta": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><path d="M12 9v4M12 17h.01"/>',
    "caneta": '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "toque": '<path d="m9 11 3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "decisao": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3M12 17h.01"/>',
    "espera": '<path d="M6 2h12M6 22h12"/><path d="M7 2c0 5 5 6 5 10s-5 5-5 10M17 2c0 5-5 6-5 10s5 5 5 10"/>',
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


def href_projeto(item, lang):
    """Site do cliente → o endereço dele. Cliente sem site publicado → a cópia em /p/<slug>/, com o «voltar» na língua certa."""
    if item.get("url"):
        return item["url"]
    return f"/p/{item['slug']}/" + ("" if lang == "ro" else f"{lang}.html")


def quadrado(item, rot, i, lang):
    nome = item["nome"]
    fs = 1 if len(nome) <= 10 else 0.86 if len(nome) <= 16 else 0.72
    # site real do cliente → separador novo (a página fica aberta por baixo); cliente sem site publicado → cópia em /p/ com «voltar»
    href = href_projeto(item, lang)
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
    """Os sites feitos, por ordem: primeiro os três em destaque, depois os outros pela ordem do ficheiro."""
    itens = [x for x in portfolio["itens"] if x.get("ativo") and not x.get("demo") and (x.get("pasta") or x.get("url"))]
    return sorted(itens, key=lambda x: not x.get("destaque"))


def sites_que_existem(portfolio, controlo):
    """Cada quadrado com site próprio tem de apontar para um domínio que existe. Um link morto trava a publicação
    (foi assim que o restaurantegruponaval.com ficou partido, a 29/09/2026). Sem rede, avisa e segue."""
    import socket
    from urllib.parse import urlsplit

    def estado(host):
        try:
            socket.getaddrinfo(host, 443)
            return "ok"
        except socket.gaierror as err:
            return "não existe" if err.errno in (socket.EAI_NONAME, getattr(socket, "EAI_NODATA", -5)) else "sem resposta"

    externos = [x for x in ativos(portfolio) if x.get("url")]
    if estado(controlo) != "ok":
        print(f"  ! sem DNS aqui: os {len(externos)} sites dos clientes ficam por confirmar")
        return
    mortos, duvidas = [], []
    for x in externos:
        r = estado(urlsplit(x["url"]).hostname)
        if r == "não existe":
            mortos.append(f'{x["nome"]}: {x["url"]}')
        elif r != "ok":
            duvidas.append(x["url"])
    if mortos:
        raise SystemExit("portfolio.json: estes sites não existem (o domínio não responde no DNS). Experimentar o mesmo "
                         "nome em .pt e .online; se também não existirem, pôr ativo: false.\n  " + "\n  ".join(mortos))
    for u in duvidas:
        print(f"  ! {u}: o DNS não respondeu agora; confirmar")
    print(f"  ✓ os {len(externos) - len(duvidas)} sites de clientes existem (DNS)")


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


def mini_quadrado(item, rot, lang, lab):
    """Um site feito, dentro do cartão do tipo de negócio dele: pequeno, com a fonte e as cores do próprio site."""
    href = href_projeto(item, lang)
    fora = href.startswith("http")
    estilo = (f"--bg:{item['bg']};--ink:{item['ink']};--ac:{item['accent']};--f:'{item['fonte']}';--w:{item['peso']}"
              + (";font-style:italic" if item.get("italico") else ""))
    info = rot["itens"].get(item["slug"], {})
    meta = " · ".join(x for x in (info.get("tip", ""), info.get("oras", "")) if x)
    alvo = ' target="_blank" rel="noopener"' if fora else ""
    aviso = f'<span class="so-leitor"> ({e(lab["novo"])})</span>' if fora else ""
    return (f'<li><a class="ex{" neutro" if item.get("neutro") else ""}" href="{e(href)}" style="{estilo}"{alvo}>'
            f'<span class="ex-nome">{e(item["nome"])}</span><span class="ex-meta">{e(meta)}</span>'
            f'{I["fora"] if fora else ""}{aviso}</a></li>')


def cartao_setor(s, i, itens, rot, lang, autos, digitos):
    """Um tipo de negócio, como os cartões das automações: fechado mostra como o cliente escolhe; aberto, as perguntas
    dele e o que o site responde, os sites que já fizemos para esse tipo, as automações que combinam e o pedido."""
    lab = rot["labels"]
    qa = "\n".join(f"      <div><dt><q>{e(q)}</q></dt><dd>{e(r)}</dd></div>" for q, r in s["qa"])
    exs = [x for x in itens if x.get("setor") == s["id"]]
    exemplos = (f'<div><h4 class="rotulo">{e(lab["exemplos"])}</h4><ul class="exemplos">'
                + "".join(mini_quadrado(x, rot, lang, lab) for x in exs) + "</ul></div>") if exs else ""
    chips = " ".join(f'<a class="chip" href="#a-{e(k)}">{e(autos[k]["scurt"])}</a>' for k in s["combina"])
    wa = f"https://wa.me/351{digitos}?text={quote(lab['cta_msg'] + s['titlu'])}"
    return f"""<details class="setor rv" name="setor" id="s-{e(s["id"])}" style="--i:{i}">
  <summary>
    <span class="setor-tipos">{e(s["tipos"])}</span>
    <h3>{e(s["titlu"])}</h3>
    <span class="durere"><span class="eyebrow">{e(lab["decide"])}</span><span class="decide">{e(s["decide"])}</span></span>
    <span class="vezi" aria-hidden="true"><span class="abre">{e(lab["ver"])}</span><span class="fecha">{e(lab["fechar"])}</span>{I["baixo"]}</span>
  </summary>
  <div class="corpo">
    <div><h4 class="rotulo">{e(lab["pergunta"])} <span aria-hidden="true">·</span> {e(lab["responde"])}</h4>
    <dl class="perguntas">
{qa}
    </dl></div>
    {exemplos}
    <div><h4 class="rotulo">{e(lab["combina"])}</h4><div class="chips">{chips}</div></div>
    <div class="demo"><p>{e(lab["cta_t"])}</p><a class="botao secundario" href="{e(wa)}">{I["chat"]}{e(lab["cta"])}</a></div>
  </div>
</details>"""


def vista_proiecte(c, portfolio, lang, digitos):
    """Sites: três em destaque, depois os tipos de negócio (o que o cliente pergunta e o que o site responde), com os
    sites feitos lá dentro, para quem os quiser ver. Não há grelha com todos: o número de trabalhos não é o assunto."""
    p = c["proiecte"]
    itens = ativos(portfolio)
    dest = [x for x in itens if x.get("destaque")]
    if len(dest) != 3:
        raise SystemExit(f"portfolio.json: «Em destaque» leva 3 sites, há {len(dest)}: {[x['slug'] for x in dest]}")
    ids = [s["id"] for s in p["setores"]]
    sem = [x["slug"] for x in itens if x.get("setor") not in ids]
    if sem:
        raise SystemExit(f"portfolio.json: estes sites não têm um «setor» de conteudo/{lang}.json (proiecte.setores): {sem}")
    autos = {x["id"]: x for x in c["automatizari"]["itens"]}
    for s in p["setores"]:
        if not set(s["combina"]) <= set(autos):
            raise SystemExit(f"conteudo/{lang}.json: o tipo «{s['id']}» combina com automações que não existem")
    selecao = "\n".join(quadrado(x, p, i, lang) for i, x in enumerate(dest))
    cartoes = "\n".join(cartao_setor(s, i, itens, p, lang, autos, digitos) for i, s in enumerate(p["setores"]))
    # os outros sites, em grelha, para mostrar mais variações: sem quadrado de contacto nem «+» (decisão de 29/09)
    resto = [x for x in itens if not x.get("destaque")]
    mais = "\n".join(quadrado(x, p, i, lang) for i, x in enumerate(resto))
    cu = p["cuidado"]
    compromissos = "\n".join(f'<li class="rv" style="--i:{i}"><h3>{e(x["t"])}</h3><p>{e(x["d"])}</p></li>'
                             for i, x in enumerate(cu["itens"]))
    m = c["metoda"]
    passos = "\n".join(f'<li class="passo rv" style="--i:{i}"><h3>{e(s["t"])}</h3><p>{e(s["d"])}</p></li>' for i, s in enumerate(m["pasi"]))
    return f"""<section id="proiecte" class="vista" aria-labelledby="t-proiecte">
  <div class="envolver seccao">
    <p class="eyebrow">{e(p["eyebrow"])}</p>
    <h2 id="t-proiecte" class="afirmacao">{e(p["titlu"])}</h2>
    <p class="lead">{e(p["intro"])}</p>
    <p class="rotulo selecao">{e(p["selecao"])}</p>
    <ul class="grelha">
{selecao}
    </ul>
    <div class="setores-grelha">
      <div class="cab">
        <p class="eyebrow">{e(p["setores_e"])}</p>
        <p class="lead">{e(p["setores_intro"])}</p>
      </div>
      <div class="setores">
{cartoes}
      </div>
    </div>
    <div class="mais">
      <p class="eyebrow">{e(p["mais_e"])}</p>
      <p class="lead">{e(p["mais_intro"])}</p>
      <ul class="grelha-mais">
{mais}
      </ul>
    </div>
    <div class="cuidado">
      <p class="eyebrow">{e(cu["eyebrow"])}</p>
      <h2 class="afirmacao">{e(cu["titlu"])}</h2>
      <ul class="compromissos">
{compromissos}
      </ul>
    </div>
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


def svg_ic(nome):
    if nome not in ICONES_ESQUEMA:
        raise SystemExit(f"conteudo/esquemas.json: ícone «{nome}» não existe em ICONES_ESQUEMA")
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONES_ESQUEMA[nome]}</svg>'


def caixa(tipo, titulo, texto, icone):
    """Uma caixa do esquema: ícone + título + linha pequena, com as portas do motor de fluxo."""
    cls = {"gatilho": "gatilho", "pessoa": "pessoa", "decizie": "decisao", "espera": "espera"}.get(tipo, "auto")
    tx = (f"<b>{e(titulo)}</b>" if titulo else "") + (f"<small>{e(texto)}</small>" if texto and titulo else "")
    if texto and not titulo:  # ramo: só a frase do que acontece
        tx = f'<span class="so">{e(texto)}</span>'
    return f'<div class="n {cls}"><span class="ic">{svg_ic(icone)}</span><span class="tx">{tx}</span></div>'


def esquema(x, lab, icones):
    """O esquema de uma automação, desenhado como o da proposta Be Legend, dentro de um <dialog> (cartão no meio do ecrã)."""
    passos = []
    for n, ic in zip(x["fluxo"], icones):
        if n.get("espera"):
            passos.append(f'<li>{caixa("espera", n["espera"], "", "espera")}</li>')
        if n.get("ramuri"):
            ramos = "".join(
                f'<li><span class="pilula">{e(r["t"])}</span>{caixa("pessoa" if r.get("tip") == "pessoa" else "auto", "", r["d"], ric)}</li>'
                for r, ric in zip(n["ramuri"], ic["ramos"]))
            passos.append(f'<li>{caixa("decizie", n["t"], n.get("d", ""), "decisao")}'
                          f'<ul class="ramos" style="--n:{len(n["ramuri"])}">{ramos}</ul></li>')
        else:
            passos.append(f'<li>{caixa(n["tip"], n["t"], n.get("d", ""), ic)}</li>')
    leg = lab["legenda"]
    legenda = "".join(f'<li><i class="l {k}"></i>{e(leg[c])}</li>' for k, c in
                      (("gatilho", "gatilho"), ("auto", "auto"), ("pessoa", "pessoa"), ("decisao", "decizie"), ("espera", "espera")))
    ide = f"esquema-{x['id']}"
    return f"""<dialog class="esquema" id="{ide}" aria-labelledby="{ide}-t">
  <div class="folha">
    <header class="folha-cab">
      <p class="eyebrow">{e(lab["esquema_eyebrow"])} · {e(x["scurt"])}</p>
      <h2 id="{ide}-t">{e(lab["esquema_titulo"])}</h2>
      <p>{e(lab["esquema_intro"])}</p>
      <a class="fechar" href="#a-{e(x["id"])}" data-fechar aria-label="{e(lab["inchide"])}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg></a>
    </header>
    <div class="tela"><ol class="fluxo">
{chr(10).join(passos)}
    </ol></div>
    <footer class="folha-pe">
      <ul class="legenda-e">{legenda}</ul>
      <p>Pacheco Studios · {e(x["titlu"])}</p>
    </footer>
  </div>
</dialog>"""


def botao_esquema(x, lab):
    ide = f"esquema-{x['id']}"
    return (f'<a class="ver-esquema" href="#{ide}" data-esquema="{ide}">'
            '<span class="mini" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<span class="txt"><b>{e(lab["esquema_cta"])}</b><small>{e(lab["esquema_nota"])}</small></span>{I["seta"]}</a>')


def vista_automatizari(c, digitos, icones, casos, servicii):
    a = c["automatizari"]
    lab = a["labels"]
    por_id = {x["id"]: x for x in a["itens"]}
    cards, dialogos = [], []
    for i, x in enumerate(a["itens"]):
        if x["id"] not in icones or len(icones[x["id"]]) != len(x["fluxo"]):
            raise SystemExit(f"conteudo/esquemas.json: «{x['id']}» tem de ter um ícone por passo do fluxo")
        dialogos.append(esquema(x, lab, icones[x["id"]]))
        reguli = "\n".join(f"<li>{e(r)}</li>" for r in x["reguli"])
        decide = "".join(f'<div><b>{e(lab[k])}</b><span>{e(x["decide"][k])}</span></div>' for k in ("tu", "masina", "noi"))
        chat = "".join(f'<div class="msg {e(m["cine"])}"><small>{e(lab["client"] if m["cine"] == "client" else lab["asistent"] if m["cine"] == "asistent" else lab["tu_msg"])}</small>{e(m["t"])}</div>'
                       for m in x["exemplu"])
        chips = " ".join(f'<a class="chip" href="#a-{e(k)}">{e(por_id[k]["scurt"])}</a>' for k in x["leaga"] if k in por_id)
        wa_demo = f"https://wa.me/351{digitos}?text={quote(lab['demo_msg'] + x['titlu'])}"
        vistos = [k for k in casos["itens"] if x["id"] in k["aplica"]]
        caso = ""
        if vistos:
            ligs = " ".join(f'<a class="chip" href="#caso-{e(k["id"])}">{e(k["empresa"])}</a>' for k in vistos)
            caso = f'\n    <div class="caso-ref"><h4 class="rotulo">{e(lab["caso"])}</h4><div class="chips">{ligs}</div></div>'

        cards.append(f"""<details class="auto rv" name="auto" id="a-{e(x["id"])}" style="--i:{i}">
  <summary>
    <h3>{e(x["titlu"])}</h3>
    <span class="durere"><span class="eyebrow">{e(lab["durere"])}</span><q>{e(x["durere"])}</q></span>
    <span class="vezi" aria-hidden="true"><span class="abre">{e(lab["vezi"])}</span><span class="fecha">{e(lab["inchide"])}</span>{I["baixo"]}</span>
  </summary>
  <div class="corpo">
    {botao_esquema(x, lab)}
    <div class="obtii"><h4 class="rotulo">{e(lab["obtii"])}</h4>{e(x["obtii"])}</div>{caso}
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
    return f"""<section id="automatizari" class="vista" aria-labelledby="t-automatizari">
  <div class="envolver seccao">
    <div class="autos-grelha">
      <div class="cab">
        <p class="eyebrow">{e(a["eyebrow"])}</p>
        <h2 id="t-automatizari" class="afirmacao">{e(a["titlu"])}</h2>
        <p class="lead">{e(a["intro"])}</p>
        <p class="lead intro-2">{e(a["intro_extra"])}</p>
      </div>
      <div class="autos">
{chr(10).join(cards)}
      </div>
    </div>
    <div class="esquemas">
{chr(10).join(dialogos)}
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
{servicii}
</section>"""


def textos_casos(c, casos, lang):
    """Junta os dados partilhados de cada caso (conteudo/casos.json) aos textos da língua; trava se faltar algum."""
    t = c["cazuri"]["itens"]
    autos = {x["id"] for x in c["automatizari"]["itens"]} | {"sites"}
    out = []
    for k in casos["itens"]:
        if k["id"] not in t:
            raise SystemExit(f"conteudo/{lang}.json: falta o caso «{k['id']}» em cazuri.itens")
        if not set(k["aplica"]) <= autos:
            raise SystemExit(f"conteudo/casos.json: o caso «{k['id']}» aplica-se a soluções que não existem: {k['aplica']}")
        if not k["url"].startswith("https://"):
            raise SystemExit(f"conteudo/casos.json: o caso «{k['id']}» precisa da ligação para a fonte")
        x = t[k["id"]]
        if len(x["numeros"]) != 3:
            raise SystemExit(f"conteudo/{lang}.json: o caso «{k['id']}» leva 3 números")
        out.append({**k, **x})
    if set(t) - {k["id"] for k in casos["itens"]}:
        raise SystemExit(f"conteudo/{lang}.json: casos sem dados em conteudo/casos.json: {sorted(set(t) - {k['id'] for k in casos['itens']})}")
    return out


def vista_consultanta(c, casos, lang, wa):
    """A porta de entrada: o objetivo do dono, a diferença entre agência e consultoria, os cinco passos, o que é a IA
    (as mesmas cinco frases de sempre), três números de casos reais (de outros, e dito), os compromissos e quem faz."""
    k = c["consultanta"]
    tx = textos_casos(c, casos, lang)
    factos = "".join(f"<li>{e(f)}</li>" for f in k["factos"])
    d = k["dif"]
    col = lambda cls, t, itens: (f'<div class="dif-col {cls}"><h3>{e(t)}</h3><ul>'
                                 + "".join(f"<li>{e(x)}</li>" for x in itens) + "</ul></div>")
    m = k["metodo"]
    passos = "\n".join(f'<li class="passo rv" style="--i:{i}"><span class="passo-q">{e(p["q"])}</span><h3>{e(p["t"])}</h3><p>{e(p["d"])}</p></li>'
                       for i, p in enumerate(m["pasi"]))
    ia = k["ia"]
    frases = "".join(f'<li class="rv" style="--i:{i}">{e(f)}</li>' for i, f in enumerate(c["automatizari"]["labels"]["ai"]))
    cs = k["casos"]
    dest = [x for x in tx if x.get("destaque")]
    numeros = "\n".join(
        f'<li class="rv" style="--i:{i}"><a href="#caso-{e(x["id"])}"><b>{e(x["numeros"][x["destaque_n"]]["v"])}</b>'
        f'<span>{e(x["numeros"][x["destaque_n"]]["l"])}</span><small>{e(x["empresa"])} · {e(cs["ver"])}{I["seta"]}</small></a></li>'
        for i, x in enumerate(dest))
    cu = k["cuidado"]
    compromissos = "\n".join(f'<li class="rv" style="--i:{i}"><h3>{e(x["t"])}</h3><p>{e(x["d"])}</p></li>'
                             for i, x in enumerate(cu["itens"]))
    q = k["quem"]
    return f"""<section id="consultanta" class="vista" aria-labelledby="t-consultanta">
  <div class="envolver heroi">
    <p class="eyebrow">{e(k["eyebrow"])}</p>
    <h2 id="t-consultanta" class="heroi-t"><span class="heroi-pre">{e(k["pre"])}</span><span class="heroi-grande">{e(k["titlu"])}</span></h2>
    <p class="heroi-passo">{e(k["passo"])}</p>
    <p class="lead heroi-lead">{e(k["lead"])}</p>
    <div class="heroi-acoes">
      <a class="botao primario grande" href="{e(wa)}">{I["chat"]}{e(c["contact"]["cta"])}</a>
      <a class="link-seta" href="#cazuri">{e(k["ver_casos"])}{I["seta"]}</a>
    </div>
    <ul class="factos">{factos}</ul>
  </div>
  <div class="envolver seccao dif">
    <p class="eyebrow">{e(d["eyebrow"])}</p>
    <h2 class="afirmacao">{e(d["titlu"])}</h2>
    <div class="dif-grelha">
      {col("agencia", d["a_t"], d["a"])}
      {col("nos", d["c_t"], d["c"])}
    </div>
  </div>
  <div class="claro">
    <div class="envolver seccao">
      <p class="eyebrow">{e(m["eyebrow"])}</p>
      <h2 class="afirmacao">{e(m["titlu"])}</h2>
      <ol class="passos passos-5">
{passos}
      </ol>
    </div>
  </div>
  <div class="envolver seccao ia-bloco">
    <p class="eyebrow">{e(ia["eyebrow"])}</p>
    <h2 class="afirmacao">{e(ia["titlu"])}</h2>
    <ol class="ia-lista">{frases}</ol>
    <p class="ia-fecho">{e(ia["fecho"])}</p>
    <a class="link-seta" href="#automatizari">{e(ia["ver"])}{I["seta"]}</a>
  </div>
  <div class="envolver seccao casos-teaser">
    <p class="eyebrow">{e(cs["eyebrow"])}</p>
    <h2 class="afirmacao">{e(cs["titlu"])}</h2>
    <ul class="numeros">
{numeros}
    </ul>
    <p class="nota-fonte">{e(cs["nota"])}</p>
    <a class="link-seta" href="#cazuri">{e(cs["todos"])}{I["seta"]}</a>
  </div>
  <div class="envolver seccao cuidado-c">
    <p class="eyebrow">{e(cu["eyebrow"])}</p>
    <h2 class="afirmacao">{e(cu["titlu"])}</h2>
    <ul class="compromissos">
{compromissos}
    </ul>
  </div>
  <div class="claro">
    <div class="envolver seccao quem">
      <p class="eyebrow">{e(q["eyebrow"])}</p>
      <h2 class="afirmacao">{e(q["titlu"])}</h2>
      <p class="quem-texto">{e(q["texto"])}</p>
      <p class="quem-assina">{e(q["assina"])}</p>
    </div>
  </div>
</section>"""


def vista_cazuri(c, casos, lang, digitos):
    """Casos reais de outras empresas, ditos como tal: o problema, o que fizeram, três números, a fonte (abre a página
    original) e a solução nossa que faz o mesmo. No fim, o lugar vazio do primeiro caso nosso."""
    z = c["cazuri"]
    lab = z["labels"]
    por_id = {x["id"]: x for x in c["automatizari"]["itens"]}
    itens = []
    for i, x in enumerate(textos_casos(c, casos, lang)):
        nums = "".join(f'<li><b>{e(n["v"])}</b><span>{e(n["l"])}</span></li>' for n in x["numeros"])
        chips = " ".join(f'<a class="chip" href="#proiecte">{e(lab["sites"])}</a>' if a == "sites" else
                         f'<a class="chip" href="#a-{e(a)}">{e(por_id[a]["scurt"])}</a>' for a in x["aplica"])
        dominio = re.sub(r"^https://(www\.)?([^/]+).*$", r"\2", x["url"])
        itens.append(f"""<li class="caso rv" id="caso-{e(x["id"])}" style="--i:{i % 2}">
  <p class="caso-tag">{e(x["setor"])}</p>
  <p class="selo">{e(lab["selo"])}</p>
  <h3 class="caso-empresa">{e(x["empresa"])}</h3>
  <p class="caso-titulo">{e(x["titlu"])}</p>
  <ul class="caso-num">{nums}</ul>
  <div class="caso-txt">
    <div><h4 class="rotulo">{e(lab["problema"])}</h4><p>{e(x["problema"])}</p></div>
    <div><h4 class="rotulo">{e(lab["solucao"])}</h4><p>{e(x["solucao"])}</p></div>
  </div>
  <div class="caso-pe">
    <div><h4 class="rotulo">{e(lab["aplica"])}</h4><div class="chips">{chips}</div></div>
    <a class="fonte" href="{e(x["url"])}" target="_blank" rel="noopener"><span>{e(lab["fonte"])}<small>{e(casos["fonte"])} · {e(dominio)}</small></span>{I["fora"]}</a>
  </div>
</li>""")
    v = z["vazio"]
    wa_v = f"https://wa.me/351{digitos}?text={quote(v['msg'])}"
    itens.append(f"""<li class="caso vazio rv" id="caso-1">
  <p class="caso-tag">{e(v["tag"])}</p>
  <h3 class="caso-empresa">{e(v["titlu"])}</h3>
  <p>{e(v["texto"])}</p>
  <a class="botao secundario" href="{e(wa_v)}">{I["chat"]}{e(v["cta"])}</a>
</li>""")
    p = z["ponte"]
    passos = "\n".join(f'<li class="passo rv" style="--i:{i}"><h3>{e(s["t"])}</h3><p>{e(s["d"])}</p></li>' for i, s in enumerate(p["pasi"]))
    return f"""<section id="cazuri" class="vista" aria-labelledby="t-cazuri">
  <div class="envolver seccao">
    <p class="eyebrow">{e(z["eyebrow"])}</p>
    <h2 id="t-cazuri" class="afirmacao">{e(z["titlu"])}</h2>
    <p class="lead">{e(z["intro"])}</p>
    <p class="aviso">{e(z["aviso"])}</p>
    <ul class="casos">
{chr(10).join(itens)}
    </ul>
  </div>
  <div class="claro">
    <div class="envolver seccao">
      <p class="eyebrow">{e(p["eyebrow"])}</p>
      <h2 class="afirmacao">{e(p["titlu"])}</h2>
      <ol class="passos">
{passos}
      </ol>
    </div>
  </div>
</section>"""


def vista_servicii(c, portfolio, lang):
    s = c["servicii"]
    ligacao = {x["slug"]: href_projeto(x, lang) for x in ativos(portfolio)}
    cards = []
    for i, x in enumerate(s["itens"]):
        ex = ""
        if x.get("exemplu") and x["exemplu"] not in ligacao:
            raise SystemExit(f"servicii «{x['id']}»: o exemplo «{x['exemplu']}» não está nos quadrados (só clientes reais)")
        if x.get("exemplu") in ligacao:
            u = ligacao[x["exemplu"]]
            ex = f'<a class="link-ex" href="{e(u)}"{" target=_blank rel=noopener" if u.startswith("http") else ""}>{e(s["exemplu"])}{I["seta"]}</a>'
        cards.append(f'<li class="svc rv" style="--i:{i}"><h3>{e(x["titlu"])}</h3><p>{e(x["ce"])}</p><p class="de-ce">{e(x["de_ce"])}</p>{ex}</li>')
    return f"""<div id="servicii" class="claro tambem">
  <div class="envolver seccao">
    <p class="eyebrow">{e(s["eyebrow"])}</p>
    <h2 class="afirmacao">{e(s["titlu"])}</h2>
    <p class="lead">{e(s["intro"])}</p>
    <ul class="svcs">
{chr(10).join(cards)}
    </ul>
  </div>
</div>"""


def contacto(c, d, wa, tel_legivel, digitos, com_site):
    k = c["contact"]
    lab = k["labels"]
    ig = d["instagram"].lstrip("@")
    site = d["site_principal"]
    linhas = [(lab["whatsapp"], tel_legivel, wa, "chat"), (lab["telefon"], tel_legivel, f"tel:+351{digitos}", "telefone"),
              (lab["email"], d["email"], f"mailto:{d['email']}", "email"),
              (lab["instagram"], f"@{ig}", f"https://www.instagram.com/{ig}/", "instagram")]
    if com_site:  # na página romena, o site principal; em pachecost.com seria uma ligação para a própria página
        linhas.append((lab["site"], site, f"https://{site}/", "site"))
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


def intro(c):
    """Ecrã de arranque: um carro passa pelos dois portais (web design + marketing, IA) e sai transformado. Só o
    JavaScript o mostra (uma vez por sessão, nunca com movimento reduzido); sem ele fica em display:none. As três
    fotografias (media/intro-{1,2,3}.webp) são postas pelo JavaScript quando carregam; o texto vem de «intro»."""
    t = c["intro"]
    slogan = re.sub(r"\*(.+?)\*", r"<em>\1</em>", e(" ".join(c["og"]["slogan"])))
    legendas = "\n".join(f'      <p id="intro-l{i + 1}"{" class=" + chr(34) + "ativa" + chr(34) if i == 0 else ""}><b>0{i + 1}</b><span>{e(x)}</span></p>'
                         for i, x in enumerate(t["legendas"]))
    portal = ('<g id="intro-p{n}"><rect class="aura" x="-12" y="0" width="24" height="250" fill="url(#intro-brilho)" opacity=".35"/>'
              '<line class="fio" x1="0" y1="4" x2="0" y2="246" stroke="#E8622C" stroke-width="2.5"/>'
              '<line x1="-10" y1="4" x2="10" y2="4" stroke="#E8622C" stroke-width="2.5" stroke-linecap="round"/></g>')
    carro = ('<g clip-path="url(#intro-z{z})"><g id="intro-c{z}"><ellipse cx="0" cy="3" rx="0" ry="8" fill="url(#intro-sombra)"/>'
             '<image x="0" y="0" width="0" height="0"/></g></g>')
    marca = '<p class="marca"><span class="ponto" aria-hidden="true"></span>Pacheco Studios</p>'
    return f'''<div class="intro" id="intro" role="dialog" aria-modal="true" aria-label="{e(t["rotulo"])}">
  <div class="intro-topo">
    {marca}
    <button class="intro-saltar" type="button" id="intro-saltar">{e(t["saltar"])}</button>
  </div>
  <div class="intro-palco">
    <div class="intro-cena">
      <p class="intro-rot" id="intro-rot1">{e(t["p1"])}</p>
      <p class="intro-rot" id="intro-rot2">{e(t["p2"])}</p>
      <svg viewBox="0 0 560 300" role="img" aria-labelledby="intro-cena-t">
        <title id="intro-cena-t">{e(t["descricao"])}</title>
        <defs>
          <clipPath id="intro-zA" clipPathUnits="userSpaceOnUse"><rect id="intro-rA" x="-1000" y="-50" width="1600" height="400"/></clipPath>
          <clipPath id="intro-zB" clipPathUnits="userSpaceOnUse"><rect id="intro-rB" x="600" y="-50" width="0" height="400"/></clipPath>
          <clipPath id="intro-zC" clipPathUnits="userSpaceOnUse"><rect id="intro-rC" x="1600" y="-50" width="4000" height="400"/></clipPath>
          <linearGradient id="intro-brilho" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#E8622C" stop-opacity="0"/><stop offset=".5" stop-color="#E8622C" stop-opacity=".55"/><stop offset="1" stop-color="#E8622C" stop-opacity="0"/></linearGradient>
          <radialGradient id="intro-sombra"><stop offset="0" stop-color="#000" stop-opacity=".6"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
        </defs>
        <line x1="-1500" y1="240" x2="2500" y2="240" stroke="rgba(239,234,227,.45)" stroke-width="1.5"/>
        <line id="intro-tracos" x1="-1500" y1="262" x2="2500" y2="262" stroke="rgba(239,234,227,.2)" stroke-width="3" stroke-dasharray="22 26"/>
        <g id="intro-riscos" stroke="#E8622C" stroke-linecap="round" opacity="0"></g>
        {carro.format(z="A")}
        {carro.format(z="B")}
        {carro.format(z="C")}
        {portal.format(n=1)}
        {portal.format(n=2)}
      </svg>
    </div>
    <div class="intro-legenda">
{legendas}
    </div>
  </div>
  <div class="intro-pe"></div>
  <div class="intro-final" aria-hidden="true">
    {marca}
    <p class="intro-slogan">{slogan}</p>
  </div>
</div>'''


def rodape(c, lang):
    r = c["rodape"]
    return f"""<footer class="rodape">
  <div class="envolver">
    <p>{e(r["linha"])}</p>
    <p><a href="https://www.livroreclamacoes.pt/inicio/" rel="noopener">{e(r["legal"])}</a></p>
    <p><a href="{e(LINGUAS[lang]["privacidade"])}">{e(r["privacidade"])}</a></p>
    <p>{e(r["nota"])}</p>
  </div>
</footer>"""


def caminho_para(de, para):
    """Mesmo domínio → caminho relativo à raiz; outro domínio → endereço completo."""
    a, b = LINGUAS[de], LINGUAS[para]
    return b["caminho"] if a["host"] == b["host"] else b["url"]


def seletor(c, lang):
    lab = c["linguas"]
    out = []
    for k, v in LINGUAS.items():
        atual = ' aria-current="true"' if k == lang else ""
        out.append(f'<a href="{e(caminho_para(lang, k))}" hreflang="{v["hreflang"]}" lang="{v["hreflang"]}"{atual}>'
                   f'<span aria-hidden="true">{k.upper()}</span><span class="so-leitor">{e(lab[k])}</span></a>')
    return f'<nav class="linguas" aria-label="{e(lab["rotulo"])}">{"".join(out)}</nav>'


def hreflang():
    linhas = [f'<link rel="alternate" hreflang="{v["hreflang"]}" href="{v["url"]}">' for v in LINGUAS.values()]
    linhas.append(f'<link rel="alternate" hreflang="x-default" href="{LINGUAS["pt"]["url"]}">')
    return "\n".join(linhas)


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
def pilula(texto, lang, voltar):
    return (f'\n<a id="ps-inapoi" href="{voltar}" lang="{lang}" style="position:fixed;left:12px;bottom:calc(12px + env(safe-area-inset-bottom));'
            'z-index:2147483647;display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:10px 16px 10px 12px;border-radius:999px;'
            'background:#141210;color:#EFEAE3;border:2px solid #E8622C;font:700 14px/1 system-ui,-apple-system,\'Segoe UI\',Roboto,sans-serif;'
            'letter-spacing:.02em;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.35)">'
            '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" style="flex:none;fill:none;stroke:#E8622C;stroke-width:2.5;'
            f'stroke-linecap:round;stroke-linejoin:round"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>{e(texto)}</a>\n'
            "<script>(function(){var a=document.getElementById('ps-inapoi');a.addEventListener('click',function(ev){try{"
            "if(document.referrer&&new URL(document.referrer).host===location.host&&history.length>1){ev.preventDefault();history.back();}"
            "}catch(e){}});})();</script>\n")


def copiar_sites(portfolio, linguas):
    """Clientes sem site publicado: uma cópia em /p/<slug>/ com os media partilhados e uma página por língua
    (index.html romeno, pt.html, en.html), cada uma com o «voltar» na língua e para a página certa."""
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
        for lang, c in linguas.items():
            nome = "index.html" if lang == "ro" else f"{lang}.html"
            voltar = LINGUAS[lang]["caminho"] + "#proiecte"
            open(os.path.join(destino, nome), "w", encoding="utf-8").write(
                h.replace("</body>", pilula(c["inapoi"], LINGUAS[lang]["hreflang"], voltar) + "</body>", 1))
        media = os.path.join(origem, "media")
        if os.path.isdir(media):
            shutil.copytree(media, os.path.join(destino, "media"), dirs_exist_ok=True)
        n += 1
    return n


def og_png(fontes, og, destino):
    def frase(l):
        t = e(l.strip("*"))
        if t.endswith("."):
            t = t[:-1] + '<span class="pf"></span>'
        return f'<span{" class=o" if l.startswith("*") else ""}>{t}</span>'
    pagina = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{fontes}
    body{{margin:0;width:1200px;height:630px;background:#141210;color:#EFEAE3;position:relative;overflow:hidden}}
    .m{{position:absolute;left:84px;top:72px;display:flex;align-items:center;gap:18px;font:700 24px/1 "Space Mono";letter-spacing:.24em}}
    .m i{{width:18px;height:18px;border-radius:50%;background:#E8622C}}
    .r{{position:absolute;right:84px;top:72px;font:700 24px/1 "Space Mono";letter-spacing:.24em;color:#A5A19B}}
    h1{{position:absolute;left:80px;top:150px;margin:0;font:400 90px/.93 "Archivo Black";text-transform:uppercase}}
    h1 span{{display:block}} .o{{color:#E8622C}}
    .pf{{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:#E8622C;margin-left:.06em}}
    .s{{position:absolute;left:84px;bottom:60px;font:700 24px/1 "Space Mono";letter-spacing:.12em;color:#A5A19B;text-transform:uppercase}}
    </style></head><body><p class="m"><i></i>PACHECO STUDIOS</p><p class="r">{e(og["regiao"].upper())}</p>
    <h1>{"".join(frase(l) for l in og["slogan"])}</h1><p class="s">{e(og["proposito"])}</p></body></html>"""
    tmp = os.path.join(AQUI, ".og.html")
    open(tmp, "w", encoding="utf-8").write(pagina)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    subprocess.run(["node", "-e", """
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + process.argv[1]); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: process.argv[2] }); await b.close(); })();
""", tmp, destino], check=True, env=NODE_ENV)
    os.remove(tmp)


def cabeca_simples(lang, titulo, estilo, extra=""):
    return f"""<!DOCTYPE html>
<html lang="{LINGUAS[lang]["hreflang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)} — Pacheco Studios</title>
<meta name="theme-color" content="#141210">
{extra}{estilo}
</head>"""


def pagina_404(c, estilo, lang):
    t = c["p404"]
    casa = LINGUAS[lang]["caminho"]
    return cabeca_simples(lang, t["titlu"], estilo, '<meta name="robots" content="noindex">\n') + f"""
<body>
<header class="envolver topo">
  <a class="marca" href="{casa}"><span class="ponto" aria-hidden="true"></span>Pacheco Studios</a>
</header>
<main id="conteudo" class="envolver seccao">
  <p class="eyebrow">404</p>
  <h1 class="afirmacao">{e(t["titlu"])}</h1>
  <p class="lead">{e(t["text"])}</p>
  <a class="botao primario grande" href="{casa}#proiecte">{I["seta"]}{e(t["cta"])}</a>
</main>
{rodape(c, lang)}
</body>
</html>
"""


def pagina_privacidade(c, estilo, lang, email):
    t = c["privacidade"]
    casa = LINGUAS[lang]["caminho"]
    url = f"https://{LINGUAS[lang]['host']}{LINGUAS[lang]['privacidade']}"
    def par(s):
        txt = e(s["p"]).replace(e(email), f'<a href="mailto:{e(email)}">{e(email)}</a>')
        lig = f' <a href="{e(s["link"]["href"])}" rel="noopener">{e(s["link"]["t"])}</a>' if s.get("link") else ""
        return f'<h2>{e(s["t"])}</h2>\n<p>{txt}{lig}</p>'
    secoes = "\n".join(par(s) for s in t["secoes"])
    extra = (f'<meta name="description" content="{e(t["intro"])}">\n<link rel="canonical" href="{url}">\n'
             '<style>.legal h2{margin-top:2.2rem;font:700 .8125rem/1.3 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--osso)}'
             '.legal h2+p{max-width:62ch;margin-top:.6rem;color:var(--osso-2)}.legal h2+p a{color:var(--osso);text-underline-offset:.2em}'
             '.legal .nota{margin-top:2.4rem;font:400 .8125rem/1.5 var(--mono)}.legal .botao{margin-top:1.6rem}</style>\n')
    return cabeca_simples(lang, t["titulo"], estilo, extra) + f"""
<body>
<a class="saltar" href="#conteudo">{e(LINGUAS[lang]["saltar"])}</a>
<header class="envolver topo">
  <a class="marca" href="{casa}"><span class="ponto" aria-hidden="true"></span>Pacheco Studios</a>
</header>
<main id="conteudo" class="envolver seccao legal">
  <p class="eyebrow">Legal</p>
  <h1 class="afirmacao">{e(t["titulo"])}</h1>
  <p class="lead">{e(t["intro"])}</p>
{secoes}
  <p class="nota">{e(t["atualizado"])}</p>
  <a class="botao secundario" href="{casa}">{e(t["voltar"])}</a>
</main>
{rodape(c, lang)}
</body>
</html>
"""


def configurar_linguas(d):
    """Onde vive cada língua. PT abre pachecost.com; EN em /en/; RO em ro.pachecost.com (o QR do cartão)."""
    principal, dominio = d["site_principal"].strip().lower(), d["dominio"].strip().lower()
    LINGUAS.clear()
    LINGUAS.update({
        "pt": {"host": principal, "caminho": "/", "pasta": "", "hreflang": "pt-PT", "og_locale": "pt_PT",
               "privacidade": "/privacidade.html", "areas": ["Portugal", "Romania"], "saltar": "Saltar para o conteúdo",
               "nav": "Secções", "com_site": False},
        "en": {"host": principal, "caminho": "/en/", "pasta": "en", "hreflang": "en", "og_locale": "en_GB",
               "privacidade": "/privacy.html", "areas": ["Portugal", "Romania"], "saltar": "Skip to content",
               "nav": "Sections", "com_site": False},
        "ro": {"host": dominio, "caminho": "/", "pasta": "ro", "hreflang": "ro", "og_locale": "ro_RO",
               "privacidade": "/confidentialitate.html", "areas": ["Romania"], "saltar": "Sari la conținut",
               "nav": "Secțiuni", "com_site": True},
    })
    for v in LINGUAS.values():
        v["url"] = f"https://{v['host']}{v['caminho']}"
    return principal, dominio


def main():
    d = json.load(open(os.path.join(MARCA, "dados.json"), encoding="utf-8"))
    portfolio = json.load(open(os.path.join(AQUI, "portfolio.json"), encoding="utf-8"))
    principal, dominio = configurar_linguas(d)
    linguas = {k: json.load(open(os.path.join(AQUI, "conteudo", f"{k}.json"), encoding="utf-8")) for k in LINGUAS}
    medicao = d.get("medicao", {})
    icones = {k: v for k, v in json.load(open(os.path.join(AQUI, "conteudo", "esquemas.json"), encoding="utf-8")).items()
              if not k.startswith("_")}
    casos = json.load(open(os.path.join(AQUI, "conteudo", "casos.json"), encoding="utf-8"))
    digitos = re.sub(r"\D", "", d["telefone"])
    digitos = digitos[3:] if digitos.startswith("351") and len(digitos) == 12 else digitos
    if len(digitos) != 9:
        raise SystemExit("marca/dados.json: telefone tem de ter 9 dígitos")
    tel_legivel = f"+351 {digitos[:3]} {digitos[3:6]} {digitos[6:]}"
    fontes = fontes_css()
    src = open(os.path.join(AQUI, "index.src.html"), encoding="utf-8").read()

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    print("LINKS DOS CLIENTES")
    sites_que_existem(portfolio, principal)

    ok = True
    print("\nCONTEÚDO")
    paginas, extras = {}, {}
    for lang, c in linguas.items():
        cfg = LINGUAS[lang]
        falta = glifos_em_falta(textos_de(c))
        print(f"  {lang}: {'todas as letras existem nas fontes' if not falta else '✗ letras sem glifo: ' + ''.join(falta)}")
        ok &= not falta
        wa = f"https://wa.me/351{digitos}?text={quote(c['contact']['mensagem_wa'])}"
        og_img = f"https://{cfg['host']}/media/og-{lang}.png"
        jsonld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Pacheco Studios", "url": cfg["url"],
                  "image": og_img, "description": c["meta"]["description"], "telephone": tel_legivel, "email": d["email"],
                  "areaServed": [{"@type": "Country", "name": n} for n in cfg["areas"]],
                  "sameAs": [f"https://www.instagram.com/{d['instagram'].lstrip('@')}/"],
                  "founder": {"@type": "Person", "name": d["nome"]}}
        k = c["consent"]
        valores = {
            "LINGUA": cfg["hreflang"], "TITLE": e(c["meta"]["title"]), "DESCRIPTION": e(c["meta"]["description"]),
            "OG_TITLE": e(c["meta"]["og_title"]), "OG_LOCALE": cfg["og_locale"], "OG_IMAGE": og_img,
            "URL_PAGINA": cfg["url"], "HREFLANG": hreflang(), "FONTES": fontes, "FONTES_GOOGLE": fontes_google(portfolio),
            "JSONLD": json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/"),
            "GOATCOUNTER": e(medicao.get("goatcounter", "")), "PIXEL": re.sub(r"\D", "", medicao.get("pixel_meta", "")) if lang in medicao.get("pixel_linguas", ["pt", "en"]) else "",
            "SALTAR": e(cfg["saltar"]), "NAV_LABEL": e(cfg["nav"]), "LINGUAS": seletor(c, lang),
            "TAB_CONSULTANTA": e(c["topo"]["tabs"]["consultanta"]), "TAB_CAZURI": e(c["topo"]["tabs"]["cazuri"]),
            "TAB_PROIECTE": e(c["topo"]["tabs"]["proiecte"]), "TAB_AUTOMATIZARI": e(c["topo"]["tabs"]["automatizari"]),
            "VISTA_CONSULTANTA": vista_consultanta(c, casos, lang, wa), "VISTA_CAZURI": vista_cazuri(c, casos, lang, digitos),
            "VISTA_AUTOMATIZARI": vista_automatizari(c, digitos, icones, casos, vista_servicii(c, portfolio, lang)),
            "VISTA_PROIECTE": vista_proiecte(c, portfolio, lang, digitos),
            "CONTACT": contacto(c, d, wa, tel_legivel, digitos, cfg["com_site"]), "RODAPE": rodape(c, lang), "INTRO": intro(c),
            "WA_URL": e(wa), "ICONE_CHAT": I["chat"], "CTA": e(c["contact"]["cta"]),
            "CONSENT_ROTULO": e(k["rotulo"]), "CONSENT_TEXTO": e(k["texto"]), "CONSENT_SIM": e(k["sim"]),
            "CONSENT_NAO": e(k["nao"]), "CONSENT_LINK": e(k["link"]), "URL_PRIVACIDADE": e(cfg["privacidade"]),
        }
        pagina = montar(src, valores)
        paginas[lang] = pagina
        pasta = os.path.join(DIST, cfg["pasta"])
        os.makedirs(pasta, exist_ok=True)
        open(os.path.join(pasta, "index.html"), "w", encoding="utf-8").write(pagina)

    # 404 e privacidade em cada língua, com o estilo da página
    estilo = re.search(r"<style>.*?</style>", paginas["pt"], re.S).group(0)
    for lang, c in linguas.items():
        cfg = LINGUAS[lang]
        extras[f"{cfg['pasta'] + '/' if cfg['pasta'] else ''}404.html"] = pagina_404(c, estilo, lang)
        extras[cfg["privacidade"].lstrip("/")] = pagina_privacidade(c, estilo, lang, d["email"])
    for nome, h in extras.items():
        open(os.path.join(DIST, nome), "w", encoding="utf-8").write(h)

    # Netlify. Um só projeto com os dois domínios: pachecost.com (principal) e ro.pachecost.com (alias).
    caminho = d.get("caminho_qr", "c").strip("/").lower()
    destino_qr = d.get("destino_qr", "/?origem=cartao").strip()
    curtos = {k: v for k, v in d.get("enderecos_curtos", {}).items() if not k.startswith("_") and v}
    red = ["# Gerado por gerar.py a partir de marca/dados.json — não editar à mão.",
           f"# 1) QR do cartão (impresso: HTTPS://{dominio.upper()}/{caminho.upper()}). Fica SEMPRE em primeiro lugar.",
           f"/{caminho}    {destino_qr}    302", f"/{caminho.upper()}    {destino_qr}    302",
           f"# 2) {dominio} abre a versão romena, guardada em /ro/. O resto dos ficheiros é partilhado.",
           f"https://{dominio}/              /ro/index.html    200!",
           f"https://{dominio}/index.html    /ro/index.html    200!",
           "# 3) cada língua no seu endereço",
           f"/ro        https://{dominio}/    301!", f"/ro/*      https://{dominio}/    301!",
           f"https://{dominio}/en      https://{principal}/en/    301!",
           f"https://{dominio}/en/*    https://{principal}/en/:splat    301!",
           f"/pt        https://{principal}/    301!", f"/pt/*      https://{principal}/    301!",
           "# 4) endereços curtos (marca/dados.json → enderecos_curtos)"]
    for slug, dest in sorted(curtos.items()):
        red.append(f"/{re.sub(r'[^a-z0-9-]', '', slug.lower())}    {dest}    302")
    red += ["# 5) página 404 na língua de cada endereço (a portuguesa é a 404.html da raiz)",
            f"https://{dominio}/*    /ro/404.html    404", "/en/*    /en/404.html    404"]
    open(os.path.join(DIST, "_redirects"), "w", encoding="utf-8").write("\n".join(red) + "\n")
    # Cabeçalhos em _headers (e não no netlify.toml): o Netlify lê _headers e _redirects também quando o zip é
    # arrastado à mão; o netlify.toml só é garantido em builds. Um sítio só, para não se duplicarem.
    open(os.path.join(DIST, "_headers"), "w", encoding="utf-8").write(
        "# Gerado por gerar.py — não editar à mão.\n/*\n  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n"
        "  Permissions-Policy: geolocation=(), microphone=(), camera=()\n"
        "/p/*\n  X-Robots-Tag: noindex, nofollow\n/media/*\n  Cache-Control: public, max-age=604800\n")
    open(os.path.join(DIST, "netlify.toml"), "w", encoding="utf-8").write(
        '# Gerado por gerar.py. Redirecionamentos em _redirects e cabeçalhos em _headers.\n[build]\npublish = "."\n')
    open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8").write(
        f"# {principal} e {dominio}\nUser-agent: *\nAllow: /\nDisallow: /p/\n\n"
        "# ferramentas de SEO que só servem para inflacionar estatísticas\n"
        + "".join(f"User-agent: {b}\nDisallow: /\n" for b in ("AhrefsBot", "SemrushBot", "MJ12bot", "DotBot", "BLEXBot",
                                                              "DataForSeoBot", "PetalBot", "Bytespider"))
        + f"\nSitemap: https://{principal}/sitemap.xml\n")
    urls = [(f"https://{principal}/", "1.0"), (f"https://{principal}/en/", "0.8"),
            (f"https://{principal}/privacidade.html", "0.2"), (f"https://{principal}/privacy.html", "0.2")]
    open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><priority>{pr}</priority></url>\n" for u, pr in urls) + "</urlset>\n")
    # ficheiros do site anterior que podem estar ligados de fora (partilhas, pesquisas)
    for f in ("favicon.svg", "logo.svg"):
        antigo = os.path.join(SITES, "pachecost-com", f)
        if os.path.exists(antigo):
            shutil.copy(antigo, os.path.join(DIST, f))

    n = copiar_sites(portfolio, linguas)
    for lang, c in linguas.items():
        og_png(fontes, c["og"], os.path.join(DIST, "media", f"og-{lang}.png"))
    # os três carros da intro (fotografias recortadas, frente à direita, WebP com transparência)
    for i in (1, 2, 3):
        carro = os.path.join(AQUI, "media", f"intro-{i}.webp")
        if not os.path.exists(carro):
            raise SystemExit(f"falta media/intro-{i}.webp (os três carros da intro: ver LEIA-ME.md)")
        shutil.copy(carro, os.path.join(DIST, "media", f"intro-{i}.webp"))

    # cópia para o git (e para abrir na app): tudo menos as cópias dos sites e os media
    antiga_pt = os.path.join(AQUI, "pt")
    if os.path.isdir(antiga_pt):
        shutil.rmtree(antiga_pt)  # a versão portuguesa passou para a raiz
    for raiz, _, fichs in os.walk(DIST):
        rel = os.path.relpath(raiz, DIST)
        if rel.split(os.sep)[0] in ("p", "media"):
            continue
        for f in fichs:
            os.makedirs(os.path.join(AQUI, rel), exist_ok=True)
            shutil.copy(os.path.join(raiz, f), os.path.join(AQUI, rel, f))

    print("\nVALIDAÇÃO")
    for lang in LINGUAS:
        nome = (LINGUAS[lang]["pasta"] + "/" if LINGUAS[lang]["pasta"] else "") + "index.html"
        ok &= validar(f"{nome} ({lang})", paginas[lang])
    for nome, h in extras.items():
        ok &= validar(nome, h)
    print(f"  páginas: {len(paginas['pt'].encode()) / 1024:.0f} KB cada · {n} site(s) copiado(s) para /p/ (uma página por língua)")
    regras = open(os.path.join(DIST, "_redirects"), encoding="utf-8").read().splitlines()
    ativas = [r.split() for r in regras if r.strip() and not r.startswith("#")]
    qr_ok = all(any(r[:3] == [f"/{x}", destino_qr, "302"] for r in ativas) for x in (caminho, caminho.upper()))
    qr_primeiro = [r[0].lower() for r in ativas[:2]] == [f"/{caminho}", f"/{caminho}"]
    ro_ok = [f"https://{dominio}/", "/ro/index.html", "200!"] in ativas
    cab_ok = "X-Robots-Tag: noindex" in open(os.path.join(DIST, "_headers"), encoding="utf-8").read()
    ok &= qr_ok and qr_primeiro and ro_ok and cab_ok
    print(f"  {'✓' if qr_ok and qr_primeiro else '✗'} _redirects: /{caminho} e /{caminho.upper()} → {destino_qr} (o QR impresso), em primeiro"
          f" · {'✓' if ro_ok else '✗'} {dominio} → versão romena · {'✓' if cab_ok else '✗'} _headers: /p/* com noindex")

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
