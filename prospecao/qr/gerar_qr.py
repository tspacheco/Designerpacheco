#!/usr/bin/env python3
"""Gera os QR da prospeção e as folhas A4 em PDF prontas para a copiadora.

    pip install segno reportlab

    # um negócio
    python3 prospecao/qr/gerar_qr.py --negocio "Casa Corvo" --demo https://casa-corvo.netlify.app \
        --place ChIJxxxxxxxx --whatsapp 351912345678 --wifi "CasaCorvo:senha123" --instagram casacorvo

    # uma lista (CSV com cabeçalho  negocio;demo;place;whatsapp;wifi;instagram)
    python3 prospecao/qr/gerar_qr.py --lista prospecao/qr/negocios.csv --lang ro --copias 2

Saída em prospecao/qr/out/ (ignorado pelo git):
    <slug>/demo.svg, avaliacoes.svg, whatsapp.svg, wifi.svg, instagram.svg   — QR soltos (vetor)
    cartoes-demo.pdf   — cartões 85×55 mm, 10 por A4, QR para a demo do negócio (deixar quando o dono não está)
    cavaletes.pdf      — cartões de mesa A6, 4 por A4, QR para as avaliações Google (o pack "5 estrelas")
    autocolantes.pdf   — autocolantes 60×60 mm, 9 por A4, QR para as avaliações (papel adesivo A4)
    pack-completo.pdf  — A6 por serviço (avaliações, Wi-Fi, WhatsApp, Instagram), só para quem tiver esses dados

Place ID das avaliações: Place ID Finder da Google (developers.google.com/maps/documentation/places/web-service/place-id).
Testar cada QR com dois telemóveis antes de imprimir. Correção de erro H em todos.
"""
import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote

try:
    import segno
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
except ImportError:
    sys.exit("Falta uma dependência: pip install segno reportlab")

MM = 72 / 25.4
MARCA = "Pacheco Studios"
PESSOA = "Tomás Pacheco"
TELEFONE = ""  # preencher: "+351 9xx xxx xxx" (pendente no playbook)
EMAIL = "tspacheco26@gmail.com"
SAIDA = Path(__file__).with_name("out")

TEXTO = {
    "pt": {
        "demo_titulo": "O seu site já existe.",
        "demo_sub": "Leia o código e veja-o no telemóvel.",
        "demo_rodape": "sites para restaurantes e negócios locais",
        "aval_titulo": "Gostou?",
        "aval_sub": "Avalie-nos no Google",
        "aval_como": "Aponte a câmara do telemóvel ao código",
        "wifi_titulo": "Wi-Fi grátis",
        "wifi_sub": "Leia o código — liga sozinho",
        "whats_titulo": "Reservas pelo WhatsApp",
        "whats_sub": "Leia o código e fale connosco",
        "insta_titulo": "Siga-nos no Instagram",
        "insta_sub": "Leia o código",
        "whats_msg": "Olá! Gostaria de fazer uma reserva.",
        "by": "site by",
    },
    "ro": {
        "demo_titulo": "Site-ul dumneavoastră există deja.",
        "demo_sub": "Scanați codul și vedeți-l pe telefon.",
        "demo_rodape": "site-uri pentru restaurante și afaceri locale",
        "aval_titulo": "V-a plăcut?",
        "aval_sub": "Lăsați-ne o recenzie pe Google",
        "aval_como": "Îndreptați camera telefonului spre cod",
        "wifi_titulo": "Wi-Fi gratuit",
        "wifi_sub": "Scanați codul — se conectează singur",
        "whats_titulo": "Rezervări pe WhatsApp",
        "whats_sub": "Scanați codul și scrieți-ne",
        "insta_titulo": "Urmăriți-ne pe Instagram",
        "insta_sub": "Scanați codul",
        "whats_msg": "Bună ziua! Aș dori să fac o rezervare.",
        "by": "site de",
    },
}


# ---------- tipografia (precisa de TTF por causa dos diacríticos ș ț ă) ----------
def registar_fontes():
    candidatos = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/TTF/DejaVuSans.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"),
        ("/Library/Fonts/DejaVuSans.ttf", "/Library/Fonts/DejaVuSans-Bold.ttf"),
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
        ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ]
    for reg, bold in candidatos:
        if Path(reg).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("Corpo", reg))
            pdfmetrics.registerFont(TTFont("Negrito", bold))
            return "Corpo", "Negrito"
    print("AVISO: sem fonte TTF — Helvetica não tem ș/ț/ă; instala DejaVu ou ajusta 'candidatos'.")
    return "Helvetica", "Helvetica-Bold"


FONTE, NEGRITO = registar_fontes()


# ---------- dados dos QR ----------
def slug(texto):
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "negocio"


def escapar_wifi(v):
    return re.sub(r'([\\;,":])', r"\\\1", v)


def payloads(n, lang):
    """Devolve {nome: conteúdo} só para o que o negócio tem."""
    p = {}
    if n.get("demo"):
        p["demo"] = n["demo"]
    if n.get("place"):
        p["avaliacoes"] = f"https://search.google.com/local/writereview?placeid={n['place']}"
    if n.get("whatsapp"):
        num = re.sub(r"\D", "", n["whatsapp"])
        p["whatsapp"] = f"https://wa.me/{num}?text={quote(TEXTO[lang]['whats_msg'])}"
    if n.get("wifi") and ":" in n["wifi"]:
        ssid, senha = n["wifi"].split(":", 1)
        p["wifi"] = f"WIFI:T:WPA;S:{escapar_wifi(ssid)};P:{escapar_wifi(senha)};;"
    if n.get("instagram"):
        p["instagram"] = f"https://instagram.com/{n['instagram'].lstrip('@')}"
    return p


def matriz(conteudo):
    return [list(linha) for linha in segno.make(conteudo, error="h").matrix]


# ---------- desenho ----------
def desenhar_qr(c, m, x, y, lado):
    """QR com zona de silêncio de 4 módulos; (x, y) é o canto inferior esquerdo."""
    n = len(m)
    mod = lado / (n + 8)
    c.setFillColorRGB(1, 1, 1)
    c.rect(x, y, lado, lado, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    ox, oy = x + 4 * mod, y + 4 * mod
    for i, linha in enumerate(m):
        for j, v in enumerate(linha):
            if v:
                c.rect(ox + j * mod, oy + (n - 1 - i) * mod, mod + 0.15, mod + 0.15, stroke=0, fill=1)


def texto_ajustado(c, s, x, y, largura, fonte, tamanho, minimo=7, centrado=False):
    while c.stringWidth(s, fonte, tamanho) > largura and tamanho > minimo:
        tamanho -= 0.5
    c.setFont(fonte, tamanho)
    if centrado:
        c.drawCentredString(x + largura / 2, y, s)
    else:
        c.drawString(x, y, s)
    return tamanho


def paragrafo(c, s, x, y_topo, largura, fonte, tamanho, max_linhas=2, entrelinha=1.25):
    """Quebra por palavras até max_linhas (encolhe a fonte se não couber). Devolve o y da última linha."""
    while True:
        linhas, atual = [], ""
        for palavra in s.split():
            tentativa = f"{atual} {palavra}".strip()
            if c.stringWidth(tentativa, fonte, tamanho) <= largura:
                atual = tentativa
            else:
                linhas.append(atual)
                atual = palavra
        linhas.append(atual)
        if len(linhas) <= max_linhas or tamanho <= 5.5:
            break
        tamanho -= 0.5
    c.setFont(fonte, tamanho)
    y = y_topo
    for linha in linhas[:max_linhas]:
        c.drawString(x, y, linha)
        y -= tamanho * entrelinha
    return y


def marcas_corte(c, x, y, w, h):
    c.setStrokeColorRGB(0.75, 0.75, 0.75)
    c.setLineWidth(0.3)
    for px in (x, x + w):
        for py in (y, y + h):
            c.line(px - 3 * MM, py, px - 1 * MM, py)
            c.line(px + 1 * MM, py, px + 3 * MM, py)
            c.line(px, py - 3 * MM, px, py - 1 * MM)
            c.line(px, py + 1 * MM, px, py + 3 * MM)


def cartao_demo(c, x, y, n, m, t):
    w, h = 85 * MM, 55 * MM
    qr = 32 * MM
    col = w - qr - 9 * MM  # coluna de texto à esquerda do QR
    marcas_corte(c, x, y, w, h)
    c.setFillColorRGB(0.08, 0.13, 0.22)
    c.rect(x, y + h - 3 * MM, w, 3 * MM, stroke=0, fill=1)  # faixa navy no topo
    c.setFillColorRGB(0.77, 0.6, 0.24)
    c.setFont(NEGRITO, 6.5)
    c.drawString(x + 5 * MM, y + h - 8 * MM, MARCA.upper())
    c.setFillColorRGB(0, 0, 0)
    yy = paragrafo(c, n["negocio"], x + 5 * MM, y + h - 15 * MM, col, NEGRITO, 11.5, max_linhas=2, entrelinha=1.1)
    yy = paragrafo(c, t["demo_titulo"], x + 5 * MM, yy - 2 * MM, col, NEGRITO, 8, max_linhas=2)
    paragrafo(c, t["demo_sub"], x + 5 * MM, yy - 0.5 * MM, col, FONTE, 7, max_linhas=2)
    c.setFillColorRGB(0.35, 0.35, 0.35)
    linha1 = f"{PESSOA} · {TELEFONE}" if TELEFONE else PESSOA
    texto_ajustado(c, linha1, x + 5 * MM, y + 10.5 * MM, col, NEGRITO, 6.5)
    texto_ajustado(c, EMAIL, x + 5 * MM, y + 7.5 * MM, col, FONTE, 6)
    texto_ajustado(c, t["demo_rodape"], x + 5 * MM, y + 4.5 * MM, col, FONTE, 5.5)
    c.setFillColorRGB(0, 0, 0)
    desenhar_qr(c, m, x + w - qr - 4 * MM, y + (h - qr) / 2, qr)


def cartao_a6(c, x, y, n, m, titulo, sub, como, t, estrelas=False):
    w, h = 105 * MM, 148 * MM
    marcas_corte(c, x, y, w, h)
    c.setFillColorRGB(0.08, 0.13, 0.22)
    c.rect(x + 8 * MM, y + h - 10 * MM, w - 16 * MM, 1.2 * MM, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    texto_ajustado(c, n["negocio"], x + 8 * MM, y + h - 21 * MM, w - 16 * MM, NEGRITO, 15, centrado=True)
    if estrelas:
        c.setFillColorRGB(0.77, 0.6, 0.24)
        c.setFont(FONTE, 20)
        c.drawCentredString(x + w / 2, y + h - 33 * MM, "★★★★★")
        c.setFillColorRGB(0, 0, 0)
    texto_ajustado(c, titulo, x + 8 * MM, y + h - 46 * MM, w - 16 * MM, NEGRITO, 22, centrado=True)
    texto_ajustado(c, sub, x + 8 * MM, y + h - 55 * MM, w - 16 * MM, NEGRITO, 12.5, centrado=True)
    lado = 62 * MM
    desenhar_qr(c, m, x + (w - lado) / 2, y + 22 * MM, lado)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    texto_ajustado(c, como, x + 8 * MM, y + 16 * MM, w - 16 * MM, FONTE, 9, centrado=True)
    c.setFillColorRGB(0.55, 0.55, 0.55)
    texto_ajustado(c, f"{t['by']} {MARCA}", x + 8 * MM, y + 8 * MM, w - 16 * MM, FONTE, 6.5, centrado=True)
    c.setFillColorRGB(0, 0, 0)


def autocolante(c, x, y, n, m, t):
    w = 60 * MM
    marcas_corte(c, x, y, w, w)
    c.setStrokeColorRGB(0.08, 0.13, 0.22)
    c.setLineWidth(0.8)
    c.roundRect(x + 1.5 * MM, y + 1.5 * MM, w - 3 * MM, w - 3 * MM, 4 * MM, stroke=1, fill=0)
    c.setFillColorRGB(0, 0, 0)
    texto_ajustado(c, t["aval_sub"], x + 4 * MM, y + w - 9 * MM, w - 8 * MM, NEGRITO, 9.5, centrado=True)
    c.setFillColorRGB(0.77, 0.6, 0.24)
    c.setFont(FONTE, 9)
    c.drawCentredString(x + w / 2, y + w - 14 * MM, "★★★★★")
    c.setFillColorRGB(0, 0, 0)
    desenhar_qr(c, m, x + (w - 40 * MM) / 2, y + 8.5 * MM, 40 * MM)
    c.setFillColorRGB(0.35, 0.35, 0.35)
    texto_ajustado(c, n["negocio"], x + 4 * MM, y + 4.5 * MM, w - 8 * MM, FONTE, 6.5, centrado=True)
    c.setFillColorRGB(0, 0, 0)


# ---------- folhas ----------
def grelha(c, itens, desenhar, cols, rows, w, h):
    """Distribui itens numa grelha cols×rows por página, centrada no A4."""
    pw, ph = A4
    mx, my = (pw - cols * w) / 2, (ph - rows * h) / 2
    for k, item in enumerate(itens):
        i = k % (cols * rows)
        if k and i == 0:
            c.showPage()
        col, row = i % cols, i // cols
        desenhar(c, mx + col * w, ph - my - (row + 1) * h, *item)
    c.showPage()


def gerar(negocios, lang, copias):
    t = TEXTO[lang]
    SAIDA.mkdir(exist_ok=True)
    demos, avals, stickers, pack = [], [], [], []
    for n in negocios:
        p = payloads(n, lang)
        if not p:
            print(f"  {n['negocio']}: sem dados para QR — ignorado")
            continue
        pasta = SAIDA / slug(n["negocio"])
        pasta.mkdir(exist_ok=True)
        ms = {}
        for nome, conteudo in p.items():
            segno.make(conteudo, error="h").save(str(pasta / f"{nome}.svg"), scale=8, border=4)
            ms[nome] = matriz(conteudo)
        print(f"  {n['negocio']}: {', '.join(p)} → {pasta.relative_to(SAIDA.parent.parent)}/")
        if "demo" in ms:
            demos += [(n, ms["demo"], t)] * copias
        if "avaliacoes" in ms:
            avals += [(n, ms["avaliacoes"], t["aval_titulo"], t["aval_sub"], t["aval_como"], t, True)] * copias
            stickers += [(n, ms["avaliacoes"], t)] * copias
            pack.append((n, ms["avaliacoes"], t["aval_titulo"], t["aval_sub"], t["aval_como"], t, True))
        for nome, titulo, sub in (("wifi", t["wifi_titulo"], t["wifi_sub"]),
                                  ("whatsapp", t["whats_titulo"], t["whats_sub"]),
                                  ("instagram", t["insta_titulo"], t["insta_sub"])):
            if nome in ms:
                pack.append((n, ms[nome], titulo, sub, t["aval_como"], t, False))

    folhas = [("cartoes-demo.pdf", demos, cartao_demo, 2, 5, 85 * MM, 55 * MM),
              ("cavaletes.pdf", avals, cartao_a6, 2, 2, 105 * MM, 148 * MM),
              ("autocolantes.pdf", stickers, autocolante, 3, 3, 60 * MM, 60 * MM),
              ("pack-completo.pdf", pack, cartao_a6, 2, 2, 105 * MM, 148 * MM)]
    for nome, itens, fn, cols, rows, w, h in folhas:
        if not itens:
            continue
        c = canvas.Canvas(str(SAIDA / nome), pagesize=A4)
        c.setTitle(f"{MARCA} — {nome[:-4]}")
        grelha(c, itens, fn, cols, rows, w, h)
        c.save()
        paginas = -(-len(itens) // (cols * rows))
        print(f"  {nome}: {len(itens)} cartões, {paginas} página(s) A4")


def ler_lista(caminho):
    with open(caminho, encoding="utf-8", newline="") as f:
        amostra = f.read(2048)
        f.seek(0)
        sep = ";" if amostra.count(";") >= amostra.count(",") else ","
        return [{k.strip(): (v or "").strip() for k, v in r.items() if k}
                for r in csv.DictReader(f, delimiter=sep) if r.get("negocio")]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lista", help="CSV: negocio;demo;place;whatsapp;wifi;instagram")
    ap.add_argument("--negocio")
    ap.add_argument("--demo", help="URL da demo")
    ap.add_argument("--place", help="Place ID Google para o link de avaliação")
    ap.add_argument("--whatsapp", help="número com indicativo, só dígitos: 351912345678")
    ap.add_argument("--wifi", help="SSID:senha")
    ap.add_argument("--instagram", help="@utilizador")
    ap.add_argument("--lang", choices=TEXTO, default="pt")
    ap.add_argument("--copias", type=int, default=1, help="cartões por negócio em cada folha")
    a = ap.parse_args()
    if a.lista:
        negocios = ler_lista(a.lista)
    elif a.negocio:
        negocios = [{"negocio": a.negocio, "demo": a.demo or "", "place": a.place or "",
                     "whatsapp": a.whatsapp or "", "wifi": a.wifi or "", "instagram": a.instagram or ""}]
    else:
        ap.error("indica --lista ou --negocio")
    if not TELEFONE:
        print("AVISO: TELEFONE vazio no topo do script — os cartões saem só com e-mail.")
    gerar(negocios, a.lang, max(1, a.copias))


if __name__ == "__main__":
    main()
