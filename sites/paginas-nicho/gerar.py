#!/usr/bin/env python3
"""Páginas por nicho e cidade (agente 5): «Site pentru frizerii în Iași», «Sites para restaurantes no Algarve».

Lê a lista DEMOS de sites/demos-pachecost/gerar.py e o HTML de cada demo, arruma as demos por nicho
(nichos.py) e escreve páginas estáticas indexáveis:

  <out>/site-uri/<nicho>-iasi/index.html   (RO, servidas em ro.pachecost.com)
  <out>/site-uri/index.html                (índice RO)
  <out>/sites/<nicho>-algarve/index.html   (PT, servidas em pachecost.com)
  <out>/sites/index.html                   (índice PT)
  <out>/sitemap-nichos.xml

  python3 gerar.py --out <pasta>                 (normal: chamado pelo gerar.py das demos)
  python3 gerar.py --out <pasta> --embutir       (pré-visualização: imagens dentro do HTML)

Cada demo nova que entra em DEMOS cai sozinha no seu nicho; uma página nova nasce quando um nicho
chega a MINIMO demos. Sem dependências além do Python (o --embutir usa o Pillow).
"""
import argparse, base64, datetime, html, io, json, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import nichos as N  # noqa: E402

e = lambda s: html.escape(str(s), quote=True)


def sem_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn") \
        .replace("ș", "s").replace("ț", "t")


def ler_demos(demos_py):
    src = open(demos_py, encoding="utf-8").read()
    m = re.search(r"^DEMOS = (\[.*?^\])", src, re.S | re.M)
    return [t for t in eval(m.group(1), {})]  # lista literal de tuplos (curto, pasta)


def ler_ld(h):
    for bloco in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            d = json.loads(bloco)
        except ValueError:
            continue
        for o in (d.get("@graph", [d]) if isinstance(d, dict) else d):
            if isinstance(o, dict) and ("address" in o or o.get("@type") not in (None, "WebSite", "BreadcrumbList", "FAQPage")):
                return o
    return {}


def imagem(h):
    m = re.search(r'property="og:image" content="(media/[^"]+\.(?:webp|jpe?g|png))"', h) or \
        re.search(r'<img[^>]+src="(media/[^"]+\.(?:webp|jpe?g|png))"', h)
    return m.group(1) if m else ""


def luminancia(hexa):
    try:
        r, g, b = (int(hexa.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return 0
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def nicho_de(curto, titulo, tipo):
    if curto in N.FIXOS:
        return N.FIXOS[curto]
    t = sem_acentos(titulo)
    for palavra, nicho in N.PALAVRAS:
        if re.search(r"\b" + re.escape(palavra), t):
            return nicho
    return N.TIPOS.get(tipo if isinstance(tipo, str) else (tipo or [""])[0])


def carregar(sites, demos):
    lista = []
    for curto, pasta in demos:
        p = os.path.join(sites, pasta, "index.html")
        if not os.path.exists(p) or curto in N.EXCLUIR:
            continue
        h = open(p, encoding="utf-8").read()
        titulo = html.unescape(re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", h, re.S).group(1))).strip()
        partes = [x.strip() for x in titulo.split("·")]
        ld = ler_ld(h)
        end = ld.get("address") or {}
        if isinstance(end, list):
            end = end[0] if end else {}
        desc = partes[1] if len(partes) > 1 else ""
        if re.search(r"\d", desc) or desc in ("Iași", end.get("addressLocality")):
            desc = ""  # o título repete a morada, que já vai na placa
        rua = re.sub(r"\s*\(.*?\)", "", (end.get("streetAddress") or "")).strip()
        rua = ", ".join(rua.split(", ")[:2])
        lingua = (re.search(r'<html[^>]*lang="([a-zA-Z]+)', h) or [None, ""])[1].lower()
        cor = (re.search(r'name="theme-color" content="(#[0-9A-Fa-f]{6})"', h) or [None, "#1D1A17"])[1]
        lista.append({
            "curto": curto, "pasta": pasta, "nome": html.unescape(ld.get("name") or partes[0]),
            "desc": desc, "rua": rua, "local": (end.get("addressLocality") or "").strip(),
            "lingua": lingua, "cidade": "iasi" if lingua == "ro" else "algarve",
            "tem_pt": os.path.exists(os.path.join(sites, pasta, "pt.html")),
            "nicho": nicho_de(curto, titulo, ld.get("@type")), "cor": cor, "img": imagem(h),
        })
    return lista


# ─────────────────────────── HTML ───────────────────────────
FONTES = ("https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;600&"
          "family=Space+Mono:wght@400;700&display=swap")

CSS = r"""
:root{--carvao:#141210;--carvao-2:#1D1A17;--carvao-3:#26221E;--osso:#EFEAE3;--osso-2:#A5A19B;--laranja:#E8622C;
--linha:rgba(239,234,227,.16);--display:"Archivo Black",system-ui,sans-serif;
--texto:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--mono:"Space Mono",ui-monospace,Menlo,monospace;
--gutter:clamp(1rem,5vw,3rem);--max:72rem;--sair:cubic-bezier(.16,1,.3,1);
--placa:#1F4596;--placa-t:#fff;--placa-b:#fff}
:root[lang="pt-PT"]{--placa:#F7F5EF;--placa-t:#1B3F94;--placa-b:#1B3F94}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%;background:var(--carvao);scroll-behavior:smooth}
body{margin:0;background:var(--carvao);color:var(--osso);font:400 1.0625rem/1.6 var(--texto);-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit}h1,h2,h3,p,ol,ul,figure{margin:0}ol,ul{padding:0;list-style:none}
:focus-visible{outline:3px solid var(--laranja);outline-offset:3px;border-radius:.4rem}
.saltar{position:absolute;left:1rem;top:-5rem;z-index:50;background:var(--osso);color:var(--carvao);padding:.8rem 1.1rem;border-radius:.5rem;font-weight:600;text-decoration:none}
.saltar:focus{top:1rem}
.env{max-width:var(--max);margin-inline:auto;padding-inline:max(var(--gutter),env(safe-area-inset-left))}
.mono{font:700 .75rem/1.3 var(--mono);letter-spacing:.16em;text-transform:uppercase}

/* topo */
.topo{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-block:.9rem}
.marca{display:inline-flex;align-items:center;gap:.7rem;min-height:2.75rem;text-decoration:none;font:700 .8125rem/1 var(--mono);letter-spacing:.24em;text-transform:uppercase;white-space:nowrap}
.marca i{width:.7rem;height:.7rem;border-radius:50%;background:var(--laranja)}
.topo nav{display:flex;align-items:center;gap:.4rem}
.topo nav a{min-height:2.75rem;display:inline-flex;align-items:center;padding-inline:.8rem;border-radius:2rem;text-decoration:none;font:700 .75rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--osso-2);transition:color .2s,background-color .2s}
.topo nav a:hover{color:var(--osso);background:var(--carvao-2)}
.topo nav a.cta-mini{color:var(--carvao);background:var(--osso)}
.topo nav a.cta-mini:hover{background:var(--laranja);color:var(--carvao)}
@media (max-width:34rem){.topo nav a.so-largo{display:none}.marca{letter-spacing:.16em}}

/* migalhas */
.migalhas{display:flex;flex-wrap:wrap;gap:.2rem .5rem;color:var(--osso-2);padding-top:.5rem}
.migalhas a{text-decoration:none}.migalhas a:hover{color:var(--osso);text-decoration:underline}
.migalhas li+li::before{content:"/";margin-right:.5rem;opacity:.5}

/* herói: texto + leque de telemóveis */
.heroi{display:grid;gap:2.5rem;padding-block:clamp(2rem,6vw,4.5rem) clamp(3rem,7vw,5rem);align-items:center}
@media (min-width:56rem){.heroi{grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr)}}
.eyebrow{color:var(--laranja);margin-bottom:1.1rem;display:flex;align-items:center;gap:.6rem}
.eyebrow::before{content:"";width:1.6rem;height:2px;background:currentColor}
h1{font:400 clamp(2.3rem,6.4vw,4.6rem)/1.02 var(--display);letter-spacing:-.01em;text-wrap:balance}
h1 em{font-style:normal;color:var(--laranja)}
.lead{margin-top:1.4rem;max-width:36rem;font-size:clamp(1.0625rem,1.6vw,1.2rem);color:#D8D3CC}
.conta{margin-top:1.6rem;display:flex;align-items:center;gap:.7rem;color:var(--osso)}
.conta b{font:400 1.9rem/1 var(--display);color:var(--laranja);letter-spacing:0}
.botoes{margin-top:2rem;display:flex;flex-wrap:wrap;gap:.8rem}
.btn{min-height:3.25rem;display:inline-flex;align-items:center;gap:.6rem;padding:0 1.5rem;border-radius:3rem;font:600 1rem/1 var(--texto);text-decoration:none;transition:transform .25s var(--sair),background-color .2s,color .2s,border-color .2s}
.btn-p{background:var(--laranja);color:var(--carvao)}
.btn-p:hover{background:var(--osso);transform:translateY(-2px)}
.btn-s{border:1.5px solid rgba(239,234,227,.45);color:var(--osso)}
.btn-s:hover{border-color:var(--osso);transform:translateY(-2px)}
.btn svg{width:1.1rem;height:1.1rem;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.leque{position:relative;height:clamp(19rem,52vw,27rem);display:grid;place-items:center}
.leque .tel{position:absolute;width:clamp(9.5rem,25vw,13.5rem)}
.leque .tel:nth-child(1){transform:translateX(-58%) rotate(-9deg) scale(.9);z-index:1}
.leque .tel:nth-child(2){transform:translateY(-3%);z-index:3}
.leque .tel:nth-child(3){transform:translateX(58%) rotate(9deg) scale(.9);z-index:2}
.leque .tel:only-child{transform:none}

/* telemóvel (a peça comum ao herói e à rua) */
.tel{display:block;aspect-ratio:9/18.5;border-radius:2rem;padding:.42rem;background:#0B0A09;
  box-shadow:0 0 0 1px rgba(239,234,227,.14),0 1.8rem 3rem -1.2rem rgba(0,0,0,.75);text-decoration:none}
.ecra{display:block;position:relative;height:100%;border-radius:1.62rem;overflow:hidden;background:var(--cor,#1D1A17)}
.ecra::before{content:"";position:absolute;z-index:2;top:.5rem;left:50%;width:30%;height:.95rem;transform:translateX(-50%);border-radius:1rem;background:#0B0A09}
.ecra img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ecra::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,var(--cor,#1D1A17) 8%,color-mix(in srgb,var(--cor,#1D1A17) 55%,transparent) 34%,transparent 62%)}
.ecra .n{display:block;position:absolute;z-index:3;left:.9rem;right:.9rem;bottom:1rem;color:var(--tn,#fff);font:400 clamp(1rem,2.4vw,1.25rem)/1.08 var(--display);text-wrap:balance}
.ecra .n small{display:block;margin-top:.4rem;font:700 .625rem/1.3 var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.85}

/* a rua */
.rua{background:var(--carvao-2);border-block:1px solid var(--linha);padding-block:clamp(3rem,7vw,5rem) 0;overflow:hidden}
.rua h2,.bloco h2{font:400 clamp(1.7rem,4vw,2.6rem)/1.08 var(--display);text-wrap:balance}
.rua .intro{display:grid;gap:1rem}.rua .intro p{max-width:40rem}
.rua .intro p{color:var(--osso-2)}
.passeio{margin-top:2.5rem;display:grid;grid-auto-flow:column;grid-auto-columns:clamp(12.5rem,62vw,15rem);gap:clamp(1rem,3vw,1.75rem);
  overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-inline:max(var(--gutter),env(safe-area-inset-left));padding:1rem max(var(--gutter),env(safe-area-inset-left)) 0;scrollbar-width:thin;scrollbar-color:var(--carvao-3) transparent;
  max-width:calc(var(--max) + 2 * var(--gutter));margin-inline:auto}
@media (min-width:64rem){.passeio{grid-auto-flow:row;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr));overflow:visible}}
.casa{scroll-snap-align:start;display:grid;gap:1rem;justify-items:center;padding-bottom:2.2rem;position:relative}
.casa::after{content:"";position:absolute;left:-1rem;right:-1rem;bottom:0;height:.7rem;
  background:repeating-linear-gradient(90deg,var(--carvao-3) 0 2.4rem,#2E2924 2.4rem 2.55rem);border-top:2px solid #3A342E}
.casa .tel{width:100%;transition:transform .45s var(--sair),box-shadow .45s var(--sair)}
.casa .tel:hover{transform:translateY(-.6rem) rotate(-1deg);box-shadow:0 0 0 1px rgba(232,98,44,.6),0 2.4rem 3.4rem -1.2rem rgba(0,0,0,.85)}
.placa{width:92%;padding:.55rem .8rem .6rem;border-radius:.35rem;background:var(--placa);color:var(--placa-t);text-align:center;
  box-shadow:inset 0 0 0 2px var(--placa),inset 0 0 0 3.5px var(--placa-b),0 .4rem .8rem -.3rem rgba(0,0,0,.6)}
.placa b{display:block;font:700 .8125rem/1.25 var(--texto);letter-spacing:.02em;text-transform:uppercase}
.placa span{display:block;margin-top:.2rem;font:400 .75rem/1.3 var(--texto);opacity:.9}
.casa .fora{position:absolute;top:0;left:50%;transform:translate(-50%,-55%);z-index:4;white-space:nowrap;padding:.35rem .7rem;border-radius:2rem;background:var(--osso);color:var(--carvao)}

/* blocos */
.bloco{padding-block:clamp(3rem,7vw,5rem)}
.ce{margin-top:2rem;display:grid;gap:1px;background:var(--linha);border:1px solid var(--linha);border-radius:1.2rem;overflow:hidden}
@media (min-width:40rem){.ce{grid-template-columns:1fr 1fr}}
.ce li{background:var(--carvao);padding:1.5rem 1.4rem 1.6rem}
.ce .mono{color:var(--laranja);display:block;margin-bottom:.6rem}
.ce p{color:#D8D3CC}
.pasos{margin-top:2rem;display:grid;gap:1.4rem;counter-reset:p}
@media (min-width:52rem){.pasos{grid-template-columns:repeat(3,1fr)}}
.pasos li{counter-increment:p;border-top:2px solid var(--osso);padding-top:1rem}
.pasos li::before{content:counter(p);display:block;font:400 2.4rem/1 var(--display);color:var(--laranja);margin-bottom:.7rem}
.pasos b{display:block;font:600 1.125rem/1.3 var(--texto);margin-bottom:.35rem}
.pasos p{color:var(--osso-2)}
.faq{margin-top:1.6rem;max-width:48rem;border-top:1px solid var(--linha)}
.faq details{border-bottom:1px solid var(--linha)}
.faq summary{min-height:3.5rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-block:1rem;cursor:pointer;list-style:none;font:600 1.0625rem/1.35 var(--texto)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font:400 1.5rem/1 var(--display);color:var(--laranja);transition:transform .3s var(--sair)}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq p{padding-bottom:1.2rem;color:#D8D3CC;max-width:42rem}
.outros{margin-top:1.4rem;display:flex;flex-wrap:wrap;gap:.6rem}
.outros a{min-height:2.75rem;display:inline-flex;align-items:center;gap:.5rem;padding:0 1rem;border:1px solid var(--linha);border-radius:2rem;text-decoration:none;font-weight:600;font-size:.9375rem;transition:border-color .2s,background-color .2s}
.outros a:hover{border-color:var(--laranja);background:var(--carvao-2)}
.outros small{font:700 .6875rem/1 var(--mono);color:var(--osso-2)}

/* fim */
.final{background:var(--laranja);color:var(--carvao);padding-block:clamp(3rem,8vw,5.5rem)}
.final h2{font:400 clamp(2rem,5.5vw,3.6rem)/1.02 var(--display);max-width:44rem;text-wrap:balance}
.final p{margin-top:1rem;font-size:1.125rem;max-width:34rem}
.final .botoes .btn-p{background:var(--carvao);color:var(--osso)}
.final .botoes .btn-p:hover{background:#000}
.final .botoes .btn-s{border-color:var(--carvao);color:var(--carvao)}
.final .botoes .btn-s:hover{background:rgba(20,18,16,.08)}
.rodape{padding-block:2rem calc(2rem + env(safe-area-inset-bottom));color:var(--osso-2);font-size:.875rem;display:flex;flex-wrap:wrap;gap:.6rem 1.4rem;align-items:center}
.rodape a{text-decoration:none;min-height:2.75rem;display:inline-flex;align-items:center}.rodape a:hover{color:var(--osso);text-decoration:underline}
.rodape p{margin-right:auto}

/* índice */
.grelha{margin-top:2.5rem;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,17rem),1fr))}
.area{display:grid;grid-template-columns:4.2rem 1fr;gap:1rem;align-items:center;padding:1rem;border:1px solid var(--linha);border-radius:1.2rem;text-decoration:none;transition:border-color .25s,transform .35s var(--sair),background-color .25s}
.area:hover{border-color:var(--laranja);transform:translateY(-3px);background:var(--carvao-2)}
.area .tel{width:4.2rem;border-radius:.9rem;padding:.2rem;box-shadow:0 0 0 1px rgba(239,234,227,.14)}
.area .ecra{border-radius:.72rem}.area .ecra::before{display:none}.area .ecra::after{background:none}
.area b{display:block;font:400 1.15rem/1.15 var(--display)}
.area small{display:block;margin-top:.35rem;color:var(--osso-2)}

/* movimento: só com JavaScript e sem «reduzir movimento» */
@media (prefers-reduced-motion:no-preference){
  .js .entra{opacity:0;transform:translateY(1.2rem);transition:opacity .8s var(--sair),transform .8s var(--sair);transition-delay:calc(var(--i,0) * 90ms)}
  .js .pronto .entra,.js .entra.visto{opacity:1;transform:none}
  .js .leque .tel{transition:transform 1.1s var(--sair) .35s,opacity .6s ease .35s}
  .js .heroi:not(.pronto) .leque .tel{transform:translateY(8%) rotate(0) scale(.92);opacity:0}
}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}.btn,.casa .tel,.area{transition:none}}
"""

SVG_SETA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
SVG_WA = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.6a8.4 8.4 0 0 1-12.4 7.4L3.5 20.5l1.6-4.4'
          'A8.4 8.4 0 1 1 20.5 11.6z"/><path d="M9 8.6c.2 2.9 2.6 5.6 6.2 6.4l1-1.4-1.9-.9-.8.8c-1.2-.5-2.3-1.6-2.8-2.8l.8-.8-.9-1.9z"/></svg>')


def plural(n, formas):
    return formas[0 if n == 1 else 1]


def url_img(d, embutir, sites):
    if not d["img"]:
        return ""
    if not embutir:
        return f"/demo/{d['curto']}/{d['img']}"
    from PIL import Image
    im = Image.open(os.path.join(sites, d["pasta"], d["img"])).convert("RGB")
    im.thumbnail((420, 900))
    b = io.BytesIO()
    im.save(b, "WEBP", quality=58)
    return "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()


def telemovel(d, cid, ui, embutir, sites, com_nome=True, classe="tel", gc=""):
    fora = d["cidade"] != cid
    href = f"/demo/{d['curto']}/" + ("pt.html" if fora else "")
    tn = "#141210" if luminancia(d["cor"]) > .45 else "#fff"
    src = url_img(d, embutir, sites)
    img = (f'<img src="{e(src)}" alt="" loading="lazy" decoding="async" onerror="this.remove()">' if src else "")
    nome = (f'<span class="n">{e(d["nome"])}<small>{e(d["desc"])}</small></span>' if com_nome else "")
    return (f'<a class="{classe}" href="{e(href)}" style="--cor:{d["cor"]};--tn:{tn}" data-gc="{e(gc)}{e(d["curto"])}"'
            f' aria-label="{e(ui["deschide"])}: {e(d["nome"])}"><span class="ecra">{img}{nome}</span></a>')


def cabeca(ui, cid, titulo, desc, url, ld, pixel_id):
    return f"""<!DOCTYPE html>
<html lang="{ui['html']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#141210">
<meta property="og:type" content="website">
<meta property="og:locale" content="{ui['og']}">
<meta property="og:site_name" content="Pacheco Studios">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="https://pachecost.com/media/og.png">
<link rel="icon" href="https://pachecost.com/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTES}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")}</script>
<script>document.documentElement.classList.add('js');window.goatcounter={{path:function(p){{return location.host+p}}}};</script>
<script data-goatcounter="https://pachecost.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
<style>{CSS}</style>
</head>
<body>
<a class="saltar" href="#conteudo">{e(ui['skip'])}</a>
"""


def topo(ui, cfg, diag):
    return f"""<header class="env topo">
  <a class="marca" href="{cfg['host']}/"><i aria-hidden="true"></i>Pacheco Studios</a>
  <nav aria-label="{e(ui['toate'])}"><a class="so-largo" href="{cfg['base']}">{e(ui['toate'])}</a><a class="cta-mini" href="{e(diag)}" data-gc="diagnostico-topo">{e(ui['cta_scurt'])}</a></nav>
</header>"""


def rodape(ui):
    pv, ck = ui["privacidade"], ui["cookies"]
    return f"""<footer class="env rodape">
  <p>© {datetime.date.today().year} Pacheco Studios · {e(ui['rodape'])}</p>
  <a href="{pv[1]}">{e(pv[0])}</a><a href="{ck[1]}">{e(ck[0])}</a>
  <a href="https://www.livroreclamacoes.pt/inicio/" rel="noopener">{e(ui['reclamacoes'])}</a>
</footer>"""


def scripts(pagina, pixel_id):
    pix = ""
    if pixel_id:
        pix = ("try{var r=localStorage.getItem('ps-consentimento')}catch(x){}if(r!=='nao'&&!navigator.globalPrivacyControl){"
               "!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};"
               "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;"
               "s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
               f"fbq('init','{pixel_id}');fbq('track','PageView');}}")
    return f"""<script>
(function(){{
  var h=document.querySelector('.heroi');
  requestAnimationFrame(function(){{requestAnimationFrame(function(){{if(h)h.classList.add('pronto')}})}});
  var vs=document.querySelectorAll('.entra:not(.heroi .entra)');
  if('IntersectionObserver' in window){{var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('visto');io.unobserve(x.target)}}}})}},{{rootMargin:'0px 0px -8% 0px'}});vs.forEach(function(v){{io.observe(v)}})}}
  else vs.forEach(function(v){{v.classList.add('visto')}});
  function gc(o){{try{{if(window.goatcounter&&window.goatcounter.count)window.goatcounter.count(o)}}catch(x){{}}}}
  document.addEventListener('click',function(ev){{var a=ev.target.closest&&ev.target.closest('[data-gc]');if(!a)return;
    var k=a.getAttribute('data-gc');gc({{path:'nisa/{pagina}/'+k,title:'nicho {pagina}: '+k,event:true}});
    if(window.fbq&&/^diagnostico|^whatsapp/.test(k))try{{fbq('track','Contact',{{canal:k}})}}catch(x){{}}}},{{passive:true}});
  {pix}
}})();
</script>
</body>
</html>
"""


def pagina_nicho(cid, cfg, ui, chave, txt, demos, outros, embutir, sites, pixel_id):  # noqa: C901
    slug = f"{txt['slug']}-{cid}"
    url = f"{cfg['host']}{cfg['base']}{slug}/"
    diag = cfg["diag"].format(pagina=slug)
    n = len(demos)
    fmt = dict(plural=txt["plural"], em=cfg["em"], de=cfg["de"], oras=cfg["nome"], sing=txt["sing"], n=n)
    titulo = ui["title"].format(**fmt)
    if len(titulo) > 70:
        titulo = titulo.replace(" · Pacheco Studios", "")
    h1 = ("Site pentru" if ui["html"] == "ro" else "Sites para") + f" <em>{e(txt['plural'])}</em> {e(cfg['em'])}"
    nomes = ", ".join(d["nome"] for d in demos[:3])
    desc = f"{txt['lead'].split('. ')[-1].rstrip('.')}. " + (
        f"Vezi {n} site-uri făcute deja pentru {txt['plural']} {cfg['de']}: {nomes}." if ui["html"] == "ro"
        else f"Vê {n} sites já feitos para {txt['plural']}: {nomes}.")
    wa = "https://wa.me/{}?text={}".format(cfg["whatsapp"], __import__("urllib.parse").parse.quote(ui["wa_msg"].format(**fmt)))
    faqs = [txt["faq"]] + ui["faq"]
    lista_url = cfg["host"] + cfg["base"]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url, "url": url, "name": titulo, "description": desc, "inLanguage": ui["html"],
         "isPartOf": {"@type": "WebSite", "name": "Pacheco Studios", "url": cfg["host"] + "/"},
         "about": {"@type": "Service", "name": re.sub("<[^>]+>", "", h1), "serviceType": "Web design",
                   "areaServed": {"@type": "Place", "name": cfg["nome"]},
                   "provider": {"@type": "ProfessionalService", "name": "Pacheco Studios", "url": "https://pachecost.com/"}},
         "mainEntity": {"@type": "ItemList", "numberOfItems": n, "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": d["nome"],
              "url": "https://pachecost.com/demo/" + d["curto"] + "/" + ("pt.html" if d["cidade"] != cid else "")}
             for i, d in enumerate(demos)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Pacheco Studios", "item": cfg["host"] + "/"},
            {"@type": "ListItem", "position": 2, "name": ui["site_uri"] + " · " + cfg["nome"], "item": lista_url},
            {"@type": "ListItem", "position": 3, "name": txt["curto"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}}
                                            for q, r in faqs]}]}
    leque = "".join(telemovel(d, cid, ui, embutir, sites, com_nome=False, gc="heroi-") for d in demos[:3])
    casas = []
    for i, d in enumerate(demos):
        fora = (f'<span class="fora mono">{e(ui["afara"].format(oras=N.CIDADES[d["cidade"]]["nome"]))}</span>'
                if d["cidade"] != cid else "")
        rua = d["rua"] or d["local"]
        sub = d["local"] if d["rua"] and d["local"] and d["local"] not in d["rua"] and d["local"] != cfg["nome"] else ""
        casas.append(f'<li class="casa entra" style="--i:{i % 6}">{fora}{telemovel(d, cid, ui, embutir, sites, gc="demo-")}'
                     f'<p class="placa"><b>{e(rua)}</b>{f"<span>{e(sub)}</span>" if sub else ""}</p></li>')
    ce = "".join(f'<li class="entra" style="--i:{i}"><span class="mono">{e(a)}</span><p>{e(b)}</p></li>' for i, (a, b) in enumerate(txt["ce"]))
    pasos = "".join(f'<li class="entra" style="--i:{i}"><b>{e(a)}</b><p>{e(b)}</p></li>' for i, (a, b) in enumerate(ui["pasi"]))
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in faqs)
    out = "".join(f'<a href="{cfg["base"]}{o["slug"]}/">{e(o["curto"])} <small>{o["n"]}</small></a>' for o in outros)
    conta = plural(n, ui["numar"]).format(**fmt)
    return slug, cabeca(ui, cid, titulo, desc, url, ld, pixel_id) + topo(ui, cfg, diag) + f"""
<main id="conteudo">
<nav class="env" aria-label="Breadcrumb"><ol class="migalhas mono"><li><a href="{cfg['host']}/">Pacheco Studios</a></li><li><a href="{cfg['base']}">{e(ui['site_uri'])} · {e(cfg['nome'])}</a></li><li aria-current="page">{e(txt['curto'])}</li></ol></nav>
<section class="env heroi">
  <div>
    <p class="eyebrow mono entra" style="--i:0">{e(cfg['nome'])} · {e(txt['curto'])}</p>
    <h1 class="entra" style="--i:1">{h1}</h1>
    <p class="lead entra" style="--i:2">{e(txt['lead'])}</p>
    <p class="conta mono entra" style="--i:3"><b>{n}</b>{e(conta)}</p>
    <div class="botoes entra" style="--i:4">
      <a class="btn btn-p" href="{e(diag)}" data-gc="diagnostico-heroi">{e(ui['cta'])} {SVG_SETA}</a>
      <a class="btn btn-s" href="#rua">{e(ui['vezi'])}</a>
    </div>
  </div>
  <div class="leque" aria-hidden="true">{leque}</div>
</section>
<section class="rua" id="rua" aria-labelledby="rua-t">
  <div class="env intro"><h2 id="rua-t">{e(ui['strada_t'])}</h2><p>{e(ui['strada_p'].format(**fmt))}</p></div>
  <ul class="passeio">{''.join(casas)}</ul>
</section>
<section class="env bloco" aria-labelledby="ce-t">
  <h2 id="ce-t">{e(ui['ce_t'].format(**fmt))}</h2>
  <ul class="ce">{ce}</ul>
</section>
<section class="env bloco" aria-labelledby="pasi-t" style="padding-top:0">
  <h2 id="pasi-t">{e(ui['pasi_t'])}</h2>
  <ol class="pasos">{pasos}</ol>
</section>
<section class="env bloco" aria-labelledby="faq-t" style="padding-top:0">
  <h2 id="faq-t">{e(ui['faq_t'])}</h2>
  <div class="faq">{faq}</div>
</section>
{f'<section class="env bloco" aria-labelledby="alte-t" style="padding-top:0"><h2 id="alte-t">{e(ui["alte_t"].format(**fmt))}</h2><nav class="outros" aria-labelledby="alte-t">{out}</nav></section>' if outros else ''}
<section class="final">
  <div class="env">
    <h2>{e(ui['final_t'])}</h2>
    <p>{e(ui['final_p'])}</p>
    <div class="botoes"><a class="btn btn-p" href="{e(diag)}" data-gc="diagnostico-fim">{e(ui['cta'])} {SVG_SETA}</a>
    <a class="btn btn-s" href="{e(wa)}" data-gc="whatsapp" rel="noopener">{SVG_WA} {e(ui['whatsapp'])}</a></div>
  </div>
</section>
</main>
{rodape(ui)}
{scripts(slug, pixel_id)}"""


def pagina_indice(cid, cfg, ui, paginas, embutir, sites, pixel_id):
    url = cfg["host"] + cfg["base"]
    diag = cfg["diag"].format(pagina="indice-" + cid)
    total = sum(p["n_locais"] for p in paginas)
    fmt = dict(de=cfg["de"], em=cfg["em"], n=total, lista=", ".join(p["curto"].lower() for p in paginas))
    titulo, desc = ui["indice_title"].format(**fmt), ui["indice_desc"].format(**fmt)
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "url": url, "name": titulo, "description": desc,
          "inLanguage": ui["html"], "hasPart": [{"@type": "WebPage", "name": p["curto"], "url": url + p["slug"] + "/"} for p in paginas]}
    cards = "".join(
        f'<a class="area entra" style="--i:{i % 6}" href="{cfg["base"]}{p["slug"]}/" data-gc="area-{p["slug"]}">'
        f'{telemovel(p["capa"], cid, ui, embutir, sites, com_nome=False, classe="tel").replace("<a ", "<span ").replace("</a>", "</span>").replace(" href=", " data-h=").replace(' data-gc="', ' data-x="')}'
        f'<span><b>{e(p["curto"])}</b><small>{e(plural(p["n"], ui["card_n"]).format(n=p["n"]))}</small></span></a>'
        for i, p in enumerate(paginas))
    return cabeca(ui, cid, titulo, desc, url, ld, pixel_id) + topo(ui, cfg, diag) + f"""
<main id="conteudo">
<section class="env heroi" style="grid-template-columns:1fr">
  <div>
    <p class="eyebrow mono entra" style="--i:0">{e(cfg['nome'])}</p>
    <h1 class="entra" style="--i:1">{e(ui['indice_h1'].format(**fmt))}</h1>
    <p class="lead entra" style="--i:2">{e(ui['indice_p'])}</p>
  </div>
</section>
<section class="env" style="padding-bottom:clamp(3rem,7vw,5rem)"><nav class="grelha" aria-label="{e(ui['toate'])}">{cards}</nav></section>
<section class="final"><div class="env"><h2>{e(ui['final_t'])}</h2><p>{e(ui['final_p'])}</p>
<div class="botoes"><a class="btn btn-p" href="{e(diag)}" data-gc="diagnostico-fim">{e(ui['cta'])} {SVG_SETA}</a></div></div></section>
</main>
{rodape(ui)}
{scripts('indice-' + cid, pixel_id)}"""


def pixel():
    p = os.path.join(AQUI, "..", "..", "marca", "dados.json")
    try:
        return json.load(open(p, encoding="utf-8"))["medicao"]["pixel_meta"]
    except (OSError, KeyError, ValueError):
        return ""


def gerar(sites, demos_py, out, embutir=False):
    demos = carregar(sites, ler_demos(demos_py))
    sem = [d["curto"] for d in demos if not d["nicho"]]
    hoje = datetime.date.today().isoformat()
    mapa, relatorio = [], []
    for cid, cfg in N.CIDADES.items():
        ui = N.UI[cfg["lingua"]]
        paginas = []
        for chave in N.ORDEM:
            txt = N.NICHOS.get(chave, {}).get(cfg["lingua"])
            locais = [d for d in demos if d["nicho"] == chave and d["cidade"] == cid]
            fora = [d for d in demos if d["nicho"] == chave and d["cidade"] != cid
                    and (cfg["lingua"] == d["lingua"] or (cfg["lingua"] == "pt" and d["tem_pt"]))]
            todos = locais + fora
            if not txt or len(locais) < N.MINIMO_LOCAIS or len(todos) < N.MINIMO:
                if locais:
                    relatorio.append(f"  {cid}/{chave}: {len(locais)} locais + {len(fora)} de fora — sem página"
                                     + ("" if txt else f" (falta texto {cfg['lingua']})"))
                continue
            capa = next((d for d in todos if d["img"]), todos[0])
            paginas.append({"chave": chave, "txt": txt, "demos": todos, "slug": f"{txt['slug']}-{cid}",
                            "curto": txt["curto"], "n": len(todos), "n_locais": len(locais), "capa": capa})
        px = pixel() if cfg["pixel"] else ""
        for p in paginas:
            outros = [o for o in paginas if o is not p]
            slug, h = pagina_nicho(cid, cfg, ui, p["chave"], p["txt"], p["demos"], outros, embutir, sites, px)
            dst = os.path.join(out, cfg["base"].strip("/"), slug)
            os.makedirs(dst, exist_ok=True)
            open(os.path.join(dst, "index.html"), "w", encoding="utf-8").write(h)
            mapa.append(f"{cfg['host']}{cfg['base']}{slug}/")
            relatorio.append(f"  {cfg['host']}{cfg['base']}{slug}/  ({p['n_locais']} + {p['n'] - p['n_locais']})")
        if paginas:
            dst = os.path.join(out, cfg["base"].strip("/"))
            os.makedirs(dst, exist_ok=True)
            open(os.path.join(dst, "index.html"), "w", encoding="utf-8").write(pagina_indice(cid, cfg, ui, paginas, embutir, sites, px))
            mapa.insert(0, cfg["host"] + cfg["base"])
    with open(os.path.join(out, "sitemap-nichos.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.writelines(f"  <url><loc>{u}</loc><lastmod>{hoje}</lastmod></url>\n" for u in mapa)
        f.write("</urlset>\n")
    print(f"páginas por nicho: {len(mapa)} páginas de {len(demos)} demos -> {out}")
    print("\n".join(relatorio))
    if sem:
        print("  demos sem nicho (acrescentar a FIXOS ou PALAVRAS em nichos.py):", ", ".join(sem))
    return mapa


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--sites", default=os.path.dirname(AQUI))
    a.add_argument("--demos", default=None, help="caminho do gerar.py das demos (por omissão <sites>/demos-pachecost/gerar.py)")
    a.add_argument("--out", required=True)
    a.add_argument("--embutir", action="store_true")
    x = a.parse_args()
    gerar(x.sites, x.demos or os.path.join(x.sites, "demos-pachecost", "gerar.py"), x.out, x.embutir)
