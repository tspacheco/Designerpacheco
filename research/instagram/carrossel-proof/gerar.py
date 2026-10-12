"""2.º carrossel fixado do Instagram: «Proof · A real system breakdown» (EN, 12 slides, 1080x1350).

Plano do Tomás (PDF de 12/10/2026): Start Here → Proof → Method. Mesmo visual do 1.º
(escuro, creme e laranja, títulos centrados, diagramas de sistema, um só CTA «DM AUDIT»).
Dados com fonte (pedido do Tomás, 12/10 18h44): HBR 2011 (2 slides de dados), Klarna 2024 e Gartner 2026
em faixas, e o caso real público do Brasil que já está no site (clínica de imagem). Quando houver um caso
da Pacheco Studios com números confirmados, substitui caso_real(); prova() fica para esse formato.
Uso: python3 gerar.py  →  saida/carrossel-proof-en.html; depois
     node ../carrossel-audit/fotografar.js saida/carrossel-proof-en.html saida/en pacheco-proof
"""
import importlib.util
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("base", os.path.join(AQUI, "..", "carrossel-audit", "gerar.py"))
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)
E, rich = base.E, base.rich

CSS_EXTRA = """
.lar .pag span{color:#16110E}
/* gráfico da capa: crescimento linear vs. exponencial (ilustrativo) */
.curva{margin-top:34px;width:900px;height:380px}
.curva text{font-family:"Liberation Sans",Arial,sans-serif}
.curva .t-forte{font-size:27px;font-weight:700;fill:#F5EFE6}
.curva .t-fraco{font-size:23px;fill:#BDB8B2}
.curva .t-gap{font-size:16px;font-weight:700;letter-spacing:.18em;fill:#F59A73}
.curva .t-nota{font-size:17px;fill:#8F8983}
.curva .t-eixo{font-size:15px;font-weight:700;letter-spacing:.18em;fill:#8F8983}
/* trilho da capa: o percurso de um pedido até ter dono */
.trilho{position:absolute;left:250px;top:1068px;width:580px;height:40px;z-index:1}
.trilho::before{content:"";position:absolute;left:0;right:0;top:19px;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.08),rgba(242,111,67,.65))}
.trilho i{position:absolute;top:9px;width:22px;height:22px;margin-left:-11px;border-radius:50%;border:1px solid rgba(255,255,255,.28);background:#121317}
.trilho em{position:absolute;top:6px;width:28px;height:28px;margin-left:-14px;border-radius:50%;background:#FF6A3B;box-shadow:0 0 0 14px rgba(255,106,59,.15)}
/* nó incerto (percurso antigo) */
.diag .n.x{border:1.5px dashed rgba(255,255,255,.30);background:transparent;color:#9C968F}
.diag .l.x{background:repeating-linear-gradient(180deg,rgba(255,255,255,.35) 0 6px,transparent 6px 12px)}
/* linhas numeradas (pergunta da auditoria, camada IA, camada humana) */
.linhas{margin-top:40px;width:800px;text-align:left;border-top:1px solid rgba(255,255,255,.14)}
.linhas div{display:flex;align-items:center;gap:22px;padding:19px 6px;border-bottom:1px solid rgba(255,255,255,.14)}
.linhas span{flex:none;min-width:86px;text-align:center;border-radius:999px;padding:7px 0;font-weight:700;font-size:15px;letter-spacing:.14em}
.linhas p{font-size:27px;line-height:1.25;color:#F5EFE6}
.linhas.ia span{border:1.5px solid rgba(255,106,59,.75);color:#FFA27E}
.linhas.hum span{background:#F5EFE6;color:#141214}
.linhas.q span{border:1.5px solid rgba(255,255,255,.28);color:#C9C4BE}
/* regra desenhada: cadeia de 5 passos sobre o laranja */
.regra{margin-top:46px;display:flex;align-items:stretch;gap:0}
.regra .p{width:168px;height:150px;background:#101115;padding:24px 10px 0;box-shadow:0 9px 0 rgba(150,50,20,.45);text-align:center}
.regra .p small{display:block;font-weight:700;font-size:15px;letter-spacing:.16em;color:#F59A73}
.regra .p b{display:block;margin-top:14px;font-family:"Liberation Serif","Times New Roman",serif;font-size:29px;letter-spacing:-.04em;line-height:1.02;color:#FBF4EC}
.regra .p.u{background:#FBF4EC}.regra .p.u small{color:#B4441E}.regra .p.u b{color:#141214}
.regra .s{width:30px;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700;color:#141214}
/* resultado comprovável */
.prova{margin-top:44px;width:820px;display:grid;gap:14px;text-align:left}
.prova div{display:grid;grid-template-columns:190px 1fr;align-items:center;background:#101115;padding:24px 28px;box-shadow:0 9px 0 rgba(150,50,20,.45)}
.prova small{font-weight:700;font-size:16px;letter-spacing:.16em;color:#F59A73}
.prova p{font-size:25px;line-height:1.3;color:#FBF4EC}
.prova .falta p{color:#FFB08F;border:1.5px dashed rgba(255,176,143,.6);padding:8px 14px}
/* gráficos de barras horizontais: barras a partir do zero, valor em texto, fonte por baixo */
.graf{margin-top:38px;width:840px;text-align:left}
.graf .tit{font-weight:700;font-size:16px;letter-spacing:.16em;margin-bottom:10px}
.graf .row{display:grid;grid-template-columns:230px 1fr 120px;align-items:center;gap:20px;padding:12px 0}
.graf .row p{font-size:24px;line-height:1.2}
.graf .tr{height:38px;display:flex;align-items:center}
.graf .b{height:38px;border-radius:0 4px 4px 0}
.graf .row b{font-family:"Liberation Serif","Times New Roman",serif;font-size:44px;letter-spacing:-.03em;text-align:right;line-height:1}
.esc .graf .tit{color:#9C968F}.esc .graf .row p{color:#E9E2D8}.esc .graf .tr{border-left:2px solid rgba(255,255,255,.4)}
.esc .graf .b{background:rgba(245,239,230,.24)}.esc .graf .b.o{background:#FF6A3B}.esc .graf .row b{color:#F5EFE6}
.lar .graf .tit{color:#4A2112}.lar .graf .row p{color:#1A0F0A}.lar .graf .tr{border-left:2px solid rgba(20,10,5,.55)}
.lar .graf .b{background:rgba(20,10,5,.20)}.lar .graf .b.o{background:#101115}.lar .graf .row b{color:#141214}
.fonte{margin-top:18px;width:840px;font-size:18px;line-height:1.35;text-align:left}
.esc .fonte{color:#8F8983}.lar .fonte{color:#4A2112}
.nota-dado{margin-top:18px;width:840px;text-align:left;font-size:24px;line-height:1.3}
.esc .nota-dado{color:#C9C4BE}.esc .nota-dado b{color:#fff}.lar .nota-dado{color:#4A2112}.lar .nota-dado b{color:#141214}
/* faixa de dados por baixo das listas (slides da IA e do humano) */
.faixa{margin-top:30px;width:840px;padding:22px 28px 20px;text-align:left;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.03)}
.faixa .graf,.faixa .fonte{width:auto;margin-top:0}
.faixa .graf .row{grid-template-columns:110px 1fr 112px;gap:16px;padding:8px 0}
.faixa .graf .tr,.faixa .graf .b{height:30px}
.faixa .graf .row b{font-size:36px}
.faixa .fonte{margin-top:12px;font-size:17px}
.faixa .duo{display:grid;grid-template-columns:1fr 190px;gap:26px;align-items:center}
.faixa .duo .lado{border-left:1px solid rgba(255,255,255,.14);padding-left:24px}
.faixa .duo .lado b,.faixa .grande b{display:block;font-family:"Liberation Serif","Times New Roman",serif;font-size:74px;letter-spacing:-.04em;line-height:1;color:#FF8A5F}
.faixa .duo .lado p{margin-top:6px;font-size:20px;line-height:1.25;color:#E9E2D8}
.faixa .grande{display:grid;grid-template-columns:200px 1fr;gap:24px;align-items:center}
.faixa .grande p{font-size:24px;line-height:1.3;color:#E9E2D8}
.medidor{margin-top:16px;height:16px;background:rgba(245,239,230,.14);border-radius:4px;overflow:hidden}
.medidor i{display:block;height:100%;background:#FF6A3B;border-radius:0 4px 4px 0}
.linhas.apertado{margin-top:30px}.linhas.apertado div{padding:13px 6px}.linhas.apertado p{font-size:25px}
/* números grandes do caso real */
.heroi{margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:16px;width:820px}
.heroi div{background:#101115;padding:24px 28px;text-align:left;box-shadow:0 9px 0 rgba(150,50,20,.45)}
.heroi b{display:block;font-family:"Liberation Serif","Times New Roman",serif;font-size:80px;letter-spacing:-.04em;line-height:1;color:#FF8A5F}
.heroi p{margin-top:10px;font-size:21px;line-height:1.3;color:#E9E2D8}
.prova.dois{margin-top:36px}
"""


def diag_antes():
    """Percurso antigo: 4 canais → caixa partilhada → interpretação manual → passo seguinte incerto."""
    fontes = ["Google", "Instagram", "WhatsApp", "Email"]
    cx = [150, 370, 590, 810]
    h = ['<div class="diag" style="height:400px;border:0">']
    for nome, c in zip(fontes, cx):
        h.append(f'<div class="n" style="left:{c-80}px;top:6px;width:160px;height:60px">{nome}</div>')
        h.append(f'<div class="l" style="left:{c-1}px;top:66px;width:2px;height:30px"></div>')
        h.append(f'<div class="d" style="left:{c}px;top:96px"></div>')
    h.append('<div class="l" style="left:149px;top:95px;width:662px;height:2px"></div>')
    h.append('<div class="d" style="left:480px;top:96px"></div>')
    h.append('<div class="l" style="left:479px;top:96px;width:2px;height:30px"></div>')
    h.append('<div class="n" style="left:350px;top:126px;width:260px;height:62px">Shared inbox</div>')
    h.append('<div class="l" style="left:479px;top:188px;width:2px;height:30px"></div>')
    h.append('<div class="n" style="left:300px;top:218px;width:360px;height:62px">Manual interpretation</div>')
    h.append('<div class="l x" style="left:479px;top:280px;width:2px;height:40px"></div>')
    h.append('<div class="n x" style="left:290px;top:320px;width:380px;height:66px">Uncertain next step&nbsp;&nbsp;?</div>')
    h.append("</div>")
    h.append('<p class="legenda" style="margin-top:14px">The lead was not lost at entry. It was lost <b>between entry and ownership.</b></p>')
    return "".join(h)


def diag_depois():
    """Percurso novo: cada pedido com estado, dono e próximo passo."""
    passos = [("Enquiry", ""), ("Qualification", ""), ("Owner", "o g"), ("Approved response", ""),
              ("Next action", "o"), ("Human handoff", "o")]
    w = [220, 280, 240, 360, 280, 320]
    h = ['<div class="diag" style="height:496px;border:0">']
    y = 4
    for k, ((nome, cls), lw) in enumerate(zip(passos, w)):
        h.append(f'<div class="n {cls}" style="left:{480-lw//2}px;top:{y}px;width:{lw}px;height:56px">{nome}</div>')
        if k < len(passos) - 1:
            h.append(f'<div class="l" style="left:479px;top:{y+56}px;width:2px;height:26px"></div>')
            h.append(f'<div class="d" style="left:480px;top:{y+69}px"></div>')
        y += 82
    h.append("</div>")
    h.append('<p class="legenda" style="margin-top:22px">Every request has <b>a state, an owner and a next action.</b></p>')
    return "".join(h)


def linhas(cls, tag, itens):
    return f'<div class="linhas {cls}">' + "".join(
        f"<div><span>{E(tag)}</span><p>{E(t)}</p></div>" for t in itens) + "</div>"


def regra():
    passos = [("01", "Trigger"), ("02", "Classify"), ("03", "Assign owner"), ("04", "Next action"), ("05", "Escalate")]
    out = []
    for k, (n, nome) in enumerate(passos):
        cls = "p u" if k == len(passos) - 1 else "p"
        out.append(f'<div class="{cls}"><small>{n}</small><b>{E(nome)}</b></div>')
        if k < len(passos) - 1:
            out.append('<div class="s">→</div>')
    return '<div class="regra">' + "".join(out) + "</div>"


def prova():
    # Só prova real e autorizada (plano do Tomás e HONEST-DATA): o que está entre [ ] é para preencher
    linhas_prova = [("BEFORE", "Requests answered from memory, with no clear owner.", ""),
                    ("AFTER", "Every request with a rule, a state and a human handoff.", ""),
                    ("VERIFIED BY", "[client · team · period]", "falta")]
    return '<div class="prova">' + "".join(
        f'<div class="{c}"><small>{a}</small><p>{E(b)}</p></div>' for a, b, c in linhas_prova) + "</div>"


def barras(tit, linhas_graf, escala, cls=""):
    """Barras horizontais a partir do zero; linhas = (rótulo, valor numérico, texto do valor, destaque)."""
    out = [f'<div class="graf {cls}"><div class="tit">{E(tit)}</div>']
    for rot, v, txt, dest in linhas_graf:
        largura = max(0.6, 100 * v / escala)
        out.append(f'<div class="row"><p>{E(rot)}</p><div class="tr"><div class="b{" o" if dest else ""}" '
                   f'style="width:{largura:.1f}%"></div></div><b>{E(txt)}</b></div>')
    return "".join(out) + "</div>"


def fonte(txt):
    return f'<p class="fonte">{E(txt)}</p>'


# Fontes (verificadas a 12/10/2026; lista completa em LEGENDA.md)
F_HBR_AUDIT = "Source: Oldroyd, McElheran & Elkington, “The Short Life of Online Sales Leads”, Harvard Business Review, 2011. Test enquiry sent to 2,241 US companies."
F_HBR_LEADS = "Source: Oldroyd, McElheran & Elkington, Harvard Business Review, 2011. Analysis of 1.25 million leads from 42 companies."
F_KLARNA = "Source: Klarna press release, 27 Feb 2024. Figures reported by the company."
F_GARTNER = "Source: Gartner survey of 3,566 customers, Feb–Mar 2026 (published 4 Aug 2026)."


def dados_resposta():
    return (barras("HOW FAST 2,241 COMPANIES ANSWERED A TEST ENQUIRY",
                   [("Within 1 hour", 37, "37%", False), ("1 to 24 hours", 16, "16%", False),
                    ("After 24 hours", 24, "24%", True), ("Never answered", 23, "23%", True)], 40)
            + '<p class="nota-dado"><b>Almost half answered a day later, or never.</b> The enquiry was there. Nobody owned it.</p>'
            + fonte(F_HBR_AUDIT))


def dados_hora():
    return (barras("LIKELIHOOD OF QUALIFYING THE LEAD (AFTER 24 HOURS = 1×)",
                   [("Within 1 hour", 60, "60×", True), ("After 24 hours", 1, "1×", False)], 60)
            + '<p class="nota-dado">And <b>nearly 7× more likely</b> than companies that called just one hour later.</p>'
            + fonte(F_HBR_LEADS))


def faixa_klarna():
    graf = barras("KLARNA · FIRST MONTH · AVG. RESOLUTION TIME",
                  [("Before", 11, "11 min", False), ("With AI", 2, "< 2 min", True)], 11)
    return ('<div class="faixa"><div class="duo"><div>' + graf + '</div>'
            '<div class="lado"><b>2/3</b><p>of service chats handled by the assistant</p></div></div>'
            + fonte(F_KLARNA) + "</div>")


def faixa_gartner():
    return ('<div class="faixa"><div class="grande"><b>87%</b>'
            '<p>of customers say a company using AI <strong style="color:#fff">must offer a way to reach a human.</strong></p></div>'
            '<div class="medidor"><i style="width:87%"></i></div>' + fonte(F_GARTNER) + "</div>")


def curva_capa():
    """Capa: crescimento linear (mais pessoas, mais horas) vs. exponencial (sistema com IA).
    Curva ilustrativa, sem números nos eixos (HONEST-DATA): os números reais estão nos slides seguintes."""
    import math
    x0, x1, yb, alt = 64, 824, 330, 300
    k = 3.3
    f = lambda u: (math.exp(k * u) - 1) / (math.exp(k) - 1)
    lin = lambda u: 0.36 * u
    px = lambda u: x0 + (x1 - x0) * u
    py = lambda v: yb - alt * v
    us = [i / 80 for i in range(81)]
    exp_pts = " ".join(f"{px(u):.1f},{py(f(u)):.1f}" for u in us)
    # ponto de cruzamento e área entre as curvas depois dele (a diferença)
    uc = next(u for u in us if f(u) >= lin(u) and u > 0.05)
    gap = [u for u in us if u >= uc]
    area = " ".join(f"{px(u):.1f},{py(f(u)):.1f}" for u in gap) + " " + " ".join(
        f"{px(u):.1f},{py(lin(u)):.1f}" for u in reversed(gap))
    grelha = "".join(f'<line x1="{x0}" x2="{x1}" y1="{yb - alt * g:.0f}" y2="{yb - alt * g:.0f}" stroke="rgba(255,255,255,.06)" stroke-width="1"/>'
                     for g in (0.25, 0.5, 0.75, 1))
    ex, ey = px(1), py(1)
    lx, ly = px(1), py(lin(1))
    return f"""<div class="curva"><svg width="900" height="380" viewBox="0 0 900 380" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="gg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF6A3B" stop-opacity=".30"/><stop offset="1" stop-color="#FF6A3B" stop-opacity=".04"/></linearGradient></defs>
{grelha}
<polygon points="{area}" fill="url(#gg)"/>
<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="rgba(255,255,255,.32)" stroke-width="2"/>
<line x1="{x0}" y1="{yb}" x2="{x0}" y2="{yb - alt - 10}" stroke="rgba(255,255,255,.32)" stroke-width="2"/>
<line x1="{px(0):.1f}" y1="{py(0):.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="#BDB5AC" stroke-width="4" stroke-linecap="round"/>
<polyline points="{exp_pts}" fill="none" stroke="#FF6A3B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M{ex + 24:.1f},{ey + 18:.1f} h10 V{ly - 14:.1f} h-10" fill="none" stroke="rgba(245,239,230,.6)" stroke-width="2"/>
<text transform="translate({ex + 62:.1f},{(ey + ly) / 2:.1f}) rotate(-90)" text-anchor="middle" class="t-gap">THE GAP</text>
<circle cx="{ex:.1f}" cy="{ey:.1f}" r="26" fill="rgba(255,106,59,.18)"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="11" fill="#FF6A3B"/>
<circle cx="{lx:.1f}" cy="{ly:.1f}" r="8" fill="#BDB5AC"/>
<text x="{ex - 40:.1f}" y="{ey + 6:.1f}" text-anchor="end" class="t-forte">Systems with AI</text>
<text x="{lx:.1f}" y="{ly + 62:.1f}" text-anchor="end" class="t-fraco">More people, more hours</text>
<text x="{x0 + 14}" y="{yb - alt + 6}" class="t-eixo">GROWTH</text>
<text x="{x1}" y="{yb + 36}" text-anchor="end" class="t-eixo">TIME →</text>
<text x="{x0}" y="{yb + 36}" class="t-nota">Illustrative curve. The real numbers are inside.</text>
</svg></div>"""


def caso_real():
    # Caso público do Brasil, o mesmo que está no site (cazuri.itens.omega; fonte interna em conteudo/casos.json)
    linhas_prova = [("BEFORE", "People asked the price, did not book, and nobody got back to them."),
                    ("AFTER", "Every request that did not book got an automatic WhatsApp follow-up.")]
    return ('<div class="prova dois">' + "".join(
        f'<div><small>{a}</small><p>{E(b)}</p></div>' for a, b in linhas_prova) + "</div>"
        '<div class="heroi"><div><b>R$40k</b><p>in 3.5 months, only from people who had not booked</p></div>'
        '<div><b>+10%</b><p>monthly revenue from the automatic follow-up</p></div></div>'
        + fonte("Real case · imaging clinic, Brazil."))


SLIDES = [
    {"tema": "esc", "eyebrow": "PROOF · A REAL SYSTEM BREAKDOWN", "marca": "PACHECO STUDIOS",
     "h1": "A business did not need<br>[[another AI tool.]]", "h1px": 88,
     "sub": "It needed **one next action** after every enquiry.",
     "html": curva_capa(),
     "pill": "SWIPE TO SEE THE SYSTEM BREAKDOWN →",
     "rodape": "Every system we build starts with the path, not the tool."},
    {"tema": "lar", "eyebrow": "THE SYMPTOM", "marca": "PACHECO STUDIOS",
     "kicker": "WHAT THE TEAM FELT", "h1": "The problem looked like<br>“slow replies”.", "h1px": 92,
     "sub": "The operational problem went **deeper.**",
     "cartoes_esc": [("Channels", "Requests entering everywhere"), ("Context", "Repeated or lost"),
                     ("Owner", "Nobody clearly responsible"), ("Follow-up", "Left to the team’s memory")],
     "rodape": "Slow replies were the symptom, not the cause."},
    {"tema": "esc", "eyebrow": "THE DATA", "marca": "PACHECO STUDIOS",
     "kicker": "HOW COMMON IS IT", "h1": "Most businesses reply late.<br>[[Or never.]]", "h1px": 80,
     "html": dados_resposta(),
     "rodape": "The symptom is common. The cause is rarely the tool."},
    {"tema": "esc", "eyebrow": "THE PATH BEFORE", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "01 / BEFORE", "h1": "Four doors in.<br>[[No one at the desk.]]", "h1px": 84,
     "sub": "Google, Instagram, WhatsApp and email all landed in one place, and **nobody owned what came next.**",
     "html": diag_antes(),
     "rodape": "This is where most enquiries actually go quiet."},
    {"tema": "lar", "eyebrow": "THE COST OF WAITING", "marca": "PACHECO STUDIOS",
     "kicker": "THE DATA", "h1": "The first hour<br>[[decides the lead.]]", "h1px": 92,
     "html": dados_hora(),
     "rodape": "Speed is not effort. It is ownership."},
    {"tema": "esc", "eyebrow": "THE AUDIT QUESTION", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "02 / QUESTION", "h1": "Who owns the<br>[[next action?]]", "h1px": 92,
     "sub": "Not just “which tool?”. The audit asks:",
     "html": linhas("q", "ASK", ["Who receives the request?", "Who qualifies it?", "Who confirms it?",
                                 "When does it hand off to a person?", "What happens if nobody replies?"]),
     "rodape": "Ownership must be explicit, not assumed."},
    {"tema": "lar", "eyebrow": "THE RULE", "marca": "PACHECO STUDIOS",
     "kicker": "03 / RULE", "h1": "One rule before<br>[[any automation.]]", "h1px": 92,
     "sub": "Written for the business’s real path, **not a universal automation.**",
     "html": regra(),
     "rodape": "The rule is written before anything is automated."},
    {"tema": "esc", "eyebrow": "WHAT AI DOES", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "04 / AI LAYER", "h1": "AI handles the<br>[[repeatable layer.]]", "h1px": 92,
     "sub": "Inside the approved rules, it can:",
     "html": linhas("ia apertado", "AI", ["Gather the context", "Classify the request", "Answer approved FAQs",
                                         "Spot missing information", "Prepare the next step"]) + faixa_klarna(),
     "rodape": "AI does the repeatable work. People keep the judgement."},
    {"tema": "esc", "eyebrow": "WHAT STAYS HUMAN", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "05 / HUMAN LAYER", "h1": "The human still owns<br>[[the exception.]]", "h1px": 88,
     "sub": "The team takes over when there is:",
     "html": linhas("hum apertado", "TEAM", ["A request outside the rules", "A complaint or a risk",
                                             "A commercial decision", "An urgent situation", "Not enough context"])
             + faixa_gartner(),
     "rodape": "A good system knows when to stop."},
    {"tema": "esc", "eyebrow": "THE PATH AFTER", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "06 / AFTER", "h1": "Same doors.<br>[[One clear path.]]", "h1px": 88,
     "html": diag_depois(),
     "rodape": "Trigger → owner → rule → next action → human."},
    {"tema": "lar", "eyebrow": "THE SAME BREAK, FIXED", "marca": "REAL CASE · BRAZIL",
     "kicker": "07 / EVIDENCE", "h1": "One next action.<br>[[Real revenue back.]]", "h1px": 84,
     "html": caso_real(),
     "rodape": "Real numbers or none at all."},
    {"tema": "lar", "eyebrow": "PACHECO STUDIOS / AI SYSTEMS AUDITS", "marca": "TALK WITH US",
     "h1": "Your operation may not need<br>[[more software.]]", "h1px": 84,
     "sub": "It may need a clear owner, rule and next action.",
     "botao": "DM “AUDIT” TO MAP THE FIRST BREAK",
     "rodape": "Tell us which process is breaking."},
]


def slide(s, i, total):
    tema = s["tema"]
    partes = []
    if s.get("kicker"):
        partes.append(f'<div class="kicker">{E(s["kicker"])}</div>')
    partes.append(f'<h1 style="font-size:{s["h1px"]}px">{rich(s["h1"]).replace("&lt;br&gt;", "<br>")}</h1>')
    if s.get("sub"):
        partes.append(f'<p class="sub">{rich(s["sub"])}</p>')
    if s.get("html"):
        partes.append(s["html"])
    if s.get("cartoes_esc"):
        partes.append('<div class="c4">' + "".join(
            f'<div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in s["cartoes_esc"]) + "</div>")
    if s.get("pill"):
        partes.append(f'<div class="pill">{E(s["pill"])}</div>')
    if s.get("botao"):
        partes.append(f'<div class="botao">{E(s["botao"])}</div>')
    trilho = ('<div class="trilho">' + "".join(f'<i style="left:{x}px"></i>' for x in (0, 145, 290, 435))
              + '<em style="left:580px"></em></div>') if s.get("trilho") else ""
    return f"""<section class="slide {tema}">
<div class="top"><div class="eyebrow">{E(s["eyebrow"])}</div><div class="marca">{E(s["marca"])}</div><div class="regua"></div></div>
<div class="miolo{' topo' if s.get('topo') else ''}">{''.join(partes)}</div>{trilho}
<div class="pag"><span>{i:02d}</span> / {total}</div>
<div class="rod">{E(s["rodape"])}</div>
</section>"""


def main():
    os.makedirs(os.path.join(AQUI, "saida", "en"), exist_ok=True)
    corpo = "\n".join(slide(s, i, len(SLIDES)) for i, s in enumerate(SLIDES, 1))
    caminho = os.path.join(AQUI, "saida", "carrossel-proof-en.html")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Proof · A real system breakdown</title>'
                f'<style>{base.CSS}{CSS_EXTRA}</style></head><body>{corpo}</body></html>')
    print(caminho)


if __name__ == "__main__":
    main()
