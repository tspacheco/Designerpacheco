#!/usr/bin/env python3
"""Primeiro ecrã para quem chega por anúncio (pachecost.com e ro.pachecost.com) + aviso de cookies compacto.

Aplica-se ao deploy exportado do Netlify (pasta cur/ → novo/). Cada substituição tem de acontecer
exatamente uma vez por ficheiro; se não acontecer, o script pára (o gerador pode ter mudado o HTML).
"""
import pathlib, re, shutil, sys

RAIZ = pathlib.Path(__file__).resolve().parent
CUR, NOVO = RAIZ / "cur", RAIZ / "novo"

WA = "https://wa.me/351967117357?text="
ICONE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 '
         '8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5'
         'a8.48 8.48 0 0 1 8 8v.5z"/></svg>')

HEROI = {
    "pt": dict(
        eyebrow="Sites para restaurantes",
        titulo="Um site assim para o teu restaurante.",
        lead="Fazemos o teu site e mostramos-to antes de pagares. Sem compromisso.",
        botao="Escreve-nos no WhatsApp",
        msg="Olá Tomás! Vi o anúncio. Queria ver como ficaria o site do meu restaurante: ",
        naval_tip="Restaurante", naval_cidade="Olhão",
        toda_chic='<li class="rv dest" style="--i:2"><a class="q" href="/p/toda-chic/pt.html"',
    ),
    "ro": dict(
        eyebrow="Site-uri pentru restaurante",
        titulo="Un site ca acesta pentru restaurantul tău.",
        lead="Îți facem site-ul și ți-l arătăm înainte să plătești. Fără obligații.",
        botao="Scrie-ne pe WhatsApp",
        msg="Bună, Tomás! Am văzut anunțul. Vreau să văd cum ar arăta site-ul restaurantului meu: ",
        naval_tip="Restaurant", naval_cidade="Olhão",
        toda_chic='<li class="rv dest" style="--i:2"><a class="q" href="/p/toda-chic/"',
    ),
}

# 1) decide-se antes de pintar: chegada por anúncio (utm_*, fbclid ou ?origem=anuncio) → html.anuncio, sem intro
CABECA_ANTES = ("(function(){try{if(!sessionStorage.getItem('ps-intro')&&!matchMedia('(prefers-reduced-motion: reduce)').matches)"
                "document.documentElement.classList.add('intro-vai')}catch(e){}})();")
CABECA_DEPOIS = ("(function(){try{var a=/[?&](utm_[a-z]+=|fbclid=|origem=anuncio)/.test(location.search);"
                 "if(a)document.documentElement.classList.add('anuncio');"
                 "if(!a&&!sessionStorage.getItem('ps-intro')&&!matchMedia('(prefers-reduced-motion: reduce)').matches)"
                 "document.documentElement.classList.add('intro-vai')}catch(e){}})();")

CSS = """
/* ═══ chegada por anúncio (html.anuncio: ?utm_*, fbclid ou ?origem=anuncio, decidido no <head>) ═══
   O primeiro ecrã fala a quem viu o vídeo de um restaurante: o que fazemos, a oferta e o WhatsApp.
   Sem parâmetros, a página é a de sempre. */
.heroi-anuncio{display:none}
html.anuncio .heroi-anuncio{display:block}
html.anuncio #proiecte > .envolver:has(.heroi-anuncio) > .eyebrow,
html.anuncio #proiecte > .envolver:has(.heroi-anuncio) > .afirmacao,
html.anuncio #proiecte > .envolver:has(.heroi-anuncio) > .lead{display:none}
.heroi-anuncio .botao{display:flex;width:100%;margin-top:1.5rem}
.heroi-anuncio .nota{margin-top:.9rem;font-size:.9375rem;color:var(--osso-2)}
/* em destaque: no anúncio, o terceiro quadrado é um restaurante e não a loja de roupa */
.so-anuncio{display:none}
html.anuncio .so-anuncio{display:block}
html.anuncio .sem-anuncio{display:none}
@media (min-width:40rem){
  .heroi-anuncio .botao{display:inline-flex;width:auto}
}
/* ═══ aviso de cookies compacto: faixa colada ao fundo no telemóvel (antes tapava um terço do ecrã) ═══ */
.rgpd{left:0;right:0;bottom:0;transform:none;width:auto;border-radius:1rem 1rem 0 0;border-bottom:0;
  gap:.55rem;padding:.7rem max(var(--gutter),env(safe-area-inset-left)) calc(.7rem + env(safe-area-inset-bottom))}
.rgpd p{font-size:.8125rem;line-height:1.4}
.rgpd .acoes{gap:.5rem}
.rgpd button{min-height:2.5rem;padding:0 .9rem}
.rgpd a{min-height:2.5rem}
@media (min-width:40rem){
  .rgpd{left:50%;right:auto;bottom:calc(1rem + env(safe-area-inset-bottom));transform:translateX(-50%);
    width:min(42rem,calc(100% - 2rem));border-radius:1rem;border-bottom:1px solid var(--linha-e);gap:.9rem;padding:1rem 1.1rem}
  .rgpd p{font-size:.875rem;line-height:1.5}
  .rgpd button{min-height:2.75rem;padding:0 1.1rem}
  .rgpd a{min-height:2.75rem}
}
"""

# 3) medição: chegadas por anúncio e as saídas delas, contadas à parte no GoatCounter
MED_ANTES = "  // tipos de negócio abertos, contados à parte: mostra o que interessa a quem visita\n"
MED_DEPOIS = ("  // chegadas por anúncio (html.anuncio, decidido no <head>) e as saídas delas para o WhatsApp, contadas à parte\n"
              "  var porAnuncio = document.documentElement.classList.contains('anuncio');\n"
              "  if (porAnuncio) {\n"
              "    window.addEventListener('load', function () { gc({ path: 'anuncio/chegada', title: 'chegada por anúncio', event: true }); });\n"
              "  }\n" + MED_ANTES)
SAIDA_ANTES = "    gc({ path: 'ir/' + canal, title: 'saída: ' + canal, event: true });\n"
SAIDA_DEPOIS = SAIDA_ANTES + "    if (porAnuncio) gc({ path: 'anuncio/' + canal, title: 'saída por anúncio: ' + canal, event: true });\n"


def uma_vez(src, antes, depois, nome):
    n = src.count(antes)
    if n != 1:
        sys.exit(f"{nome}: esperava 1 ocorrência de «{antes[:60]}…», encontrei {n}")
    return src.replace(antes, depois)


def heroi(h):
    from urllib.parse import quote
    return (f'    <div class="heroi-anuncio">\n'
            f'      <p class="eyebrow">{h["eyebrow"]}</p>\n'
            f'      <h2 class="afirmacao">{h["titulo"]}</h2>\n'
            f'      <p class="lead">{h["lead"]}</p>\n'
            f'      <a class="botao primario grande" href="{WA}{quote(h["msg"], safe="")}">{ICONE}{h["botao"]}</a>\n'
            f'    </div>\n')


def naval(h):
    return ('<li class="rv dest so-anuncio" style="--i:2"><a class="q" href="https://gruponaval.online" '
            'style="--bg:#0A1C2E;--ink:#F2EDE2;--ac:#C9A227;--f:\'Sora\';--w:800;--fs:1" target="_blank" rel="noopener">'
            '<span class="q-nome">Grupo Naval</span><span class="q-meta"><span class="q-tip">' + h["naval_tip"] +
            '</span><span class="q-sep">&nbsp;· </span><span class="q-oras">' + h["naval_cidade"] + '</span></span></a></li>\n')


def tratar(rel, lingua):
    src = (CUR / rel).read_text(encoding="utf-8")
    src = uma_vez(src, CABECA_ANTES, CABECA_DEPOIS, rel)
    i = src.rfind("</style>", 0, src.find("</head>"))
    assert i > 0, rel
    src = src[:i] + CSS + src[i:]
    src = uma_vez(src, MED_ANTES, MED_DEPOIS, rel)
    src = uma_vez(src, SAIDA_ANTES, SAIDA_DEPOIS, rel)
    if lingua:
        h = HEROI[lingua]
        abre = '<section id="proiecte" class="vista" aria-labelledby="t-proiecte">\n  <div class="envolver seccao">\n'
        src = uma_vez(src, abre, abre + heroi(h), rel)
        tc = h["toda_chic"]
        src = uma_vez(src, tc, tc.replace('class="rv dest"', 'class="rv dest sem-anuncio"'), rel)
        j = src.find('class="rv dest sem-anuncio"'); k = src.find("</li>\n", j) + len("</li>\n")
        src = src[:k] + naval(h) + src[k:]
    (NOVO / rel).parent.mkdir(parents=True, exist_ok=True)
    (NOVO / rel).write_text(src, encoding="utf-8")
    print(f"{rel}: {len((CUR / rel).read_text(encoding='utf-8'))} → {len(src)} bytes")


if NOVO.exists():
    shutil.rmtree(NOVO)
shutil.copytree(CUR, NOVO)
tratar("index.html", "pt")
tratar("ro/index.html", "ro")
tratar("en/index.html", None)
