#!/usr/bin/env python3
"""Exporta cada direção da capa.html para PNG 1640×924 e monta as pré-visualizações (computador e telemóvel),
com o selo por cima no sítio aproximado onde o Facebook põe a foto de perfil."""
import asyncio, json, pathlib
from PIL import Image, ImageDraw, ImageFont
from playwright.async_api import async_playwright

AQUI = pathlib.Path(__file__).resolve().parent
SELO = AQUI.parent / "facebook-perfil-selo.png"
W, H, B0, B1 = 1640, 924, 150, 774
NOMES = {"a": "ondas", "b": "selo-aberto"}


async def capturar():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page(viewport={"width": W, "height": 2 * H + 80}, device_scale_factor=1)
        await pg.goto("file://" + str(AQUI / "capa.html"))
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(400)
        medidas = {}
        for d in ("a", "b"):
            el = await pg.query_selector(f"#{d}")
            await el.screenshot(path=str(AQUI / f"capa-facebook-{NOMES[d]}-1640x924.png"))
            medidas[d] = await pg.evaluate(f"""() => {{
              const c=document.getElementById('{d}').getBoundingClientRect();
              return [...document.querySelectorAll('#{d} .bloco > *')].map(e => {{ const r=e.getBoundingClientRect();
                return [e.className, Math.round(r.left-c.left), Math.round(r.top-c.top), Math.round(r.right-c.left), Math.round(r.bottom-c.top)] }}) }}""")
        print(json.dumps({"fontes": await pg.evaluate("[...document.fonts].map(f=>f.family+':'+f.status)")}, ensure_ascii=False))
        await b.close()
        return medidas


def redondo(img, d):
    s = img.convert("RGBA").resize((d, d), Image.LANCZOS)
    m = Image.new("L", (d, d), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
    s.putalpha(m)
    aro = Image.new("RGBA", (d + 12, d + 12), (0, 0, 0, 0))
    ImageDraw.Draw(aro).ellipse((0, 0, d + 11, d + 11), fill=(255, 255, 255, 255))
    aro.paste(s, (6, 6), s)
    return aro


def previsualizar(d):
    capa = Image.open(AQUI / f"capa-facebook-{NOMES[d]}-1640x924.png").convert("RGB")
    selo = Image.open(SELO)
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    # computador: faixa central, 1250 px de largura, foto de perfil de 168 px a meio da aresta de baixo
    pc = capa.crop((0, B0, W, B1)).resize((1250, round(1250 * 624 / 1640)), Image.LANCZOS)
    tela_pc = Image.new("RGB", (1250, pc.height + 150), "#F0F2F5")
    tela_pc.paste(pc, (0, 0))
    av = redondo(selo, 168)
    tela_pc.paste(av, (24, pc.height - 90), av)
    dr = ImageDraw.Draw(tela_pc)
    dr.text((214, pc.height + 18), "Pacheco Studios", fill="#050505", font=f1)
    dr.text((214, pc.height + 58), "Computador (aproximado)", fill="#65676B", font=f2)
    # telemóvel: imagem inteira a 390 pt (×3), foto de perfil grande a sobrepor o canto inferior esquerdo
    mw = 1170
    mo = capa.resize((mw, round(mw * H / W)), Image.LANCZOS)
    tela_mo = Image.new("RGB", (mw, mo.height + 330), "#FFFFFF")
    tela_mo.paste(mo, (0, 0))
    av2 = redondo(selo, 400)
    tela_mo.paste(av2, (36, mo.height - 230), av2)
    dr2 = ImageDraw.Draw(tela_mo)
    f3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
    f4 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    dr2.text((40, mo.height + 200), "Pacheco Studios", fill="#050505", font=f3)
    dr2.text((40, mo.height + 268), "Telemóvel (aproximado)", fill="#65676B", font=f4)
    tela_pc.save(AQUI / f"previa-{NOMES[d]}-computador.png")
    tela_mo.save(AQUI / f"previa-{NOMES[d]}-telemovel.png")


medidas = asyncio.run(capturar())
for d, linhas in medidas.items():
    print(d, "faixa do computador y", B0, "–", B1)
    for cls, x0, y0, x1, y1 in linhas:
        avisos = []
        if y0 < B0 + 20 or y1 > B1 - 20: avisos.append("FORA DA FAIXA")
        if x1 > W - 60: avisos.append("COLADO À DIREITA")
        print(f"   {cls:<9} x {x0:4d}–{x1:4d}  y {y0:3d}–{y1:3d}  {' '.join(avisos)}")
    previsualizar(d)
print("ok")
