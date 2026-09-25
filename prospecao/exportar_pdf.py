#!/usr/bin/env python3
"""Exporta a rotina de prospeção para um PDF em formato de telemóvel (100 × 178 mm).

    pip install reportlab fonttools
    python3 prospecao/exportar_pdf.py        # → prospecao/prospecao-10x.pdf

A fonte de verdade são os .md listados em PARTES. Editar lá e voltar a correr — nunca editar o PDF.
Tipografia das peças de Instagram da Pacheco Studios (Archivo Black, Inter, Space Mono), descarregada
uma vez do repositório google/fonts para prospecao/.fontes/ (ignorado pelo git). Sem rede → DejaVu.
Tabelas longas passam a cartões (lê-se melhor num ecrã estreito); capa com índice clicável e marcadores.
"""
import re
import sys
import urllib.request
from datetime import date
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

try:
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether, NextPageTemplate,
                                    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)
except ImportError:
    sys.exit("Falta o reportlab: pip install reportlab fonttools")

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
SAIDA = AQUI / "prospecao-10x.pdf"
CACHE = AQUI / ".fontes"

# (ficheiro, etiqueta, título da parte, subtítulo, nome curto para o rodapé)
PARTES = [
    ("prospecao/checklist-diario.md", "Todos os dias", "Checklist diário",
     "Mínimo 10 portas, objetivo 25. Em cada porta: um facto, o WhatsApp do dono e o cartão "
     "— e, se der, a reunião marcada.", "Checklist"),
    ("research/iasi.md", "Onde estás", "Iași",
     "Zonas, primeiros alvos sem site e a primeira semana na rua.", "Iași"),
    ("research/romenia.md", "Expansão", "Roménia",
     "Plano, preços em lei, script em romeno, legal e engine RO.", "Roménia"),
    ("research/metodo-10x-cardone.md", "O método", "Método 10X",
     "Grant Cardone: o que serve, o que se adapta e o que se ignora.", "Método 10X"),
]

PW, PH = 100 * mm, 178 * mm          # formato de telemóvel
ML = MR = 20
MT, MB = 24, 32
W = PW - ML - MR

TINTA = HexColor("#141210")          # cores das peças de Instagram (social/)
CREME = HexColor("#EFEAE3")
CREME_DIM = HexColor("#BDB5AB")
LARANJA = HexColor("#E8622C")        # acentos grandes
LARANJA_ESC = HexColor("#B8441A")    # texto pequeno em laranja (contraste AA sobre branco)
CINZA = HexColor("#6B645C")
CINZA_CLARO = HexColor("#9A9188")
REGRA = HexColor("#E6E0D8")
FUNDO_CAB = HexColor("#F5F0EA")
FUNDO_COD = "#F3EDE6"
REGRA_ESCURA = HexColor("#3A342E")

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONTES_WEB = {
    "ArchivoBlack.ttf": GF + "archivoblack/ArchivoBlack-Regular.ttf",
    "SpaceMono.ttf": GF + "spacemono/SpaceMono-Regular.ttf",
    "SpaceMono-Bold.ttf": GF + "spacemono/SpaceMono-Bold.ttf",
    "Inter-VF.ttf": GF + "inter/Inter%5Bopsz,wght%5D.ttf",
    "Inter-Italic-VF.ttf": GF + "inter/Inter-Italic%5Bopsz,wght%5D.ttf",
}
INSTANCIAS = {"Inter.ttf": ("Inter-VF.ttf", 400), "Inter-Bold.ttf": ("Inter-VF.ttf", 700),
              "Inter-Italic.ttf": ("Inter-Italic-VF.ttf", 400),
              "Inter-BoldItalic.ttf": ("Inter-Italic-VF.ttf", 700)}
DEJAVU = Path("/usr/share/fonts/truetype/dejavu")


# ---------------------------------------------------------------- fontes
def fontes_da_marca():
    """Descarrega e instancia as fontes da marca. Devolve True se ficaram prontas."""
    try:
        CACHE.mkdir(exist_ok=True)
        for nome, url in FONTES_WEB.items():
            destino = CACHE / nome
            if not destino.exists():
                print(f"  a descarregar {nome}…")
                with urllib.request.urlopen(url, timeout=30) as r:
                    destino.write_bytes(r.read())
        from fontTools.ttLib import TTFont as FTFont
        from fontTools.varLib.instancer import instantiateVariableFont
        for nome, (vf, peso) in INSTANCIAS.items():
            destino = CACHE / nome
            # o reportlab reaproveita fontes com o mesmo nome PostScript: cada instância precisa do seu
            ps = "Inter-Regular" if nome == "Inter.ttf" else nome[:-4]
            if destino.exists() and FTFont(destino)["name"].getDebugName(6) == ps:
                continue
            inst = instantiateVariableFont(FTFont(CACHE / vf), {"wght": peso, "opsz": 14})
            for rec in list(inst["name"].names):
                if rec.nameID in (4, 6):
                    inst["name"].setName(ps if rec.nameID == 6 else ps.replace("-", " "),
                                         rec.nameID, rec.platformID, rec.platEncID, rec.langID)
            inst.save(destino)
        return True
    except Exception as e:  # sem rede ou sem fonttools
        print(f"AVISO: fontes da marca indisponíveis ({e}) — a usar DejaVu.")
        return False


def registar_fontes():
    if fontes_da_marca():
        mapa = {"Corpo": "Inter.ttf", "Corpo-B": "Inter-Bold.ttf", "Corpo-I": "Inter-Italic.ttf",
                "Corpo-BI": "Inter-BoldItalic.ttf", "Titulo": "ArchivoBlack.ttf",
                "Mono": "SpaceMono.ttf", "Mono-B": "SpaceMono-Bold.ttf"}
        for nome, ficheiro in mapa.items():
            pdfmetrics.registerFont(TTFont(nome, str(CACHE / ficheiro)))
    else:
        for nome, ficheiro in {"Corpo": "DejaVuSans.ttf", "Corpo-B": "DejaVuSans-Bold.ttf",
                               "Corpo-I": "DejaVuSans.ttf", "Corpo-BI": "DejaVuSans-Bold.ttf",
                               "Titulo": "DejaVuSans-Bold.ttf", "Mono": "DejaVuSansMono.ttf",
                               "Mono-B": "DejaVuSansMono-Bold.ttf"}.items():
            pdfmetrics.registerFont(TTFont(nome, str(DEJAVU / ficheiro)))
    pdfmetrics.registerFont(TTFont("Simbolos", str(DEJAVU / "DejaVuSans.ttf")))  # ☐ e recurso
    pdfmetrics.registerFont(TTFont("MonoAlt", str(DEJAVU / "DejaVuSansMono.ttf")))
    pdfmetrics.registerFontFamily("Corpo", normal="Corpo", bold="Corpo-B", italic="Corpo-I",
                                  boldItalic="Corpo-BI")


def cobre(fonte, texto):
    mapa = pdfmetrics.getFont(fonte).face.charToGlyph
    return all(ord(ch) in mapa for ch in texto if not ch.isspace())


# ---------------------------------------------------------------- markdown → blocos
LISTA = re.compile(r"(\s*)(-|\*|\d+\.)\s+(\[[ xX]\]\s+)?(.*)")
INICIO_BLOCO = re.compile(r"\s*(#{1,4}\s|>|\||[-*]\s|\d+\.\s)")


def blocos(md):
    linhas, i, out = md.splitlines(), 0, []
    while i < len(linhas):
        s = linhas[i].strip()
        if not s:
            i += 1
            continue
        m = re.match(r"(#{1,4})\s+(.*)", s)
        if m:
            out.append((f"h{len(m.group(1))}", m.group(2).strip()))
            i += 1
        elif s.startswith(">"):
            q = []
            while i < len(linhas) and linhas[i].strip().startswith(">"):
                q.append(linhas[i].strip()[1:].strip())
                i += 1
            out.append(("citacao", q))
        elif s.startswith("|"):
            filas = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                cel = [c.strip() for c in linhas[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cel):
                    filas.append(cel)
                i += 1
            out.append(("tabela", filas))
        elif LISTA.match(linhas[i]):
            itens = []
            while i < len(linhas):
                m = LISTA.match(linhas[i])
                if m:
                    itens.append([m.group(2), bool(m.group(3)), m.group(4).strip()])
                elif linhas[i].startswith("  ") and linhas[i].strip() and itens:
                    itens[-1][2] += " " + linhas[i].strip()
                else:
                    break
                i += 1
            out.append(("lista", itens))
        else:
            p = [s]
            i += 1
            while i < len(linhas) and linhas[i].strip() and not INICIO_BLOCO.match(linhas[i]):
                p.append(linhas[i].strip())
                i += 1
            texto = " ".join(p)
            if re.fullmatch(r"\*\*[^*]+\*\*:?", texto):
                out.append(("rotulo", texto.strip("*: ").rstrip(":")))
            else:
                out.append(("p", texto))
    return out


def inline(s, tam_cod=8.2):
    """Markdown em linha → mini-HTML do reportlab (negrito, itálico, código, links)."""
    codigos = []

    def guardar(m):
        codigos.append(m.group(1))
        return f"{len(codigos) - 1}"

    s = re.sub(r"`([^`]+)`", guardar, s)
    s = escape(s)
    s = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"~~(?=\S)(.+?)(?<=\S)~~", r"<strike>\1</strike>", s)
    s = re.sub(r"(?<![*\w])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![*\w])", r"<i>\1</i>", s)
    s = re.sub(r"(?<![\w_])_(?=[^\s_])([^_\n]+?)(?<=[^\s_])_(?![\w_])", r"<i>\1</i>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<link href="\2" color="#B8441A">\1</link>', s)

    def repor(m):
        cod = codigos[int(m.group(1))]
        fonte = "Mono" if cobre("Mono", cod) else "MonoAlt"
        pedacos = []
        for token in re.split(r"(\s+)", cod):
            if len(token) > 34:  # URL sem espaços não cabe numa linha de 100 mm: partir num / ou ?
                meio = len(token) // 2
                cortes = [k + 1 for k, ch in enumerate(token[:-1]) if ch in "/?&="]
                if cortes:
                    k = min(cortes, key=lambda c: abs(c - meio))
                    pedacos.append((token[:k], True))
                    token = token[k:]
            pedacos.append((token, False))
        html = ""
        for texto, quebra in pedacos:
            if texto:
                html += f'<font name="{fonte}" size="{tam_cod}" backColor="{FUNDO_COD}">{escape(texto)}</font>'
            if quebra:
                html += "<br/>"
        return html

    return re.sub("(\\d+)", repor, s)


def plano(s):
    return re.sub(r"[*_`]", "", s)


# ---------------------------------------------------------------- estilos
def estilos():
    E = {}
    E["p"] = ParagraphStyle("p", fontName="Corpo", fontSize=9.5, leading=13.3, textColor=TINTA,
                            spaceAfter=5)
    E["li"] = ParagraphStyle("li", parent=E["p"], leftIndent=13, bulletIndent=0, spaceAfter=3.3,
                             bulletFontName="Corpo-B", bulletFontSize=9.5)
    E["li"].bulletColor = LARANJA
    E["li_num"] = ParagraphStyle("li_num", parent=E["li"], leftIndent=15, bulletFontName="Mono-B",
                                 bulletFontSize=7.8)
    E["li_num"].bulletColor = LARANJA_ESC
    E["li_caixa"] = ParagraphStyle("li_caixa", parent=E["li"], leftIndent=15,
                                   bulletFontName="Simbolos", bulletFontSize=10.5)
    E["li_caixa"].bulletColor = LARANJA
    E["h2"] = ParagraphStyle("h2", fontName="Titulo", fontSize=11.4, leading=14, textColor=TINTA,
                             spaceBefore=15, spaceAfter=7, keepWithNext=1)
    E["h3"] = ParagraphStyle("h3", fontName="Corpo-B", fontSize=10, leading=13.4, textColor=TINTA,
                             spaceBefore=10, spaceAfter=4.5, keepWithNext=1)
    E["rotulo"] = ParagraphStyle("rotulo", fontName="Corpo-B", fontSize=9.5, leading=13.2,
                                 textColor=TINTA, spaceBefore=5, spaceAfter=3.5, keepWithNext=1)
    E["citacao"] = ParagraphStyle("citacao", fontName="Corpo-I", fontSize=8.3, leading=11.8,
                                  textColor=CINZA)
    E["cel"] = ParagraphStyle("cel", fontName="Corpo", fontSize=8, leading=10.8, textColor=TINTA)
    E["cel_c"] = ParagraphStyle("cel_c", parent=E["cel"], alignment=1)
    E["cab"] = ParagraphStyle("cab", fontName="Mono-B", fontSize=6.3, leading=8.2, textColor=CINZA)
    E["cab_c"] = ParagraphStyle("cab_c", parent=E["cab"], alignment=1)
    E["cartao_tit"] = ParagraphStyle("cartao_tit", fontName="Corpo-B", fontSize=9.2, leading=12.4,
                                     textColor=TINTA, spaceAfter=2)
    E["cartao_txt"] = ParagraphStyle("cartao_txt", fontName="Corpo", fontSize=8.6, leading=12,
                                     textColor=TINTA, spaceAfter=2.5)
    return E


# ---------------------------------------------------------------- blocos → flowables
def partir_titulo(t):
    """'2. Na rua (2 h) — sequência…' → ('2', 'Na rua', '2 h — sequência…')."""
    m = re.match(r"(\d+)\.\s+(.*)", t)
    num, resto = (m.group(1), m.group(2)) if m else (None, t)
    cortes = [k for k in (resto.find(" ("), resto.find(" — ")) if k > 0]
    if not cortes:
        return num, resto, ""
    k = min(cortes)
    principal, sub = resto[:k], resto[k:].strip()
    if sub.startswith("— "):
        sub = sub[2:]
    elif sub.startswith("(") and ")" in sub:
        fecho = sub.index(")")
        sub = sub[1:fecho] + sub[fecho + 1:]
    return num, principal, sub.strip()


def titulo_h2(texto, E, chave):
    num, principal, sub = partir_titulo(texto)
    fonte = "Titulo" if cobre("Titulo", principal.upper()) else "Corpo-B"
    html = ""
    if num is not None:
        html += f'<font name="Mono-B" size="7.6" color="#B8441A">{int(num):02d}</font>&nbsp;&nbsp;'
    html += f'<font name="{fonte}">{escape(principal.upper())}</font>'
    if sub:
        html += f'<br/><font name="Corpo" size="8.4" color="#6B645C">{inline(sub, 7.4)}</font>'
    p = Paragraph(html, E["h2"])
    p._marcador = (chave, plano(texto), 1)
    return p


def com_barra(conteudo, espessura=1.6, esquerda=9):
    t = Table([[conteudo]], colWidths=[W])
    t.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, 0), espessura, LARANJA),
                           ("LEFTPADDING", (0, 0), (0, 0), esquerda),
                           ("RIGHTPADDING", (0, 0), (0, 0), 0),
                           ("TOPPADDING", (0, 0), (0, 0), 1.5),
                           ("BOTTOMPADDING", (0, 0), (0, 0), 1.5)]))
    return t


def e_cartoes(filas):
    """Tabelas com texto longo viram cartões (num ecrã de 100 mm uma grelha de 3-4 colunas não se lê)."""
    cab, corpo = filas[0], filas[1:]
    if not corpo:
        return False
    if len(cab) >= 3:
        return max(len(plano(c)) for f in corpo for c in f[1:]) > 45
    if len(cab) == 2:
        return sum(len(plano(f[1])) for f in corpo if len(f) > 1) / len(corpo) > 90
    return False


def tabela(filas, E):
    ncol = len(filas[0])
    filas = [(f + [""] * ncol)[:ncol] for f in filas]
    cab, corpo = filas[0], filas[1:]
    if e_cartoes(filas):
        out = []
        for f in corpo:
            conteudo = [Paragraph(inline(f[0], 7.8), E["cartao_tit"])]
            for h, c in zip(cab[1:], f[1:]):
                if not c:
                    continue
                rotulo = (f'<font name="Mono-B" size="6.1" color="#B8441A">{escape(plano(h).upper())}</font>'
                          f"&nbsp;&nbsp;" if ncol >= 3 else "")
                conteudo.append(Paragraph(rotulo + inline(c, 7.4), E["cartao_txt"]))
            out += [com_barra(conteudo), Spacer(1, 7.5)]
        return out + [Spacer(1, 2)], False

    # grelha: larguras pelo conteúdo, colunas curtas centradas
    def largura(txt, fonte, tam):
        return pdfmetrics.stringWidth(plano(txt), fonte, tam)

    pad = 9
    nat, minimo, curtas = [], [], []
    for j in range(ncol):
        col = [f[j] for f in corpo]
        nat.append(max([largura(c, "Corpo", 8) * 1.08 for c in col] + [largura(cab[j].upper(), "Mono-B", 6.3)]) + pad)
        palavras = [p for c in col + [cab[j]] for p in plano(c).split()] or [""]
        curtas.append(all(len(plano(c)) <= 12 for c in col))
        # colunas curtas (números, sim/não) nunca encolhem: é a coluna de texto que cede
        minimo.append(nat[-1] if curtas[-1] and j else max(largura(p, "Corpo-B", 8) for p in palavras) + pad)
    if sum(nat) <= W:
        larguras = [n * W / sum(nat) for n in nat]
    else:
        resto = W - sum(minimo)
        extra = [max(n - m, 0) for n, m in zip(nat, minimo)]
        if resto <= 0 or not sum(extra):
            larguras = [m * W / sum(minimo) for m in minimo]
        else:
            larguras = [m + resto * e / sum(extra) for m, e in zip(minimo, extra)]
    dados = [[Paragraph(escape(plano(h).upper()), E["cab_c" if curtas[j] and j else "cab"])
              for j, h in enumerate(cab)]]
    for f in corpo:
        dados.append([Paragraph(inline(c, 6.9), E["cel_c" if curtas[j] and j else "cel"])
                      for j, c in enumerate(f)])
    t = Table(dados, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), FUNDO_CAB),
        ("LINEBELOW", (0, 0), (-1, -1), 0.45, REGRA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5), ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ]))
    # tabelas curtas (a versão de bolso, a cadência) ficam inteiras numa página — são para print
    return [Spacer(1, 2), t], len(corpo) <= 10


def lista(itens, E):
    out = []
    for marca, caixa, texto in itens:
        if caixa:
            out.append(Paragraph(inline(texto), E["li_caixa"], bulletText="☐"))
        elif marca[0].isdigit():
            out.append(Paragraph(inline(texto), E["li_num"], bulletText=marca))
        else:
            out.append(Paragraph(inline(texto), E["li"], bulletText="•"))
    return out + [Spacer(1, 3.5)]


class Abertura(Flowable):
    """Faixa escura no topo da 1.ª página de cada parte (sangra até às margens da página)."""

    def __init__(self, n, etiqueta, titulo, sub, curto):
        super().__init__()
        self.n, self.etiqueta, self.titulo, self.sub, self.curto = n, etiqueta, titulo, sub, curto
        self._marcador = (f"parte{n}", f"{n}. {titulo}", 0)

    def wrap(self, aw, ah):
        self.p_tit = Paragraph(escape(self.titulo.upper()), ParagraphStyle(
            "ab_t", fontName="Titulo", fontSize=25, leading=27, textColor=CREME))
        self.p_sub = Paragraph(escape(self.sub), ParagraphStyle(
            "ab_s", fontName="Corpo", fontSize=9, leading=12.6, textColor=CREME_DIM))
        self.h_tit = self.p_tit.wrap(aw, ah)[1]
        self.h_sub = self.p_sub.wrap(aw, ah)[1]
        self.h = 8 + 7 + 14 + self.h_tit + 7 + self.h_sub + 20
        return aw, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        topo = self.h + MT
        c.setFillColor(TINTA)
        c.rect(-ML, 0, PW, topo, stroke=0, fill=1)
        caminho = c.beginPath()
        caminho.rect(-ML, 0, PW, topo)
        c.clipPath(caminho, stroke=0, fill=0)
        brilho(c, PW - ML + 6, topo - 30, 150, 0.02)
        y = self.h - 8 - 7
        t = c.beginText(0, y)
        t.setFont("Mono-B", 6.4)
        t.setCharSpace(1.5)
        t.setFillColor(LARANJA)
        t.textOut(f"PARTE {self.n} · {self.etiqueta.upper()}")
        t.setCharSpace(0)
        c.drawText(t)
        y -= 14 + self.h_tit
        self.p_tit.drawOn(c, 0, y + 2)
        y -= 7 + self.h_sub
        self.p_sub.drawOn(c, 0, y)
        c.restoreState()


def brilho(c, x, y, raio, alfa):
    """O brilho laranja das peças de Instagram, em círculos concêntricos translúcidos."""
    c.saveState()
    c.setFillColor(LARANJA)
    c.setFillAlpha(alfa)
    passos = 26
    for k in range(passos):
        c.circle(x, y, raio * (1 - k / passos), stroke=0, fill=1)
    c.restoreState()


def historia(E):
    story = [NextPageTemplate("corpo"), PageBreak()]
    for n, (caminho, etiqueta, titulo, sub, curto) in enumerate(PARTES, 1):
        while isinstance(story[-1], Spacer):  # um espaço que transborda criava uma página em branco
            story.pop()
        if n > 1:
            story.append(PageBreak())
        story += [Abertura(n, etiqueta, titulo, sub, curto), Spacer(1, 12)]
        k = 0
        for bloco in blocos((RAIZ / caminho).read_text(encoding="utf-8")):
            tipo = bloco[0]
            if tipo == "h1":
                continue  # substituído pela abertura
            if tipo == "h2":
                k += 1
                story.append(titulo_h2(bloco[1], E, f"p{n}s{k}"))
            elif tipo in ("h3", "h4"):
                story.append(Paragraph(inline(bloco[1]), E["h3"]))
            elif tipo == "citacao":
                story += [com_barra(Paragraph("<br/>".join(inline(l, 7.2) for l in bloco[1]),
                                              E["citacao"])), Spacer(1, 8)]
            elif tipo == "tabela":
                fl, inteira = tabela(bloco[1], E)
                if inteira:
                    # o reportlab não junta um KeepTogether ao título anterior (keepWithNext):
                    # agrupar aqui título(s) + tabela, para o título nunca ficar sozinho no fundo da página
                    cab = []
                    while story and isinstance(story[-1], Paragraph) and story[-1].getKeepWithNext():
                        cab.insert(0, story.pop())
                    story += [KeepTogether(cab + fl), Spacer(1, 9)]
                else:
                    story += fl + [Spacer(1, 9)] if isinstance(fl[-1], Table) else fl
            elif tipo == "lista":
                story += lista(bloco[1], E)
            elif tipo == "rotulo":
                story.append(Paragraph(inline(bloco[1]), E["rotulo"]))
            else:
                story.append(Paragraph(inline(bloco[1]), E["p"]))
    return story


# ---------------------------------------------------------------- documento
class Doc(BaseDocTemplate):
    def __init__(self, destino, paginas_capa, total):
        super().__init__(destino, pagesize=(PW, PH), leftMargin=ML, rightMargin=MR, topMargin=MT,
                         bottomMargin=MB, title="Pacheco Studios — Prospeção 10X",
                         author="Tomás Pacheco", subject="Checklist diário, método 10X e plano Roménia",
                         creator="prospecao/exportar_pdf.py")
        self.paginas_capa, self.total = paginas_capa, total
        self.paginas, self.parte_atual = {}, ""
        sem_margem = dict(leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate("capa", [Frame(0, 0, PW, PH, id="capa", **sem_margem)], onPage=self.capa),
            PageTemplate("corpo", [Frame(ML, MB, W, PH - MT - MB, id="corpo", **sem_margem)],
                         onPageEnd=self.rodape),
        ])

    def afterFlowable(self, f):
        marcador = getattr(f, "_marcador", None)
        if not marcador:
            return
        chave, titulo, nivel = marcador
        if nivel == 0:
            self.canv.bookmarkPage(chave)
            self.paginas[chave] = self.canv.getPageNumber()
            self.parte_atual = f.curto
        else:
            self.canv.bookmarkHorizontalAbsolute(chave, self.frame._y + getattr(f, "height", 0) + 18)
        self.canv.addOutlineEntry(titulo, chave, level=nivel, closed=nivel == 0 and False)

    def rodape(self, c, doc):
        c.saveState()
        t = c.beginText(ML, 17)
        t.setFont("Mono-B", 5.6)
        t.setCharSpace(1)
        t.setFillColor(CINZA_CLARO)
        t.textOut(f"PACHECO STUDIOS · {self.parte_atual.upper()}")
        t.setCharSpace(0)
        c.drawText(t)
        c.setFont("Mono", 6.2)
        c.drawRightString(PW - MR, 17, f"{c.getPageNumber()}/{self.total or '—'}")
        c.restoreState()

    def capa(self, c, doc):
        c.saveState()
        c.setFillColor(TINTA)
        c.rect(0, 0, PW, PH, stroke=0, fill=1)
        brilho(c, PW + 8, PH - 78, 235, 0.02)
        brilho(c, -40, 40, 170, 0.009)
        x, y = 22, PH - 34
        t = c.beginText(x, y)
        t.setFont("Mono-B", 6.4)
        t.setCharSpace(1.6)
        t.setFillColor(LARANJA)
        t.textOut("PACHECO STUDIOS")
        t.setCharSpace(0)
        c.drawText(t)
        c.setFont("Mono", 6.2)
        c.setFillColor(CREME_DIM)
        hoje = date.today()
        c.drawRightString(PW - 22, y, f"{hoje:%d/%m/%Y}")

        largura = PW - 44
        # índice ancorado em baixo (por cima do rodapé); o "10X" encolhe se houver muitas partes
        estilo_d = ParagraphStyle("capa_d", fontName="Corpo", fontSize=7.4, leading=9.6, textColor=CREME_DIM)
        indice = []
        for n, (_, _, titulo, subt, _) in enumerate(PARTES, 1):
            desc = Paragraph(escape(subt), estilo_d)
            indice.append((n, titulo, desc, desc.wrap(largura - 22 - 26, 60)[1]))
        topo_indice = 40 + sum(26 + hd for *_, hd in indice)

        sub = Paragraph("O dia porta a porta, com o mínimo e o objetivo de cada passo. Depois: Iași, "
                        "o plano para a Roménia e o método 10X por trás.",
                        ParagraphStyle("capa_s", fontName="Corpo", fontSize=9.6, leading=13.6,
                                       textColor=CREME_DIM))
        h = sub.wrap(largura, 200)[1]
        tam = min(40, largura / pdfmetrics.stringWidth("PROSPEÇÃO", "Titulo", 1))
        y = PH - 116
        k = max(1.3, min(2.2, (y - topo_indice - 26 - 20 - h) / tam))
        c.setFont("Titulo", tam)
        c.setFillColor(CREME)
        c.drawString(x - 1, y, "PROSPEÇÃO")
        c.setFont("Titulo", tam * k * 1.07)
        c.setFillColor(LARANJA)
        y -= tam * k
        c.drawString(x - 3, y, "10X")
        y -= 20 + h
        sub.drawOn(c, x, y)

        y = topo_indice
        c.setStrokeColor(REGRA_ESCURA)
        c.setLineWidth(0.6)
        for n, titulo, desc, hd in indice:
            c.line(x, y, PW - 22, y)
            c.setFont("Mono-B", 7)
            c.setFillColor(LARANJA)
            c.drawString(x, y - 15, f"{n:02d}")
            c.setFont("Corpo-B", 11)
            c.setFillColor(CREME)
            c.drawString(x + 22, y - 15.5, titulo)
            pagina = self.paginas_capa.get(f"parte{n}")
            c.setFont("Mono", 6.6)
            c.setFillColor(CREME_DIM)
            c.drawRightString(PW - 22, y - 15, f"p. {pagina}" if pagina else "")
            desc.drawOn(c, x + 22, y - 20 - hd)
            fundo = y - 26 - hd
            c.linkRect("", f"parte{n}", (x, fundo, PW - 22, y), relative=0, thickness=0)
            y = fundo
        c.line(x, y, PW - 22, y)

        c.setFont("Mono", 5.6)
        c.setFillColor(CINZA_CLARO)
        c.drawString(x, 26, "Gerado dos .md do repositório — editar lá, não aqui.")
        c.drawString(x, 18, "python3 prospecao/exportar_pdf.py")
        c.restoreState()


def main():
    global SAIDA
    if len(sys.argv) > 1:  # destino alternativo (testes): python3 prospecao/exportar_pdf.py /tmp/x.pdf
        SAIDA = Path(sys.argv[1]).resolve()
    em_falta = [p[0] for p in PARTES if not (RAIZ / p[0]).exists()]
    if em_falta:
        print(f"AVISO: a saltar partes sem ficheiro: {', '.join(em_falta)}")
        PARTES[:] = [p for p in PARTES if (RAIZ / p[0]).exists()]
    registar_fontes()
    E = estilos()
    for caminho, *_ in PARTES:
        texto = (RAIZ / caminho).read_text(encoding="utf-8")
        falta = sorted({ch for ch in texto if not ch.isspace() and ord(ch) > 127
                        and ord(ch) not in pdfmetrics.getFont("Corpo").face.charToGlyph})
        if falta:
            print(f"AVISO: {caminho} tem caracteres sem glifo na fonte do corpo: {''.join(falta)}")
    ensaio = Doc(BytesIO(), {}, 0)       # 1.ª passagem: descobrir as páginas de cada parte
    ensaio.build(historia(E))
    doc = Doc(str(SAIDA), ensaio.paginas, ensaio.page)
    doc.build(historia(E))
    print(f"{SAIDA}: {doc.page} páginas "
          f"({', '.join(f'parte {k[-1]} → p. {v}' for k, v in doc.paginas.items())})")


if __name__ == "__main__":
    main()
