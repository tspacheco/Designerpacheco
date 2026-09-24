#!/usr/bin/env python3
"""Carrossel de outono (outubro 2026) — Simona's O Bom Paladar, Almancil.

Continua a série dos azulejos de setembro: Caladea (a Cambria do original) +
Open Sans, creme, azul-marinho, faixa de texto em baixo com o azulejo a
transparecer. A diferença é pequena e visível:
  · o azulejo passa de azul e branco a azul e ocre (padrão polícromo do séc. XVII);
  · o itálico ganha a cor do barro dos tachos;
  · um filete ocre por dentro das faixas e pontos ocre nos separadores.

Uso:
  python3 build.py            prepara img/, gera carrossel.html, os 5 PNG e a folha de revisão
  python3 build.py --baixar   antes disso descarrega as 3 imagens do Higgsfield para img/

Sem as imagens do Higgsfield em img/ o carrossel sai com as fotos reais
(rascunho: tachos e tábua na bancada, azulejo azul e branco de setembro).
"""
import base64, html, pathlib, subprocess, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
FOTOS = RAIZ / "media/bom-paladar/fotos"
FONTES = RAIZ / "social/fonts"
IMG = AQUI / "img"
W, H = 1080, 1350

# ---------- fotos reais (nomes em media/bom-paladar/fotos) ----------
REAIS = {
    "tachos":  "WhatsApp Image 2026-08-07 at 13.05.57.jpeg",      # arroz em tachos de barro
    "grelha":  "WhatsApp Image 2026-08-07 at 13.03.42 (1).jpeg",  # bifes na grelha com chama
    "tabua":   "WhatsApp Image 2026-08-07 at 12.42.05 (1).jpeg",  # tábua de queijos e enchidos
    "entrada": "WhatsApp Image 2026-07-03 at 15.06.12 (2).jpeg",  # a porta, à noite
    "set-03":  "WhatsApp Image 2026-09-16 at 17.29.23 (1).jpeg",  # slide 03 de setembro (azulejo azul)
}

# ---------- imagens geradas no Higgsfield (GPT Image 2.5, 24/09/2026) ----------
# Prato real, só a bancada trocada por mesa de azulejo azul e ocre; e um painel de azulejo de frente.
CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_3Etg0s14W0GAU3lX2MY49HlxGwO/"
IA = {
    "ia-tachos.png": CDN + "hf_20260924_085318_3adfa67b-730f-4897-ad5c-1b18a02e6473.png",
    "ia-tabua.png":  CDN + "hf_20260924_085317_cda815da-fb0e-4c1a-bf1c-4362d484c76b.png",
    "ia-painel.png": CDN + "hf_20260924_085318_6e0449be-881e-48e0-96aa-687346929588.png",
}

CASA = {
    "whatsapp": "918 958 233",
    "morada": "R. do Comércio 367A",
    "terra": "Almancil",
    "site": "bompaladar.pt",
    "jantar": "Jantar de segunda a sábado, 19h–22h30",
}

# Tintos da carta fotografada a 13/07/2026 (ementa.md). Sem preços: confirmar com a Simona antes de publicar.
TINTOS = [
    ("Piano Reserva Touriga Nacional", "Douro"),
    ("Monte do Álamo Reserva", "Alentejo"),
    ("Barranco Longo Private Selection", "Algarve"),
]


def baixar():
    IMG.mkdir(exist_ok=True)
    for nome, url in IA.items():
        destino = IMG / nome
        if destino.exists():
            continue
        print("a descarregar", nome)
        urllib.request.urlretrieve(url, destino)


def cobrir(src, zoom=1.0, px=0.5, py=0.5):
    """Recorta a imagem para 1080×1350 como o object-fit:cover, com zoom e ponto de foco."""
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - W) * px)
    y = round((im.height - H) * py)
    return im.crop((x, y, x + W, y + H))


def preparar():
    """Gera os fundos 1080×1350 e os recortes de azulejo em img/. Devolve o modo de cada peça."""
    IMG.mkdir(exist_ok=True)
    modo = {}
    for chave, ia, real, ajuste in [
        ("01", "ia-tachos.png", "tachos", dict(zoom=1.0, py=1.0)),
        ("04", "ia-tabua.png", "tabua", dict(zoom=1.06, px=0.55, py=0.25)),
    ]:
        if (IMG / ia).exists():
            cobrir(IMG / ia).save(IMG / f"{chave}.jpg", quality=92)
            modo[chave] = "ia"
        else:
            cobrir(FOTOS / REAIS[real], **ajuste).save(IMG / f"{chave}.jpg", quality=92)
            modo[chave] = "real"
    cobrir(FOTOS / REAIS["grelha"], zoom=1.15, px=0.35, py=0.7).save(IMG / "02.jpg", quality=92)
    cobrir(FOTOS / REAIS["entrada"]).save(IMG / "05.jpg", quality=92)

    # azulejo do slide 03: faixas de cima e de baixo + o azulejo emoldurado
    if (IMG / "ia-painel.png").exists():
        p = Image.open(IMG / "ia-painel.png").convert("RGB")
        p = p.resize((1560, round(p.height * 1560 / p.width)), Image.LANCZOS)  # azulejo ≈ 390 px, como em setembro
        x0 = (p.width - W) // 2
        p.crop((x0, 0, x0 + W, 200)).save(IMG / "03-cima.jpg", quality=92)
        p.crop((x0, 390, x0 + W, 590)).save(IMG / "03-baixo.jpg", quality=92)
        t = p.width // 4
        p.crop((t, t, 2 * t, 2 * t)).resize((270, 270), Image.LANCZOS).save(IMG / "03-azulejo.jpg", quality=92)
        modo["03"] = "ia"
    else:
        s = Image.open(FOTOS / REAIS["set-03"]).convert("RGB")
        s.crop((0, 0, W, 200)).save(IMG / "03-cima.jpg", quality=92)
        s.crop((0, 1150, W, 1350)).save(IMG / "03-baixo.jpg", quality=92)
        s.crop((406, 332, 675, 600)).resize((270, 270), Image.LANCZOS).save(IMG / "03-azulejo.jpg", quality=92)
        modo["03"] = "real"
    return modo


# ---------- HTML ----------
def fonte(familia, estilo, peso, ficheiro):
    b64 = base64.b64encode((FONTES / ficheiro).read_bytes()).decode()
    return (f"@font-face{{font-family:'{familia}';font-style:{estilo};font-weight:{peso};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")


CSS = """
:root{--navy:#18316B;--pilula:#17316E;--filete:#1D3E8B;--barro:#9A4222;--ocre:#C9922E;--cinza:#6E6757;--creme:#F5F1E6}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1b1b1b;display:flex;flex-direction:column;align-items:center;gap:48px;padding:48px 0}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;background:var(--creme);
  font-family:'Caladea',serif;color:var(--navy);text-align:center;-webkit-font-smoothing:antialiased}
.fundo{position:absolute;inset:0;width:100%;height:100%;display:block}
.pilula{position:absolute;top:72px;left:50%;transform:translateX(-50%);height:60px;padding:0 30px 0 34px;border-radius:30px;
  background:var(--pilula);color:#fff;font:600 20px/60px 'Open Sans',sans-serif;letter-spacing:.22em;white-space:nowrap}
.sep{display:inline-block;width:1.25em;text-align:center;letter-spacing:0;color:var(--ocre);font-weight:700}
.pilula .sep{margin-left:-.22em}
.faixa{position:absolute;left:0;right:0;top:1000px;height:331px;background:rgba(245,241,230,.9);
  border-top:9px solid var(--filete);border-bottom:9px solid var(--filete);
  display:flex;flex-direction:column;align-items:center;padding-top:38px}
.faixa::before,.faixa::after{content:"";position:absolute;left:0;right:0;height:3px;background:var(--ocre)}
.faixa::before{top:5px}.faixa::after{bottom:5px}
.t{font-weight:700;font-size:85px;line-height:1.08;letter-spacing:-.003em}
.it{font-style:italic;font-weight:400;font-size:47px;line-height:1.15;color:var(--barro);margin-top:22px}
.caps{font:600 20px/1 'Open Sans',sans-serif;letter-spacing:.3em;color:var(--cinza);text-transform:uppercase}
.caps{padding-left:.3em}
.caps .sep{margin-left:-.3em;width:1.6em}
.faixa .caps{margin-top:34px}
.faixa.capa{justify-content:center;padding:0 0 26px}
.faixa.capa .t{font-size:96px}

/* 03 — só texto, azulejo em cima e em baixo */
.azul{position:absolute;left:0;right:0;height:200px;background-size:1080px 200px}
.azul.cima{top:0;border-bottom:9px solid var(--filete);height:209px}
.azul.baixo{bottom:0;border-top:9px solid var(--filete);height:209px}
.azul.cima::after,.azul.baixo::after{content:"";position:absolute;left:0;right:0;height:3px;background:var(--ocre)}
.azul.cima::after{bottom:-17px}.azul.baixo::after{top:-17px}
.miolo{position:absolute;left:0;right:0;top:209px;bottom:209px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.moldura{width:236px;height:236px;padding:13px;background:#FBF8F1;border-radius:10px;
  box-shadow:0 16px 30px rgba(40,30,10,.20),0 2px 6px rgba(40,30,10,.12)}
.moldura img{display:block;width:210px;height:210px;border:1.5px solid var(--navy)}
.miolo .it{font-size:72px;margin-top:46px}
.miolo .t{font-size:85px;margin-top:4px}
.risca{width:120px;height:5px;background:var(--navy);margin:34px 0 34px}
.vinhos{display:flex;flex-direction:column;gap:16px}
.vinho{font-weight:700;font-size:34px;line-height:1.1}
.vinho span{display:block;font:600 16px/1 'Open Sans',sans-serif;letter-spacing:.3em;color:var(--cinza);text-transform:uppercase;margin-top:8px}
.miolo .caps{margin-bottom:26px}

/* 05 — reservar */
.faixa.alta{top:828px;height:503px;padding:0;justify-content:center}
.faixa.alta .t{font-size:84px;line-height:1.07}
.faixa.alta .it{font-size:84px;line-height:1.07;margin-top:0}
.botao{margin-top:30px;height:68px;padding:0 40px 0 44px;border-radius:34px;background:var(--pilula);color:#fff;
  font:600 24px/68px 'Open Sans',sans-serif;letter-spacing:.2em}
.wa{margin-top:24px;font:600 36px/1 'Open Sans',sans-serif;color:#1D3163}
.wa span{margin-left:.55em}
.morada{margin-top:14px;font:600 24px/1.3 'Open Sans',sans-serif;color:var(--cinza);letter-spacing:.01em}
.morada .sep{margin-left:-.01em;width:1.3em}
"""

PONTO = '<b class="sep">·</b>'


def e(t):
    return html.escape(t, quote=False)


def slides():
    c = CASA
    out = []
    # 01 — capa
    out.append(f'''
<section class="slide" id="01-capa">
  <img class="fundo" src="img/01.jpg" alt="">
  <div class="pilula">OUTONO{PONTO}ALMANCIL</div>
  <div class="faixa capa">
    <h1 class="t">Tempo de tacho.</h1>
    <p class="caps">Simona's{PONTO}O Bom Paladar</p>
  </div>
</section>''')
    # 02 — o lume
    out.append(f'''
<section class="slide" id="02-o-lume">
  <img class="fundo" src="img/02.jpg" alt="">
  <div class="pilula">O LUME</div>
  <div class="faixa">
    <p class="t">As noites arrefecem.</p>
    <p class="it">A grelha, não.</p>
  </div>
</section>''')
    # 03 — outubro pede tinto
    vinhos = "".join(f'<p class="vinho">{e(n)}<span>{e(r)}</span></p>' for n, r in TINTOS)
    out.append(f'''
<section class="slide" id="03-outubro">
  <div class="azul cima" style="background-image:url(img/03-cima.jpg)"></div>
  <div class="miolo">
    <div class="moldura"><img src="img/03-azulejo.jpg" alt=""></div>
    <p class="it">O verão pediu branco.</p>
    <p class="t">Outubro pede tinto.</p>
    <div class="risca"></div>
    <p class="caps">Três tintos da nossa carta</p>
    <div class="vinhos">{vinhos}</div>
  </div>
  <div class="azul baixo" style="background-image:url(img/03-baixo.jpg)"></div>
</section>''')
    # 04 — a tábua
    out.append(f'''
<section class="slide" id="04-a-tabua">
  <img class="fundo" src="img/04.jpg" alt="">
  <div class="pilula">PARA PARTILHAR</div>
  <div class="faixa">
    <p class="t">E o tinto pede tábua.</p>
    <p class="it">Queijos e enchidos, para dois.</p>
  </div>
</section>''')
    # 05 — reservar
    out.append(f'''
<section class="slide" id="05-reservar">
  <img class="fundo" src="img/05.jpg" alt="">
  <div class="faixa alta">
    <p class="t">Venha pelo tacho.</p>
    <p class="it">Fique pelo tinto.</p>
    <p class="botao">RESERVE A SUA MESA</p>
    <p class="wa">WhatsApp<span>{e(c["whatsapp"])}</span></p>
    <p class="morada">{e(c["jantar"])}</p>
    <p class="morada" style="margin-top:4px">{e(c["morada"])}{PONTO}{e(c["terra"])}{PONTO}{e(c["site"])}</p>
  </div>
</section>''')
    return "".join(out)


def pagina():
    fontes = (fonte("Caladea", "normal", 700, "caladea-700.woff2")
              + fonte("Caladea", "italic", 400, "caladea-400-italic.woff2")
              + fonte("Open Sans", "normal", "300 800", "open-sans-variable.woff2"))
    return f'''<!doctype html>
<html lang="pt-PT"><head><meta charset="utf-8">
<title>Bom Paladar — carrossel de outono</title>
<style>{fontes}{CSS}</style></head>
<body>{slides()}
</body></html>'''


def folha(nomes):
    """Folha de revisão: os 5 slides lado a lado + a capa a 150 px (como aparece na grelha do perfil)."""
    th = 460
    tw = round(th * W / H)
    gap, pad, leg = 24, 32, 34
    ims = [Image.open(AQUI / f"{n}.png").convert("RGB").resize((tw, th), Image.LANCZOS) for n in nomes]
    capa = Image.open(AQUI / f"{nomes[0]}.png").convert("RGB").resize((150, round(150 * H / W)), Image.LANCZOS)
    largura = pad * 2 + len(ims) * tw + (len(ims) - 1) * gap + gap + 150
    f = Image.new("RGB", (largura, pad * 2 + th + leg), (27, 27, 27))
    d = ImageDraw.Draw(f)
    try:
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    except OSError:
        fnt = ImageFont.load_default()
    x = pad
    for n, im in zip(nomes, ims):
        f.paste(im, (x, pad))
        d.text((x, pad + th + 10), f"{n}.png", fill=(214, 178, 94), font=fnt)
        x += tw + gap
    f.paste(capa, (x, pad))
    d.text((x, pad + capa.height + 10), "capa a 150 px", fill=(214, 178, 94), font=fnt)
    f.save(AQUI / "folha-revisao.png")


def main():
    if "--baixar" in sys.argv:
        baixar()
    modo = preparar()
    (AQUI / "carrossel.html").write_text(pagina(), encoding="utf-8")
    subprocess.run(["node", str(AQUI / "shot.js"), str(AQUI / "carrossel.html"), str(AQUI), "--slides"],
                   check=True, cwd=AQUI,
                   env={**__import__("os").environ,
                        "NODE_PATH": subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()})
    nomes = ["01-capa", "02-o-lume", "03-outubro", "04-a-tabua", "05-reservar"]
    folha(nomes)
    print("modo:", modo)


if __name__ == "__main__":
    main()
