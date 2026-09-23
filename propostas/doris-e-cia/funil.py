#!/usr/bin/env python3
"""Página do funil de anúncios (Doris & Cia) — das impressões até ao cliente que volta.
Importado por build_apresentacao.py. Reconcilia com as premissas de build_checklist.py:
CPM x CTR x MSG dá exatamente o custo por conversa de lá (R$ 8)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "be-legend-olhao"))
import build as B
from build import esc, NAVY, GOLD, TEAL, LINE, MUTED, INK, PAPER
from build_checklist import CPC, AGENDA, TICKET, RECOR

CPM = 25.0      # R$ por 1000 impressões (raio de 3 km, público pequeno → CPM mais alto)
CTR = 0.0125    # dos que veem, quantos tocam no botão
MSG = 0.25      # dos que tocam, quantos escrevem mesmo a primeira mensagem

def ic_(kind, x, y, col):
    """Ícones próprios desta página; os restantes vêm de build.icon."""
    st = f'stroke="{col}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "eye":
        g = f'<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6-10-6-10-6z" {st}/><circle cx="12" cy="12" r="3" {st}/>'
    elif kind == "tap":
        g = f'<path d="M9 11V5.5a1.8 1.8 0 0 1 3.6 0V12" {st}/><path d="M12.6 12V9.6a1.7 1.7 0 0 1 3.4 0V13" {st}/><path d="M16 13v-1.2a1.7 1.7 0 0 1 3.4 0V16a5 5 0 0 1-5 5h-2a5 5 0 0 1-4.3-2.4L6 15.4a1.7 1.7 0 0 1 2.6-2.1L9 14" {st}/>'
    elif kind == "repeat":
        g = f'<path d="M4 10a8 8 0 0 1 13.7-5.6L20 6" {st}/><path d="M20 3v3.5h-3.5" {st}/><path d="M20 14a8 8 0 0 1-13.7 5.6L4 18" {st}/><path d="M4 21v-3.5h3.5" {st}/>'
    else:
        return B.icon(kind, x, y, col)
    return f'<g transform="translate({x},{y})">{g}</g>'

def funil(budget, eff=1.0):
    imp = budget / CPM * 1000
    cli = imp * CTR * eff
    conv = cli * MSG
    cls = conv * AGENDA
    vol = cls * RECOR
    return dict(imp=imp, cli=cli, conv=conv, cls=cls, vol=vol,
                cpc=budget / cli, cpconv=budget / conv, cpa=budget / cls)

def n(x):
    return f"{x:,.0f}".replace(",", ".")
def r(x):
    return "R$ " + n(x)

# ---------- o funil desenhado ----------
def desenho(d):
    W, H = 1000, 424
    rows = [
        ("Impressões",  d["imp"],  "o anúncio aparece na tela de quem mora perto", None,          NAVY,  "eye"),
        ("Cliques",     d["cli"],  "tocam no botão e o WhatsApp abre",             d["cpc"],      NAVY,  "tap"),
        ("Conversas",   d["conv"], "escrevem mesmo a primeira mensagem",           d["cpconv"],   TEAL,  "msg"),
        ("Clientes",    d["cls"],  "agendam, aparecem e pagam R$ 80",                    d["cpa"],      TEAL,  "check"),
        ("Recorrentes", d["vol"],  "voltam no mês seguinte",                       None,          GOLD,  "repeat"),
    ]
    perdas = ["1,2 % tocam", "25 % escrevem", "35 % fecham", "40 % voltam"]
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<defs>'
             f'<marker id="dn" viewBox="0 0 10 10" refX="5" refY="9" markerWidth="7" markerHeight="7" orient="auto">'
             f'<path d="M0 0L5 9L10 0" fill="none" stroke="{LINE}" stroke-width="1.6" stroke-linecap="round"/></marker></defs>')
    bw = [780, 640, 505, 385, 285]   # largura de cada degrau
    y = 8
    for i, (lab, val, sub, custo, col, icn) in enumerate(rows):
        w = bw[i]
        x = (W - w) / 2
        h = 58
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{col}" opacity="{0.10 if col != GOLD else 0.16}"/>')
        o.append(f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2.5" fill="{col}"/>')
        o.append(ic_(icn, x + 18, y + 17, col))
        o.append(f'<text x="{x+56}" y="{y+26}" font-family="Barlow Condensed" font-weight="700" font-size="19" fill="{NAVY}">{esc(lab)}</text>')
        o.append(f'<text x="{x+56}" y="{y+44}" font-family="Inter" font-size="10.5" fill="{MUTED}">{esc(sub)}</text>')
        o.append(f'<text x="{x+w-18}" y="{y+32}" text-anchor="end" font-family="Barlow Condensed" font-weight="800" font-size="28" fill="{col}">{n(val)}</text>')
        if custo:
            o.append(f'<text x="{x+w-18}" y="{y+47}" text-anchor="end" font-family="JetBrains Mono" font-size="9.5" fill="{MUTED}">{r(custo)} de anúncio</text>')
        if i < len(rows) - 1:
            ay = y + h
            o.append(f'<path d="M{W/2},{ay+5} L{W/2},{ay+23}" stroke="{LINE}" stroke-width="1.6" marker-end="url(#dn)"/>')
            o.append(f'<text x="{W/2+14}" y="{ay+19}" font-family="JetBrains Mono" font-size="11" fill="{MUTED}">{esc(perdas[i])}</text>')
        y += h + 30
    o.append("</svg>")
    return "".join(o)

# ---------- o que decide cada degrau ----------
DECIDE = [
    ("Impressões → cliques", "Manda o vídeo.",
     "Vídeo cru do celular, com antes e depois da tosa, bate qualquer arte bonita."),
    ("Cliques → conversas", "Manda o que a pessoa vê ao abrir o WhatsApp.",
     "Três em cada quatro desistem aqui. A mensagem já escrita no link e o perfil verificado da loja resolvem grande parte."),
    ("Conversas → clientes", "Manda o tempo de resposta.",
     "Responder em 10 minutos dobra este número. Responder no dia seguinte mata-o."),
    ("Clientes → recorrentes", "Manda o lembrete automático.",
     "Com a mensagem aos 15 dias, 4 em cada 10 voltam. Sem ela, a loja vive só de cliente novo, que é o caro."),
]

def pagina(page, h, C):
    d8 = funil(800)
    niveis = [(400, funil(400)), (800, d8), (1500, funil(1500, 0.92))]
    trs = "".join(
        f'<tr><td class="lab">{r(b)}</td><td>{n(x["imp"])}</td><td>{n(x["cli"])}</td>'
        f'<td>{n(x["conv"])}</td><td class="hl">{n(x["cls"])}</td><td>{r(x["cpa"])}</td></tr>'
        for b, x in niveis)
    dec = "".join(
        f'<div class="dec"><span class="mono">{esc(a)}</span><b>{esc(t)}</b><p>{esc(p)}</p></div>'
        for a, t, p in DECIDE)
    inner = h("01 · Como funciona",
              "De quem vê o anúncio até quem volta todo mês.",
              "O caminho tem quatro degraus e cada um perde gente. É normal: o que interessa é quanto sobra no fim e quanto custou. O exemplo é com R$ 800 por mês.") + f'''
<div class="fn">{desenho(d8)}</div>
<p class="fine">Premissas: R$ {CPM:.0f} por mil impressões (raio de 3 km), {CTR*100:.2f} % de cliques, {MSG*100:.0f} % dos cliques viram conversa, {AGENDA*100:.0f} % das conversas viram atendimento pago, {RECOR*100:.0f} % voltam no mês seguinte. Os dois primeiros degraus são médias de mercado; os dois últimos dependem de quem atende.</p>
'''
    inner2 = f'''
<h3 class="mt">O mesmo funil, nos três níveis de investimento</h3>
<table class="tbl num2 fnl">
  <thead><tr><th>Por mês</th><th>Impressões</th><th>Cliques</th><th>Conversas</th><th class="hl">Clientes novos</th><th>Custo do anúncio por cliente</th></tr></thead>
  <tbody>{trs}</tbody>
</table>
<h3 class="mt">O que decide cada degrau</h3>
<div class="decs">{dec}</div>
<div class="callout"><b>Onde a Doris &amp; Cia perde hoje:</b> nos dois últimos degraus. O anúncio traz gente, mas se a ficha do Google leva a “loja de répteis” e a resposta demora, o dinheiro para no meio do caminho.</div>
'''
    return page("", inner + inner2, 2)

EXTRA = """
.fn{margin:4px 0 0}
.fn svg{width:100%;height:auto;max-height:95mm}
.tbl.num2.fnl td,.tbl.num2.fnl th{font-size:9.4pt;padding:6px 8px}
.decs{display:grid;grid-template-columns:1fr 1fr;gap:7px 16px;margin-top:2px}
.dec .mono{display:block;color:var(--gold);font-size:8.4pt;margin-bottom:1px}
.dec b{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13pt;color:var(--navy);line-height:1.15}
.dec p{font-size:9pt;color:#3A3F4B;line-height:1.3}
.fn + .fine{margin-top:2px}
.decs + .callout{margin-top:10px}
"""
