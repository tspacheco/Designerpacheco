#!/usr/bin/env python3
"""Capa do Facebook da Pacheco Studios — duas direções, 1640×924 (16:9).

Computador: o Facebook mostra a faixa central 1640×624 (820×312 a 2×). Telemóvel: mostra a imagem inteira (640×360).
Tudo o que importa fica dentro da faixa central (y 150–774) e longe do canto inferior esquerdo, onde a foto de perfil
(o selo) se sobrepõe à capa.

    python3 gerar.py            # escreve capa.html (duas direções × PT e EN, uma por baixo da outra)
"""
import base64, pathlib

AQUI = pathlib.Path(__file__).resolve().parent
F = AQUI / "fontes"


def fonte(nome, ficheiro, peso):
    b = base64.b64encode((F / ficheiro).read_bytes()).decode()
    return f'@font-face{{font-family:"{nome}";font-weight:{peso};src:url(data:font/woff2;base64,{b}) format("woff2")}}'


W, H = 1640, 924
BANDA = (150, 774)          # o que o computador mostra

TEXTOS = {
    "pt": dict(
        eyebrow="Automações com IA · Sites",
        l1="Tens um objetivo a atingir?",
        big=("A IA vai", "<span class=\"nb\">fazê-lo</span>", "acontecer."),
        l3="Só tens de dar o primeiro passo.",
        tel="967 117 357",
        site="pachecost.com",
        local=None,
    ),
    "en": dict(
        eyebrow="AI audit · Automations · Solutions",
        l1="Do you have a goal to reach?",
        big=("AI will", "make it", "happen."),
        l3="You just have to take the first step.",
        tel="+351 967 117 357",
        site="pachecost.com",
        local="HQ Portugal · Working worldwide",
    ),
}


def aneis_selo(cx, cy, r_ouro, extra=""):
    """Os três anéis do selo (proporções do logo.svg: 280 · 274 ouro, 258 laranja tracejado), à escala r_ouro."""
    k = r_ouro / 280
    return (f'<circle cx="{cx}" cy="{cy}" r="{280*k:.1f}" fill="none" stroke="#C9A256" stroke-width="{4*k:.2f}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{274*k:.1f}" fill="none" stroke="#C9A256" stroke-width="{1.5*k:.2f}" opacity=".7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{258*k:.1f}" fill="none" stroke="#E8622C" stroke-width="{2.5*k:.2f}" '
            f'stroke-dasharray="{9*k:.1f} {5.5*k:.1f}" opacity=".9" {extra}/>')


def ondas(cx, cy, raios):
    return "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#C9A256" stroke-width="{w}" opacity="{o}"/>'
                   for r, w, o in raios)


def bloco(t, classe=""):
    big = "<br>".join(t["big"])
    return (f'<div class="bloco {classe}">'
            f'<p class="eyebrow">{t["eyebrow"]}</p>'
            f'<p class="l1">{t["l1"]}</p>'
            f'<p class="big">{big}</p>'
            f'<p class="l3">{t["l3"]}</p>'
            f'<p class="contacto"><b>{t["tel"]}</b><i aria-hidden="true">·</i>{t["site"]}</p>'
            + (f'<p class="local">{t["local"]}</p>' if t.get("local") else "")
            + '</div>')


# ── A: ondas do selo — os anéis saem de onde está a foto de perfil e o texto fica à direita ──
CA = (170, 830)
svg_a = (f'<svg class="fundo" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
         + ondas(*CA, [(440, 1.6, .40), (630, 1.3, .27), (850, 1.1, .18), (1100, 1, .11), (1380, 1, .06)])
         + aneis_selo(*CA, 300)
         # o primeiro passo: o ponto da marca em cima do anel tracejado, a apontar para a frase
         + f'<circle cx="{CA[0] + 276*0.866:.0f}" cy="{CA[1] - 276*0.5:.0f}" r="15" fill="#E8622C"/>'
         + '</svg>')

# ── B: o selo aberto — o anel do selo em ponto grande, com a frase no lugar do P ──
CB = (1050, 462)
svg_b = (f'<svg class="fundo" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
         + ondas(*CB, [(700, 1.1, .16), (860, 1, .09)])
         + aneis_selo(*CB, 540)
         + f'<circle cx="{CB[0] - 540*258/280:.0f}" cy="{CB[1]}" r="15" fill="#E8622C"/>'
         + '</svg>')

CSS = """
:root{--fundo:#0D0B08;--ouro:#C9A256;--laranja:#E8622C;--creme:#EDE8D8;--creme-2:#B9B2A2}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#2a2a2a}
.capa{position:relative;width:1640px;height:924px;overflow:hidden;background:var(--fundo);margin-bottom:40px}
.fundo{position:absolute;inset:0}
.brilho{position:absolute;inset:0}
.bloco{position:absolute;color:var(--creme);width:max-content}
.eyebrow{font:700 24px/1 "Space Mono";letter-spacing:.32em;text-transform:uppercase;color:var(--ouro)}
.l1,.l3{font:600 42px/1.2 "Inter";letter-spacing:-.005em}
.l1{margin-top:34px}
.big{margin-top:14px;font:400 98px/.96 "Archivo Black";text-transform:uppercase;color:var(--laranja);letter-spacing:.005em}
.l3{margin-top:20px}
.contacto{margin-top:40px;font:700 26px/1 "Space Mono";letter-spacing:.08em;color:var(--creme-2)}
.contacto b{color:var(--ouro);font-weight:700}
.contacto i{font-style:normal;color:var(--ouro);margin:0 .7em}
.nb{white-space:nowrap}
.local{margin-top:14px;font:700 20px/1 "Space Mono";letter-spacing:.22em;text-transform:uppercase;color:var(--creme-2)}
.d-b .local{margin-right:-.22em}
/* inglês: três linhas curtas no destaque e o bloco mais compacto, para caber a linha da sede */
.l-en .l1{margin-top:28px}
.l-en .contacto{margin-top:30px}
.l-en .eyebrow{letter-spacing:.22em}
.d-b.l-en .eyebrow{margin-right:-.22em}
/* A */
.d-a .brilho{background:radial-gradient(760px 620px at 10% 92%,rgba(232,98,44,.17),transparent 70%),
  radial-gradient(900px 700px at 72% 46%,rgba(201,162,86,.07),transparent 72%)}
.d-a .bloco{left:800px;top:50%;transform:translateY(-50%)}
/* B */
.d-b .brilho{background:radial-gradient(620px 520px at 64% 50%,rgba(232,98,44,.12),transparent 70%)}
.d-b .bloco{left:1050px;top:50%;transform:translate(-50%,-50%);text-align:center}
.d-b .l1,.d-b .l3{font-size:40px}
.d-b .eyebrow{margin-right:-.32em}
.d-b .contacto{margin-right:-.08em}
.d-b .big{font-size:92px}
"""

DIRECOES = {"a": svg_a, "b": svg_b}
capas = "".join(f'<div class="capa d-{d} l-{l}" id="{d}-{l}" lang="{l}"><div class="brilho"></div>{svg}{bloco(t)}</div>'
                for l, t in TEXTOS.items() for d, svg in DIRECOES.items())
html = (f'<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>Pacheco Studios — capa Facebook</title><style>'
        + fonte("Archivo Black", "archivo-black-400.woff2", 400) + fonte("Space Mono", "space-mono-700.woff2", 700)
        + fonte("Inter", "inter-600.woff2", 600) + CSS + '</style></head><body>' + capas + '</body></html>')
(AQUI / "capa.html").write_text(html, encoding="utf-8")
print("capa.html", len(html) // 1024, "KB")
