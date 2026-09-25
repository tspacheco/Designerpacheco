#!/usr/bin/env python3
"""Gera o cartão de visita da Pacheco Studios a partir de ../dados.json (os mesmos dados da página).

    python3 gerar.py

Saídas (nesta pasta):
  cartao.html                    fonte renderizável (não editar — editar cartao.src.html)
  cartao-impressao.pdf           PDF para a gráfica: 2 páginas (frente, verso), 91×61 mm com 3 mm de sangria
  cartao-impressao-PROVA.pdf     o mesmo com faixa "PROVA" enquanto faltar telefone ou domínio confirmado
  cartao-preview.png             frente e verso lado a lado, já cortados (85×55 mm)
  face-frente/verso-600ppp.png   cada face a 600 ppp, com sangria
  acessibilidade.json            tamanho (pt) e contraste de cada texto

Testes que correm sempre: letra ≥ 7,5 pt, contraste ≥ 4,5:1, e o QR tem de ser lido a partir da imagem
renderizada — em alta resolução, reduzido ao tamanho de uma câmara de telemóvel, e desfocado.
Requer: pip install segno opencv-python-headless ; Playwright global (/opt/node22/lib/node_modules).
"""
import html
import json
import os
import re
import subprocess
import sys

import cv2
import segno

AQUI = os.path.dirname(os.path.abspath(__file__))
TEL_PROVISORIO = "9XX XXX XXX"


def formatar_telefone(t):
    d = re.sub(r"\D", "", t)
    if d.startswith("351") and len(d) == 12:
        d = d[3:]
    return f"{d[:3]} {d[3:6]} {d[6:]}" if len(d) == 9 else t


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
    svg = (f'<svg viewBox="0 0 {n} {n}" role="img" aria-label="Código QR para {html.escape(url.lower())}">'
           f'<path fill="var(--carvao)" d="{"".join(partes)}"/></svg>')
    return svg, qr.version, qr.error, n


def main():
    d = json.load(open(os.path.join(AQUI, "..", "dados.json"), encoding="utf-8"))
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

    def linha(l):
        classe = ' class="o"' if l.startswith("*") else ""
        t = html.escape(l.strip("*"))
        if t.endswith("."):  # ponto final → ponto laranja da marca
            t = t[:-1] + '<span class="pf" aria-hidden="true"></span><span class="so-leitor">.</span>'
        return f"<span{classe}>{t}</span>"
    slogan = "".join(linha(l) for l in d["slogan"])
    valores = {
        "NOME": html.escape(d["nome"].upper()),
        "FUNCAO": html.escape(d["funcao"]),
        "TELEFONE": html.escape(formatar_telefone(tel) if tel else TEL_PROVISORIO),
        "WHATSAPP": '<span class="r">WhatsApp</span>' if d.get("telefone_tem_whatsapp") else "",
        "EMAIL": html.escape(d["email"]),
        "INSTAGRAM": html.escape(d["instagram"].lstrip("@")),
        "DOMINIO": html.escape(dominio),
        "REGIAO": html.escape(d["regiao"].upper()),
        "SERVICOS": html.escape(d["servicos"].upper()),
        "SLOGAN": slogan,
        "QR_SVG": svg,
        "PROVA": "PROVA · FALTA: " + " E ".join(falta) if falta else "",
    }
    src = open(os.path.join(AQUI, "cartao.src.html"), encoding="utf-8").read()
    out = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: valores[m.group(1)], src)
    open(os.path.join(AQUI, "cartao.html"), "w", encoding="utf-8").write(out)

    for antigo in ("cartao-impressao.pdf", "cartao-impressao-PROVA.pdf"):
        p = os.path.join(AQUI, antigo)
        if os.path.exists(p):
            os.remove(p)
    env = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
    subprocess.run(["node", os.path.join(AQUI, "render.cjs"), os.path.join(AQUI, "cartao.html"), AQUI,
                    "1" if falta else "0"], check=True, env=env)

    # ——— testes ———
    ok = True
    rel = json.load(open(os.path.join(AQUI, "acessibilidade.json"), encoding="utf-8"))
    print(f"\nTEXTO ({len(rel)} elementos)")
    for r in rel:
        marca = ""
        if r["pt"] < 7.5 or r["contraste"] < 4.5:
            marca, ok = "  ✗", False
        elif r["contraste"] < 7:
            marca = "  (AA)"
        print(f"  {r['face']:6} {r['pt']:>5} pt  {r['contraste']:>5}:1  {r['texto']}{marca}")

    print(f"\nQR  {url_qr}  → versão {versao}-{erro}, {modulos}×{modulos} módulos, "
          f"módulo = {21 / modulos:.2f} mm")
    img = cv2.imread(os.path.join(AQUI, "face-verso-600ppp.png"))
    det = cv2.QRCodeDetector()
    h, w = img.shape[:2]
    px_mm = w / 91
    testes = {"600 ppp": img}
    # QR com ~120 px de largura, como numa câmara de telemóvel a ~30 cm
    f = 120 / (21 * px_mm)
    pequeno = cv2.resize(img, (int(w * f), int(h * f)), interpolation=cv2.INTER_AREA)
    testes["telemóvel (~120 px)"] = pequeno
    testes["telemóvel desfocado"] = cv2.GaussianBlur(pequeno, (3, 3), 1.0)
    for nome, im in testes.items():
        txt, _, _ = det.detectAndDecode(im)
        passou = txt.upper() == url_qr
        ok &= passou
        print(f"  {'✓' if passou else '✗'} {nome}: {txt or '(não leu)'}")

    if falta:
        print(f"\n⚠ Falta: {', '.join(falta)} → gerado só cartao-impressao-PROVA.pdf (com faixa vermelha).")
    else:
        print("\n✓ cartao-impressao.pdf pronto para a gráfica.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
