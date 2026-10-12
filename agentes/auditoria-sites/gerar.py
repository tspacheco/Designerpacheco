#!/usr/bin/env python3
"""Agente 3 · biblioteca e ranking (Pacheco Studios).

Lê o que a PONTE mediu (auditorias/dados/<slug>.json, operação «auditar») e as fichas Google (candidatos.csv).

  python3 gerar.py        auditorias/RANKING.md: todos os sites medidos, do mais fraco ao mais forte

As páginas para os donos (Raio-X do primeiro contacto, o gatilho grátis da consultoria) saem de raiox.py, que usa
as funções daqui.
"""
import base64, csv, io, json, os, re, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
DADOS = os.path.join(RAIZ, "auditorias", "dados")
SAIDA = os.path.join(RAIZ, "auditorias")
RAMO = "claude/auditoria-sites-fracos-fpyd0h"
ANO = datetime.date.today().year

# Demo nossa medida com a mesma ferramenta, por tipo de negócio («o que podia ser»).
DEMO_POR_TIPO = [
    (r"barber|frizer|saloon|tuns", "trend-barbershop", "Trend Barbershop"),
    (r"flor|fleur|flower|floral|bujor|rosalia", "elenor", "Florăria Elenor"),
    (r"cofetar|patiser|tort|cake|creme|gelat|brut[aă]r|p[aâ]ine|paini|desert", "laurinda", "Cofetăria Laurinda"),
    (r"vet|pet|animal", "pumbavet", "PumbaVet"),
    (r"sp[aă]l[aă]tor|wash|detailing", "auto-spa", "Auto Spa & Detailing"),
    (r"auto|motors|service|vulcan|termo|geam|tâmpl|tampl|ferestre", "la-punct", "Service Auto La Punct"),
    (r"cafe|coffee|cafenea|roast", "fika", "Fika"),
    (r"shaorm|shaworm|tacos|fast|kebab", "dubai-shaworma", "Dubai Shaworma"),
    (r"pizz|restaurant|bistro|conac|c[aâ]rcium|berăr|berar|trai|rustic|cheffa|vindum|vin", "la-gioia", "La Gioia di Giovanni"),
    (r"salon|beauty|nail|unghii|lash|gene|estetic|skin|body|clinic|masaj|tatu|tattoo|ink|epil|fit|kinetic", "beauty-zone", "Beauty Zone"),
]
DEMO_PADRAO = ("fika", "Fika")
# Fora do --top: lojas de cadeia (a decisão não é local, PLAYBOOK §11).
EXCLUIR = {"magazin-aurora-iasi-calea-gala", "tacos-king-ia-i", "doppio-zero-iasi"}

# Think with Google (2017), «Find out how you stack up to new industry benchmarks for mobile page speed»:
# quando o carregamento passa de 1 s para X s, a probabilidade de o visitante sair (bounce) aumenta Y %.
GOOGLE_ABANDONO = [(10, 123), (6, 106), (5, 90), (3, 32)]
FONTE_GOOGLE = "Think with Google, 2017 — «Find out how you stack up to new industry benchmarks for mobile page speed»"

def ler_candidatos():
    return {r["slug"]: r for r in csv.DictReader(open(os.path.join(AQUI, "candidatos.csv"), encoding="utf-8"))}


def ler(slug):
    p = os.path.join(DADOS, f"{slug}.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def aud(d, k, campo="valor"):
    return ((d or {}).get("auditorias", {}).get(k) or {}).get(campo)


def seg(ms):
    return None if ms is None else round(ms / 1000, 1)


def demo_para(c):
    txt = f"{c.get('categoria', '')} {c.get('nome', '')} {c.get('site', '')}".lower()
    for rx, slug, nome in DEMO_POR_TIPO:
        if re.search(rx, txt):
            return slug, nome
    return DEMO_PADRAO


def verificacoes(d, c):
    """Cada verificação: (chave, passou?) — None quando não foi possível medir."""
    p = d.get("pagina") or {}
    if not p:
        return []
    url = d.get("url_final_tel") or d.get("url_final") or d.get("url", "")
    tipos = " ".join(map(str, p.get("jsonld") or [])).lower()
    marc = re.search(r"salon|barber|frizer|beauty|nail|unghii|lash|gene|estetic|clinic|masaj|tatu|tattoo|vet|service|restaurant|bistro|pizz|kinetic|fit",
                     f"{c.get('categoria', '')} {c.get('nome', '')}".lower())
    out = [
        ("https", url.startswith("https://")),
        ("viewport", "width=device-width" in (p.get("viewport") or "")),
        ("cabe", not p.get("transborda")),
        ("tel", (p.get("tel") or 0) > 0),
        ("tel1", bool(p.get("tel_no_1o_ecra"))),
        ("whatsapp", (p.get("whatsapp") or 0) > 0),
    ]
    if marc:
        out.append(("marcacao", (p.get("marcacao") or 0) > 0))
    out += [
        ("mapa", (p.get("mapa") or 0) > 0),
        ("jsonld", any(t in tipos for t in ("localbusiness", "restaurant", "store", "salon", "barber", "beauty",
                                                "clinic", "veterinary", "autorepair", "bakery", "florist", "cafe",
                                                "foodestablishment", "health", "automotive", "professionalservice"))),
        ("descricao", len((p.get("descricao") or "").strip()) >= 50),
    ]
    if p.get("ano_copyright"):
        out.append(("ano", p["ano_copyright"] >= ANO - 1))
    return out


def fraqueza(d, c):
    """0–100: quanto mais alto, mais fraco o site (e mais fácil mostrar a diferença)."""
    if not d:
        return None
    if d.get("erro_pagina") and not d.get("notas"):
        return 100
    n = dict(d.get("notas") or {})
    if n.get("performance") == 0 and aud(d, "largest-contentful-paint") is None:
        n["performance"] = 50  # o Lighthouse não apanhou o LCP: nota 0 não é real
    f = (100 - n.get("performance", 50)) * 0.35 + (100 - n.get("seo", 80)) * 0.15 + (100 - n.get("accessibility", 80)) * 0.1
    pesos = {"https": 10, "viewport": 15, "cabe": 8, "tel": 10, "tel1": 5, "whatsapp": 5, "marcacao": 6,
             "jsonld": 4, "descricao": 3, "ano": 6, "mapa": 2}
    for k, ok in verificacoes(d, c):
        if ok is False:
            f += pesos.get(k, 2)
    lcp = seg(aud(d, "largest-contentful-paint"))
    if lcp and lcp > 4:
        f += min(10, (lcp - 4) * 2)
    return round(min(100, f))


def nota_num(c):
    try:
        return float(c.get("nota", "0").replace(",", "."))
    except ValueError:
        return 0


def ranking(cands):
    linhas = []
    for slug, c in cands.items():
        d = ler(slug)
        if not d:
            continue
        fr = fraqueza(d, c)
        n = d.get("notas") or {}
        linhas.append((fr, slug, c, d, n))
    linhas.sort(key=lambda x: (-(x[0] or 0), -nota_num(x[2])))
    return linhas


def escrever_ranking(cands):
    linhas = ranking(cands)
    demos = {s: ler(f"demo-{s}") for _, s, _ in DEMO_POR_TIPO + [(None,) + DEMO_PADRAO]}
    out = ["# Agente 3 · ranking dos sites medidos (Iași)", "",
           "Do mais fraco para o mais forte. Fraqueza 0–100 (velocidade, SEO, acessibilidade e o que falta ao cliente no telemóvel). "
           "Medido pela PONTE (`auditar`): Lighthouse móvel + Chromium com ecrã de iPhone. Regerar: `python3 agentes/auditoria-sites/gerar.py ranking`.", "",
           "## As nossas demos, medidas da mesma forma", "", "| Demo | Velocidade | SEO | Acess. | Conteúdo principal |", "|---|---|---|---|---|"]
    for s, d in demos.items():
        if d and d.get("notas"):
            n = d["notas"]
            out.append(f"| {s} | {n.get('performance')} | {n.get('seo')} | {n.get('accessibility')} | {seg(aud(d, 'largest-contentful-paint'))} s |")
    out += ["", "## Negócios", "", "| # | Fraqueza | Negócio | Google | Velocidade | SEO | Conteúdo principal | Falta | Site |", "|---|---|---|---|---|---|---|---|---|"]
    for i, (fr, slug, c, d, n) in enumerate(linhas, 1):
        falta = [k for k, ok in verificacoes(d, c) if ok is False]
        lcp = seg(aud(d, "largest-contentful-paint"))
        erro = "não abre" if d.get("erro_pagina") and not n else ""
        out.append(f"| {i} | {fr} | {c['nome']} ({slug}) | {c.get('nota')}{' · ' + c['avaliacoes'] if c.get('avaliacoes') else ''} | "
                   f"{n.get('performance', '—')} | {n.get('seo', '—')} | {str(lcp) + ' s' if lcp else '—'} | {erro or ', '.join(falta) or '—'} | {c['site']} |")
    open(os.path.join(SAIDA, "RANKING.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    return linhas


def b64img(path, largura=520):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


CSS = """
@page{size:A4;margin:0}
:root{--carvao:#141210;--osso:#EFEAE3;--papel:#FAF8F4;--laranja:#E8622C;--laranja-t:#A64923;--linha:#D9D2C6;--cinza:#6B655C;
--mau:#C4372B;--medio:#B7791F;--bom:#2F7D5B;--display:"Archivo Black",system-ui,sans-serif;--corpo:"Archivo",system-ui,sans-serif;--num:"JetBrains Mono",ui-monospace,monospace}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#E7E1D7}
body{font:400 10.5pt/1.45 var(--corpo);color:var(--carvao);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.folha{width:210mm;height:297mm;margin:0 auto 10mm;background:var(--papel);padding:16mm 15mm 14mm;position:relative;display:flex;flex-direction:column;page-break-after:always;break-after:page;overflow:hidden}
.folha:last-child{page-break-after:auto;break-after:auto}
@media print{html{background:none}.folha{margin:0}}
.topo{display:flex;align-items:center;justify-content:space-between;font:600 8pt/1 var(--corpo);letter-spacing:.14em;text-transform:uppercase;color:var(--cinza);margin-bottom:9mm}
.topo .marca{display:flex;align-items:center;gap:8px;color:var(--carvao)}
.topo svg{width:26px;height:26px}
.etiqueta{align-self:flex-start;display:inline-block;background:var(--laranja);color:#fff;font:700 7.5pt/1 var(--corpo);letter-spacing:.16em;text-transform:uppercase;padding:5px 8px 4px;border-radius:2px}
h1{font:400 30pt/0.98 var(--display);text-transform:uppercase;letter-spacing:-.01em;margin:4mm 0 3mm;max-width:16ch}
h1 em{font-style:normal;color:var(--laranja)}
h2{font:400 17pt/1 var(--display);text-transform:uppercase;margin-bottom:4mm}
.dominio{font:500 10pt/1 var(--num);color:var(--cinza)}
.elogio{font:500 12pt/1.4 var(--corpo);margin-top:4mm;max-width:52ch}
.medido{font-size:8pt;color:var(--cinza);margin-top:2mm}
.duelo{display:grid;grid-template-columns:1fr 1fr;gap:7mm;margin-top:7mm;flex:1}
.lado{border:1px solid var(--linha);border-radius:6px;padding:5mm;background:#fff;display:flex;flex-direction:column;gap:4mm}
.lado.nosso{background:var(--carvao);color:var(--osso);border-color:var(--carvao)}
.lado h3{font:400 11pt/1 var(--display);text-transform:uppercase;letter-spacing:.02em}
.lado .sub{font-size:7pt;line-height:1.3;color:var(--cinza);margin-top:-2.5mm;min-height:4em}
.lado.nosso .sub{color:#A9A196}
.tel{width:43mm;height:88mm;margin:0 auto;border-radius:7mm;border:2.2mm solid #1E1C1A;background:#1E1C1A;overflow:hidden;box-shadow:0 6px 18px rgba(0,0,0,.18)}
.lado.nosso .tel{border-color:#3A3631;background:#3A3631}
.tel img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;border-radius:4.5mm}
.aneis{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm}
.anel{position:relative;text-align:center}
.anel svg{width:100%;max-width:17mm;display:block;margin:0 auto;transform:rotate(-90deg)}
.anel .trilho{fill:none;stroke:rgba(128,120,110,.22);stroke-width:6}
.anel .arco{fill:none;stroke-width:6;stroke-linecap:round}
.anel b{position:absolute;top:0;left:0;right:0;height:17mm;display:flex;align-items:center;justify-content:center;font:700 12pt/1 var(--num)}
.lado.nosso .anel b{filter:brightness(1.35)}
.anel span{display:block;font-size:6.5pt;line-height:1.15;margin-top:1mm;letter-spacing:.02em}
.tempos{display:grid;gap:1.6mm;font-size:8pt}
.tempos div{display:flex;justify-content:space-between;border-top:1px dashed rgba(128,120,110,.35);padding-top:1.4mm}
.tempos b{font:700 9pt/1 var(--num)}
table.chk{width:100%;border-collapse:collapse;font-size:10pt}
table.chk td{padding:2.4mm 0;border-bottom:1px solid var(--linha);vertical-align:middle}
table.chk td.r{text-align:right;width:20mm}
.pill{display:inline-block;min-width:13mm;text-align:center;padding:3px 7px 2px;border-radius:20px;font:700 7.5pt/1.2 var(--corpo);letter-spacing:.06em;text-transform:uppercase}
.pill.s{background:#E3F0E9;color:var(--bom)}.pill.n{background:#F7E1DD;color:var(--mau)}
.numeros{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin:6mm 0 7mm}
.numeros div{border:1px solid var(--linha);border-radius:5px;padding:3.5mm;background:#fff}
.numeros b{display:block;font:700 15pt/1 var(--num);margin-bottom:1.5mm}
.numeros span{font-size:7.5pt;color:var(--cinza);line-height:1.25;display:block}
.numeros i{font-style:normal;font:500 7.5pt/1 var(--num);color:var(--bom);display:block;margin-top:1.5mm}
.vit{display:grid;gap:4mm;margin-bottom:7mm}
.v{display:grid;grid-template-columns:11mm 1fr;gap:3mm;border:1px solid var(--linha);border-radius:6px;background:#fff;padding:4mm}
.v .n{font:400 22pt/1 var(--display);color:var(--laranja)}
.v h3{font:700 11.5pt/1.2 var(--corpo);margin-bottom:2mm}
.v dl{display:grid;grid-template-columns:24mm 1fr;gap:1.2mm 3mm;font-size:9pt}
.v dt{font:700 7pt/1.6 var(--corpo);letter-spacing:.12em;text-transform:uppercase;color:var(--cinza)}
.v dd.g{font-weight:700;color:var(--bom)}
.clientes{background:var(--osso);border-radius:6px;padding:5mm;font-size:10pt;display:grid;gap:2mm}
.clientes .grande{font:700 12pt/1.35 var(--corpo)}
.fonte{font-size:7pt;color:var(--cinza)}
.cta{margin-top:auto;background:var(--carvao);color:var(--osso);border-radius:6px;padding:6mm;display:flex;justify-content:space-between;align-items:center;gap:6mm}
.cta h3{font:400 14pt/1.05 var(--display);text-transform:uppercase;margin-bottom:2mm}
.cta p{font-size:9.5pt;color:#CFC8BC;max-width:46ch}
.cta a{flex:none;background:var(--laranja);color:#fff;text-decoration:none;font:700 10pt/1 var(--corpo);padding:4mm 5mm;border-radius:4px;text-align:center}
.cta a small{display:block;font:500 8pt/1 var(--num);margin-top:1.5mm;opacity:.9}
.rodape{display:flex;justify-content:space-between;font-size:7pt;color:var(--cinza);margin-top:5mm;padding-top:3mm;border-top:1px solid var(--linha)}
.notas{font-size:9.5pt;display:grid;gap:3mm}
.notas pre{white-space:pre-wrap;font:400 9pt/1.45 var(--corpo);background:#fff;border:1px solid var(--linha);border-radius:5px;padding:4mm}
.notas h3{font:700 10pt/1 var(--corpo);margin-top:2mm}
"""


def logo_mini():
    return ('<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="31" fill="#141210"/>'
            '<circle cx="32" cy="32" r="27" fill="none" stroke="#C9A256" stroke-width="1.6"/>'
            '<text x="32" y="43" text-anchor="middle" font-family="Archivo Black,sans-serif" font-size="30" fill="#E8622C">P</text></svg>')


def whatsapp(c):
    """Regra do PLAYBOOK: «sim» só com prova pública. Fixo (+40 2…/3…) não tem WhatsApp."""
    t = re.sub(r"\D", "", c.get("telefone", ""))
    return "não (fixo: ligar)" if t.startswith(("402", "403")) else "?"


def nome_curto(c):
    n = re.split(r"\s+[-|–]\s+|,|\(", c["nome"])[0].strip()
    if len(n) > 30:
        n = " ".join(n.split()[:3])
    return n if len(n) <= 40 else n[:38].rsplit(" ", 1)[0]


def pdf(html_path, pdf_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  (sem playwright: só HTML)")
        return False
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
        pg = b.new_page()
        pg.goto("file://" + html_path, wait_until="networkidle")
        pg.pdf(path=pdf_path, format="A4", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        b.close()
    return True


def main():
    """Só o ranking; as páginas para os donos geram-se com raiox.py (Raio-X do primeiro contacto)."""
    for i, (fr, slug, c, d, n) in enumerate(escrever_ranking(ler_candidatos())[:25], 1):
        print(i, fr, slug, n.get("performance"), c.get("nota"))


if __name__ == "__main__":
    main()
