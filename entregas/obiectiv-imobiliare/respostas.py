#!/usr/bin/env python3
"""Respostas às 7 perguntas do Gabriel Ciobotariu (Obiectiv Imobiliare), em inglês, 2 páginas A4 deitado.

Uso: python3 respostas.py [--mensal "X–Y €"] [--ref "texto"]  →  obiectiv-answers-en.pdf
Sem --mensal, o intervalo fica marcado a laranja para o Tomás preencher.
"""
import os, sys, subprocess
from gerar import AQUI, FONTES, CSS, CHROME, esc, rod

args = sys.argv[1:]
def opt(nome):
    return args[args.index(nome) + 1] if nome in args else None

MENSAL = opt("--mensal")
REF = opt("--ref")

marca = "PACHECO STUDIOS · ANSWERS FOR OBIECTIV IMOBILIARE · OCTOBER 2026"
falta = lambda s: f'<mark>{esc(s)}</mark>'

ref_txt = (esc(REF) if REF else
           "In Romania we work with service businesses in Iași. If you want to speak with one of them, "
           "I will ask for their permission and connect you directly.")
mensal_txt = esc(MENSAL) if MENSAL else falta("[range to confirm: X–Y € per month]")

Q = [
    ("Do you have a real estate client or a client in Romania I could talk to?",
     "We do not have a real estate client yet. You would be the first, and that is exactly why the pilot is small, "
     "30 days and 1,000 €: you see results on your own numbers before any larger decision. " + ref_txt),
    ("What is the monthly subscription after implementation?",
     f"It covers monitoring, adjustments and support of what we build. {mensal_txt}, fixed in writing in the "
     "implementation plan at the end of the pilot, depending on how many flows and channels are in the system. "
     "It starts only after the first month of implementation, during which we accompany the solution."),
    ("What exactly will you build? A new platform, or will it connect to what we already use?",
     "No new platform. We connect what you already use: ImmoFlux CRM, your website, the app and Alesia. "
     "The shared board and the rules (who answers, when, what happens next) live as close to ImmoFlux as its "
     "integrations allow. In week 1 we check exactly what ImmoFlux lets us connect; if something cannot be "
     "connected, you will know before we build."),
    ("Who owns the system and the data if we stop working together?",
     "You do. Everything is built inside your own accounts, with your data. If we stop working together, "
     "it keeps running without us, with written documentation and a handover session for your team."),
    ("575 properties on one page and 538 listings on another. Which numbers did you use?",
     "Both come from your website on 22 October: 575 properties is the figure on your About page, "
     "538 is the total listings counter on the homepage. In the pilot we use the real count from your CRM, "
     "not the website."),
    ("“At least doubling houses sold” in a shrinking market: what is this based on, and how will you measure it?",
     "It is the objective of the full implementation, not of the pilot. It is based on where sales are lost "
     "between the first message and the signature: response time, follow-up after viewings, owners who leave. "
     "We measure it against your own baseline from the CRM: closed transactions in the same period of the "
     "previous 12 months. If the diagnosis shows that doubling is not realistic for your market, we tell you "
     "in writing and set the target from your data."),
    ("What happens if the pilot results are not what you expected? Is there a refund or guarantee?",
     "There is no refund. What you keep regardless: the complete diagnosis with all bottlenecks and priorities, "
     "the organization system already running, the results report, and a training session for your team on AI "
     "and on how to maintain what was built. You decide about implementation only after seeing the results."),
]

CSS4 = CSS + """
mark{background:var(--l);color:var(--c);padding:0 1.2mm;font-weight:600}
.qa{display:grid;grid-template-columns:repeat(2,1fr);gap:7mm 12mm;margin-top:7mm}
.qa>div{border-top:2px solid var(--c);padding-top:3mm}
.qa .n{font-family:"Space Mono",monospace;font-size:8pt;color:var(--l);letter-spacing:.1em}
.qa h3{font-family:"Archivo Black",sans-serif;font-weight:400;font-size:12.5pt;line-height:1.2;margin:1.5mm 0 2mm}
.qa p{font-size:10.6pt;line-height:1.45;color:var(--t2)}
"""


def bloco(i, q, a):
    return f'<div><div class="n">{i:02d}</div><h3>{esc(q)}</h3><p>{a}</p></div>'


def pagina(n, itens, titulo, extra=""):
    qa = ''.join(bloco(i, q, a) for i, q, a in itens)
    return f'''<section class="p">
<div class="k"><i></i>Answers · Obiectiv Imobiliare</div><h2>{esc(titulo)}</h2>
<div class="qa">{qa}</div>
{extra}
<div class="rod"><span>{marca}</span><span>{n:02d}</span></div></section>'''


# os textos fixos não têm & < >; as partes variáveis (ref, mensal) já vêm escapadas
itens = [(i + 1, q, a) for i, (q, a) in enumerate(Q)]

fecho = '''<div class="conc" style="margin-top:auto">Happy to go through any of these on a call. The goal of the pilot is simple: for you to see, on your own numbers, whether Pacheco Studios is the partner you want to work with.<br><span style="font-family:Space Mono,monospace;font-size:8.5pt;color:var(--o2)">Tomás Pacheco · Pacheco Studios · WhatsApp +40 723 098 556 · ro.pachecost.com</span></div>'''

html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Answers for Obiectiv Imobiliare</title>'
        f'<style>{FONTES}{CSS4}</style></head><body>'
        + pagina(1, itens[:4], "Hi Gabriel, clear answers to your seven questions.")
        + pagina(2, itens[4:], "The numbers, the goal and what you keep.", fecho)
        + '</body></html>')
h = os.path.join(AQUI, "obiectiv-answers-en.html")
open(h, "w").write(html)
pdf = os.path.join(AQUI, "obiectiv-answers-en.pdf")
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                f"--print-to-pdf={pdf}", "file://" + h], check=True, capture_output=True)
print(os.path.getsize(pdf) // 1024, "KB", "· mensal:", MENSAL or "POR PREENCHER")
