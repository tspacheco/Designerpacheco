#!/usr/bin/env python3
"""PDF visual «O que vem depois do diagnóstico» (RO, EN, PT). Sem números: objetivo, abordagens e gráficos.

Uso: python3 gerar.py  →  pos-diagnostico-ro.pdf, -en.pdf, -pt.pdf (A4 deitado) e os .html correspondentes.
"""
import os, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = open(os.path.join(AQUI, "fonts.css")).read()
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

T = {
 "ro": dict(
  marca="Pacheco Studios · Consultanță de sisteme cu IA",
  capa_k="După diagnostic", capa_t="Ce urmează pentru afacerea ta", capa_s="De la problemele găsite la sisteme care lucrează pentru tine.",
  rota=["Diagnostic", "Hartă", "Decizie", "Design", "Pilot", "Control"],
  obj_k="Obiectivul", obj_t="Afacerea ta, cu mai puțină fricțiune", obj_antes="Azi", obj_depois="După",
  obj_metas=["Timp eliberat pentru echipă", "Niciun client pierdut pe drum", "Decizii pe date clare"],
  mapa_k="Harta afacerii", mapa_t="Vedem unde se pierde timpul și unde apar erorile",
  motores=[("Atragere", ["Mesaj primit", "Răspuns", "Ofertă", "Programare"]),
           ("Livrare", ["Pregătire", "Execuție", "Factură", "Plată"]),
           ("Revenire", ["Follow-up", "Recenzie", "Ofertă nouă", "Client fidel"])],
  leg_t="pierde timp", leg_e="produce erori",
  mat_k="Decizia", mat_t="Alegem ce merită făcut primul",
  mat_y="Impact", mat_x="Efort",
  quad=["Câștiguri rapide", "Pariuri mari", "Extra", "De evitat"],
  pontos=["Răspuns rapid", "Reamintiri", "Ofertă rapidă", "Raport săptămânal", "Integrare completă", "Aplicație proprie"],
  qw_k="Câștigurile rapide", qw_t="Primele trei sisteme, înainte de orice proiect mare",
  qw=[("Niciun mesaj fără răspuns", ["Mesaj nou", "Răspuns în regulile tale", "Caz dificil → om"]),
      ("Programări care nu se pierd", ["Programare", "Reamintire", "Confirmare"]),
      ("Clienți care revin", ["Serviciu terminat", "Mulțumire", "Invitație la revenire"])],
  sp_k="System Print", sp_t="Fiecare sistem, desenat înainte de a fi construit",
  sp=[("Simptom", "ce doare azi"), ("Declanșator", "când pornește"), ("Flux", "pașii, în ordine"),
      ("Regulă", "ce are voie să facă"), ("Responsabil", "cine răspunde"), ("Predare la om", "excepțiile"), ("Măsură", "cum măsurăm")],
  plano_k="Planul", plano_t="Pas cu pas, fără să oprim ce funcționează",
  fases=[("Acum", "Câștiguri rapide", "Sisteme mici, rezultat vizibil"), ("Apoi", "Pilot", "Testăm cu clienți reali"), ("Mai departe", "Extindere", "Ce funcționează, în toată afacerea")],
  graf_a="Muncă manuală", graf_b="Valoare pentru client", graf_x="Timp",
  ctrl_k="Cum lucrăm", ctrl_t="Tu păstrezi controlul",
  ciclo=["Implementăm", "Măsurăm", "Ajustăm"],
  promessas=["Conturile și datele rămân ale tale", "IA doar în regulile aprobate de tine", "Fiecare excepție ajunge la un om", "Măsurăm de la punctul de plecare"],
  cta="Hai să vorbim", site="ro.pachecost.com", tel="WhatsApp +40 723 098 556"),
 "en": dict(
  marca="Pacheco Studios · AI systems consulting",
  capa_k="After the audit", capa_t="What comes next for your business", capa_s="From the problems we found to systems that work for you.",
  rota=["Audit", "Map", "Decide", "Design", "Pilot", "Govern"],
  obj_k="The goal", obj_t="Your business, with less friction", obj_antes="Today", obj_depois="After",
  obj_metas=["Time freed up for your team", "No customer lost along the way", "Decisions on clear data"],
  mapa_k="The business map", mapa_t="We see where time leaks and where errors happen",
  motores=[("Win", ["Message in", "Reply", "Quote", "Booking"]),
           ("Deliver", ["Prepare", "Do the work", "Invoice", "Payment"]),
           ("Keep", ["Follow-up", "Review", "New offer", "Loyal customer"])],
  leg_t="loses time", leg_e="causes errors",
  mat_k="The decision", mat_t="We pick what is worth doing first",
  mat_y="Impact", mat_x="Effort",
  quad=["Quick wins", "Big bets", "Nice to have", "Avoid"],
  pontos=["Fast reply", "Reminders", "Fast quote", "Weekly report", "Full integration", "Custom app"],
  qw_k="Quick wins", qw_t="The first three systems, before any big project",
  qw=[("No message left unanswered", ["New message", "Reply within your rules", "Hard case → a person"]),
      ("Bookings that don't slip", ["Booking", "Reminder", "Confirmation"]),
      ("Customers who come back", ["Job done", "Thank you", "Invite back"])],
  sp_k="System Print", sp_t="Every system is drawn before it is built",
  sp=[("Symptom", "what hurts today"), ("Trigger", "when it starts"), ("Flow", "the steps, in order"),
      ("Rule", "what it may do"), ("Owner", "who is accountable"), ("Handoff", "exceptions go to people"), ("Measure", "how we track it")],
  plano_k="The plan", plano_t="Step by step, without stopping what already works",
  fases=[("Now", "Quick wins", "Small systems, visible results"), ("Next", "Pilot", "Tested with real customers"), ("Then", "Scale", "What works, across the business")],
  graf_a="Manual work", graf_b="Value for the customer", graf_x="Time",
  ctrl_k="How we work", ctrl_t="You stay in control",
  ciclo=["Build", "Measure", "Adjust"],
  promessas=["Your accounts and data stay yours", "AI only inside rules you approve", "Every exception goes to a person", "We measure from the starting point"],
  cta="Let's talk", site="pachecost.com", tel="WhatsApp +351 967 117 357"),
 "pt": dict(
  marca="Pacheco Studios · Consultoria de sistemas com IA",
  capa_k="Depois do diagnóstico", capa_t="O que vem a seguir para o teu negócio", capa_s="Dos problemas encontrados a sistemas que trabalham por ti.",
  rota=["Diagnóstico", "Mapa", "Decisão", "Desenho", "Piloto", "Controlo"],
  obj_k="O objetivo", obj_t="O teu negócio, com menos fricção", obj_antes="Hoje", obj_depois="Depois",
  obj_metas=["Tempo libertado para a equipa", "Nenhum cliente perdido pelo caminho", "Decisões com dados claros"],
  mapa_k="O mapa do negócio", mapa_t="Vemos onde se perde tempo e onde nascem os erros",
  motores=[("Atrair", ["Mensagem", "Resposta", "Orçamento", "Marcação"]),
           ("Entregar", ["Preparar", "Executar", "Fatura", "Pagamento"]),
           ("Fidelizar", ["Follow-up", "Avaliação", "Nova oferta", "Cliente fiel"])],
  leg_t="perde tempo", leg_e="gera erros",
  mat_k="A decisão", mat_t="Escolhemos o que vale a pena fazer primeiro",
  mat_y="Impacto", mat_x="Esforço",
  quad=["Vitórias rápidas", "Grandes apostas", "Extras", "Evitar"],
  pontos=["Resposta rápida", "Lembretes", "Orçamento rápido", "Relatório semanal", "Integração total", "App própria"],
  qw_k="Vitórias rápidas", qw_t="Os três primeiros sistemas, antes de qualquer projeto grande",
  qw=[("Nenhuma mensagem sem resposta", ["Mensagem nova", "Resposta nas tuas regras", "Caso difícil → pessoa"]),
      ("Marcações que não se perdem", ["Marcação", "Lembrete", "Confirmação"]),
      ("Clientes que voltam", ["Serviço feito", "Agradecimento", "Convite a voltar"])],
  sp_k="System Print", sp_t="Cada sistema é desenhado antes de ser construído",
  sp=[("Sintoma", "o que dói hoje"), ("Gatilho", "quando começa"), ("Fluxo", "os passos, por ordem"),
      ("Regra", "o que pode fazer"), ("Dono", "quem responde"), ("Passagem", "exceções vão a pessoas"), ("Medida", "como medimos")],
  plano_k="O plano", plano_t="Passo a passo, sem parar o que já funciona",
  fases=[("Agora", "Vitórias rápidas", "Sistemas pequenos, resultado visível"), ("Depois", "Piloto", "Testado com clientes reais"), ("A seguir", "Expandir", "O que funciona, no negócio todo")],
  graf_a="Trabalho manual", graf_b="Valor para o cliente", graf_x="Tempo",
  ctrl_k="Como trabalhamos", ctrl_t="Tu ficas com o controlo",
  ciclo=["Implementar", "Medir", "Ajustar"],
  promessas=["As contas e os dados ficam teus", "IA só dentro das regras que aprovas", "Cada exceção vai a uma pessoa", "Medimos desde o ponto de partida"],
  cta="Vamos conversar", site="pachecost.com", tel="WhatsApp +351 967 117 357"),
}

CSS = """
@page{size:297mm 210mm;margin:0}
:root{--c:#141210;--c2:#1D1A17;--o:#EFEAE3;--o2:#A5A19B;--t2:#4D4A47;--l:#E8622C;--lt:#A64923;--f:#FAF8F4;--b:#CFC8BC;--am:#E3A33B;--vm:#C8432B}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;color:var(--c);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.p{width:297mm;height:210mm;position:relative;overflow:hidden;background:var(--f);padding:16mm 18mm 14mm;page-break-after:always;display:flex;flex-direction:column}
.p.esc{background:var(--c);color:var(--o)}
.k{font-family:"Space Mono",monospace;font-size:10pt;letter-spacing:.14em;text-transform:uppercase;color:var(--lt);display:flex;align-items:center;gap:3mm}
.esc .k{color:var(--l)}
.k i{display:inline-block;width:9mm;height:2px;background:currentColor}
h1,h2{font-family:"Archivo Black",sans-serif;font-weight:400;letter-spacing:-.01em;line-height:1.02}
h2{font-size:28pt;margin-top:4mm;max-width:220mm}
.rod{position:absolute;left:18mm;right:18mm;bottom:8mm;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:7.5pt;color:var(--o2);letter-spacing:.06em}
.esc .rod{color:#6f6a63}
.corpo{flex:1;display:flex;align-items:center;justify-content:center;margin-top:6mm}
svg text{font-family:Inter,sans-serif}
.mono{font-family:"Space Mono",monospace}
"""

def rod(t, n):
    return f'<div class="rod"><span>{t["marca"]}</span><span>{n:02d}</span></div>'

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def capa(t):
    r = t["rota"]; w = 250; xs = [24 + i * (w - 48) / (len(r) - 1) for i in range(len(r))]
    nos = ""
    for i, (x, nome) in enumerate(zip(xs, r)):
        if i == 0:
            nos += f'<circle cx="{x}" cy="30" r="7" fill="#E8622C"/><path d="M{x-3.2} 30l2.3 2.4 4.3-4.8" stroke="#141210" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
        else:
            nos += f'<circle cx="{x}" cy="30" r="5.5" fill="#141210" stroke="#EFEAE3" stroke-width="1.4"/>'
        cor = "#E8622C" if i == 0 else "#EFEAE3"
        nos += f'<text x="{x}" y="52" text-anchor="middle" font-size="5.4" fill="{cor}" class="mono" style="font-family:Space Mono;letter-spacing:.08em">{esc(nome.upper())}</text>'
    svg = (f'<svg viewBox="0 0 {w} 60" width="100%"><line x1="{xs[0]}" y1="30" x2="{xs[-1]}" y2="30" stroke="#EFEAE3" stroke-opacity=".35" stroke-width="1.2" stroke-dasharray="2 3"/>'
           f'<line x1="{xs[0]}" y1="30" x2="{xs[1]}" y2="30" stroke="#E8622C" stroke-width="1.6"/>{nos}</svg>')
    deco = ''.join(f'<circle cx="{40+ (i%9)*30}" cy="{30+(i//9)*30}" r="1.1" fill="#EFEAE3" fill-opacity=".12"/>' for i in range(54))
    return f'''<section class="p esc">
<svg style="position:absolute;right:-10mm;top:-6mm;width:150mm" viewBox="0 0 300 200">{deco}</svg>
<div class="k"><i></i>{esc(t["capa_k"])}</div>
<h1 style="font-size:52pt;margin-top:10mm;max-width:210mm">{esc(t["capa_t"])}</h1>
<p style="font-size:15pt;color:var(--o2);margin-top:7mm;max-width:170mm">{esc(t["capa_s"])}</p>
<div style="margin-top:auto;margin-bottom:10mm">{svg}</div>
{rod(t,1)}</section>'''

def objetivo(t):
    # emaranhado vs fluxo limpo
    caos = ('<path d="M20 60 C60 10 80 120 120 50 S170 20 150 90 S60 130 90 70 S170 40 200 100 S90 20 60 110 S150 140 210 60" '
            'fill="none" stroke="#4D4A47" stroke-width="2.2" stroke-linecap="round" opacity=".85"/>'
            '<path d="M30 100 C70 140 110 10 160 70 S200 130 120 120 S40 40 100 30" fill="none" stroke="#C8432B" stroke-width="2" stroke-linecap="round" opacity=".7"/>')
    limpo = ''.join(f'<line x1="20" y1="{y}" x2="210" y2="{y}" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>'
                    f'<circle cx="20" cy="{y}" r="5" fill="{c}"/><path d="M204 {y-6}l8 6-8 6" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
                    for y, c in [(40, "#E8622C"), (75, "#141210"), (110, "#141210")])
    def painel(titulo, conteudo, escuro=False):
        bg = "#141210" if escuro else "#FFFFFF"
        return (f'<div style="flex:1;background:{bg};border:1px solid var(--b);border-radius:4mm;padding:6mm 7mm">'
                f'<div class="k" style="color:{"#E8622C" if escuro else "#4D4A47"}"><i></i>{esc(titulo)}</div>'
                f'<svg viewBox="0 0 230 150" width="100%" style="margin-top:4mm">{conteudo}</svg></div>')
    limpo_esc = limpo.replace('#141210', '#EFEAE3')
    metas = ''.join(f'<div style="display:flex;align-items:center;gap:3mm;font-weight:600;font-size:12.5pt">'
                    f'<span style="width:7mm;height:7mm;border-radius:50%;background:var(--l);display:inline-flex;align-items:center;justify-content:center">'
                    f'<svg width="12" height="12" viewBox="0 0 12 12"><path d="M2.5 6.2l2.4 2.4 4.6-5" stroke="#141210" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg></span>{esc(m)}</div>'
                    for m in t["obj_metas"])
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["obj_k"])}</div><h2>{esc(t["obj_t"])}</h2>
<div class="corpo" style="gap:8mm;align-items:stretch">
{painel(t["obj_antes"], caos)}
<div style="display:flex;align-items:center"><svg width="16mm" viewBox="0 0 40 20"><path d="M2 10h32M27 3l8 7-8 7" stroke="#E8622C" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
{painel(t["obj_depois"], limpo_esc, True)}
</div>
<div style="display:flex;justify-content:space-between;gap:6mm;margin-top:7mm;margin-bottom:6mm">{metas}</div>
{rod(t,2)}</section>'''

def mapa(t):
    # marcações: (motor, passo) -> 't' tempo / 'e' erro
    marcas = {(0, 1): "t", (0, 2): "e", (1, 2): "t", (1, 3): "e", (2, 0): "t", (2, 2): "t"}
    W, colw = 270, 82
    s = ""
    for m, (nome, passos) in enumerate(t["motores"]):
        x0 = 6 + m * (colw + 10)
        s += f'<rect x="{x0}" y="4" width="{colw}" height="22" rx="4" fill="#141210"/><text x="{x0+colw/2}" y="18.5" text-anchor="middle" fill="#EFEAE3" font-size="8.5" font-weight="700" style="font-family:Archivo Black">{esc(nome.upper())}</text>'
        for i, p in enumerate(passos):
            y = 36 + i * 27
            k = marcas.get((m, i))
            borda = {"t": "#E3A33B", "e": "#C8432B"}.get(k, "#CFC8BC")
            fundo = {"t": "#FBEFD9", "e": "#F6DDD6"}.get(k, "#FFFFFF")
            s += f'<rect x="{x0+6}" y="{y}" width="{colw-12}" height="19" rx="3" fill="{fundo}" stroke="{borda}" stroke-width="{1.6 if k else .8}"/>'
            s += f'<text x="{x0+colw/2}" y="{y+12.4}" text-anchor="middle" font-size="6.6" font-weight="600" fill="#141210">{esc(p)}</text>'
            if k:
                s += f'<circle cx="{x0+colw-8}" cy="{y}" r="4" fill="{borda}"/>'
                s += (f'<path d="M{x0+colw-8} {y-2}v2.2l1.4 1" stroke="#fff" stroke-width=".9" fill="none" stroke-linecap="round"/>' if k == "t"
                      else f'<path d="M{x0+colw-8} {y-2.2}v2.4M{x0+colw-8} {y+1.6}v.1" stroke="#fff" stroke-width="1.1" stroke-linecap="round"/>')
            if i < len(passos) - 1:
                s += f'<path d="M{x0+colw/2} {y+19}v8" stroke="#A5A19B" stroke-width=".9"/>'
        if m < 2:
            s += f'<path d="M{x0+colw+1} 15h8M{x0+colw+6} 12l3 3-3 3" stroke="#E8622C" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
    leg = (f'<div style="display:flex;gap:9mm;font-size:10.5pt;color:var(--t2);margin-top:3mm;margin-bottom:6mm">'
           f'<span style="display:flex;align-items:center;gap:2mm"><span style="width:4mm;height:4mm;border-radius:50%;background:var(--am)"></span>{esc(t["leg_t"])}</span>'
           f'<span style="display:flex;align-items:center;gap:2mm"><span style="width:4mm;height:4mm;border-radius:50%;background:var(--vm)"></span>{esc(t["leg_e"])}</span></div>')
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["mapa_k"])}</div><h2>{esc(t["mapa_t"])}</h2>
<div class="corpo"><svg viewBox="0 0 {W} 150" style="width:100%;max-height:118mm">{s}</svg></div>{leg}
{rod(t,3)}</section>'''

def matriz(t):
    q = t["quad"]; p = [t["pontos"][0], t["pontos"][1], t["pontos"][2], t["pontos"][3], t["pontos"][4], t["pontos"][5]]
    s = ('<rect x="40" y="10" width="110" height="80" fill="#FCE3D7"/><rect x="150" y="10" width="110" height="80" fill="#FFFFFF"/>'
         '<rect x="40" y="90" width="110" height="80" fill="#FFFFFF"/><rect x="150" y="90" width="110" height="80" fill="#EFEAE3"/>'
         '<rect x="40" y="10" width="220" height="160" fill="none" stroke="#CFC8BC"/><line x1="150" y1="10" x2="150" y2="170" stroke="#CFC8BC"/><line x1="40" y1="90" x2="260" y2="90" stroke="#CFC8BC"/>')
    pos = [(48, 24), (158, 24), (48, 104), (158, 104)]
    cores = ["#A64923", "#141210", "#4D4A47", "#A5A19B"]
    for (x, y), nome, c in zip(pos, q, cores):
        s += f'<text x="{x}" y="{y}" font-size="8" fill="{c}" style="font-family:Archivo Black">{esc(nome.upper())}</text>'
    pts = [(56, 42, 1), (56, 60, 1), (56, 78, 1), (60, 128, 0), (168, 45, 0), (168, 138, 0)]
    for (x, y, dest), nome in zip(pts, p):
        r = 6 if dest else 4.5
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{"#E8622C" if dest else "#141210"}" stroke="#fff" stroke-width="1.5"/>'
        s += f'<text x="{x+9}" y="{y+2.4}" font-size="6.6" font-weight="600" fill="#141210">{esc(nome)}</text>'
    s += ('<path d="M30 170V14M27 18l3-5 3 5" stroke="#141210" stroke-width="1.2" fill="none"/>'
          '<path d="M40 180H256M252 177l5 3-5 3" stroke="#141210" stroke-width="1.2" fill="none"/>'
          f'<text x="22" y="90" font-size="7.5" fill="#141210" transform="rotate(-90 22 90)" text-anchor="middle" style="font-family:Space Mono;letter-spacing:.12em">{esc(t["mat_y"].upper())}</text>'
          f'<text x="150" y="192" font-size="7.5" fill="#141210" text-anchor="middle" style="font-family:Space Mono;letter-spacing:.12em">{esc(t["mat_x"].upper())}</text>')
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["mat_k"])}</div><h2>{esc(t["mat_t"])}</h2>
<div class="corpo" style="margin-bottom:6mm"><svg viewBox="0 0 280 198" style="height:128mm">{s}</svg></div>
{rod(t,4)}</section>'''

def quick(t):
    cards = ""
    for i, (titulo, passos) in enumerate(t["qw"]):
        s = ""
        for j, p in enumerate(passos):
            y = 6 + j * 46
            ultimo = j == len(passos) - 1
            c = "#E8622C" if j == 0 else ("#EFEAE3" if not ultimo else "#141210")
            tc = "#141210" if c != "#141210" else "#EFEAE3"
            s += f'<rect x="8" y="{y}" width="164" height="32" rx="16" fill="{c}" stroke="#141210" stroke-width="{0 if c!="#EFEAE3" else .8}"/>'
            s += f'<text x="90" y="{y+20}" text-anchor="middle" font-size="9.6" font-weight="600" fill="{tc}">{esc(p)}</text>'
            if not ultimo:
                s += f'<path d="M90 {y+33}v12M86.5 {y+41.5}l3.5 3.5 3.5-3.5" stroke="#141210" stroke-width="1.2" fill="none"/>'
        icone = ['<path d="M8 10h22v14H16l-6 5v-5H8z" fill="none" stroke="#E8622C" stroke-width="2.2" stroke-linejoin="round"/>',
                 '<rect x="7" y="9" width="24" height="21" rx="3" fill="none" stroke="#E8622C" stroke-width="2.2"/><path d="M7 15h24M13 6v6M25 6v6" stroke="#E8622C" stroke-width="2.2" stroke-linecap="round"/>',
                 '<path d="M30 16a11 11 0 1 0-2 9M30 8v8h-8" fill="none" stroke="#E8622C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'][i]
        cards += (f'<div style="flex:1;background:#fff;border:1px solid var(--b);border-radius:4mm;padding:6mm;display:flex;flex-direction:column;gap:4mm">'
                  f'<svg width="12mm" height="12mm" viewBox="0 0 38 36">{icone}</svg>'
                  f'<div style="font-family:Archivo Black;font-size:17pt;line-height:1.1;min-height:20mm">{esc(titulo)}</div>'
                  f'<svg viewBox="0 0 180 136" width="100%" style="margin:auto 0">{s}</svg></div>')
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["qw_k"])}</div><h2>{esc(t["qw_t"])}</h2>
<div class="corpo" style="gap:7mm;align-items:stretch;margin-bottom:8mm">{cards}</div>
{rod(t,5)}</section>'''

def sprint(t):
    itens = t["sp"]; n = len(itens); W = 270; passo = (W - 24) / n
    s = f'<line x1="{12+passo/2}" y1="40" x2="{W-12-passo/2}" y2="40" stroke="#EFEAE3" stroke-opacity=".3" stroke-width="1.2"/>'
    for i, (nome, sub) in enumerate(itens):
        x = 12 + passo / 2 + i * passo
        destaque = nome in (t["sp"][5][0],)
        c = "#E8622C" if i in (0, 5) else "#EFEAE3"
        s += f'<circle cx="{x}" cy="40" r="{11 if i in (0,5) else 8}" fill="#141210" stroke="{c}" stroke-width="2"/>'
        s += f'<circle cx="{x}" cy="40" r="3" fill="{c}"/>'
        yl, ys = (72, 84) if i % 2 == 0 else (10, 22)
        s += f'<line x1="{x}" y1="{51 if i%2==0 else 29}" x2="{x}" y2="{62 if i%2==0 else 26}" stroke="{c}" stroke-opacity=".5" stroke-width=".8"/>' if i != 5 else ''
        s += f'<text x="{x}" y="{yl}" text-anchor="middle" font-size="8.6" fill="{c}" style="font-family:Archivo Black">{esc(nome)}</text>'
        s += f'<text x="{x}" y="{ys}" text-anchor="middle" font-size="6.2" fill="#A5A19B">{esc(sub)}</text>'
        if i < n - 1:
            s += f'<path d="M{x+passo/2-3} 37l3 3-3 3" stroke="#EFEAE3" stroke-opacity=".6" stroke-width="1.2" fill="none"/>'
    # ramificação para a pessoa
    x5 = 12 + passo / 2 + 5 * passo
    s += (f'<path d="M{x5} 51 C{x5} 105 {x5-30} 105 {x5-30} 118" stroke="#E8622C" stroke-width="1.4" stroke-dasharray="3 3" fill="none"/>'
          f'<circle cx="{x5-30}" cy="126" r="7" fill="#E8622C"/><circle cx="{x5-30}" cy="123.5" r="2.4" fill="#141210"/><path d="M{x5-34.5} 130.5a4.5 4 0 0 1 9 0" fill="#141210"/>')
    return f'''<section class="p esc">
<div class="k"><i></i>{esc(t["sp_k"])}</div><h2>{esc(t["sp_t"])}</h2>
<div class="corpo" style="margin-bottom:6mm"><svg viewBox="0 -6 {W} 146" width="100%">{s}</svg></div>
{rod(t,6)}</section>'''

def plano(t):
    fases = ""
    for i, (quando, nome, sub) in enumerate(t["fases"]):
        on = i == 0
        fases += (f'<div style="flex:1;border-top:3px solid {"var(--l)" if on else "var(--c)"};padding-top:4mm">'
                  f'<div class="k" style="color:{"var(--lt)" if on else "var(--t2)"}">{esc(quando)}</div>'
                  f'<div style="font-family:Archivo Black;font-size:16pt;margin-top:2mm">{esc(nome)}</div>'
                  f'<div style="font-size:11pt;color:var(--t2);margin-top:1.5mm">{esc(sub)}</div></div>')
    g = ('<rect x="0" y="0" width="300" height="120" fill="#fff"/>'
         + ''.join(f'<line x1="30" y1="{y}" x2="290" y2="{y}" stroke="#EFEAE3"/>' for y in (25, 50, 75))
         + '<line x1="116" y1="10" x2="116" y2="100" stroke="#CFC8BC" stroke-dasharray="2 3"/><line x1="203" y1="10" x2="203" y2="100" stroke="#CFC8BC" stroke-dasharray="2 3"/>'
         '<path d="M30 22 C80 26 100 40 130 55 S220 82 290 88" fill="none" stroke="#4D4A47" stroke-width="2.4" stroke-linecap="round"/>'
         '<path d="M30 92 C70 90 100 80 130 64 S220 26 290 18" fill="none" stroke="#E8622C" stroke-width="3" stroke-linecap="round"/>'
         '<path d="M30 100H292M288 97l5 3-5 3" stroke="#141210" stroke-width="1" fill="none"/>'
         f'<text x="292" y="112" text-anchor="end" font-size="6.5" fill="#4D4A47" style="font-family:Space Mono;letter-spacing:.1em">{esc(t["graf_x"].upper())}</text>'
         f'<text x="36" y="16" font-size="7" font-weight="700" fill="#4D4A47">{esc(t["graf_a"])}</text>'
         f'<text x="286" y="12" text-anchor="end" font-size="7" font-weight="700" fill="#A64923">{esc(t["graf_b"])}</text>')
    return f'''<section class="p">
<div class="k"><i></i>{esc(t["plano_k"])}</div><h2>{esc(t["plano_t"])}</h2>
<div style="margin-top:7mm;display:flex;gap:7mm">{fases}</div>
<div class="corpo" style="margin-top:6mm;margin-bottom:6mm"><svg viewBox="0 0 300 120" style="width:100%;max-height:82mm">{g}</svg></div>
{rod(t,7)}</section>'''

def controlo(t):
    c = t["ciclo"]; cx, cy, R = 70, 70, 46
    import math
    s = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#EFEAE3" stroke-opacity=".25" stroke-width="10"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#E8622C" stroke-width="3" stroke-dasharray="70 26.4" transform="rotate(-80 {cx} {cy})"/>'
    for i, nome in enumerate(c):
        a = math.radians(-90 + i * 120)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#E8622C"/>'
        tx, ty = cx + (R + 26) * math.cos(a), cy + (R + 22) * math.sin(a)
        s += f'<text x="{tx:.1f}" y="{ty+3:.1f}" text-anchor="middle" font-size="8.5" fill="#EFEAE3" style="font-family:Archivo Black">{esc(nome)}</text>'
    prom = ''.join(f'<div style="display:flex;gap:4mm;align-items:center;padding:4.2mm 0;border-bottom:1px solid rgba(239,234,227,.18);font-size:13pt;font-weight:600">'
                   f'<span style="flex:none;width:8mm;height:8mm;border:2px solid var(--l);border-radius:50%;display:flex;align-items:center;justify-content:center">'
                   f'<svg width="12" height="12" viewBox="0 0 12 12"><path d="M2.5 6.2l2.4 2.4 4.6-5" stroke="#E8622C" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg></span>{esc(p)}</div>'
                   for p in t["promessas"])
    return f'''<section class="p esc">
<div class="k"><i></i>{esc(t["ctrl_k"])}</div><h2>{esc(t["ctrl_t"])}</h2>
<div class="corpo" style="gap:14mm;align-items:center">
<svg viewBox="-38 -12 216 164" style="width:112mm;flex:none">{s}</svg>
<div style="flex:1">{prom}
<div style="margin-top:8mm;display:flex;align-items:baseline;gap:6mm;flex-wrap:wrap">
<span style="font-family:Archivo Black;font-size:22pt;color:var(--l)">{esc(t["cta"])}</span>
<span class="mono" style="font-size:11pt">{esc(t["site"])}</span><span class="mono" style="font-size:11pt;color:var(--o2)">{esc(t["tel"])}</span></div></div>
</div>
{rod(t,8)}</section>'''

for lang, t in T.items():
    html = (f'<!doctype html><html lang="{ {"ro":"ro","en":"en","pt":"pt-PT"}[lang] }"><head><meta charset="utf-8"><title>{esc(t["capa_t"])}</title>'
            f'<style>{FONTES}{CSS}</style></head><body>'
            + capa(t) + objetivo(t) + mapa(t) + matriz(t) + quick(t) + sprint(t) + plano(t) + controlo(t) + '</body></html>')
    h = os.path.join(AQUI, f"pos-diagnostico-{lang}.html")
    open(h, "w").write(html)
    pdf = os.path.join(AQUI, f"pos-diagnostico-{lang}.pdf")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "file://" + h], check=True, capture_output=True)
    print(lang, os.path.getsize(pdf) // 1024, "KB")
