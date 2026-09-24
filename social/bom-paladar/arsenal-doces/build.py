#!/usr/bin/env python3
"""Carrossel de arsenal — "Cinco maneiras de acabar um jantar." (Simona's O Bom Paladar).

Peça intemporal, fora da série dos azulejos: tema, cores, letra e pratos são outros.
  · cinco sobremesas reais, nunca publicadas, em ecrã inteiro: o prato é o post;
  · chocolate, rosa de açúcar e caramelo; Noto Serif Display itálico + Work Sans;
  · assinatura: um fio de caramelo contínuo que atravessa os cinco slides na faixa de
    baixo (ao deslizar, a linha continua), sem nunca passar por cima da comida.

Uso: python3 build.py  → img/, carrossel.html, 01…05 PNG e folha de revisão.
"""
import base64, html, math, os, pathlib, subprocess
from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
FOTOS = RAIZ / "media/bom-paladar/fotos"
FONTES = RAIZ / "social/fonts"
IMG = AQUI / "img"
W, H = 1080, 1350

CASA = {
    "whatsapp": "918 958 233",
    "morada": "R. do Comércio 367A",
    "terra": "Almancil",
    "site": "bompaladar.pt",
    "jantar": "Jantar de segunda a sábado, 19h–22h30",
}

# (id, numeral, legenda, foto, zoom, foco x, foco y)
DOCES = [
    ("01-capa", "I", "Num ninho de caramelo.", "WhatsApp Image 2026-07-03 at 14.59.40.jpeg", 1.0, 0.5, 0.3),
    ("02-canela", "II", "Com canela e lascas de caramelo.", "WhatsApp Image 2026-08-07 at 13.05.21.jpeg", 1.0, 0.5, 0.45),
    ("03-chocolate", "III", "Chocolate, gelado e framboesa.", "WhatsApp Image 2026-07-03 at 14.38.42 (4).jpeg", 1.0, 0.5, 0.6),
    ("04-colher", "IV", "Com a colher desenhada a cacau.", "WhatsApp Image 2026-08-07 at 12.57.48.jpeg", 1.0, 0.4, 0.5),
    ("05-reservar", "V", "Numa nuvem de açúcar.", "WhatsApp Image 2026-07-03 at 14.59.08.jpeg", 1.0, 0.5, 0.1),
]


def cobrir(src, zoom, fx, fy):
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - W) * fx)
    y = round((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H))


def preparar():
    IMG.mkdir(exist_ok=True)
    for sid, _, _, foto, z, fx, fy in DOCES:
        cobrir(FOTOS / foto, z, fx, fy).save(IMG / f"{sid}.jpg", quality=93)


# ---------- o fio de caramelo, só na faixa de baixo (y 1240–1330) ----------
LACOS = [620, 300, 760, 420, 640]   # x local do laço em cada slide


def pontos():
    """Onda suave pelos 5 slides, com um laço por slide em sítio diferente."""
    pts = [(-60, 1290)]
    for k, lx in enumerate(LACOS):
        x0, gx = k * W, k * W + lx
        for x in range(x0 + 120, x0 + W + 1, 240):
            if abs(x - gx) >= 160:
                pts.append((x, 1290 + round(22 * math.sin(x / 190))))
        pts += [(gx - 90, 1296), (gx + 20, 1262), (gx + 40, 1318), (gx - 30, 1320), (gx - 10, 1266), (gx + 110, 1284)]
    pts.append((5460, 1290))
    # ordenar por slide/posição, mantendo a ordem interna de cada laço
    fixos = sorted([p for p in pts if not any(abs(p[0] - (k * W + lx)) < 150 for k, lx in enumerate(LACOS))])
    out = []
    for k, lx in enumerate(LACOS):
        gx = k * W + lx
        laco = [(gx - 90, 1296), (gx + 20, 1262), (gx + 40, 1318), (gx - 30, 1320), (gx - 10, 1266), (gx + 110, 1284)]
        antes = [p for p in fixos if p[0] < gx - 90 and (not out or p[0] > out[-1][0])]
        out += antes + laco
    out += [p for p in fixos if p[0] > out[-1][0]]
    return out


def caminho(pts):
    d = [f"M{pts[0][0]},{pts[0][1]}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[0]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}")
    return " ".join(d)


FIO_D = caminho(pontos())


def fio(i):
    return (f'<svg class="fio" viewBox="{i * W} 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">'
            f'<path d="{FIO_D}" stroke="#E7B77E" stroke-width="8" fill="none" stroke-linecap="round" opacity=".35"/>'
            f'<path d="{FIO_D}" stroke="var(--caramelo)" stroke-width="3" fill="none" stroke-linecap="round"/></svg>')


# ---------- HTML ----------
def fonte(familia, estilo, peso, ficheiro):
    b64 = base64.b64encode((FONTES / ficheiro).read_bytes()).decode()
    return (f"@font-face{{font-family:'{familia}';font-style:{estilo};font-weight:{peso};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")


CSS = """
:root{--rosa:#F4E3DA;--choc:#2E160E;--caramelo:#D38A3E;--creme:#FBF1EA}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1b1b1b;display:flex;flex-direction:column;align-items:center;gap:48px;padding:48px 0}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;color:var(--creme);text-align:center;background:var(--choc);
  -webkit-font-smoothing:antialiased}
.fundo{position:absolute;inset:0;width:100%;height:100%;display:block}
.sombra{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(46,22,14,.55) 0,rgba(46,22,14,0) 13%),
  linear-gradient(0deg,rgba(46,22,14,.97) 0,rgba(46,22,14,.9) 13%,rgba(46,22,14,.55) 24%,rgba(46,22,14,0) 36%)}
.sombra.alta{background:
  linear-gradient(180deg,rgba(46,22,14,.55) 0,rgba(46,22,14,0) 13%),
  linear-gradient(0deg,rgba(46,22,14,.98) 0,rgba(46,22,14,.94) 32%,rgba(46,22,14,.6) 44%,rgba(46,22,14,0) 58%)}
.fio{position:absolute;inset:0;z-index:2}
.marca{position:absolute;top:58px;left:0;right:0;z-index:3;font:600 17px/1 'Work Sans',sans-serif;letter-spacing:.34em;
  color:var(--creme);padding-left:.34em;text-transform:uppercase;text-shadow:0 1px 8px rgba(0,0,0,.35)}
.marca b{display:inline-block;width:1.5em;margin-left:-.34em;color:var(--caramelo);letter-spacing:0}
.rodape{position:absolute;left:0;right:0;z-index:3;display:flex;align-items:baseline;justify-content:center;gap:26px}
.num{font:italic 300 96px/1 'Noto Serif Display',serif;color:var(--caramelo)}
.leg{font:italic 400 58px/1.1 'Noto Serif Display',serif;letter-spacing:-.005em}
.t{font:italic 300 100px/1.02 'Noto Serif Display',serif;letter-spacing:-.015em}
.t em{font-style:italic;color:var(--caramelo)}
.botao{display:inline-block;margin-top:30px;height:68px;padding:0 42px 0 46px;border-radius:34px;background:var(--rosa);color:var(--choc);
  font:600 22px/68px 'Work Sans',sans-serif;letter-spacing:.2em}
.wa{margin-top:24px;font:600 34px/1 'Work Sans',sans-serif}
.wa span{margin-left:.5em}
.linha{margin-top:12px;font:500 23px/1.35 'Work Sans',sans-serif;color:#E9D3C6}
.linha b{color:var(--caramelo);margin:0 .45em}
"""

PONTO = "<b>·</b>"


def e(t):
    return html.escape(t, quote=False)


def slide(i, d):
    sid, num, leg, *_ = d
    marca = f'<p class="marca">Simona’s{PONTO}O Bom Paladar</p>'
    fundo = f'<img class="fundo" src="img/{sid}.jpg" alt="">'
    pequeno = f'<span class="num" style="font-size:54px">{num}</span><span class="leg" style="font-size:36px;color:#E9D3C6">{e(leg)}</span>'
    if sid == "01-capa":
        corpo = f'''<div class="sombra alta"></div>
  <h1 class="t" style="position:absolute;left:0;right:0;top:930px;z-index:3">Cinco maneiras<br>de acabar <em>um jantar.</em></h1>
  <div class="rodape" style="top:1158px">{pequeno}</div>'''
    elif sid == "05-reservar":
        c = CASA
        corpo = f'''<div class="sombra alta"></div>
  <div class="rodape" style="top:760px">{pequeno}</div>
  <div style="position:absolute;left:0;right:0;top:838px;z-index:3">
    <p class="t" style="font-size:86px">Qual vai ser a sua?</p>
    <a class="botao">RESERVE A SUA MESA</a>
    <p class="wa">WhatsApp<span>{e(c["whatsapp"])}</span></p>
    <p class="linha">{e(c["jantar"])}<br>{e(c["morada"])}{PONTO}{e(c["terra"])}{PONTO}{e(c["site"])}</p>
  </div>'''
    else:
        corpo = f'''<div class="sombra"></div>
  <div class="rodape" style="top:1100px"><span class="num">{num}</span><span class="leg">{e(leg)}</span></div>'''
    return f'<section class="slide" id="{sid}">{fundo}\n  {corpo}\n  {fio(i)}{marca}\n</section>'


def pagina():
    fontes = (fonte("Noto Serif Display", "italic", "300 400", "noto-serif-display-italic-variable.woff2")
              + fonte("Work Sans", "normal", "500 600", "work-sans-variable.woff2"))
    return f'''<!doctype html>
<html lang="pt-PT"><head><meta charset="utf-8">
<title>Bom Paladar — cinco maneiras de acabar um jantar</title>
<style>{fontes}{CSS}</style></head>
<body>{"".join(slide(i, d) for i, d in enumerate(DOCES))}
</body></html>'''


def folha(nomes):
    th = 460
    tw = round(th * W / H)
    pad, leg = 32, 34   # slides encostados: vê-se o fio contínuo
    ims = [Image.open(AQUI / f"{n}.png").convert("RGB").resize((tw, th), Image.LANCZOS) for n in nomes]
    capa = Image.open(AQUI / f"{nomes[0]}.png").convert("RGB").resize((150, round(150 * H / W)), Image.LANCZOS)
    f = Image.new("RGB", (pad * 2 + len(ims) * tw + 24 + 150, pad * 2 + th + leg), (27, 27, 27))
    d = ImageDraw.Draw(f)
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    x = pad
    for n, im in zip(nomes, ims):
        f.paste(im, (x, pad))
        d.text((x + 4, pad + th + 10), f"{n}.png", fill=(214, 178, 94), font=fnt)
        x += tw
    x += 24
    f.paste(capa, (x, pad))
    d.text((x, pad + capa.height + 10), "capa a 150 px", fill=(214, 178, 94), font=fnt)
    f.save(AQUI / "folha-revisao.png")


def main():
    preparar()
    (AQUI / "carrossel.html").write_text(pagina(), encoding="utf-8")
    raiz_npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(AQUI / "shot.js"), str(AQUI / "carrossel.html"), str(AQUI), "--slides"],
                   check=True, cwd=AQUI, env={**os.environ, "NODE_PATH": raiz_npm})
    folha([d[0] for d in DOCES])


if __name__ == "__main__":
    main()
