#!/usr/bin/env python3
"""Carrossel de arsenal — "Cinco maneiras de acabar um jantar." (Simona's O Bom Paladar).

Peça intemporal, para publicar em qualquer semana. Não pertence à série dos
azulejos: tema, cores, letra e pratos são outros.
  · cinco sobremesas reais, nunca publicadas (fotos em media/bom-paladar/fotos);
  · rosa de açúcar, chocolate e caramelo; Noto Serif Display itálico + Work Sans;
  · assinatura: um fio de caramelo contínuo que atravessa os cinco slides ao deslizar
    e passa por trás das fotos, recortadas em arco.

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

# (id, numeral, legenda, foto, largura×altura do arco, foco x, foco y, zoom)
DOCES = [
    ("01-capa", "I", "Num ninho de caramelo.",
     "WhatsApp Image 2026-07-03 at 14.59.40.jpeg", (660, 700), 0.5, 0.45, 1.0),
    ("02-fios", "II", "Com fios de açúcar e mirtilos.",
     "WhatsApp Image 2026-07-03 at 14.59.08 (2).jpeg", (740, 860), 0.5, 0.5, 1.0),
    ("03-chocolate", "III", "Chocolate, gelado e framboesa.",
     "WhatsApp Image 2026-07-03 at 14.38.42 (4).jpeg", (740, 860), 0.5, 0.75, 1.0),
    ("04-colher", "IV", "Com a colher desenhada a cacau.",
     "WhatsApp Image 2026-08-07 at 12.57.48.jpeg", (740, 860), 0.45, 0.5, 1.0),
    ("05-reservar", "V", "Numa nuvem de açúcar.",
     "WhatsApp Image 2026-07-03 at 14.59.08.jpeg", (600, 600), 0.5, 0.35, 1.0),
]


def recortar(src, tamanho, fx, fy, zoom):
    tw, th = tamanho
    im = Image.open(src).convert("RGB")
    s = max(tw / im.width, th / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - tw) * fx)
    y = round((im.height - th) * fy)
    return im.crop((x, y, x + tw, y + th))


def preparar():
    IMG.mkdir(exist_ok=True)
    for sid, _, _, foto, tam, fx, fy, z in DOCES:
        # 2× para ficar nítido no ecrã do telemóvel ao ampliar
        recortar(FOTOS / foto, (tam[0] * 2, tam[1] * 2), fx, fy, z).save(IMG / f"{sid}.jpg", quality=90)


# ---------- o fio de caramelo ----------
# Pontos pelos 5 slides (x global 0–5400). Voltas para trás fazem os laços.
FIO = [(-60, 450), (200, 470), (420, 440), (400, 505), (330, 470), (620, 455), (880, 470),
       (1000, 620), (1030, 900), (1005, 1170), (1110, 1300), (1400, 1285), (1560, 1250),
       (1600, 1310), (1530, 1322), (1500, 1265), (1750, 1292), (2000, 1298), (2110, 1190),
       (2120, 880), (2100, 500), (2140, 200), (2300, 100), (2420, 160), (2480, 215), (2400, 215),
       (2385, 150), (2700, 102), (3000, 110), (3150, 260), (3205, 700), (3190, 1100),
       (3260, 1285), (3450, 1292), (3600, 1250), (3640, 1310), (3570, 1324), (3540, 1265),
       (3800, 1295), (4100, 1290), (4270, 1170), (4290, 800), (4280, 400), (4310, 150),
       (4450, 105), (4560, 190), (4610, 140), (4560, 118), (4520, 160), (4750, 100),
       (5000, 102), (5250, 140), (5460, 180)]


def caminho(pts):
    """Catmull-Rom → Bézier cúbica."""
    d = [f"M{pts[0][0]},{pts[0][1]}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[0]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}")
    return " ".join(d)


def fio(i):
    d = caminho(FIO)
    return (f'<svg class="fio" viewBox="{i * W} 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">'
            f'<path d="{d}" stroke="#E7B77E" stroke-width="9" fill="none" stroke-linecap="round" opacity=".45"/>'
            f'<path d="{d}" stroke="var(--caramelo)" stroke-width="3.2" fill="none" stroke-linecap="round"/></svg>')


# ---------- HTML ----------
def fonte(familia, estilo, peso, ficheiro):
    b64 = base64.b64encode((FONTES / ficheiro).read_bytes()).decode()
    return (f"@font-face{{font-family:'{familia}';font-style:{estilo};font-weight:{peso};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")


CSS = """
:root{--rosa:#F2E1D8;--rosa2:#EBD2C6;--choc:#3A1E14;--choc2:#6B4535;--caramelo:#B8651F}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1b1b1b;display:flex;flex-direction:column;align-items:center;gap:48px;padding:48px 0}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;color:var(--choc);text-align:center;
  background:radial-gradient(120% 80% at 50% 45%,var(--rosa) 55%,var(--rosa2) 100%);-webkit-font-smoothing:antialiased}
.fio{position:absolute;inset:0;z-index:1}
.marca{position:absolute;top:64px;left:0;right:0;z-index:3;font:600 17px/1 'Work Sans',sans-serif;letter-spacing:.34em;
  color:var(--choc2);padding-left:.34em;text-transform:uppercase}
.marca b{display:inline-block;width:1.5em;margin-left:-.34em;color:var(--caramelo);letter-spacing:0}
.arco{position:absolute;left:50%;transform:translateX(-50%);z-index:2}
.arco img{display:block;border-radius:999px 999px 26px 26px;box-shadow:0 30px 60px -20px rgba(58,30,20,.45)}
.arco::before{content:"";position:absolute;inset:-16px;border:2px solid var(--caramelo);border-radius:999px 999px 38px 38px;opacity:.75}
.num{position:absolute;z-index:3;font:italic 300 150px/1 'Noto Serif Display',serif;color:var(--caramelo)}
.leg{position:absolute;left:0;right:0;z-index:3;font:italic 400 60px/1.12 'Noto Serif Display',serif;letter-spacing:-.005em}
.t{font:italic 300 104px/1.02 'Noto Serif Display',serif;letter-spacing:-.015em}
.t em{font-style:italic;color:var(--caramelo)}
.botao{display:inline-block;margin-top:34px;height:70px;padding:0 42px 0 46px;border-radius:35px;background:var(--choc);color:#F7ECE4;
  font:600 22px/70px 'Work Sans',sans-serif;letter-spacing:.2em}
.wa{margin-top:26px;font:600 34px/1 'Work Sans',sans-serif}
.wa span{margin-left:.5em}
.linha{margin-top:14px;font:500 23px/1.35 'Work Sans',sans-serif;color:var(--choc2)}
.linha b{color:var(--caramelo);margin:0 .45em}
"""

PONTO = "<b>·</b>"


def e(t):
    return html.escape(t, quote=False)


def slide(i, d):
    sid, num, leg, _, (aw, ah), *_ = d
    marca = f'<p class="marca">Simona’s{PONTO}O Bom Paladar</p>'
    img = f'<img src="img/{sid}.jpg" width="{aw}" height="{ah}" alt="">'
    if sid == "01-capa":
        corpo = f'''
  <h1 class="t" style="position:absolute;left:0;right:0;top:150px;z-index:3">Cinco maneiras<br>de acabar <em>um jantar.</em></h1>
  <div class="arco" style="top:520px">{img}</div>
  <p class="num" style="left:118px;top:1060px">{num}</p>
  <p class="leg" style="top:1248px;font-size:44px;color:var(--choc2)">{e(leg)}</p>'''
    elif sid == "05-reservar":
        c = CASA
        corpo = f'''
  <div class="arco" style="top:170px">{img}</div>
  <p class="num" style="left:150px;top:590px">{num}</p>
  <p class="leg" style="top:826px;font-size:44px;color:var(--choc2)">{e(leg)}</p>
  <div style="position:absolute;left:0;right:0;top:930px;z-index:3">
    <p class="t" style="font-size:84px">Qual vai ser a sua?</p>
    <a class="botao">RESERVE A SUA MESA</a>
    <p class="wa">WhatsApp<span>{e(c["whatsapp"])}</span></p>
    <p class="linha">{e(c["jantar"])}<br>{e(c["morada"])}{PONTO}{e(c["terra"])}{PONTO}{e(c["site"])}</p>
  </div>'''
    else:
        corpo = f'''
  <div class="arco" style="top:150px">{img}</div>
  <p class="num" style="left:{70 if len(num) < 3 else 40}px;top:905px">{num}</p>
  <p class="leg" style="top:1112px">{e(leg)}</p>'''
    return f'<section class="slide" id="{sid}">{fio(i)}{marca}{corpo}\n</section>'


def pagina():
    fontes = (fonte("Noto Serif Display", "italic", "300 400", "noto-serif-display-italic-variable.woff2")
              + fonte("Noto Serif Display", "normal", "500", "noto-serif-display-variable.woff2")
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
    gap, pad, leg = 0, 32, 34   # sem espaço entre slides: vê-se o fio contínuo
    ims = [Image.open(AQUI / f"{n}.png").convert("RGB").resize((tw, th), Image.LANCZOS) for n in nomes]
    capa = Image.open(AQUI / f"{nomes[0]}.png").convert("RGB").resize((150, round(150 * H / W)), Image.LANCZOS)
    f = Image.new("RGB", (pad * 2 + len(ims) * tw + 24 + 150, pad * 2 + th + leg), (27, 27, 27))
    d = ImageDraw.Draw(f)
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    x = pad
    for n, im in zip(nomes, ims):
        f.paste(im, (x, pad))
        d.text((x + 4, pad + th + 10), f"{n}.png", fill=(214, 178, 94), font=fnt)
        x += tw + gap
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
