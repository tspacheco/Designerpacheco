#!/usr/bin/env python3
"""QR para imprimir. Aponta para o mesmo endereço do cartão: https://ro.pachecost.com/C
(o Netlify reencaminha /C para a página romena; o destino muda em ../dados.json → destino_qr, sem reimprimir).

    python3 marca/qr/gerar.py

Saídas (nesta pasta):
  qr-ro-pachecost.pdf     QR vetorial, preto sobre branco, 50 × 50 mm com a margem branca incluída (gráfica)
  qr-ro-pachecost.svg     o mesmo em SVG (designer, Canva, Illustrator)
  qr-ro-pachecost.png     1980 × 1980 px a 600 ppp (Word, Canva, redes)
  qr-autocolante.pdf      autocolante da marca, 55 × 85 mm + 3 mm de sangria, em romeno
  qr-autocolante.png      o autocolante a 600 ppp, com sangria (para gráficas online que pedem PNG)
  qr-autocolante-preview.png   o autocolante já cortado, para ver
  qr-teste-a4.pdf         folha A4 para imprimir em casa: 5 tamanhos, régua de 100 mm e lista de verificação

Testes que correm sempre: cada PDF é renderizado outra vez (pdfium, como uma impressora) e cada QR tem de ser
lido como um telemóvel o vê — de perto, a meia distância e desfocado; o QR do cartão final também.
Tamanho de cada página; zona de silêncio (4 módulos) sem tinta; nada a menos de 4 mm do corte; letra ≥ 7,5 pt;
contraste ≥ 4,5:1; todas as letras existem nas fontes (Ă, Ș, Ț incluídos); régua com 100 mm.
Requer: segno opencv-python-headless fonttools brotli pypdfium2 ; Playwright global (/opt/node22/lib/node_modules).
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import cv2
import numpy as np
import pypdfium2 as pdfium
import segno
from fontTools.ttLib import TTFont
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
MARCA = os.path.dirname(AQUI)
FONTES = os.path.join(MARCA, "fontes")
NODE_ENV = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
LATIN_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,"
             "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF")
FICHEIROS_FONTE = {
    ("Archivo Black", 400): ["archivo-black.woff2", "archivo-black-latin-ext.woff2"],
    ("Space Mono", 400): ["space-mono-400.woff2", "space-mono-400-latin-ext.woff2"],
    ("Space Mono", 700): ["space-mono-700.woff2", "space-mono-700-latin-ext.woff2"],
}
MARGEM = 4          # zona de silêncio: 4 módulos (norma ISO/IEC 18004)
PX_MODULO = 60      # PNG: 60 px por módulo, sem antialiasing
PPP = 600

FONT_FACES = "\n".join(
    f'@font-face{{font-family:"{fam}";font-weight:{peso};src:url("../fontes/{fs[0]}") format("woff2")}}\n'
    f'@font-face{{font-family:"{fam}";font-weight:{peso};src:url("../fontes/{fs[1]}") format("woff2");unicode-range:{LATIN_EXT}}}'
    for (fam, peso), fs in FICHEIROS_FONTE.items())
TOKENS = """:root{--carvao:#141210;--osso:#EFEAE3;--laranja:#E8622C;
  --tinta-2:#4D4A47;        /* texto secundário sobre osso — 7,4:1 */
  --laranja-tinta:#A64923;  /* texto laranja sobre osso — 4,9:1 */
  --laranja-traco:#D35A29;  /* traços e pontos sobre osso — 3,3:1 */}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#fff}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:"Space Mono",monospace;
  font-kerning:normal;text-rendering:geometricPrecision}
.so-leitor{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.ponto{display:inline-block;width:1.9mm;height:1.9mm;border-radius:50%;background:var(--laranja-traco);flex:none}
.pf{display:inline-block;width:.21em;height:.21em;border-radius:50%;background:var(--laranja-tinta);margin-left:.07em}
.o{color:var(--laranja-tinta)}
svg.qr{display:block;shape-rendering:crispEdges}"""


def caminho(m):
    """Módulos escuros → um só path SVG (uma linha de retângulos por fila)."""
    partes = []
    for y, linha in enumerate(m):
        x, n = 0, len(linha)
        while x < n:
            if linha[x]:
                x0 = x
                while x < n and linha[x]:
                    x += 1
                partes.append(f"M{x0} {y}h{x - x0}v1h-{x - x0}z")
            else:
                x += 1
    return "".join(partes)


def qr_inline(d, n, url, cor, classe="qr"):
    """QR sem margem (a margem é o espaço à volta, na página), para pôr dentro de HTML."""
    return (f'<svg class="{classe}" viewBox="0 0 {n} {n}" role="img" aria-label="QR: {html.escape(url.lower())}">'
            f'<path fill="{cor}" d="{d}"/></svg>')


def montar(src, valores):
    return re.sub(r"\{\{([A-Z_0-9]+)\}\}", lambda m: valores[m.group(1)], src)


def frase_html(s):
    """*palavras* → laranja; ponto final → ponto laranja da marca (igual ao cartão)."""
    ponto = s.rstrip("*").endswith(".")
    if ponto:
        i = len(s.rstrip("*")) - 1
        s = s[:i] + s[i + 1:]
    partes = re.split(r"\*([^*]+)\*", s)
    out = "".join(f'<span class="o">{html.escape(p)}</span>' if k % 2 else html.escape(p) for k, p in enumerate(partes))
    if ponto:
        out += '<span class="pf" aria-hidden="true"></span><span class="so-leitor">.</span>'
    return out


AUTOCOLANTE = """<!DOCTYPE html>
<!-- Autocolante 55 × 85 mm + 3 mm de sangria (61 × 91 mm). Gerado por marca/qr/gerar.py — não editar à mão. -->
<html lang="ro">
<head>
<meta charset="utf-8">
<title>Pacheco Studios — autocolante QR</title>
<style>
{{FONT_FACES}}
{{TOKENS}}
@page{size:61mm 91mm;margin:0}
/* medidas a partir do canto da página; o corte está a 3 mm de cada lado */
.face{position:relative;width:61mm;height:91mm;overflow:hidden;background:var(--osso);color:var(--carvao)}
.marca{position:absolute;left:13mm;top:9mm;display:flex;align-items:center;gap:1.7mm;
  font-weight:700;font-size:7.5pt;letter-spacing:.2em;line-height:1}
/* QR de 35 mm (módulo 1,4 mm), centrado: 10 mm de osso de cada lado depois do corte (a zona de silêncio pede 5,6) */
.qr-caixa{position:absolute;left:13mm;top:17.5mm;width:35mm;height:35mm}
.qr-caixa svg{width:100%;height:100%}
.legenda{position:absolute;left:13mm;top:58.9mm;line-height:1}
.legenda b{display:block;font-size:9pt;letter-spacing:.05em}
.legenda span{display:block;margin-top:1.5mm;font-size:8.5pt;color:var(--tinta-2)}
.frase{position:absolute;left:13mm;right:7mm;bottom:9mm;font-family:"Archivo Black",sans-serif;font-size:13pt;
  line-height:1.08;letter-spacing:.005em;text-transform:uppercase;text-wrap:balance}
</style>
</head>
<body>
<div class="face">
  <p class="marca"><span class="ponto" aria-hidden="true"></span>PACHECO STUDIOS</p>
  <div class="qr-caixa" data-qr="{{MODULOS}}" data-nome="autocolante">{{QR}}</div>
  <p class="legenda"><b>{{LEGENDA}}</b><span>{{DOMINIO}}</span></p>
  <p class="frase">{{FRASE}}</p>
</div>
</body>
</html>
"""

SIMPLES = """<!DOCTYPE html>
<!-- QR 50 × 50 mm com a margem branca incluída. Gerado por marca/qr/gerar.py — não editar à mão. -->
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<title>QR — {{URL}}</title>
<style>
@page{size:50mm 50mm;margin:0}
*{margin:0;padding:0}
html,body{background:#fff}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.face{width:50mm;height:50mm;background:#fff}
.face svg{display:block;width:50mm;height:50mm}
</style>
</head>
<body>
<div class="face" data-qr="{{N_TOTAL}}" data-nome="simples">{{SVG}}</div>
</body>
</html>
"""

TESTE = """<!DOCTYPE html>
<!-- Folha de teste A4. Gerado por marca/qr/gerar.py — não editar à mão. -->
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<title>QR — folha de teste</title>
<style>
{{FONT_FACES}}
{{TOKENS}}
@page{size:210mm 297mm;margin:0}
.face{position:relative;width:210mm;height:297mm;padding:14mm 15mm;background:#fff;color:#141210}
.marca{display:flex;align-items:center;gap:1.7mm;font-weight:700;font-size:8pt;letter-spacing:.2em;line-height:1}
h1{margin-top:6mm;font-family:"Archivo Black",sans-serif;font-weight:400;font-size:20pt;line-height:1.1;
  text-transform:uppercase;max-width:170mm}
.info{margin-top:4mm;font-size:9pt;line-height:1.5;max-width:172mm;color:#3B3936}
.info b{color:#141210}
.regua{margin-top:7mm;display:flex;align-items:flex-end;gap:5mm}
.regua svg{display:block;width:100mm;height:7mm;flex:none;overflow:visible}
.regua p{font-size:8pt;line-height:1.45;color:#3B3936}
.fila{margin-top:8mm;display:flex;align-items:flex-end;gap:5mm}
figure{flex:none}
.q{background:#fff;padding:var(--m)}
.q svg{width:var(--s);height:var(--s)}
figcaption{margin-top:1mm;padding-left:var(--m);font-size:8pt;line-height:1.35}
figcaption b{display:block;font-size:9pt}
.baixo{margin-top:6mm;display:flex;gap:7mm;align-items:flex-start}
.lista{padding-top:6mm;font-size:9pt;line-height:1.45}
.lista h2{font-size:9pt;letter-spacing:.14em;text-transform:uppercase;margin-bottom:3mm}
.lista li{list-style:none;display:flex;gap:2.5mm;margin-bottom:3mm}
.lista li::before{content:"";flex:none;width:3.6mm;height:3.6mm;margin-top:.5mm;border:.35mm solid #141210}
.lista p{margin-top:5mm;font-size:8pt;color:#3B3936}
</style>
</head>
<body>
<div class="face">
  <p class="marca"><span class="ponto" aria-hidden="true"></span>PACHECO STUDIOS · QR · FOLHA DE TESTE</p>
  <h1>Imprimir a 100&nbsp;% e ler cada QR com dois telemóveis</h1>
  <p class="info">Todos abrem <b>{{URL_LEGIVEL}}</b>, que o Netlify reencaminha para a página romena. É o mesmo QR do
    cartão. Enquanto o site não estiver publicado com o domínio <b>{{DOMINIO}}</b>, o telemóvel lê o QR mas a página
    não abre.</p>
  <div class="regua">
    <svg data-regua viewBox="0 0 100 7" aria-label="Régua de 100 mm">{{REGUA}}</svg>
    <p>Esta régua tem de medir 100&nbsp;mm. Se medir menos, a impressora reduziu a folha: desligar «Ajustar à página».</p>
  </div>
  <div class="fila">{{FILA}}</div>
  <div class="baixo">{{GRANDE}}
    <div class="lista">
      <h2>Antes de mandar imprimir</h2>
      <ul>
        <li>A régua mede 100&nbsp;mm.</li>
        <li>Os cinco QR abrem a página num iPhone e num Android.</li>
        <li>O de 21&nbsp;mm (o do cartão) lê-se a um palmo de distância.</li>
        <li>A página abre em romeno e o «Înapoi» volta aos projetos.</li>
      </ul>
      <p>Regra prática: um QR lê-se até cerca de 10 vezes o seu tamanho. 21&nbsp;mm dá uns 20&nbsp;cm; 80&nbsp;mm, quase 1&nbsp;m.</p>
    </div>
  </div>
</div>
</body>
</html>
"""


def figura(d, n, url, s, rotulo, nota):
    """QR de s mm com a margem branca (4 módulos) à volta; a caixa medida inclui a margem."""
    m = s * MARGEM / n
    return (f'<figure style="--s:{s}mm;--m:{m:.3f}mm"><div class="q" data-qr="{n + 2 * MARGEM}" data-nome="{s} mm">'
            f'{qr_inline(d, n, url, "#000")}</div><figcaption><b>{rotulo}</b>{nota}</figcaption></figure>')


def regua_svg():
    riscos = ['<path d="M0 7H100" stroke="#141210" stroke-width=".35"/>']
    for mm in range(0, 101):
        alto = 4 if mm % 10 == 0 else (2.6 if mm % 5 == 0 else 1.6)
        riscos.append(f'<path d="M{mm} 7V{7 - alto}" stroke="#141210" stroke-width="{.3 if mm % 10 == 0 else .18}"/>')
    riscos.append('<text x="0" y="1.2" font-family="Space Mono" font-size="2.7" fill="#141210">0</text>')
    riscos.append('<text x="100" y="1.2" text-anchor="end" font-family="Space Mono" font-size="2.7" fill="#141210">100 mm</text>')
    return "".join(riscos)


def render(html_path, pdf, png=None, ppp=PPP):
    args = ["node", os.path.join(AQUI, "render.cjs"), html_path, pdf] + ([png, str(ppp)] if png else [])
    r = subprocess.run(args, env=NODE_ENV, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"render.cjs falhou em {os.path.basename(html_path)}:\n{r.stderr}")
    return json.loads(r.stdout)


def pagina_png(pdf, i=0, ppp=PPP):
    doc = pdfium.PdfDocument(pdf)
    try:
        pg = doc[i]
        w, h = pg.get_size()
        img = pg.render(scale=ppp / 72).to_pil().convert("RGB")
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR), (w * 25.4 / 72, h * 25.4 / 72), len(doc)
    finally:
        doc.close()


def ler(img, url, qr_mm, pxmm):
    """Lê o QR como um telemóvel o vê: de perto (~400 px de QR), a meia distância (~120 px) e desfocado.
    Devolve [(nome, texto, ok)]. (O detetor do OpenCV falha com QR enormes, acima de ~1500 px: não é o QR.)"""
    det = cv2.QRCodeDetector()
    h, w = img.shape[:2]

    def escala(alvo):
        f = min(1.0, alvo / (qr_mm * pxmm))
        return cv2.resize(img, (max(1, int(w * f)), max(1, int(h * f))), interpolation=cv2.INTER_AREA)
    pequeno = escala(120)
    out = []
    for nome, im in (("de perto (~400 px)", escala(400)), ("câmara (~120 px)", pequeno),
                     ("câmara desfocada", cv2.GaussianBlur(pequeno, (3, 3), 1.0))):
        txt, _, _ = det.detectAndDecode(im)
        out.append((nome, txt, txt.upper() == url))
    return out


def recorte(img, mm, pxmm, folga_mm):
    x0, y0, x1, y1 = (round(v * pxmm) for v in (mm[0] - folga_mm, mm[1] - folga_mm, mm[2] + folga_mm, mm[3] + folga_mm))
    return img[max(0, y0):y1, max(0, x0):x1]


def main():
    d = json.load(open(os.path.join(MARCA, "dados.json"), encoding="utf-8"))
    c = d["cartao"]
    dominio = d["dominio"].strip().lower()
    cam = d["caminho_qr"].strip("/")
    # Igual ao cartão: maiúsculas → modo alfanumérico do QR (menos módulos, módulos maiores).
    url = f"HTTPS://{dominio.upper()}/{cam.upper()}"
    url_legivel = f"https://{dominio}/{cam.upper()}"
    qr = segno.make(url, error="q", micro=False)
    m = [list(l) for l in qr.matrix]
    n = len(m)
    total = n + 2 * MARGEM
    d_qr = caminho(m)
    d_total = caminho([[0] * total] * MARGEM + [[0] * MARGEM + l + [0] * MARGEM for l in m] + [[0] * total] * MARGEM)
    ok = True
    print(f"QR  {url}  → versão {qr.version}-{qr.error.upper()}, {n}×{n} módulos (+{MARGEM} de margem = {total})")
    if not d.get("dominio_confirmado"):
        print("  ⚠ dominio_confirmado: false em marca/dados.json — confirmar que o domínio abre antes de imprimir")

    # ——— SVG e PNG simples: preto sobre branco, margem incluída ———
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="50mm" height="50mm" viewBox="0 0 {total} {total}" '
           f'shape-rendering="crispEdges" role="img" aria-label="QR: {html.escape(url_legivel)}">'
           f'<title>Pacheco Studios — {html.escape(url_legivel)}</title>'
           f'<rect width="{total}" height="{total}" fill="#fff"/><path fill="#000" d="{d_total}"/></svg>\n')
    open(os.path.join(AQUI, "qr-ro-pachecost.svg"), "w", encoding="utf-8").write(svg)
    grelha = np.full((total, total), 255, np.uint8)
    grelha[MARGEM:MARGEM + n, MARGEM:MARGEM + n] = np.where(np.array(m, dtype=bool), 0, 255)
    png = np.kron(grelha, np.ones((PX_MODULO, PX_MODULO), np.uint8))
    Image.fromarray(png).save(os.path.join(AQUI, "qr-ro-pachecost.png"), dpi=(PPP, PPP), optimize=True)

    tmp = tempfile.mkdtemp(dir=AQUI, prefix=".render-")
    try:
        def escrever(nome, texto):
            p = os.path.join(tmp, nome)
            # os ficheiros temporários ficam numa subpasta: as fontes estão um nível mais acima
            open(p, "w", encoding="utf-8").write(texto.replace('url("../fontes/', 'url("../../fontes/'))
            return p

        comum = {"FONT_FACES": FONT_FACES, "TOKENS": TOKENS, "DOMINIO": html.escape(dominio)}
        medidas = {}
        medidas["simples"] = render(escrever("simples.html", montar(SIMPLES, {"URL": html.escape(url_legivel),
                                    "N_TOTAL": str(total), "SVG": svg})), os.path.join(AQUI, "qr-ro-pachecost.pdf"))
        frase = c["frases"][int(c.get("frase", 1)) - 1]
        medidas["autocolante"] = render(
            escrever("autocolante.html", montar(AUTOCOLANTE, dict(comum, MODULOS=str(n), QR=qr_inline(d_qr, n, url, "var(--carvao)"),
                     LEGENDA=html.escape(c["legenda_qr"].upper()), FRASE=frase_html(frase)))),
            os.path.join(AQUI, "qr-autocolante.pdf"), os.path.join(AQUI, "qr-autocolante.png"))
        fila = "".join(figura(d_qr, n, url, s, f"{s} mm", nota) for s, nota in
                       ((15, "o mínimo"), (21, "o do cartão"), (35, "o do autocolante"), (50, "flyer, porta")))
        grande = figura(d_qr, n, url, 80, "80 mm", "montra, balcão, cartaz")
        medidas["teste"] = render(escrever("teste.html", montar(TESTE, dict(comum, URL_LEGIVEL=html.escape(url_legivel),
                                  REGUA=regua_svg(), FILA=fila, GRANDE=grande))), os.path.join(AQUI, "qr-teste-a4.pdf"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # pré-visualização do autocolante já cortado (sem os 3 mm de sangria)
    im = Image.open(os.path.join(AQUI, "qr-autocolante.png"))
    pxmm = im.width / 61
    corte = im.crop((round(3 * pxmm), round(3 * pxmm), round(58 * pxmm), round(88 * pxmm)))
    corte.resize((corte.width // 3, corte.height // 3), Image.LANCZOS).save(os.path.join(AQUI, "qr-autocolante-preview.png"), optimize=True)

    # ——— testes ———
    cmaps = {k: set().union(*(TTFont(os.path.join(FONTES, f)).getBestCmap() for f in fs)) for k, fs in FICHEIROS_FONTE.items()}
    for peca in ("autocolante", "teste"):
        print(f"\nTEXTO · {peca}")
        antes = ok
        for r in medidas[peca]["textos"]:
            texto = r["t"].upper() if r["tt"] == "uppercase" else r["t"]
            cmap = cmaps.get((r["familia"], r["peso"]))
            sem = sorted({ch for ch in texto if not ch.isspace() and (cmap is None or ord(ch) not in cmap)})
            marca = ""
            if r["pt"] < 7.5 or r["contraste"] < 4.5 or sem:
                marca, ok = "  ✗" + (f" letras sem glifo: {''.join(sem)}" if sem else ""), False
            if peca == "autocolante" or marca:
                print(f"  {r['pt']:>5} pt  {r['contraste']:>5}:1  {r['familia']} {r['peso']}  {r['t'][:48]}{marca}")
        if peca == "teste" and ok == antes:
            print(f"  ✓ {len(medidas[peca]['textos'])} textos: letra ≥ 7,5 pt, contraste ≥ 4,5:1, todas as letras nas fontes")

    print("\nPDF → renderizado de novo (pdfium, 600 ppp) → leitura")
    esperado = {"qr-ro-pachecost.pdf": (50, 50), "qr-autocolante.pdf": (61, 91), "qr-teste-a4.pdf": (210, 297)}
    for nome, (ew, eh) in esperado.items():
        img, (w, h), paginas = pagina_png(os.path.join(AQUI, nome))
        pxmm = img.shape[1] / w
        tam_ok = abs(w - ew) < .3 and abs(h - eh) < .3 and paginas == 1
        ok &= tam_ok
        print(f"  {'✓' if tam_ok else '✗'} {nome}: {w:.1f} × {h:.1f} mm, {paginas} página(s)")
        chave = {"qr-ro-pachecost.pdf": "simples", "qr-autocolante.pdf": "autocolante", "qr-teste-a4.pdf": "teste"}[nome]
        for q in medidas[chave]["qrs"]:
            lado = (q["mm"][2] - q["mm"][0]) * (n / q["modulos"])       # lado do símbolo, sem margem
            corte = recorte(img, q["mm"], pxmm, 4 * lado / n if chave == "autocolante" else 0)
            res = ler(corte, url, lado, pxmm)
            passou = all(r[2] for r in res)
            ok &= passou
            falhou = [f"{r[0]}: {r[1] or '(não leu)'}" for r in res if not r[2]]
            print(f"    {'✓' if passou else '✗'} QR {q['nome']:<12} ({lado:.0f} mm, módulo {lado / n:.2f} mm)"
                  + (" lido de perto, a meia distância e desfocado" if passou else " — " + "; ".join(falhou)))
        if chave == "teste":
            rg = medidas["teste"]["regua"]
            comp = rg[2] - rg[0]
            passou = abs(comp - 100) < .2
            # e no PDF renderizado: a distância entre o primeiro e o último risco
            y0, y1, x0 = round((rg[3] - .5) * pxmm), round((rg[3] - .3) * pxmm), round((rg[0] - 1) * pxmm)
            faixa = img[y0:y1, x0:round((rg[2] + 1) * pxmm)]
            cols = np.nonzero((faixa.mean(axis=2) < 160).any(axis=0))[0]
            corridas = np.split(cols, np.nonzero(np.diff(cols) > 1)[0] + 1) if cols.size else []
            px = (corridas[-1].mean() - corridas[0].mean()) / pxmm if len(corridas) > 1 else 0
            passou &= abs(px - 100) < .3
            ok &= passou
            print(f"    {'✓' if passou else '✗'} régua: {comp:.2f} mm no desenho, {px:.2f} mm no PDF")
        if chave == "autocolante":
            fundo = img[round(5 * pxmm), round(5 * pxmm)].astype(int)
            # a última fila e coluna do bitmap são meio píxel de página (arredondamento), não tinta
            util = img[:int(h * pxmm) - 1, :int(w * pxmm) - 1].astype(int)
            tinta = np.abs(util - fundo).sum(axis=2) > 60
            seg = [round(v * pxmm) for v in (7, 7, 54, 84)]       # 3 mm de sangria + 4 mm de margem segura
            fora = tinta.copy()
            fora[seg[1]:seg[3], seg[0]:seg[2]] = False
            q = medidas["autocolante"]["qrs"][0]["mm"]
            mod = (q[2] - q[0]) / n
            anel = [round(v * pxmm) for v in (q[0] - 4 * mod, q[1] - 4 * mod, q[2] + 4 * mod, q[3] + 4 * mod)]
            dentro = [round(v * pxmm) + e for v, e in zip(q, (-3, -3, 3, 3))]
            zona = tinta[anel[1]:anel[3], anel[0]:anel[2]].copy()
            zona[dentro[1] - anel[1]:dentro[3] - anel[1], dentro[0] - anel[0]:dentro[2] - anel[0]] = False
            corte_ok = (anel[0] >= round(3 * pxmm) and anel[2] <= round(58 * pxmm)
                        and anel[1] >= round(3 * pxmm) and anel[3] <= round(88 * pxmm))
            passou = not fora.any() and not zona.any() and corte_ok
            ok &= passou
            print(f"    {'✓' if not fora.any() else '✗'} nada a menos de 4 mm do corte")
            print(f"    {'✓' if not zona.any() and corte_ok else '✗'} zona de silêncio livre e dentro do autocolante "
                  f"({4 * mod:.1f} mm exigidos; depois do corte ficam {q[0] - 3:.1f} mm de cada lado)")

    # PNG (60 px por módulo) e SVG (XML válido; é o mesmo desenho que foi lido no PDF simples)
    res = ler(cv2.imread(os.path.join(AQUI, "qr-ro-pachecost.png")), url, n * PX_MODULO, 1)
    import xml.etree.ElementTree as ET
    svg_ok = ET.parse(os.path.join(AQUI, "qr-ro-pachecost.svg")).getroot().tag.endswith("svg")
    passou = all(r[2] for r in res) and svg_ok
    ok &= passou
    print(f"  {'✓' if passou else '✗'} qr-ro-pachecost.png ({(n + 2 * MARGEM) * PX_MODULO} px, {PPP} ppp) lido; "
          f"qr-ro-pachecost.svg {'válido' if svg_ok else 'inválido'}")

    cartao = os.path.join(MARCA, "cartao", "cartao-impressao.pdf")
    if os.path.exists(cartao):
        img, (w, h), paginas = pagina_png(cartao, 1)
        res = ler(img, url, 21, img.shape[1] / w)
        passou = all(r[2] for r in res)
        ok &= passou
        print(f"  {'✓' if passou else '✗'} cartao-impressao.pdf (verso, {w:.0f} × {h:.0f} mm): o QR do cartão lê "
              f"{res[0][1] or '(nada)'} — o mesmo endereço")
    else:
        print("  ⚠ marca/cartao/cartao-impressao.pdf ainda não existe (python3 marca/cartao/gerar.py)")

    print("\n✓ Tudo lido. Pronto para imprimir." if ok else "\n✗ Há problemas — ver acima.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
