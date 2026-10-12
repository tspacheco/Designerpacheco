"""2.º carrossel fixado do Instagram: «Proof · A real system breakdown» (EN, 10 slides, 1080x1350).

Plano do Tomás (PDF de 12/10/2026): Start Here → Proof → Method. Mesmo visual do 1.º
(escuro, creme e laranja, títulos centrados, diagramas de sistema, um só CTA «DM AUDIT»).
O slide 9 só leva prova real e autorizada: os campos entre parênteses retos ficam por preencher.
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


SLIDES = [
    {"tema": "esc", "eyebrow": "PROOF · A REAL SYSTEM BREAKDOWN", "marca": "PACHECO STUDIOS",
     "h1": "A business did not need<br>[[another AI tool.]]", "h1px": 88,
     "sub": "It needed **one next action** after every enquiry.",
     "pill": "SWIPE TO SEE THE SYSTEM BREAKDOWN →", "trilho": True,
     "rodape": "Every system we build starts with the path, not the tool."},
    {"tema": "lar", "eyebrow": "THE SYMPTOM", "marca": "PACHECO STUDIOS",
     "kicker": "WHAT THE TEAM FELT", "h1": "The problem looked like<br>“slow replies”.", "h1px": 92,
     "sub": "The operational problem went **deeper.**",
     "cartoes_esc": [("Channels", "Requests entering everywhere"), ("Context", "Repeated or lost"),
                     ("Owner", "Nobody clearly responsible"), ("Follow-up", "Left to the team’s memory")],
     "rodape": "Slow replies were the symptom, not the cause."},
    {"tema": "esc", "eyebrow": "THE PATH BEFORE", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "01 / BEFORE", "h1": "Four doors in.<br>[[No one at the desk.]]", "h1px": 84,
     "sub": "Google, Instagram, WhatsApp and email all landed in one place, and **nobody owned what came next.**",
     "html": diag_antes(),
     "rodape": "This is where most enquiries actually go quiet."},
    {"tema": "esc", "eyebrow": "THE AUDIT QUESTION", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "02 / QUESTION", "h1": "Who owns the<br>[[next action?]]", "h1px": 92,
     "sub": "Not just “which tool?”. We asked:",
     "html": linhas("q", "ASK", ["Who receives the request?", "Who qualifies it?", "Who confirms it?",
                                 "When does it hand off to a person?", "What happens if nobody replies?"]),
     "rodape": "Ownership must be explicit, not assumed."},
    {"tema": "lar", "eyebrow": "THE RULE WE DESIGNED", "marca": "PACHECO STUDIOS",
     "kicker": "03 / RULE", "h1": "One rule before<br>[[any automation.]]", "h1px": 92,
     "sub": "Written for this business and its real path, **not a universal automation.**",
     "html": regra(),
     "rodape": "The rule is written before anything is automated."},
    {"tema": "esc", "eyebrow": "WHAT AI DOES", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "04 / AI LAYER", "h1": "AI handles the<br>[[repeatable layer.]]", "h1px": 92,
     "sub": "Inside the approved rules, it can:",
     "html": linhas("ia", "AI", ["Gather the context", "Classify the request", "Answer approved FAQs",
                                "Spot missing information", "Prepare the next step"]),
     "rodape": "AI does the repeatable work. People keep the judgement."},
    {"tema": "esc", "eyebrow": "WHAT STAYS HUMAN", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "05 / HUMAN LAYER", "h1": "The human still owns<br>[[the exception.]]", "h1px": 88,
     "sub": "The team takes over when there is:",
     "html": linhas("hum", "TEAM", ["A request outside the rules", "A complaint or a risk", "A commercial decision",
                                    "An urgent situation", "Not enough context"]),
     "rodape": "A good system knows when to stop."},
    {"tema": "esc", "eyebrow": "THE PATH AFTER", "marca": "PACHECO STUDIOS", "topo": True,
     "kicker": "06 / AFTER", "h1": "Same doors.<br>[[One clear path.]]", "h1px": 88,
     "html": diag_depois(),
     "rodape": "Trigger → owner → rule → next action → human."},
    {"tema": "lar", "eyebrow": "THE RESULT", "marca": "PACHECO STUDIOS",
     "kicker": "07 / EVIDENCE", "h1": "What changed.", "h1px": 100,
     "sub": "Shown only with **verified evidence.** No estimates.",
     "html": prova(),
     "rodape": "We publish verified results, or none at all."},
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
