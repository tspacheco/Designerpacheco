#!/usr/bin/env python3
"""Gera resumo.html → PDF curto "O que vai mudar" (Be Legend Olhão).
Reutiliza fontes, cores e CSS de build.py. Render: NODE_PATH=$(npm root -g) node render.js resumo.html Be-Legend-Olhao-O-que-vai-mudar.pdf"""
import build as B
from build import esc, NAVY, GOLD, TEAL, LINE, MUTED, INK, PAPER

C = dict(B.CFG)

def page(cls, inner, num=None, footer=True):
    ft = f'<footer class="ft"><span>{esc(C["marca"])} · O que vai mudar · {esc(C["cliente"])} {esc(C["local"])}</span><span>{num or ""}</span></footer>' if footer else ""
    return f'<section class="page {cls}">{inner}{ft}</section>'

def h(kicker, title, lead=None):
    out = f'<p class="kicker">{kicker}</p><h2>{title}</h2>'
    if lead: out += f'<p class="lead">{lead}</p>'
    return out

# ---------- stepper SVG (6 passos, horizontal) ----------
def stepper():
    steps = [
        ("clock", "1", "09:00", "O sistema lê a lista"),
        ("branch", "2", "classifica", "Percebe a situação"),
        ("msg", "3", "WhatsApp", "Envia o toque certo"),
        ("wait", "4", "espera", "3 toques em 7 dias"),
        ("phone", "5", "receção", "Liga a quem respondeu"),
        ("chart", "6", "painel", "Números à 2.ª feira"),
    ]
    W, H = 1000, 150
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    n = len(steps); gap = W / n
    for i, (ic, num, tag, lab) in enumerate(steps):
        cx = gap * i + gap / 2
        human = ic == "phone"
        col = TEAL if human else (GOLD if i == 0 else NAVY)
        if i < n - 1:
            s.append(f'<line x1="{cx+34}" y1="52" x2="{cx+gap-34}" y2="52" stroke="{LINE}" stroke-width="2" stroke-dasharray="4 4"/>')
        s.append(f'<circle cx="{cx}" cy="52" r="30" fill="{"#E6F2F0" if human else ("#FBF3E1" if i==0 else "#EEF0F4")}" stroke="{col}" stroke-width="2"/>')
        s.append(B.icon(ic, cx - 12, 40, col))
        s.append(f'<text x="{cx}" y="104" text-anchor="middle" font-family="JetBrains Mono" font-size="11" fill="{MUTED}">{num} · {esc(tag)}</text>')
        s.append(f'<text x="{cx}" y="126" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="17" fill="{INK}">{esc(lab)}</text>')
    s.append("</svg>")
    return "".join(s)

pages = []

# 1 — capa curta + antes/depois na mesma página
before_after = [
    ("Quem faz o primeiro contacto", "A receção, ao telefone, 100+ vezes por dia.", "O sistema, por WhatsApp, todos os dias às 09:00. Sem ninguém carregar em nada."),
    ("Quantas tentativas", "Uma chamada. Se não atende, fica dependente de alguém se lembrar.", "Três mensagens em sete dias, cada uma diferente. Depois pára sozinho."),
    ("A quem a receção liga", "A toda a gente, incluindo quem nunca atende.", "Só a quem respondeu “sim” ou “depois”. Lista curta, com o motivo e a resposta."),
    ("O que fica registado", "Nada, ou notas soltas.", "Cada envio, cada resposta, cada chamada e o resultado. Automático."),
    ("O que o dono vê", "Não sabe quantos leads viraram inscrição nem quantos membros saíram.", "Um painel à 2.ª feira: enviadas, respostas, chamadas, recuperados."),
]
rows = "".join(f'<tr><td class="lab">{esc(a)}</td><td class="bef">{esc(b)}</td><td class="aft">{esc(c)}</td></tr>' for a, b, c in before_after)
pages.append(page("", f'''
<div class="topbar"><span class="brand">{esc(C["marca"])}</span><span class="mono">{esc(C["data"])}</span></div>
<p class="kicker">{esc(C["cliente"])} · {esc(C["local"])} · resumo em 2 minutos</p>
<h2 class="big">O que vai mudar.</h2>
<p class="lead">Hoje a receção faz mais de 100 chamadas por dia e quase ninguém atende. O sistema que propomos faz o primeiro contacto por WhatsApp, insiste por si, e entrega à receção só quem já respondeu. Em cinco linhas, é isto que muda:</p>
<table class="tbl ba">
  <thead><tr><th></th><th>Hoje</th><th>Com o sistema</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<div class="callout"><b>A chamada passa a ser o último passo, não o primeiro.</b> A receção deixa de gastar a manhã a marcar números e passa a falar com quem quer falar.</div>
''', 1))

# 2 — o fluxo em 6 passos + o que o dono decide em cada um
decide = [
    ("1 · Quando", "A hora e os dias em que as mensagens saem.", "09:00, de 2.ª a sábado"),
    ("2 · Quem entra", "O que conta como “inativo”, “lead” ou “em atraso”, e por onde começamos.", "inativo = 14 dias sem entrada; começar pelos inativos"),
    ("3 · O que se diz", "O texto de cada mensagem e quem a assina.", "escrito convosco, assinado por alguém da receção"),
    ("4 · Quantas vezes", "O número de toques e o intervalo entre eles.", "3 toques: dia 0, dia 3, dia 7"),
    ("5 · Quem liga", "Quem recebe a lista, a que horas, e o que conta como resultado.", "receção, lista às 09:15, resultado com um toque"),
    ("6 · O que se mede", "Os números que aparecem no painel e para quem vão.", "enviadas · respostas · chamadas · recuperados, à 2.ª feira"),
]
cards = "".join(f'<div class="dc"><span class="mono">{esc(a)}</span><p>{esc(b)}</p><em>a nossa proposta: {esc(c)}</em></div>' for a, b, c in decide)
pages.append(page("", h("O fluxo em seis passos", "Simples de perceber, e cada passo é afinável.") + f'''
<div class="stepper">{stepper()}</div>
<div class="adjust"><b>Nada disto está fechado.</b> Cada passo tem uma proposta nossa, mas a decisão é da casa. Se o dono quiser que alguma parte funcione de outra maneira, ajustamos antes de arrancar, ou durante o piloto, sem custo extra.</div>
<div class="grid3 dgrid">{cards}</div>
''', 2))

# 3 — investimento + próximos passos
pages.append(page("", h("Investimento", "Um sistema para todos os Legends de Portugal.") + f'''
<div class="pricebox">
  <div class="pl">
    <span class="mono">montagem · pagamento único</span>
    <b>{esc(C["setup"])}</b>
    <span class="mono">acompanhamento · por mês</span>
    <b class="m">{esc(C["mensal"])}</b>
    <p>A mensalidade cobre <b class="t">todos os ginásios Be Legend em Portugal</b>. Custos de plataforma (n8n e mensagens WhatsApp, cêntimos por conversa) pagos ao custo, em nome do ginásio.</p>
  </div>
  <ul class="ul tight pr">
    <li>Construção dos 5 fluxos: leads, aulas experimentais, inativos, pagamentos, renovações</li>
    <li>Um sistema, replicado por ginásio: Olhão primeiro, Faro e Lisboa a seguir, sem nova montagem</li>
    <li>Mensagens escritas com a equipa, na voz do Be Legend, e registadas na Meta</li>
    <li>Ligação ao software do ginásio ou à folha de contactos</li>
    <li>Lista diária da receção e painel por ginásio, no telemóvel</li>
    <li>Formação das receções, piloto de {esc(C["piloto_dias"])} dias acompanhado</li>
    <li>Mensalidade: sistema vigiado, ajustes sem limite, relatório mensal, suporte direto</li>
  </ul>
</div>
<h3 class="mt">Os três passos seguintes</h3>
<ol class="ol">
  <li><b>Reunião de 30 minutos</b> com o dono e a receção: confirmar o software do ginásio e decidir os seis passos da página anterior.</li>
  <li><b>Aprovação das mensagens</b> pelo ginásio. Nada sai sem ser lido pela casa.</li>
  <li><b>Piloto de {esc(C["piloto_dias"])} dias</b> só com os membros inativos. Na revisão, olhamos para um número: quantos voltaram.</li>
</ol>
<div class="callout final">
  <div><b>{esc(C["marca"])}</b><br><span>Web design e sistemas para negócios locais · Algarve</span></div>
  <div class="r"><span class="mono">{esc(C["email"])}</span></div>
</div>
<p class="fine">O esquema completo, com o diagrama do fluxo, as mensagens exemplo e a lista da receção, está no documento “Follow-up &amp; Recuperação de Clientes” que acompanha este resumo.</p>
''', 3))

EXTRA = f"""
.topbar{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:26px}}
.topbar .brand{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13pt;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}}
h2.big{{font-size:44pt;margin-bottom:10px}}
.lead{{max-width:160mm}}
.tbl.ba{{margin-top:10px}}
.tbl.ba th{{font-size:8.5pt}}
.tbl.ba th:nth-child(2){{color:var(--muted)}}
.tbl.ba th:nth-child(3){{color:var(--teal)}}
.tbl.ba td{{padding:11px 10px;font-size:10.2pt;line-height:1.45}}
.tbl.ba td.lab{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13pt;color:var(--navy);width:38mm;line-height:1.1}}
.tbl.ba td.bef{{color:#5B6070;width:60mm}}
.tbl.ba td.aft{{color:var(--ink);background:#F2F8F7;border-left:3px solid var(--teal)}}
.callout{{margin-top:16px}}
.stepper{{margin:6px 0 12px}}
.stepper svg{{width:100%;height:auto}}
.adjust{{background:var(--navy);color:#fff;border-radius:10px;padding:14px 16px;font-size:10.6pt;margin-bottom:14px}}
.adjust b{{color:var(--gold)}}
.dgrid{{grid-template-columns:repeat(2,1fr);gap:10px}}
.dc{{background:var(--paper);border:1px solid #EAE5DA;border-radius:10px;padding:14px 14px 12px}}
.dc .mono{{display:block;color:var(--gold);margin-bottom:4px;font-size:9pt}}
.dc p{{font-size:10.2pt;color:var(--ink);margin-bottom:6px}}
.dc em{{display:block;font-style:normal;font-size:9.2pt;color:var(--teal)}}
.pricebox{{display:grid;grid-template-columns:1fr 1.15fr;gap:20px;background:var(--paper);border:1px solid #EAE5DA;border-radius:12px;padding:22px 24px;margin-top:6px}}
.pricebox .pl b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:44pt;line-height:1;color:var(--navy);margin:4px 0 12px}}
.pricebox .pl b.m{{font-size:30pt;color:var(--teal)}}
.pricebox .pl p b.t{{display:inline;font-family:Inter;font-weight:700;font-size:inherit;color:var(--navy);margin:0}}
.pricebox .pl p{{font-size:9.6pt;color:#3A3F4B}}
.ul.pr li{{font-size:10pt;margin-bottom:6px}}
"""

doc = f"""<!DOCTYPE html>
<html lang="pt-PT"><head><meta charset="utf-8"><title>O que vai mudar · {esc(C["cliente"])} {esc(C["local"])}</title>
<style>{B.CSS}{EXTRA}</style></head><body>{''.join(pages)}</body></html>"""
(B.HERE / "resumo.html").write_text(doc, encoding="utf-8")
print("resumo.html", len(doc) // 1024, "KB")
