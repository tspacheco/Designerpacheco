#!/usr/bin/env python3
"""Central das prospeções WhatsApp: gera central-prospecoes.pdf (via Chromium).
Acrescentar um dia = nova entrada em DIAS (lista `divisoes`) e voltar a correr.
Uso: python3 gerar.py"""
import html, subprocess, pathlib
R = "https://github.com/tspacheco/Designerpacheco/raw/"
B = "https://github.com/tspacheco/Designerpacheco/tree/"
def raw(ramo, p): return f"{R}claude/{ramo}/{p}"

CAC, PAR, EMP = "cacador-diario-nkiz36", "parceiros-indicam-4kcnrc", "empresas-novas-43xm0c"
AVA, RX, IG = "avaliacoes-queixas-m7qdst", "auditoria-sites-fracos-fpyd0h", "prospecao-instagram-eu958u"

# (divisão, ramo, quantidade/estado, [(texto, ramo, caminho)])
DIAS = [
 ("12/10/2026 (segunda, hoje)", [
  ("Demos · Audit Hook by Demo (Iași)", CAC,
   "50 negócios: 25 com demo no ramo (à espera de «publica») + 25 só na lista. WhatsApp: 47 «?», 3 «não (fixo)».",
   [("Lista com mensagens (WhatsApp)", CAC, "research/cacador/2026-10-12.md"),
    ("Tabela (tsv)", CAC, "research/cacador/2026-10-12.tsv"),
    ("Briefs das demos", CAC, "research/cacador/briefs-2026-10-12.md")]),
  ("Parceiros que indicam (Iași e Faro)", PAR,
   "10 novos (8 Iași, 2 Faro), só pesquisa; total 57 na lista (43 «?», 14 fixos). Nada se envia sem o «envia».",
   [("Lista completa de parceiros (tsv)", PAR, "research/parceiros/parceiros.tsv"),
    ("Mensagens de parceiros", PAR, "research/parceiros/PARCEIROS.md"),
    ("Comissão", PAR, "research/parceiros/COMISSAO.md")]),
  ("Marcas (Instagram, triagem para DM)", EMP,
   "2 triagens em PT, PDF + PNG: Cristina Tomás (fisioterapeuta) e Bruno Pereira (judo, Lanheses).",
   [("Como enviar", EMP, "research/triagens-instagram/ENVIAR.md"),
    ("Cristina Tomás · PDF", EMP, "research/triagens-instagram/cristina-tomas-fisio.pdf"),
    ("Cristina Tomás · PNG (DM)", EMP, "research/triagens-instagram/cristina-tomas-fisio.png"),
    ("Bruno Pereira · PDF", EMP, "research/triagens-instagram/bruno-pereira-judo-lanheses.pdf"),
    ("Bruno Pereira · PNG (DM)", EMP, "research/triagens-instagram/bruno-pereira-judo-lanheses.png")]),
  ("Empresas acabadas de abrir (ANAF, Iași)", EMP,
   "3 empresas novas; WhatsApp «?» em todas (telefone da ANAF pode ser do contabilista).",
   [("Lista de 12/10", EMP, "agentes/empresas-novas/listas/2026-10-12.md")]),
  ("Avaliações Google com queixas (Iași)", AVA,
   "7 negócios com queixas de telefone, mensagens ou marcações (935 avaliações lidas em 86 fichas), RO + PT.",
   [("Lista de 12/10 com mensagens", AVA, "agentes/avaliacoes-queixas/listas/2026-10-12.md")]),
 ]),
 ("11/10/2026 (domingo)", [
  ("Demos · Audit Hook by Demo (Iași)", CAC,
   "52 negócios: 25 demos publicadas + 25 só na lista + 2 fechados temporariamente. WhatsApp: 50 «?», 1 «sim (montra)», 1 «não (fixo)».",
   [("Lista com mensagens (WhatsApp)", CAC, "research/cacador/2026-10-11.md"),
    ("Tabela (tsv)", CAC, "research/cacador/2026-10-11.tsv"),
    ("Briefs das demos", CAC, "research/cacador/briefs-2026-10-11.md")]),
  ("Parceiros que indicam", PAR,
   "Sem contactos novos: kit de parceria (incentivo + proposta, RO/EN/PT) e triagem do Iulian Paraschiv (por «tu»).",
   [("Incentivo PT", PAR, "research/parceiros/kit/incentivo-pt.pdf"),
    ("Incentivo RO", PAR, "research/parceiros/kit/incentivo-ro.pdf"),
    ("Incentivo EN", PAR, "research/parceiros/kit/incentivo-en.pdf"),
    ("Proposta de parceria PT", PAR, "research/parceiros/kit/proposta-parceria-pt.pdf"),
    ("Proposta de parceria RO", PAR, "research/parceiros/kit/proposta-parceria-ro.pdf"),
    ("Proposta de parceria EN", PAR, "research/parceiros/kit/proposta-parceria-en.pdf"),
    ("Triagem Iulian Paraschiv PT", PAR, "research/parceiros/triagens/iulian-paraschiv/triagem-pt.pdf"),
    ("Triagem Iulian Paraschiv RO", PAR, "research/parceiros/triagens/iulian-paraschiv/triagem-ro.pdf")]),
  ("Raio-X do primeiro contacto (PDF grátis)", RX,
   "10 negócios de Iași com mensagem + PDF RO (dono) e PT (Tomás). Fixos: ligar.",
   [("Lista para enviar (ENVIAR.md)", RX, "raio-x/ENVIAR.md")]),
  ("Empresas acabadas de abrir (ANAF)", EMP,
   "Sem lista: a rotina corre seg–sex e 11/10 foi domingo.", []),
 ]),
]
OUTROS = [
 ("Instagram · DMs (lote 1, 11/10)", "19 DMs com seguimentos a 15/10, 18/10 e 23/10; o Tomás confirma os @. Não é WhatsApp.",
  [("Lote 1", IG, "research/instagram/envios/2026-10-11-lote-1.md")]),
 ("E-mails pelo n8n", "12/10: 159 saíram, 91 por enviar (listas de 250 e 200 em /mnt/project-files/prospecao/, ficheiros fora do GitHub). Não é WhatsApp.", []),
]
REGRAS = ["Triagem como isca; nunca preço nem minutos numa mensagem («uma reunião»).",
 "WhatsApp: 1 minuto entre mensagens, saudação a variar; marca «sim / ? / não» em cada contacto (sem prova pública = «?»: visita ou chamada).",
 "Repositório público: nada de dados privados de clientes. Fecho em RO: «Voi fi pregătit.»"]

def a(t, ramo, p): return f'<a href="{html.escape(raw(ramo,p))}">{html.escape(t)}</a>'
h = ['<!doctype html><html lang="pt-PT"><meta charset="utf-8"><title>Central das prospeções WhatsApp</title><style>'
 '@page{size:A4;margin:16mm}body{font:11pt/1.45 system-ui,Helvetica,Arial,sans-serif;color:#1b1f24}'
 'h1{font-size:22pt;margin:0 0 2mm}h2{font-size:15pt;border-bottom:2px solid #1b1f24;padding-bottom:1mm;margin:8mm 0 3mm}'
 'h3{font-size:12pt;margin:5mm 0 1mm}.sub{color:#555;margin:0 0 4mm}.n{margin:0 0 1.5mm}ul{margin:0 0 2mm 5mm;padding:0}'
 'li{margin:0.5mm 0}a{color:#0b57d0;word-break:break-all}.r{font-size:10pt;color:#444}.b{font-size:9pt;color:#777}'
 '.d{break-inside:avoid}</style><body>']
h.append('<h1>Central das prospeções WhatsApp</h1><p class="sub">Pacheco Studios · atualizado a 12/10/2026 · cada linha abre o ficheiro no GitHub (ramo do agente)</p>')
for dia, divs in DIAS:
    h.append(f'<h2>{html.escape(dia)}</h2>')
    for nome, ramo, resumo, links in divs:
        h.append(f'<div class="d"><h3>{html.escape(nome)}</h3><p class="n">{html.escape(resumo)}</p>')
        h.append(f'<p class="b">Ramo: <a href="{B}claude/{ramo}">claude/{ramo}</a></p>')
        if links: h.append('<ul>'+''.join(f'<li>{a(t,r,p)}</li>' for t,r,p in links)+'</ul>')
        h.append('</div>')
h.append('<h2>Outros canais (fora do WhatsApp, só para registo)</h2>')
for nome, resumo, links in OUTROS:
    h.append(f'<div class="d"><h3>{html.escape(nome)}</h3><p class="n">{html.escape(resumo)}</p>')
    if links: h.append('<ul>'+''.join(f'<li>{a(t,r,p)}</li>' for t,r,p in links)+'</ul>')
    h.append('</div>')
h.append('<h2>Regras que valem em todas as divisões</h2><ul class="r">'+''.join(f'<li>{html.escape(x)}</li>' for x in REGRAS)+'</ul>')
h.append('</body></html>')
d = pathlib.Path(__file__).parent
(d/'central-prospecoes.html').write_text(''.join(h), encoding='utf-8')
subprocess.run(['/opt/pw-browsers/chromium','--headless','--no-sandbox','--disable-gpu',
  f'--print-to-pdf={d/"central-prospecoes.pdf"}','--no-pdf-header-footer',(d/'central-prospecoes.html').as_uri()],check=True,stderr=subprocess.DEVNULL)
print('ok')
