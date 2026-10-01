#!/usr/bin/env python3
"""pachecost.com — alterações de 01/10/2026 sobre o deploy exportado do Netlify (pasta cur/ → novo/).

1. Primeiro ecrã para quem chega por anúncio (PT e RO): utm_*, fbclid ou ?origem=anuncio → html.anuncio.
2. Aviso de cookies compacto no telemóvel.
3. Separadores com mais ar no computador.
4. Lema acima da secção dos sites (PT, RO, EN), escondido a quem chega por anúncio.
5. "Ponte" para as automações entre os tipos de negócio e "Mais sites que fizemos" (PT, RO, EN).

Cada substituição tem de acontecer exatamente uma vez por ficheiro; se não acontecer, o script pára
(o gerador pode ter mudado o HTML).
"""
import pathlib, shutil, sys
from urllib.parse import quote

RAIZ = pathlib.Path(__file__).resolve().parent
CUR, NOVO = RAIZ / "cur", RAIZ / "novo"

WA = "https://wa.me/351967117357?text="
ICONE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 '
         '8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5'
         'a8.48 8.48 0 0 1 8 8v.5z"/></svg>')
SETA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

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

LEMA = {
    "pt": "O trabalho que faz o teu negócio subir de nível.",
    "ro": "Munca care îți duce afacerea la următorul nivel.",
    "en": "The work that takes your business to the next level.",
}

PONTE = {
    "pt": dict(
        eyebrow="E depois do site",
        titulo="O site traz clientes. As automações mantêm-nos.",
        lead="Oito coisas que hoje fazes à mão, a andarem sozinhas no WhatsApp: marcações confirmadas, "
             "avaliações no Google, os clientes que não voltaram, faturas para o contabilista.",
        botao="Ver as automações", cliente="Cliente", assistente="Assistente",
        m1="Têm mesa para 4 hoje às 20h?",
        m2="Temos, sim. Em nome de quem fica? Confirmo já a reserva das 20:00 para 4 pessoas.",
    ),
    "ro": dict(
        eyebrow="Și după site",
        titulo="Site-ul aduce clienți. Automatizările îi păstrează.",
        lead="Opt lucruri pe care le faci acum de mână, mergând singure pe WhatsApp: programări confirmate, "
             "recenzii pe Google, clienții care nu s-au mai întors, facturi pentru contabil.",
        botao="Vezi automatizările", cliente="Client", assistente="Asistent",
        m1="Aveți masă pentru 4 diseară la 20?",
        m2="Da, avem. Pe ce nume o trec? Confirm imediat rezervarea de la 20:00 pentru 4 persoane.",
    ),
    "en": dict(
        eyebrow="And after the website",
        titulo="Your website brings customers. Automations keep them.",
        lead="Eight things you do by hand today, running on their own on WhatsApp: confirmed bookings, "
             "Google reviews, the customers who haven’t come back, invoices for your accountant.",
        botao="See the automations", cliente="Customer", assistente="Assistant",
        m1="Do you have a table for 4 tonight at 8?",
        m2="We do. What name should I put it under? I’ll confirm the booking for 4 people at 20:00 right away.",
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
/* ═══ separadores com mais ar no computador (no telemóvel ficam como estão: os três têm de caber) ═══ */
@media (min-width:48rem){
  :root{--tabs:3.5rem}
  .tabs ul{gap:2.25rem}
  .tabs a{padding-inline:.15rem}
}
/* ═══ lema: a frase da casa, acima da secção dos sites. Escondido a quem chega por anúncio: aí fala o herói. ═══ */
.lema{display:flex;align-items:flex-start;gap:1rem;margin:0 0 clamp(2.5rem,7vw,4rem);max-width:28ch;
  font:600 clamp(1.25rem,2.6vw,1.75rem)/1.3 var(--texto);color:var(--osso);text-wrap:balance}
.lema-traco{flex:none;width:2.25rem;height:3px;margin-top:.6em;border-radius:2px;background:var(--laranja);
  transform-origin:left center;transform:scaleX(0);animation:lema-traco .9s var(--sair) .3s forwards}
@keyframes lema-traco{to{transform:none}}
html.anuncio .lema{display:none}
/* ═══ ponte para as automações: entre os tipos de negócio e "Mais sites que fizemos" ═══ */
.ponte{margin-top:clamp(3rem,9vw,5rem);display:grid;gap:1.75rem;padding:clamp(1.4rem,4vw,2.5rem);
  border:1px solid var(--linha-e);border-radius:1.25rem;background:var(--carvao-2);
  background-image:radial-gradient(70% 90% at 100% 0%,rgba(232,98,44,.16),transparent 70%)}
.ponte .afirmacao{font-size:clamp(1.5rem,3.2vw,2.25rem);margin-top:.7rem;max-width:16ch}
.ponte .lead{font-size:1rem}
.ponte-botao{margin-top:1.4rem;border-color:var(--laranja);color:var(--laranja)}
.ponte-botao:hover,.ponte-botao:focus-visible{background:var(--laranja);color:var(--carvao)}
.ponte-botao svg{transition:transform .25s var(--sair)}
.ponte-botao:hover svg,.ponte-botao:focus-visible svg{transform:translateX(.3rem)}
.ponte .chat{max-width:none}
@media (min-width:48rem){
  .ponte{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);align-items:center;gap:clamp(2rem,5vw,4rem)}
}
@media (prefers-reduced-motion:reduce){
  .lema-traco{animation:none;transform:none}
  .ponte-botao svg{transition:none}
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

ABRE_SITES = '<section id="proiecte" class="vista" aria-labelledby="t-proiecte">\n  <div class="envolver seccao">\n'
MAIS = '<div class="mais">\n'


def uma_vez(src, antes, depois, nome):
    n = src.count(antes)
    if n != 1:
        sys.exit(f"{nome}: esperava 1 ocorrência de «{antes[:60]}…», encontrei {n}")
    return src.replace(antes, depois)


def heroi(h):
    return (f'    <div class="heroi-anuncio">\n'
            f'      <p class="eyebrow">{h["eyebrow"]}</p>\n'
            f'      <h2 class="afirmacao">{h["titulo"]}</h2>\n'
            f'      <p class="lead">{h["lead"]}</p>\n'
            f'      <a class="botao primario grande" href="{WA}{quote(h["msg"], safe="")}">{ICONE}{h["botao"]}</a>\n'
            f'    </div>\n')


def lema(texto):
    return f'    <p class="lema"><span class="lema-traco" aria-hidden="true"></span>{texto}</p>\n'


def ponte(p):
    return (f'      <aside class="ponte rv" aria-labelledby="t-ponte">\n'
            f'        <div class="ponte-texto">\n'
            f'          <p class="eyebrow">{p["eyebrow"]}</p>\n'
            f'          <h3 id="t-ponte" class="afirmacao">{p["titulo"]}</h3>\n'
            f'          <p class="lead">{p["lead"]}</p>\n'
            f'          <a class="botao ponte-botao" href="#automatizari">{p["botao"]}{SETA}</a>\n'
            f'        </div>\n'
            f'        <div class="chat" aria-hidden="true">\n'
            f'          <div class="msg client rv" style="--i:3"><small>{p["cliente"]}</small>{p["m1"]}</div>\n'
            f'          <div class="msg asistent rv" style="--i:14"><small>{p["assistente"]}</small>{p["m2"]}</div>\n'
            f'        </div>\n'
            f'      </aside>\n    ')


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
    topo = heroi(HEROI[lingua]) if lingua in HEROI else ""
    src = uma_vez(src, ABRE_SITES, ABRE_SITES + topo + lema(LEMA[lingua]), rel)
    if lingua in HEROI:
        tc = HEROI[lingua]["toda_chic"]
        src = uma_vez(src, tc, tc.replace('class="rv dest"', 'class="rv dest sem-anuncio"'), rel)
        j = src.find('class="rv dest sem-anuncio"'); k = src.find("</li>\n", j) + len("</li>\n")
        src = src[:k] + naval(HEROI[lingua]) + src[k:]
    src = uma_vez(src, MAIS, ponte(PONTE[lingua]) + MAIS, rel)
    (NOVO / rel).parent.mkdir(parents=True, exist_ok=True)
    (NOVO / rel).write_text(src, encoding="utf-8")
    print(f"{rel}: {len((CUR / rel).read_text(encoding='utf-8'))} → {len(src)} bytes")


if NOVO.exists():
    shutil.rmtree(NOVO)
shutil.copytree(CUR, NOVO)
tratar("index.html", "pt")
tratar("ro/index.html", "ro")
tratar("en/index.html", "en")
