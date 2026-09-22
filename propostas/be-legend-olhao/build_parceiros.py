#!/usr/bin/env python3
"""Gera parceiros.html → PDF "Programa de parceiros" (Be Legend).
Render: NODE_PATH=$(npm root -g) node render.js parceiros.html Be-Legend-Programa-de-Parceiros.pdf"""
import build as B
from build import esc, NAVY, GOLD, TEAL, LINE, MUTED, INK, PAPER

C = dict(B.CFG)
MESES = ["Set", "Out", "Nov", "Dez", "Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago"]
LAG = 3  # fecho em setembro → dezembro grátis (outubro e novembro de intervalo)

def page(cls, inner, num=None, footer=True):
    ft = f'<footer class="ft"><span>{esc(C["marca"])} · Programa de parceiros · {esc(C["cliente"])}</span><span>{num or ""}</span></footer>' if footer else ""
    return f'<section class="page {cls}">{inner}{ft}</section>'

def h(kicker, title, lead=None):
    out = f'<p class="kicker">{kicker}</p><h2>{title}</h2>'
    if lead: out += f'<p class="lead">{lead}</p>'
    return out

def strip(closes, label):
    """closes: dict {mes_idx: n negócios fechados}. Meses grátis: por cada fecho, um mês, a partir de idx+LAG, em sequência."""
    free = []
    queue = []
    for i in range(12):
        queue += [i + LAG] * closes.get(i, 0)
    # sequência: nunca dois no mesmo mês; empurra para o próximo livre
    taken = set()
    for m in sorted(queue):
        while m in taken: m += 1
        taken.add(m)
    free = sorted(taken)
    W, H = 1000, 118
    cw = W / 12
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for i, m in enumerate(MESES):
        x = i * cw
        is_close = i in closes; is_free = i in free
        fill = TEAL if is_free else "#fff"
        stroke = GOLD if is_close else ("#D6D0C2" if not is_free else TEAL)
        o.append(f'<rect x="{x+3}" y="26" width="{cw-6}" height="54" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{2.4 if is_close else 1.4}"/>')
        o.append(f'<text x="{x+cw/2}" y="59" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="18" fill="{"#fff" if is_free else INK}">{m}</text>')
        lab = []
        if is_close:
            n = closes[i]
            o.append(f'<circle cx="{x+cw-8}" cy="26" r="11" fill="{GOLD}"/><text x="{x+cw-8}" y="30.5" text-anchor="middle" font-family="Barlow Condensed" font-weight="800" font-size="13" fill="{NAVY}">{n}</text>')
            lab.append("fecho" if n == 1 else f"{n} fechos")
        if is_free: lab.append("grátis")
        if lab:
            o.append(f'<text x="{x+cw/2}" y="98" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" fill="{TEAL if is_free else MUTED}" font-weight="500">{" · ".join(lab)}</text>')
    o.append("</svg>")
    return f'<div class="ex"><p class="exl">{label}</p>{"".join(o)}</div>'

pages = []

pages.append(page("", f'''
<div class="topbar"><span class="brand">{esc(C["marca"])}</span><span class="mono">{esc(C["data"])}</span></div>
<p class="kicker">{esc(C["cliente"])} · programa de parceiros</p>
<h2 class="big">Um mês grátis por cada cliente que nos apresentem.</h2>
<p class="lead">O Be Legend conhece donos de negócios em Olhão, Faro e Lisboa. Cada apresentação que se transforme em cliente da Pacheco Studios devolve ao Be Legend um mês inteiro da mensalidade do sistema. Sem limite, sem letras pequenas.</p>
<div class="rule">
  <span class="mono">a regra, numa frase</span>
  <p>Por cada negócio fechado a partir de uma recomendação do Be Legend, <b>a mensalidade do sistema fica grátis um mês</b>, com dois meses de intervalo: fecho em setembro, dezembro grátis. Dois negócios, dois meses. E assim sucessivamente.</p>
</div>
<h3 class="mt">Como fica no calendário</h3>
{strip({0: 1}, "Um negócio fechado em setembro → dezembro grátis.")}
{strip({0: 2}, "Dois negócios fechados em setembro → dezembro e janeiro grátis.")}
{strip({0: 1, 1: 1, 5: 1}, "Um em setembro, um em outubro, um em fevereiro → dezembro, janeiro e maio grátis. Os meses nunca se perdem: se dois calharem no mesmo mês, o segundo passa para o seguinte.")}
<div class="legend"><span><i class="c"></i>mês do fecho</span><span><i class="f"></i>mês grátis</span></div>
<p class="fine">Cada mês grátis vale {esc(C["mensal"])} + IVA, a mensalidade que cobre os três ginásios. O intervalo de dois meses é o tempo de o novo cliente arrancar e pagar a montagem.</p>
''', 1))

pages.append(page("", h("Como funciona", "Três passos. O trabalho é nosso.") + f'''
<ol class="ol big">
  <li><b>Apresentar.</b> O Be Legend envia a mensagem abaixo a um dono de negócio que conhece, ou dá-nos o contacto com autorização para o abordarmos em nome do ginásio. Uma frase chega.</li>
  <li><b>Nós tratamos do resto.</b> Demonstração feita à medida desse negócio, proposta, reunião, montagem. O Be Legend não tem de acompanhar nada.</li>
  <li><b>Fecho.</b> Quando o cliente apresentado assina e paga a montagem, conta. Passam dois meses e, no terceiro, a mensalidade do Be Legend é zero. Aparece na fatura como “mês de parceiro”.</li>
</ol>
<div class="cols2 mt">
  <div>
    <h3>O que conta</h3>
    <ul class="ul">
      <li>Qualquer negócio novo para a Pacheco Studios: ginásios, restaurantes, lojas, clínicas, serviços. Qualquer serviço nosso com montagem paga.</li>
      <li>Apresentação feita por qualquer pessoa da equipa Be Legend, em qualquer dos três ginásios.</li>
      <li>Sem limite de recomendações nem de meses grátis. Doze fechos num ano, um ano grátis.</li>
    </ul>
  </div>
  <div>
    <h3>Condições</h3>
    <ul class="ul">
      <li>O mês grátis é um desconto na mensalidade; não é convertível em dinheiro.</li>
      <li>Vale enquanto o contrato do sistema estiver ativo.</li>
      <li>Conta a partir do pagamento da montagem pelo cliente apresentado, não da assinatura.</li>
      <li>O Be Legend recebe uma confirmação por escrito de cada fecho, com o mês grátis marcado.</li>
    </ul>
  </div>
</div>
<h3 class="mt">A mensagem pronta a enviar</h3>
<div class="phone">
  <div class="bub"><p>Olá [nome], é o [nome] do Be Legend. Estamos a usar um sistema da Pacheco Studios que trata do acompanhamento dos nossos clientes por WhatsApp e que nos poupou as chamadas todas. Achei que fazia sentido para o teu negócio. Se quiseres ver como funciona, fala com o Tomás: {esc(C["email"])}. Diz que vais da minha parte.</p><span class="mono">modelo · o Be Legend adapta à sua maneira</span></div>
</div>
<div class="callout final">
  <div><b>{esc(C["marca"])}</b><br><span>Web design e sistemas para negócios locais · Algarve</span></div>
  <div class="r"><span class="mono">{esc(C["email"])}</span></div>
</div>
''', 2))

EXTRA = f"""
.topbar{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:26px}}
.topbar .brand{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13pt;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}}
h2.big{{font-size:40pt;margin-bottom:10px}}
.lead{{max-width:160mm}}
.rule{{background:var(--navy);color:#fff;border-radius:12px;padding:16px 20px;margin-top:8px}}
.rule .mono{{display:block;color:var(--gold);margin-bottom:6px}}
.rule p{{font-family:'Barlow Condensed',sans-serif;font-weight:600;font-size:17pt;line-height:1.25;color:#fff}}
.rule b{{color:var(--gold);font-weight:800}}
.ex{{margin-top:6px}}
.ex svg{{width:100%;height:auto}}
.exl{{font-size:10pt;color:#3A3F4B;margin:6px 0 -4px}}
.legend{{display:flex;gap:18px;margin-top:6px;font-size:9.2pt;color:var(--muted)}}
.legend i{{display:inline-block;width:14px;height:10px;border-radius:3px;margin-right:6px;vertical-align:middle}}
.legend i.c{{border:2px solid var(--gold);background:#fff}}
.legend i.f{{background:var(--teal)}}
.ol.big li{{font-size:10.6pt;margin-bottom:10px;padding-left:34px}}
.ol.big li::before{{width:24px;height:24px;line-height:24px;font-size:13pt}}
.phone{{background:#EFEAE2;border-radius:14px;padding:12px;border:1px solid #E1DACB;margin-top:4px}}
.phone .bub{{margin:0}}
.callout.final{{margin-top:16px}}
"""

doc = f"""<!DOCTYPE html>
<html lang="pt-PT"><head><meta charset="utf-8"><title>Programa de parceiros · {esc(C["cliente"])}</title>
<style>{B.CSS}{EXTRA}</style></head><body>{''.join(pages)}</body></html>"""
(B.HERE / "parceiros.html").write_text(doc, encoding="utf-8")
print("parceiros.html", len(doc) // 1024, "KB")
