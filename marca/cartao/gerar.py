#!/usr/bin/env python3
"""Gera o cartão de visita da Pacheco Studios a partir de ../dados.json (contactos + bloco "cartao").

    python3 gerar.py

Saídas (nesta pasta):
  cartao.html                    fonte renderizável (não editar — editar cartao.src.html)
  cartao-impressao.pdf           PDF para a gráfica: 2 páginas (frente, verso), 91×61 mm com 3 mm de sangria
  cartao-impressao-PROVA.pdf     o mesmo com faixa "PROVA" enquanto faltar telefone ou domínio confirmado
  cartao-preview.png             frente e verso lado a lado, já cortados (85×55 mm)
  frases-opcoes.png              o verso com cada uma das frases de dados.json, para escolher
  face-frente/verso-600ppp.png   cada face a 600 ppp, com sangria
  acessibilidade.json            tamanho, contraste, fonte e posição (mm) de cada texto

Testes que correm sempre: letra ≥ 7,5 pt; contraste ≥ 4,5:1; nenhum texto fora da margem segura, sobreposto
a outro ou dentro da zona de silêncio do QR; todas as letras existem na fonte (Ă, Ș, Ț do romeno incluídos); e o QR
tem de ser lido a partir da imagem renderizada — em alta resolução, ao tamanho de uma câmara de telemóvel e desfocado.
Requer: pip install segno opencv-python-headless fonttools brotli ; Playwright global (/opt/node22/lib/node_modules).
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
import segno
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "..", "fontes")
NODE_ENV = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
TEL_PROVISORIO = "+351 9XX XXX XXX"
LATIN_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,"
             "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF")
FICHEIROS_FONTE = {  # (família, peso) → ficheiros (base + latin-ext)
    ("Archivo Black", 400): ["archivo-black.woff2", "archivo-black-latin-ext.woff2"],
    ("Space Mono", 400): ["space-mono-400.woff2", "space-mono-400-latin-ext.woff2"],
    ("Space Mono", 700): ["space-mono-700.woff2", "space-mono-700-latin-ext.woff2"],
}


def formatar_telefone(t):
    """Mostra sempre o indicativo português: +351 967 117 357."""
    d = re.sub(r"\D", "", t)
    if len(d) == 9:
        d = "351" + d
    if d.startswith("351") and len(d) == 12:
        return f"+351 {d[3:6]} {d[6:9]} {d[9:]}"
    return t.strip()


def frase_html(s):
    """*palavras* → laranja; ponto final → ponto laranja da marca."""
    ponto = s.rstrip("*").endswith(".")
    if ponto:
        i = len(s.rstrip("*")) - 1
        s = s[:i] + s[i + 1:]
    partes = re.split(r"\*([^*]+)\*", s)
    out = "".join(f'<span class="o">{html.escape(p)}</span>' if k % 2 else html.escape(p) for k, p in enumerate(partes))
    if ponto:
        out += '<span class="pf" aria-hidden="true"></span><span class="so-leitor">.</span>'
    return out


def slogan_html(linhas):
    out = []
    for l in linhas:
        h = frase_html(l)
        out.append(f"<span>{h}</span>")
    return "".join(out)


def qr_svg(url):
    """QR em SVG vetorial (um só path), sem margem: a zona de silêncio é o próprio fundo do cartão."""
    qr = segno.make(url, error="q", micro=False)
    m = qr.matrix
    n = len(m)
    partes = []
    for y, linha in enumerate(m):
        x = 0
        while x < n:
            if linha[x]:
                x0 = x
                while x < n and linha[x]:
                    x += 1
                partes.append(f"M{x0} {y}h{x - x0}v1h-{x - x0}z")
            else:
                x += 1
    svg = (f'<svg viewBox="0 0 {n} {n}" role="img" aria-label="QR: {html.escape(url.lower())}">'
           f'<path fill="var(--carvao)" d="{"".join(partes)}"/></svg>')
    return svg, qr.version, qr.error, n


def montar(src, valores):
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: valores[m.group(1)], src)


def main():
    d = json.load(open(os.path.join(AQUI, "..", "dados.json"), encoding="utf-8"))
    c = d["cartao"]
    dominio = d["dominio"].strip().lower()
    caminho = d["caminho_qr"].strip("/")
    # Maiúsculas → modo alfanumérico do QR: menos módulos, módulos maiores, leitura mais fácil.
    url_qr = f"HTTPS://{dominio.upper()}/{caminho.upper()}"
    svg, versao, erro, modulos = qr_svg(url_qr)

    falta = []
    tel = d.get("telefone", "").strip()
    if not tel:
        falta.append("TELEFONE")
    if not d.get("dominio_confirmado"):
        falta.append("DOMÍNIO")
    escolha = int(c.get("frase", 1))
    frases = c["frases"]
    if not 1 <= escolha <= len(frases):
        raise SystemExit(f"dados.json: 'frase' tem de ser de 1 a {len(frases)}")

    valores = {
        "LINGUA": c.get("lingua", "pt-PT"), "LATIN_EXT": LATIN_EXT,
        "NOME": html.escape(d["nome"].upper()), "FUNCAO": html.escape(c["funcao"]),
        "TELEFONE": html.escape(formatar_telefone(tel) if tel else TEL_PROVISORIO),
        "WHATSAPP": '<span class="r">WhatsApp</span>' if d.get("telefone_tem_whatsapp") else "",
        "EMAIL": html.escape(d["email"]), "INSTAGRAM": html.escape(d["instagram"].lstrip("@")),
        "DOMINIO": html.escape(dominio), "REGIAO": html.escape(c["regiao"].upper()),
        "PROPOSITO": html.escape(c["proposito"].upper()), "SLOGAN": slogan_html(c["slogan"]),
        "LEGENDA_QR": html.escape(c["legenda_qr"]), "QR_SVG": svg,
        "FRASE": frase_html(frases[escolha - 1]),
        "PROVA": "PROVA · FALTA: " + " E ".join(falta) if falta else "",
        "ROTULO_FRENTE": "FRENTE", "ROTULO_VERSO": f"VERSO · FRASE {escolha}",
    }
    src = open(os.path.join(AQUI, "cartao.src.html"), encoding="utf-8").read()
    open(os.path.join(AQUI, "cartao.html"), "w", encoding="utf-8").write(montar(src, valores))

    for antigo in ("cartao-impressao.pdf", "cartao-impressao-PROVA.pdf"):
        p = os.path.join(AQUI, antigo)
        if os.path.exists(p):
            os.remove(p)
    subprocess.run(["node", os.path.join(AQUI, "render.cjs"), os.path.join(AQUI, "cartao.html"), AQUI,
                    "1" if falta else "0"], check=True, env=NODE_ENV)

    # ——— folha com as frases todas, para escolher ———
    tmp = tempfile.mkdtemp(dir=AQUI, prefix=".opcoes-")
    try:
        ficheiros = []
        for i, f in enumerate(frases, 1):
            p = os.path.join(tmp, f"opcao-{i}.html")
            v = dict(valores, FRASE=frase_html(f), PROVA="")
            open(p, "w", encoding="utf-8").write(montar(src, v).replace('url("../fontes/', 'url("../../fontes/'))
            ficheiros.append(p)
        subprocess.run(["node", os.path.join(AQUI, "render.cjs"), "--verso", tmp, *ficheiros], check=True, env=NODE_ENV)
        pt = c.get("frases_pt", [""] * len(frases))
        cartoes = "".join(
            f'<figure{" class=esc" if i == escolha else ""}><img src="verso-{i}.png"><figcaption><b>{i}</b>'
            f'<span>{html.escape(frases[i - 1].replace("*", ""))}<i>{html.escape(pt[i - 1])}</i></span>'
            f'{"<em>no cartão</em>" if i == escolha else ""}</figcaption></figure>' for i in range(1, len(frases) + 1))
        folha = f"""<!DOCTYPE html><html lang="pt-PT"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Space Mono";font-weight:400;src:url("../../fontes/space-mono-400.woff2")}}
@font-face{{font-family:"Space Mono";font-weight:400;src:url("../../fontes/space-mono-400-latin-ext.woff2");unicode-range:{LATIN_EXT}}}
@font-face{{font-family:"Space Mono";font-weight:700;src:url("../../fontes/space-mono-700.woff2")}}
@font-face{{font-family:"Space Mono";font-weight:700;src:url("../../fontes/space-mono-700-latin-ext.woff2");unicode-range:{LATIN_EXT}}}
body{{margin:0;padding:48px;background:#D8D2C9;font-family:"Space Mono",monospace;color:#141210;width:1500px}}
h1{{font-size:22px;letter-spacing:.2em;margin:0 0 36px}}
main{{display:grid;grid-template-columns:1fr 1fr;gap:44px 40px}}
figure{{margin:0}} img{{width:100%;display:block;box-shadow:0 2px 4px rgba(20,18,16,.18),0 10px 24px rgba(20,18,16,.16)}}
figcaption{{display:flex;gap:16px;align-items:baseline;margin-top:16px;font-size:18px;line-height:1.4}}
figcaption b{{font-size:30px;line-height:1}} figcaption i{{display:block;font-style:normal;color:#4D4A47;font-size:16px}}
figcaption em{{margin-left:auto;font-style:normal;font-weight:700;font-size:14px;letter-spacing:.14em;text-transform:uppercase;
  background:#141210;color:#EFEAE3;padding:6px 12px;border-radius:99px;white-space:nowrap}}
.esc img{{outline:6px solid #E8622C;outline-offset:6px}}
</style></head><body><h1>FRASE DO VERSO — 5 OPÇÕES</h1><main>{cartoes}</main></body></html>"""
        pf = os.path.join(tmp, "folha.html")
        open(pf, "w", encoding="utf-8").write(folha)
        subprocess.run(["node", "-e", """
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1596, height: 900 } });
  await p.goto('file://' + process.argv[1]); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: process.argv[2], fullPage: true }); await b.close(); })();
""", pf, os.path.join(AQUI, "frases-opcoes.png")], check=True, env=NODE_ENV)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ——— testes ———
    ok = True
    rel = json.load(open(os.path.join(AQUI, "acessibilidade.json"), encoding="utf-8"))
    cmaps = {k: set().union(*(TTFont(os.path.join(FONTES, f)).getBestCmap() for f in fs)) for k, fs in FICHEIROS_FONTE.items()}
    print(f"\nTEXTO ({len(rel['textos'])} elementos)")
    for r in rel["textos"]:
        marca = ""
        texto = r["t"].upper() if r["tt"] == "uppercase" else r["t"]
        cmap = cmaps.get((r["familia"], r["peso"]))
        sem = sorted({ch for ch in texto if not ch.isspace() and (cmap is None or ord(ch) not in cmap)})
        if r["pt"] < 7.5 or r["contraste"] < 4.5 or sem:
            marca, ok = "  ✗" + (f" letras sem glifo: {''.join(sem)}" if sem else ""), False
        elif r["contraste"] < 7:
            marca = "  (AA)"
        print(f"  {r['face']:6} {r['pt']:>5} pt  {r['contraste']:>5}:1  {r['t'][:40]}{marca}")
    for e in rel["erros"]:
        ok = False
        print("  ✗ " + e)

    # ——— tinta real (píxeis a 600 ppp): margem segura de 4 mm do corte e zona de silêncio do QR ———
    for face in ("frente", "verso"):
        im = cv2.imread(os.path.join(AQUI, f"face-{face}-600ppp.png")).astype(int)
        pxmm = im.shape[1] / 91
        im = im[:round(61 * pxmm) - 2, :]                # a captura pode trazer 1–2 linhas a mais por arredondamento
        tinta = np.abs(im - im[2, 2]).sum(axis=2) > 60   # tudo o que não é o fundo
        seg = [round(v * pxmm) for v in (7, 7, 84, 54)]  # 3 mm de sangria + 4 mm de margem segura
        fora = tinta.copy()
        fora[seg[1]:seg[3], seg[0]:seg[2]] = False
        if fora.any():
            ok = False
            ys, xs = np.nonzero(fora)
            print(f"  ✗ {face}: tinta a menos de 4 mm do corte (x {xs.min() / pxmm:.1f}–{xs.max() / pxmm:.1f} mm,"
                  f" y {ys.min() / pxmm:.1f}–{ys.max() / pxmm:.1f} mm)")
        if face == "verso" and rel["qr"]:
            q, mod = rel["qr"]["mm"], (rel["qr"]["mm"][2] - rel["qr"]["mm"][0]) / rel["qr"]["modulos"]
            anel = [round(v * pxmm) for v in (q[0] - 4 * mod, q[1] - 4 * mod, q[2] + 4 * mod, q[3] + 4 * mod)]
            dentro = [round(v * pxmm) + e for v, e in zip(q, (-3, -3, 3, 3))]  # ±0,1 mm: antialiasing do próprio QR
            zona = tinta[anel[1]:anel[3], anel[0]:anel[2]].copy()
            zona[dentro[1] - anel[1]:dentro[3] - anel[1], dentro[0] - anel[0]:dentro[2] - anel[0]] = False
            if zona.any():
                ok = False
                ys, xs = np.nonzero(zona)
                print(f"  ✗ verso: há tinta na zona de silêncio do QR ({4 * mod:.1f} mm à volta): "
                      f"x {(xs.min() + anel[0]) / pxmm:.1f}–{(xs.max() + anel[0]) / pxmm:.1f} mm, "
                      f"y {(ys.min() + anel[1]) / pxmm:.1f}–{(ys.max() + anel[1]) / pxmm:.1f} mm; QR em x {q[0]:.1f}–{q[2]:.1f}, y {q[1]:.1f}–{q[3]:.1f}")
            else:
                folga = []
                for lado, faixa in (("esquerda", tinta[dentro[1]:dentro[3], :dentro[0]][:, ::-1]),
                                    ("baixo", tinta[dentro[3]:, dentro[0]:dentro[2]].T)):
                    col = np.nonzero(faixa.any(axis=0))[0]
                    folga.append(f"{lado} {col.min() / pxmm:.1f} mm" if col.size else f"{lado} livre")
                print(f"  ✓ zona de silêncio do QR livre ({4 * mod:.1f} mm exigidos; folga: {', '.join(folga)})")
    if ok:
        print("  ✓ nenhuma tinta a menos de 4 mm do corte; nenhum texto sobreposto")

    print(f"\nQR  {url_qr}  → versão {versao}-{erro}, {modulos}×{modulos} módulos, módulo = {21 / modulos:.2f} mm")
    img = cv2.imread(os.path.join(AQUI, "face-verso-600ppp.png"))
    det = cv2.QRCodeDetector()
    h, w = img.shape[:2]
    f = 120 / (21 * w / 91)  # QR com ~120 px de largura, como numa câmara de telemóvel a ~30 cm
    pequeno = cv2.resize(img, (int(w * f), int(h * f)), interpolation=cv2.INTER_AREA)
    for nome, im in {"600 ppp": img, "telemóvel (~120 px)": pequeno,
                     "telemóvel desfocado": cv2.GaussianBlur(pequeno, (3, 3), 1.0)}.items():
        txt, _, _ = det.detectAndDecode(im)
        passou = txt.upper() == url_qr
        ok &= passou
        print(f"  {'✓' if passou else '✗'} {nome}: {txt or '(não leu)'}")

    print(f"\nFrase no cartão: {escolha} — {frases[escolha - 1].replace('*', '')}")
    if falta:
        print(f"⚠ Falta: {', '.join(falta)} → gerado só cartao-impressao-PROVA.pdf (com faixa vermelha).")
    else:
        print("✓ cartao-impressao.pdf pronto para a gráfica.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
