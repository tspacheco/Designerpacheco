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


# ---------- modelo de números (pressupostos explícitos, a validar no piloto) ----------
N = 100                 # chamadas/contactos por dia, um ginásio
P = dict(
    atende_fria=0.20,   # chamada fria atendida
    resp_wa=0.35,       # responde ao WhatsApp em 3 toques
    atende_quente=0.70, # atende a chamada depois de ter respondido
    conv_fria=0.25,     # conversa fria → resultado
    conv_quente=0.35,   # conversa quente → resultado
    min_tent=2,         # minutos por tentativa de chamada
    min_conv=5,         # minutos por conversa
    dias=22,            # dias úteis por mês
)
def calc(variante, r=None):
    r = P["resp_wa"] if r is None else r
    if variante == "hoje":
        tent = N; conv = N*P["atende_fria"]; res = conv*P["conv_fria"]
        msgs = 0; resp = 0; tent_q = 0; conv_q = 0
    elif variante == "A":
        tent = N; conv = N*P["atende_fria"]; res_f = conv*P["conv_fria"]
        nao = N - conv; msgs = nao*3; resp = nao*r; tent_q = resp; conv_q = resp*P["atende_quente"]
        res = res_f + conv_q*P["conv_quente"]
    else:
        tent = 0; conv = 0; msgs = N*3; resp = N*r; tent_q = resp; conv_q = resp*P["atende_quente"]
        res = conv_q*P["conv_quente"]
    minutos = (tent+tent_q)*P["min_tent"] + (conv+conv_q)*P["min_conv"]
    return dict(tent=tent+tent_q, conv=conv+conv_q, msgs=msgs, resp=resp, res=res, horas=minutos/60,
                mes=res*P["dias"], por_hora=(res/(minutos/60)) if minutos else 0, perdidos=N-conv-conv_q)
H, A, Bv = calc("hoje"), calc("A"), calc("B")
def f0(x): return f"{x:.0f}".replace("-","−")
MG = B.CFG["mensalidade_ginasio"]
MENSAL_IVA = 400 * 1.23
def eur(x, sign=False, neg=False):
    v = f"{abs(x):,.0f}".replace(",", " ")
    if neg: return f"− {v} €"
    return (("+ " if x >= 0 else "− ") if sign else "") + f"{v} €"
def f1(x): return f"{x:.1f}".replace(".",",")
def pct(x): return f"{x*100:.0f} %"

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
<p class="lead">Hoje a receção faz mais de 100 chamadas por dia. O sistema que propomos faz o primeiro contacto por WhatsApp, insiste por si, e entrega à receção só quem já respondeu. Em cinco linhas, é isto que muda:</p>
<table class="tbl ba">
  <thead><tr><th></th><th>Hoje</th><th>Com o sistema</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<div class="callout"><b>A chamada passa a ser o último passo, não o primeiro.</b> A receção deixa de gastar a manhã a marcar números e passa a falar com quem quer falar.</div>
<p class="fine">A coluna “com o sistema” descreve a variante B. Se preferir manter a chamada em primeiro (variante A), o sistema entra a seguir a cada chamada não atendida. As duas variantes estão na página 3, as ofertas na página 4 e os números na página 5.</p>
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

# 3 — duas variantes
def mini(variante):
    W, Hh = 520, 132
    o = [f'<svg viewBox="0 0 {W} {Hh}" xmlns="http://www.w3.org/2000/svg">']
    def box(x, y, w, t, kind, ic):
        col = {"human": TEAL, "action": NAVY, "trigger": GOLD, "end": "#9AA0AE"}[kind]
        fill = {"human": "#E6F2F0", "action": "#fff", "trigger": "#FBF3E1", "end": "#EEEDF0"}[kind]
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="9" fill="{fill}" stroke="{col}" stroke-width="1.6"/>')
        o.append(B.icon(ic, x+8, y+8, col))
        o.append(f'<text x="{x+34}" y="{y+25}" font-family="Barlow Condensed" font-weight="700" font-size="14.5" fill="{INK}">{esc(t)}</text>')
    def arrow(pts, lab=None, side="top"):
        d = "M" + " L".join(f"{a},{b}" for a, b in pts)
        o.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ar2)"/>')
        if lab:
            (x1,y1),(x2,y2)=pts[0],pts[-1]
            if side == "top":
                o.append(f'<text x="{(x1+x2)/2}" y="{y1-6}" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" fill="{MUTED}">{esc(lab)}</text>')
            else:
                o.append(f'<text x="{x1+8}" y="{(y1+y2)/2+4}" font-family="JetBrains Mono" font-size="9.5" fill="{MUTED}">{esc(lab)}</text>')
    o.append(f'<defs><marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{LINE}"/></marker></defs>')
    if variante == "A":
        box(0, 14, 150, "Chamada da receção", "human", "phone")
        arrow([(150, 34), (230, 34)], "atendeu")
        box(230, 14, 100, "Conversa", "human", "user")
        arrow([(330, 34), (410, 34)])
        box(410, 14, 100, "Resultado", "end", "check")
        arrow([(60, 54), (60, 84)], "não atendeu", "right")
        box(0, 84, 150, "WhatsApp · 3 toques", "action", "msg")
        arrow([(150, 104), (230, 104)], "respondeu")
        box(230, 84, 170, "2.ª chamada, quente", "human", "phone")
        arrow([(400, 104), (460, 104), (460, 54)])
    else:
        box(0, 14, 150, "WhatsApp · 3 toques", "action", "msg")
        arrow([(150, 34), (230, 34)], "respondeu")
        box(230, 14, 170, "Chamada da receção", "human", "phone")
        arrow([(400, 34), (410, 34)])
        box(410, 14, 100, "Resultado", "end", "check")
        arrow([(60, 54), (60, 84)], "não respondeu", "right")
        box(0, 84, 150, "Pausa 3 semanas", "end", "pause")
    o.append("</svg>")
    return "".join(o)

pages.append(page("", h("Duas formas de arrancar", "A escolha é do dono. O sistema é o mesmo.", "A dúvida legítima: deixar ou não de ligar primeiro. Por isso o sistema tem duas variantes. A lógica, as mensagens e a lista da receção são iguais; muda só a ordem em que a chamada entra.") + f'''
<div class="var">
  <div class="var-head"><span class="vtag">Variante A</span><h3>Chamada primeiro. O sistema recupera quem não atende.</h3></div>
  <div class="mini">{mini("A")}</div>
  <p class="vdesc">A receção continua a ligar como hoje. Cada chamada não atendida entra automaticamente no WhatsApp: três toques em sete dias. Quem responde volta à lista da receção, já quente. A segunda chamada nunca mais é desperdiçada.</p>
  <div class="pc">
    <div class="pro"><b>Vantagem</b><p>Mantém a metodologia atual, sem mudar hábitos da equipa. A chamada fria continua a apanhar quem atende à primeira, e o sistema trata dos outros 80 %. Mais resultados no total.</p></div>
    <div class="con"><b>Desvantagem</b><p>Continua a gastar o tempo útil da receção nas 100 tentativas diárias. Esse tempo podia estar na sala, a vender e a acompanhar membros. Com as chamadas quentes por cima, o dia ainda fica mais cheio.</p></div>
  </div>
</div>
<div class="var">
  <div class="var-head"><span class="vtag b">Variante B</span><h3>Mensagem primeiro. A receção liga só a quem respondeu.</h3></div>
  <div class="mini">{mini("B")}</div>
  <p class="vdesc">O sistema faz o primeiro contacto por WhatsApp a todos. A receção recebe uma lista curta e liga só a quem disse “sim” ou “depois”. Quem não responde em sete dias fica em pausa três semanas e recebe depois um novo toque, com uma oferta. Ninguém se perde.</p>
  <div class="pc">
    <div class="pro"><b>Vantagem</b><p>Liberta a maior parte do tempo da receção para trabalho que gera vendas. Cada chamada feita é uma conversa com quem já quis falar. Melhor resultado por hora de trabalho, de longe.</p></div>
    <div class="con"><b>Desvantagem</b><p>Muda a metodologia: quem só reage a uma chamada e nunca lê mensagens deixa de ser apanhado à primeira. Menos resultados no total do que a variante A, embora com muito menos horas.</p></div>
  </div>
</div>
''', 3))

# 4 — ofertas rotativas
ing = [
    ("Batido de proteína", "Custa cêntimos, sabe a recompensa. Serve para trazer alguém à porta."),
    ("Água do ginásio", "O gesto mais simples. Funciona como lembrete físico de que a casa está à espera."),
    ("Sessão com o massagista", "Vale muito para quem está parado ou cansado. Ideal para quem já foi sócio."),
    ("1 hora com personal trainer", f"A oferta que fecha contratos: uma hora de treino a quem assina mensalidade. A {MG} €/mês com contrato, paga-se no primeiro mês."),
]
ings = "".join(f'<div class="ing"><b>{esc(a)}</b><p>{esc(b)}</p></div>' for a, b in ing)
pages.append(page("", h("Ofertas que abrem portas", "Três ofertas ativas, renovadas de 3 em 3 meses.", "Uma mensagem com uma oferta concreta converte melhor do que um convite vazio. O ginásio já tem os ingredientes; o sistema tem os lugares certos para os pôr.") + f'''
<div class="mech">
  <div><span class="num">1</span><b>Cada toque leva uma oferta</b><p>O terceiro toque de cada sequência, o da última mensagem, passa a ter sempre uma oferta concreta. Nas situações mais valiosas, também o primeiro.</p></div>
  <div><span class="num">3</span><b>Três ofertas ativas de cada vez</b><p>Uma por situação: uma para quem nunca entrou, uma para quem parou, uma para quem vai renovar. Poucas, para a receção e os sócios as reconhecerem.</p></div>
  <div><span class="num">90</span><b>Renovadas de 3 em 3 meses</b><p>Ao fim de um trimestre trocam-se. As mensagens nunca ficam gastas, e o painel mostra qual das três converteu melhor antes de decidir as próximas.</p></div>
</div>
<h3 class="mt">O que o ginásio já tem para oferecer</h3>
<div class="ings">{ings}</div>
<div class="callout"><b>Nada disto é um pacote fechado.</b> São opções. As combinações, os limites e o que cada oferta custa à casa definem-se convosco na primeira reunião. O que fica claro desde já: há espaço para criar ofertas para qualquer perfil, e um sistema capaz de as pôr à frente da pessoa certa, no dia certo.</div>
''', 4))

# 4 — números previstos
def row(lab, key, fmt=f0, unit=""):
    return f'<tr><td class="lab">{esc(lab)}</td><td>{fmt(H[key])}{unit}</td><td>{fmt(A[key])}{unit}</td><td class="hl">{fmt(Bv[key])}{unit}</td></tr>'
sens = "".join(f'<tr><td class="lab">Resposta ao WhatsApp de {pct(r)}</td><td>{f0(calc("hoje")["res"])}</td><td>{f0(calc("A", r)["res"])}</td><td class="hl">{f0(calc("B", r)["res"])}</td></tr>' for r in (0.25, 0.35, 0.45))
pages.append(page("", h("Números previstos", "100 chamadas por dia, em cada variante.", "Projeção para um só ginásio. Não são resultados medidos: são contas feitas a partir dos pressupostos abaixo, que o piloto de 30 dias vai substituir por números reais.") + f'''
<h3>Pressupostos usados</h3>
<div class="assump">
  <div><b>{pct(P["atende_fria"])}</b><span>atendem a chamada fria<br><em>valor prudente para chamadas frias; a validar</em></span></div>
  <div><b>{pct(P["resp_wa"])}</b><span>respondem ao WhatsApp em 3 toques<br><em>a validar no piloto; ver tabela em baixo</em></span></div>
  <div><b>{pct(P["atende_quente"])}</b><span>atendem a chamada depois de responderem<br><em>já disseram “sim”, a chamada é esperada</em></span></div>
  <div><b>{pct(P["conv_fria"])} · {pct(P["conv_quente"])}</b><span>conversa fria · quente que dá resultado<br><em>inscrição, regresso ou pagamento</em></span></div>
  <div><b>{P["min_tent"]} · {P["min_conv"]} min</b><span>por tentativa · por conversa<br><em>inclui marcar, esperar e anotar</em></span></div>
  <div><b>{P["dias"]} dias</b><span>úteis por mês<br><em>para a linha mensal</em></span></div>
</div>
<table class="tbl num">
  <thead><tr><th>Por dia, num ginásio</th><th>Hoje</th><th>Variante A</th><th class="hl">Variante B</th></tr></thead>
  <tbody>
    {row("Chamadas feitas pela receção", "tent")}
    {row("Mensagens WhatsApp enviadas (automáticas)", "msgs")}
    {row("Pessoas que respondem por mensagem", "resp")}
    {row("Conversas reais (alguém do outro lado)", "conv")}
    {row("Contactos perdidos sem conversa", "perdidos")}
    <tr class="sep"><td class="lab">Resultados por dia</td><td>{f0(H["res"])}</td><td>{f0(A["res"])}</td><td class="hl">{f0(Bv["res"])}</td></tr>
    <tr><td class="lab">Resultados por mês ({P["dias"]} dias)</td><td>{f0(H["mes"])}</td><td>{f0(A["mes"])}</td><td class="hl">{f0(Bv["mes"])}</td></tr>
    <tr><td class="lab">Horas da receção ao telefone, por dia</td><td>{f1(H["horas"])} h</td><td>{f1(A["horas"])} h</td><td class="hl">{f1(Bv["horas"])} h</td></tr>
    <tr class="sep"><td class="lab">Resultados por hora de receção</td><td>{f1(H["por_hora"])}</td><td>{f1(A["por_hora"])}</td><td class="hl">{f1(Bv["por_hora"])}</td></tr>
    <tr class="gain"><td class="lab">Mensalidades ganhas por mês, a {MG} € cada</td><td>{eur(H["mes"]*MG)}</td><td>{eur(A["mes"]*MG)}</td><td class="hl">{eur(Bv["mes"]*MG)}</td></tr>
    <tr class="gain"><td class="lab">Ganho face a hoje, por mês</td><td>—</td><td>{eur((A["mes"]-H["mes"])*MG, sign=True)}</td><td class="hl">{eur((Bv["mes"]-H["mes"])*MG, sign=True)}</td></tr>
    <tr class="gain"><td class="lab">Mensalidade do sistema (400 € + 92 € IVA = 492 €)</td><td>—</td><td>{eur(MENSAL_IVA, sign=False, neg=True)}</td><td class="hl">{eur(MENSAL_IVA, sign=False, neg=True)}</td></tr>
    <tr class="gain sep"><td class="lab">Ganho líquido por mês, num ginásio</td><td>—</td><td>{eur((A["mes"]-H["mes"])*MG-MENSAL_IVA, sign=True)}</td><td class="hl">{eur((Bv["mes"]-H["mes"])*MG-MENSAL_IVA, sign=True)}</td></tr>
  </tbody>
</table>
<p class="fine">Um “resultado” vale uma mensalidade de {MG} € (inscrição nova, sócio que volta ou pagamento regularizado). Com contrato, cada mês acrescenta às anteriores: o ganho acumula. A mensalidade do sistema cobre os três ginásios; aqui está contada por inteiro contra um só.</p>
<div class="sens"><b>E se a taxa de resposta ao WhatsApp for outra?</b> resultados por dia · {" · ".join(f'<span><i>{pct(r)}</i> A {f0(calc("A", r)["res"])} · B {f0(calc("B", r)["res"])}</span>' for r in (0.25, 0.35, 0.45))} · hoje {f0(H["res"])} em qualquer caso</div>
<div class="note"><b>Como ler.</b> A variante A dá mais resultados porque soma a chamada fria ao sistema, mas custa mais horas. A variante B devolve à receção cerca de {f1(H["horas"]-Bv["horas"])} h por dia, com o melhor resultado por hora. Em três ginásios, multiplica-se por três. O piloto troca estes pressupostos por números medidos.</div>
''', 5))

# 5 — investimento + escolha
pages.append(page("", h("Investimento e escolha", "Um sistema para todos os Legends de Portugal.") + f'''
<div class="pricebox">
  <div class="pl">
    <span class="mono">montagem · pagamento único</span>
    <b>{esc(C["setup"])} <small>{esc(C["setup_nota"])}</small></b>
    <span class="mono">acompanhamento · por mês</span>
    <b class="m">{esc(C["mensal"])} <small>{esc(C["mensal_nota"])}</small></b>
    <p>A mensalidade cobre <b class="t">todos os ginásios Be Legend em Portugal</b>, com todos os servidores a funcionar e reparação prioritária. Só as mensagens WhatsApp são pagas à Meta ao custo, em nome do ginásio.</p>
  </div>
  <ul class="ul tight pr">
    <li>Construção dos 5 fluxos: leads, aulas experimentais, inativos, pagamentos, renovações</li>
    <li>Variante A ou B à escolha; pode mudar-se de uma para a outra durante o piloto</li>
    <li>Três ofertas rotativas por trimestre, definidas convosco e medidas no painel</li>
    <li>Um sistema, replicado por ginásio: Olhão primeiro, Faro e Lisboa a seguir, sem nova montagem</li>
    <li>Mensagens escritas com a equipa, na voz do Be Legend, e registadas na Meta</li>
    <li>Ligação ao software do ginásio ou à folha de contactos</li>
    <li>Lista diária da receção e painel por ginásio, no telemóvel</li>
    <li>Mensalidade: servidores a funcionar e vigiados, reparação prioritária, ajustes sem limite, relatório mensal, suporte direto</li>
  </ul>
</div>
<h3 class="mt">A decisão do dono</h3>
<div class="choice">
  <div class="opt"><span class="cb"></span><div><b>Variante A</b><span>Chamada primeiro. O sistema recupera quem não atende.</span></div></div>
  <div class="opt"><span class="cb"></span><div><b>Variante B</b><span>Mensagem primeiro. A receção liga só a quem respondeu.</span></div></div>
  <div class="opt wide"><span class="cb"></span><div><b>Aplicável em todos os Be Legend Portugal</b><span>Olhão, Faro e Lisboa, com a mesma variante e a mesma mensalidade.</span></div></div>
</div>
<p class="fine next">Mais tarde, o mesmo motor pode receber um segundo fluxo: aquisição de novos clientes. Depois do piloto.</p>
<div class="sign"><div><span class="mono">nome</span><i></i></div><div><span class="mono">data</span><i></i></div><div><span class="mono">assinatura</span><i></i></div></div>
<div class="callout final">
  <div><b>{esc(C["marca"])}</b><br><span>Web design e sistemas para negócios locais · Algarve</span><br><span class="pres">Assistência presencial: um subdiretor da Pacheco Studios desloca-se ao ginásio sempre que for necessário.</span></div>
  <div class="r"><span class="mono">{esc(C["email"])}</span></div>
</div>
<p class="fine">O esquema completo está no documento “Follow-up &amp; Recuperação de Clientes” que acompanha este resumo.</p>
''', 6))

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
.ul.pr li{{font-size:9.8pt;margin-bottom:5px}}
.var{{border:1px solid #EAE5DA;border-radius:12px;padding:10px 14px 10px;margin-top:8px;background:#fff}}
.var-head{{display:flex;align-items:center;gap:10px;margin-bottom:6px}}
.var-head h3{{margin:0;font-size:14.5pt}}
.vtag{{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:11pt;letter-spacing:.06em;text-transform:uppercase;background:var(--navy);color:var(--gold);padding:3px 10px;border-radius:20px;white-space:nowrap}}
.vtag.b{{background:var(--teal);color:#fff}}
.mini{{margin:2px 0 4px}}
.mini svg{{width:100%;height:auto;max-height:36mm}}
.vdesc{{font-size:9.8pt;color:#3A3F4B;margin-bottom:8px}}
.pc{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.pro,.con{{border-radius:8px;padding:7px 10px;font-size:9.2pt;color:#3A3F4B;line-height:1.4}}
.pro{{background:#E6F2F0;border-left:3px solid var(--teal)}}
.con{{background:#FBF3E1;border-left:3px solid var(--gold)}}
.pro b,.con b{{display:block;font-family:'JetBrains Mono',monospace;font-size:8pt;letter-spacing:.08em;text-transform:uppercase;margin-bottom:2px}}
.pro b{{color:var(--teal)}} .con b{{color:#8A6414}}
.assump{{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:2px 0 8px}}
.assump div{{background:var(--paper);border:1px solid #EAE5DA;border-radius:8px;padding:7px 10px}}
.assump b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:15.5pt;color:var(--navy);line-height:1;margin-bottom:3px}}
.assump span{{font-size:8.6pt;color:#3A3F4B;line-height:1.3}}
.assump em{{display:block;font-style:normal;font-family:'JetBrains Mono',monospace;font-size:7.4pt;color:var(--muted);margin-top:3px}}
.tbl.num td,.tbl.num th{{text-align:right;padding:4px 10px}}
.tbl.num td.lab,.tbl.num th:first-child{{text-align:left}}
.tbl.num td{{font-family:'JetBrains Mono',monospace;font-size:9.6pt}}
.tbl.num td.lab{{font-family:Inter;font-size:9.6pt}}
.tbl.num th.hl,.tbl.num td.hl{{background:#F2F8F7;color:var(--teal);font-weight:700}}
.tbl.num tr.sep td{{border-top:1.5px solid var(--navy);font-weight:700;color:var(--navy)}}
.tbl.num.small td{{padding:3.5px 10px;font-size:9pt}}
.mt2{{margin-top:8px}}
.pricebox .pl b small{{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:9pt;color:var(--muted);letter-spacing:0;margin-left:2px}}
.mech{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:4px}}
.mech div{{background:var(--paper);border:1px solid #EAE5DA;border-radius:10px;padding:14px 14px 12px}}
.mech .num{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:24pt;color:var(--gold);line-height:1;margin-bottom:6px}}
.mech b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:14pt;color:var(--navy);line-height:1.1;margin-bottom:4px}}
.mech p{{font-size:9.6pt;color:#3A3F4B}}
.ings{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px}}
.ing{{border:1.5px dashed var(--teal);border-radius:10px;padding:12px 14px;background:#fff}}
.ing b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:14pt;color:var(--teal);line-height:1.1;margin-bottom:3px}}
.ing p{{font-size:9.8pt;color:#3A3F4B}}
.tbl.num tr.gain td{{background:#FBF3E1}}
.tbl.num tr.gain td.hl{{background:#EEF3E4}}
.tbl.num tr.gain.sep td{{color:var(--navy);font-weight:700}}
.sens{{margin-top:10px;background:var(--paper);border:1px solid #EAE5DA;border-radius:8px;padding:8px 12px;font-size:9.2pt;color:#3A3F4B}}
.sens b{{color:var(--navy);margin-right:4px}}
.sens span{{font-family:'JetBrains Mono',monospace;font-size:8.8pt;color:var(--navy);white-space:nowrap}}
.sens i{{font-style:normal;color:var(--gold)}}
.fine.next{{margin:10px 0 0;color:var(--navy)}}
.choice{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px}}
.opt{{display:flex;gap:10px;align-items:flex-start;border:1.5px solid var(--navy);border-radius:10px;padding:10px 12px}}
.opt.wide{{grid-column:1/3;background:var(--paper)}}
.opt b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13pt;color:var(--navy);line-height:1.1}}
.opt span:not(.cb){{font-size:9.2pt;color:#3A3F4B}}
.cb{{flex:0 0 18px;width:18px;height:18px;border:2px solid var(--navy);border-radius:4px;margin-top:2px;background:#fff}}
.sign{{display:grid;grid-template-columns:1.2fr .7fr 1.2fr;gap:14px;margin-top:12px}}
.sign i{{display:block;border-bottom:1.5px solid var(--navy);height:22px}}
.sign .mono{{display:block;margin-bottom:2px}}
.callout.final{{margin-top:12px;padding:11px 16px}}
"""

doc = f"""<!DOCTYPE html>
<html lang="pt-PT"><head><meta charset="utf-8"><title>O que vai mudar · {esc(C["cliente"])} {esc(C["local"])}</title>
<style>{B.CSS}{EXTRA}</style></head><body>{''.join(pages)}</body></html>"""
(B.HERE / "resumo.html").write_text(doc, encoding="utf-8")
print("resumo.html", len(doc) // 1024, "KB")
