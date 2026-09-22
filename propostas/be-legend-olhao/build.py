#!/usr/bin/env python3
"""Gera proposta.html (fontes embutidas) para o PDF "Follow-up & Recuperação de Clientes — Be Legend Olhão".
Depois: NODE_PATH=$(npm root -g) node render.js
Tudo o que é preço/valor editável está no dicionário CFG."""
import base64, pathlib, html

HERE = pathlib.Path(__file__).parent

CFG = dict(
    cliente="Be Legend",
    local="Olhão",
    data="Setembro 2026",
    chamadas_dia="100+",
    min_por_tentativa=2,          # estimativa, assinalada no documento
    setup="2700 €",
    setup_nota="IVA incluído",
    mensal="400 €",
    mensal_nota="+ IVA (92 €) = 492 €",
    mensalidade_ginasio=40,     # € por mensalidade de sócio, em média (dado do Tomás)
    piloto_dias="30",
    email="tspacheco26@gmail.com",
    marca="Pacheco Studios",
)

# ---------- fontes ----------
def font_face(fam, weight, file):
    b64 = base64.b64encode((HERE / "fontes" / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{weight};font-style:normal;src:url(data:font/woff2;base64,{b64}) format('woff2');}}"

FONTS = "\n".join([
    font_face("Barlow Condensed", 600, "BarlowCondensed-600.woff2"),
    font_face("Barlow Condensed", 700, "BarlowCondensed-700.woff2"),
    font_face("Barlow Condensed", 800, "BarlowCondensed-800.woff2"),
    font_face("Inter", 400, "Inter-400.woff2"),
    font_face("Inter", 500, "Inter-500.woff2"),
    font_face("Inter", 600, "Inter-600.woff2"),
    font_face("Inter", 700, "Inter-700.woff2"),
    font_face("JetBrains Mono", 500, "JetBrainsMono-500.woff2"),
])

# ---------- diagrama (estilo n8n) ----------
NAVY, GOLD, PAPER, INK, MUTED, TEAL, LINE = "#142238", "#C59A3E", "#F6F3EC", "#1B1F2A", "#6B7280", "#1F7A6D", "#B9B2A3"

def icon(kind, x, y, col):
    s = f'stroke="{col}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    g = f'<g transform="translate({x},{y})">'
    if kind == "clock":
        g += f'<circle cx="12" cy="12" r="9" {s}/><path d="M12 7v5l3 2" {s}/>'
    elif kind == "list":
        g += f'<path d="M5 6h14M5 12h14M5 18h9" {s}/>'
    elif kind == "branch":
        g += f'<path d="M12 4v6M12 10L6 16M12 10l6 6" {s}/><circle cx="6" cy="18" r="2" {s}/><circle cx="18" cy="18" r="2" {s}/><circle cx="12" cy="4" r="2" {s}/>'
    elif kind == "msg":
        g += f'<path d="M4 5h16v11H9l-5 4z" {s}/>'
    elif kind == "wait":
        g += f'<path d="M6 3h12M6 21h12M7 3c0 6 5 6 5 9s-5 3-5 9M17 3c0 6-5 6-5 9s5 3 5 9" {s}/>'
    elif kind == "q":
        g += f'<circle cx="12" cy="12" r="9" {s}/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 1-1 1.7M12 17h.01" {s}/>'
    elif kind == "phone":
        g += f'<path d="M6 3h4l2 5-2.5 1.5a11 11 0 0 0 5 5L16 12l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 4 5a2 2 0 0 1 2-2z" {s}/>'
    elif kind == "check":
        g += f'<circle cx="12" cy="12" r="9" {s}/><path d="M8 12l3 3 5-6" {s}/>'
    elif kind == "pause":
        g += f'<path d="M12 3v18M3 12h18M6 6l12 12M18 6L6 18" {s}/>'
    elif kind == "inbox":
        g += f'<path d="M4 13l2-8h12l2 8v6H4z M4 13h5l1.5 2h3L15 13h5" {s}/>'
    elif kind == "brain":
        g += f'<path d="M9 4a3 3 0 0 0-3 3v1a3 3 0 0 0-2 3 3 3 0 0 0 2 3v1a3 3 0 0 0 3 3h1V4zM15 4a3 3 0 0 1 3 3v1a3 3 0 0 1 2 3 3 3 0 0 1-2 3v1a3 3 0 0 1-3 3h-1V4z" {s}/>'
    elif kind == "chart":
        g += f'<path d="M4 20h16M7 17v-6M12 17V7M17 17v-9" {s}/>'
    elif kind == "user":
        g += f'<circle cx="12" cy="8" r="4" {s}/><path d="M4 21a8 8 0 0 1 16 0" {s}/>'
    return g + "</g>"

def esc(t): return html.escape(t, quote=True)

def node(id_, x, y, title, sub, kind, ic, w=200, h=60):
    """kind: trigger | action | decision | wait | human | end"""
    fill, stroke, tcol, icol, dash = "#FFFFFF", LINE, INK, NAVY, ""
    if kind == "trigger":  fill, stroke, icol = "#FBF3E1", GOLD, GOLD
    if kind == "decision": stroke, dash, icol = NAVY, ' stroke-dasharray="5 4"', NAVY
    if kind == "wait":     fill, stroke, tcol, icol = "#F1EFE9", "#D6D0C2", MUTED, MUTED
    if kind == "human":    fill, stroke, icol = "#E6F2F0", TEAL, TEAL
    if kind == "end":      fill, stroke, tcol, icol = "#EEEDF0", "#C9C6D0", MUTED, MUTED
    r = 10
    out = f'<g id="{id_}">'
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"{dash}/>'
    out += f'<rect x="{x+10}" y="{y+(h-36)//2}" width="36" height="36" rx="8" fill="{stroke if kind in ("trigger","human") else "#EEF0F4"}" opacity="{0.18 if kind in ("trigger","human") else 1}"/>'
    out += icon(ic, x+16, y+(h-36)//2+6, icol)
    ty = y + h/2 - (7 if sub else -6)
    out += f'<text x="{x+56}" y="{ty}" font-family="Barlow Condensed" font-weight="700" font-size="19" fill="{tcol}">{esc(title)}</text>'
    if sub:
        out += f'<text x="{x+56}" y="{ty+17}" font-family="Inter" font-size="10.5" fill="{MUTED}">{esc(sub)}</text>'
    # ports
    out += f'<circle cx="{x}" cy="{y+h/2}" r="3.5" fill="#fff" stroke="{stroke}" stroke-width="1.6"/>'
    out += f'<circle cx="{x+w}" cy="{y+h/2}" r="3.5" fill="#fff" stroke="{stroke}" stroke-width="1.6"/>'
    return out + "</g>"

def chip(x, y, label, w=150, h=38):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="19" fill="{NAVY}"/>'
            f'<text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="16" fill="#fff" letter-spacing="0.5">{esc(label)}</text>')

def edge(pts, label=None, col=LINE, lab_col=MUTED, arrow=True, lab_dx=0, lab_dy=-6):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    out = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.8" marker-end="url(#arr)"/>' if arrow else f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.8"/>'
    if label:
        (x1, y1), (x2, y2) = pts[0], pts[1]
        lx, ly = (x1 + x2) / 2 + lab_dx, (y1 + y2) / 2 + lab_dy
        out += f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="JetBrains Mono" font-size="10.5" fill="{lab_col}" font-weight="500">{esc(label)}</text>'
    return out

def diagram():
    W, H = 1000, 1180
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Inter">']
    s.append(f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{LINE}"/></marker>'
             f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.2" r="1.2" fill="#DDD8CB"/></pattern></defs>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')

    # ----- linha 1: gatilho → lê → classifica
    s.append(node("A", 40, 40, "Todos os dias, 09:00", "gatilho automático", "trigger", "clock", w=220))
    s.append(edge([(260, 70), (330, 70)]))
    s.append(node("B", 330, 40, "Lê os contactos", "software do ginásio ou folha", "action", "list", w=230))
    s.append(edge([(560, 70), (630, 70)]))
    s.append(node("C", 630, 40, "Classifica a situação", "5 situações (ver página 5)", "action", "branch", w=230))

    # ----- linha 2: 5 chips
    chips = ["Lead novo", "Aula experimental", "Inativo 14 dias", "Pagamento em atraso", "Renovação"]
    xs = [40, 232, 424, 616, 808]
    cy = 160
    for x, lab in zip(xs, chips):
        s.append(edge([(745, 100), (745, 130), (x + 75, 130), (x + 75, cy)], arrow=False))
        s.append(chip(x, cy, lab))
    # junção para D
    for x in xs:
        s.append(edge([(x + 75, cy + 38), (x + 75, 225), (500, 225)], arrow=False))
    s.append(edge([(500, 225), (500, 258)]))

    # ----- coluna central
    cx = 380
    s.append(node("D", cx, 258, "WhatsApp · toque 1", "mensagem aprovada pela Meta", "action", "msg", w=240))
    s.append(edge([(500, 318), (500, 350)]))
    s.append(node("E", cx, 350, "Espera 24 h", None, "wait", "wait", w=240))
    s.append(edge([(500, 410), (500, 442)]))
    s.append(node("F", cx, 442, "Respondeu?", None, "decision", "q", w=240))
    s.append(edge([(620, 472), (700, 472)], "sim"))
    s.append(edge([(500, 502), (500, 534)], "não", lab_dx=18, lab_dy=4))
    s.append(node("I", cx, 534, "WhatsApp · toque 2", "dia 3 · lembrete curto", "action", "msg", w=240))
    s.append(edge([(500, 594), (500, 626)]))
    s.append(node("J", cx, 626, "Espera 4 dias", None, "wait", "wait", w=240))
    s.append(edge([(500, 686), (500, 718)]))
    s.append(node("K", cx, 718, "Respondeu?", None, "decision", "q", w=240))
    s.append(edge([(620, 748), (660, 748), (660, 472)], "sim", lab_dy=-6, arrow=False))
    s.append(edge([(500, 778), (500, 810)], "não", lab_dx=18, lab_dy=4))
    s.append(node("L", cx, 810, "WhatsApp · toque 3", "dia 7 · última mensagem + oferta", "action", "msg", w=240))
    s.append(edge([(500, 870), (500, 902)]))
    s.append(node("M", cx, 902, "Espera 3 dias", None, "wait", "wait", w=240))
    s.append(edge([(500, 962), (500, 994)]))
    s.append(node("N", cx, 994, "Respondeu?", None, "decision", "q", w=240))
    s.append(edge([(620, 1024), (660, 1024), (660, 748)], "sim", arrow=False))
    s.append(edge([(500, 1054), (500, 1086)], "não", lab_dx=18, lab_dy=4))
    s.append(node("O", cx, 1086, "Pausa 30 dias", "volta à lista mais tarde, sem insistir", "end", "pause", w=260))

    # ----- coluna direita: receção
    rx = 700
    s.append(node("G", rx, 442, "Lista da receção", "ligar hoje · nome, situação, resposta", "human", "phone", w=260))
    s.append(edge([(830, 502), (830, 534)]))
    s.append(node("H", rx, 534, "Resultado registado", "inscreveu · reagendou · não quer", "human", "check", w=260))

    # ----- coluna direita: respostas a qualquer hora
    s.append(f'<rect x="{rx-14}" y="646" width="288" height="420" rx="14" fill="none" stroke="{LINE}" stroke-dasharray="6 5"/>')
    s.append(f'<text x="{rx}" y="668" font-family="JetBrains Mono" font-size="10.5" fill="{MUTED}" font-weight="500">EM PARALELO · 24/7</text>')
    s.append(node("P", rx, 680, "Resposta recebida", "a qualquer hora, de qualquer toque", "trigger", "inbox", w=260))
    s.append(edge([(830, 740), (830, 772)]))
    s.append(node("Q", rx, 772, "Interpreta a resposta", "sim · depois · não · PARA", "action", "brain", w=260))
    s.append(edge([(830, 832), (830, 862)]))
    rows = [("sim", "entra na lista da receção de hoje"), ("depois", "reagenda o próximo toque"), ("não / PARA", "sai da lista, sem mais mensagens")]
    for i, (k, v) in enumerate(rows):
        y = 862 + i * 58
        s.append(f'<rect x="{rx}" y="{y}" width="260" height="46" rx="8" fill="#fff" stroke="{LINE}"/>')
        s.append(f'<text x="{rx+12}" y="{y+19}" font-family="JetBrains Mono" font-size="11" fill="{NAVY}" font-weight="500">{esc(k)}</text>')
        s.append(f'<text x="{rx+12}" y="{y+35}" font-family="Inter" font-size="10.5" fill="{MUTED}">{esc(v)}</text>')
        if i < 2:
            s.append(edge([(830, y + 46), (830, y + 58)], arrow=False))

    # ----- painel
    s.append(node("S", 40, 1086, "Painel semanal", "enviados · respostas · chamadas · recuperados", "action", "chart", w=300))

    # ----- legenda
    lg = [(GOLD, "gatilho"), (NAVY, "ação automática"), (TEAL, "pessoa (receção)"), ("#D6D0C2", "espera")]
    x0 = 40
    for col, lab in lg:
        s.append(f'<rect x="{x0}" y="1150" width="14" height="14" rx="4" fill="{col}"/>')
        s.append(f'<text x="{x0+20}" y="1161" font-family="Inter" font-size="10.5" fill="{MUTED}">{esc(lab)}</text>')
        x0 += 30 + len(lab) * 6.4
    s.append("</svg>")
    return "".join(s)

# ---------- página HTML ----------
C = CFG
horas = C["chamadas_dia"].rstrip("+")
horas_dia = int(horas) * C["min_por_tentativa"] / 60

def page(cls, inner, num=None, footer=True):
    ft = ""
    if footer:
        ft = f'<footer class="ft"><span>{esc(C["marca"])} · Follow-up &amp; Recuperação de Clientes · {esc(C["cliente"])} {esc(C["local"])}</span><span>{num if num else ""}</span></footer>'
    return f'<section class="page {cls}">{inner}{ft}</section>'

def h(kicker, title, lead=None):
    out = f'<p class="kicker">{kicker}</p><h2>{title}</h2>'
    if lead: out += f'<p class="lead">{lead}</p>'
    return out

pages = []

# 1 — capa
pages.append(page("cover", f'''
<div class="cover-top"><span class="brand">{esc(C["marca"])}</span><span class="mono">{esc(C["data"])}</span></div>
<div class="cover-mid">
  <p class="cover-kicker">Esquema de funcionamento · proposta</p>
  <h1>Follow-up &amp;<br>Recuperação<br>de Clientes</h1>
  <p class="cover-client">{esc(C["cliente"])} · {esc(C["local"])}</p>
  <p class="cover-sub">Como transformar {esc(C["chamadas_dia"])} chamadas por dia num sistema que faz o primeiro contacto sozinho, insiste por si, e só entrega à receção quem já respondeu.</p>
</div>
<div class="cover-bot">
  <div class="cover-stat"><b>{esc(C["chamadas_dia"])}</b><span>chamadas por dia, hoje</span></div>
  <div class="cover-stat"><b>3</b><span>toques automáticos em 7 dias</span></div>
  <div class="cover-stat"><b>1</b><span>lista por dia para a receção</span></div>
</div>
<div class="cover-rule"></div>
<p class="cover-foot">Documento de apresentação para decisão · leitura em 6 minutos</p>
''', footer=False))

# 2 — ponto de partida
pages.append(page("", h("01 · O ponto de partida", "100 chamadas por dia. E depois?", None) + f'''
<div class="grid3">
  <div class="tile"><b>{esc(C["chamadas_dia"])}</b><span>chamadas por dia, no mínimo<br><em>base de cálculo deste documento</em></span></div>
  <div class="tile"><b>7 dias</b><span>de insistência automática por contacto<br><em>três toques, sem ocupar a receção</em></span></div>
  <div class="tile"><b>~{horas_dia:.0f} h</b><span>de trabalho por dia só em tentativas<br><em>estimativa: {C["min_por_tentativa"]} min por tentativa, incluindo marcar e anotar</em></span></div>
</div>
<div class="cols2">
  <div>
    <h3>O que se perde</h3>
    <ul class="ul">
      <li><b>A chamada não deixa rasto.</b> Um número desconhecido que toca uma vez é ignorado. Não fica nada no telemóvel da pessoa para ela voltar.</li>
      <li><b>O tempo vai para as tentativas.</b> A receção gasta a manhã a marcar números em vez de falar com quem quer falar.</li>
      <li><b>Não há segunda tentativa organizada.</b> Quem não atendeu hoje fica dependente de alguém se lembrar de voltar a ligar.</li>
      <li><b>Não se mede.</b> Sem registo, não se sabe quantos leads viraram inscrição nem quantos membros saíram sem uma única conversa.</li>
    </ul>
  </div>
  <div>
    <h3>O que muda com o sistema</h3>
    <ul class="ul ok">
      <li><b>A mensagem fica lá.</b> Um WhatsApp com o nome da pessoa e o assunto certo fica no telemóvel até ser lido.</li>
      <li><b>O sistema insiste, a pessoa não.</b> Três toques em sete dias, cada um diferente e cada um com uma oferta, sem ninguém ter de se lembrar.</li>
      <li><b>A receção só liga a quem respondeu.</b> Todos os dias recebe uma lista curta: nome, situação, o que a pessoa disse.</li>
      <li><b>Tudo fica registado.</b> Enviados, respostas, chamadas feitas, inscrições recuperadas. Em números, todas as semanas.</li>
    </ul>
  </div>
</div>
<h3 class="mt">Porquê WhatsApp, e não mais chamadas</h3>
<table class="tbl mini cmp">
  <thead><tr><th>Canal</th><th>O que acontece do lado da pessoa</th><th>Resposta</th></tr></thead>
  <tbody>
    <tr><td><b>Chamada</b></td><td>Número desconhecido a tocar. Interrompe. Se não atende, não fica nada.</td><td>só se atender</td></tr>
    <tr><td><b>SMS</b></td><td>Fica, mas sem nome do ginásio nem foto de perfil. Parece publicidade.</td><td>rara</td></tr>
    <tr><td><b>WhatsApp</b></td><td>Fica no telemóvel com o nome e o selo do ginásio. Lê-se quando dá jeito.</td><td>uma palavra chega</td></tr>
  </tbody>
</table>
<div class="callout"><b>A ideia numa frase:</b> a chamada passa a ser o último passo, não o primeiro. Quem chega à receção já disse “sim” ou “depois” por mensagem.</div>
''', 2))

# 3 — princípio + dia típico
pages.append(page("", h("02 · O princípio", "Ligar só a quem responde.") + f'''
<div class="grid3 rules">
  <div class="rule"><span class="num">1</span><h3>O primeiro contacto é automático</h3><p>Todos os dias às 09:00 o sistema lê a lista de contactos, percebe em que situação está cada pessoa e envia a mensagem certa. Ninguém carrega em nada.</p></div>
  <div class="rule"><span class="num">2</span><h3>Três toques, depois pára</h3><p>Dia 0, dia 3 e dia 7. Cada mensagem é diferente e mais curta que a anterior. Quem não responde em sete dias fica em pausa 30 dias. Sem perseguir.</p></div>
  <div class="rule"><span class="num">3</span><h3>A pessoa é o passo final</h3><p>A receção liga só a quem respondeu, com o contexto à frente. Uma chamada a quem disse “sim” vale mais do que cinquenta a quem não atende.</p></div>
</div>
<h3 class="mt">Um dia com o sistema a funcionar</h3>
<div class="timeline">
  <div class="tl"><span class="mono">09:00</span><p>O sistema lê a lista e classifica: <b>leads novos, aulas experimentais sem inscrição, membros sem visita há 14 dias, pagamentos em atraso, renovações</b>.</p></div>
  <div class="tl"><span class="mono">09:05</span><p>Saem as mensagens do dia, cada uma com o nome da pessoa e o motivo. Quem já respondeu antes não recebe repetidas.</p></div>
  <div class="tl"><span class="mono">ao longo do dia</span><p>As respostas entram e são interpretadas na hora: <b>sim</b> vai para a lista da receção, <b>depois</b> reagenda, <b>não</b> ou <b>PARA</b> sai da lista para sempre.</p></div>
  <div class="tl"><span class="mono">receção</span><p>Abre a lista do dia e liga. Vê o nome, a situação e a resposta exata. Marca o resultado com um toque: inscreveu, reagendou, não quer.</p></div>
  <div class="tl"><span class="mono">2.ª feira</span><p>Chega o painel da semana: mensagens enviadas, taxa de resposta, chamadas feitas, membros recuperados e leads inscritos.</p></div>
</div>
<div class="note alt"><b>Duas formas de arrancar, à escolha do dono.</b> <b>Variante A:</b> a receção continua a ligar primeiro e o sistema recupera por WhatsApp quem não atendeu, para a segunda chamada já ser quente. <b>Variante B:</b> a mensagem vai primeiro e a receção liga só a quem respondeu. A lógica e as mensagens são as mesmas; muda a ordem. Comparação com números no documento-resumo.</div>
''', 3))

# 4 — diagrama
pages.append(page("diagram", h("03 · O esquema", "Como o fluxo corre, passo a passo.", "Desenho do fluxo tal como fica montado no motor de fluxo da Pacheco Studios. Cada caixa é um passo automático; as caixas verdes são os únicos momentos em que uma pessoa entra.") + f'<div class="dg">{diagram()}</div>', 4))

# 5 — os 5 fluxos
flows = [
    ("Lead novo", "Pediu informação pelo site, Instagram, telefone ou à porta e ainda não se inscreveu.", "Marcar visita ou aula experimental", "Dia 0: “obrigado pelo interesse, quando queres vir conhecer?” · Dia 3: horários com vaga · Dia 7: última mensagem com convite direto"),
    ("Aula experimental", "Veio experimentar e saiu sem inscrição.", "Fechar a inscrição", "Dia 0: “como correu?” · Dia 3: o que está incluído no plano · Dia 7: convite para decidir, com data limite"),
    ("Inativo 14 dias", "Membro ativo sem entrada registada há 14 dias.", "Trazer de volta antes de cancelar", "Dia 0: “sentimos a tua falta” · Dia 3: sugestão concreta (horário, treino) · Dia 7: pergunta direta: “há alguma coisa que possamos resolver?”"),
    ("Pagamento em atraso", "Mensalidade por regularizar.", "Regularizar sem constrangimento", "Dia 0: aviso simples com forma de pagar · Dia 3: lembrete · Dia 7: chamada da receção (aqui a pessoa liga sempre)"),
    ("Renovação", "Fim de fidelização ou de plano a aproximar-se.", "Renovar antes de expirar", "Dia −14: “o teu plano termina em duas semanas” · Dia −7: opções · Dia −1: última chamada da receção"),
]
rows = "".join(f'<tr><td><span class="chip">{esc(a)}</span></td><td>{esc(b)}</td><td>{esc(c)}</td><td class="small">{esc(d)}</td></tr>' for a, b, c, d in flows)
pages.append(page("", h("04 · As cinco situações", "Uma sequência diferente para cada motivo de contacto.", "O sistema não manda a mesma mensagem a toda a gente. Cada situação tem o seu objetivo, o seu tom e o seu ritmo.") + f'''
<table class="tbl">
  <thead><tr><th>Situação</th><th>Quem entra</th><th>Objetivo</th><th>Os três toques</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<div class="note"><b>De onde vêm os dados.</b> As situações “inativo”, “pagamento” e “renovação” dependem de o software de gestão do ginásio exportar entradas, pagamentos e datas de plano. <b>A confirmar na primeira reunião</b> qual é o software e o que exporta. Se não exportar, arranca-se com leads e aulas experimentais, que vivem numa folha simples preenchida pela receção.</div>
<div class="note alt"><b>Arranque recomendado.</b> Um fluxo primeiro, o dos <b>membros inativos</b>: é o que tem mais dinheiro em cima da mesa (cada membro recuperado é uma mensalidade que não se perde) e o mais fácil de medir.</div>
''', 5))

# 6 — mensagens
def bubble(text, when):
    return f'<div class="bub"><p>{text}</p><span class="mono">{esc(when)}</span></div>'
pages.append(page("", h("05 · As mensagens", "Curtas, com nome, com a voz do Be Legend.", "Exemplos para o fluxo de membros inativos. Todas as mensagens são aprovadas pelo ginásio antes de entrarem no sistema e registadas na Meta como modelos oficiais.") + f'''
<div class="cols2 wa">
  <div class="phone">
    <div class="phone-top"><span class="avatar">BL</span><div><b>Be Legend Olhão</b><span>conta verificada</span></div></div>
    {bubble("Olá João, é o Be Legend Olhão. Já não te vemos há duas semanas e sentimos a tua falta no ferro. Está tudo bem? Responde só “sim” e a Rita liga-te para combinar o regresso.", "dia 0 · 09:05")}
    {bubble("João, passo rápido: esta semana temos vaga às 18h30 e às 20h. Queres que te guardemos o horário?", "dia 3 · 09:05")}
    {bubble("Última mensagem, prometemos. Se houver alguma coisa que possamos resolver, diz-nos. Se preferires não receber mais mensagens, responde PARA.", "dia 7 · 09:05")}
    <div class="bub me"><p>sim</p><span class="mono">dia 3 · 13:42</span></div>
    <div class="sys">→ João entra na lista da receção de hoje: “inativo 14 dias · respondeu sim · dia 3”</div>
  </div>
  <div>
    <h3>Regras das mensagens</h3>
    <ul class="ul">
      <li><b>Nome próprio e motivo</b> logo na primeira linha. Nunca “Olá cliente”.</li>
      <li><b>Uma pergunta só</b>, com resposta de uma palavra. “Sim” é suficiente para desencadear a chamada.</li>
      <li><b>Assinada por uma pessoa real</b> da receção. Quem responde sabe com quem vai falar.</li>
      <li><b>Sem promoções agressivas.</b> O tom é o do ginásio: direto, próximo, sem enchimento.</li>
      <li><b>Saída sempre visível.</b> Responder PARA remove a pessoa de todos os fluxos, de imediato e para sempre.</li>
      <li><b>Horário decente.</b> Nada sai antes das 09:00 nem depois das 20:00, nem ao domingo.</li>
    </ul>
    <div class="note"><b>Nomes e horários deste exemplo são fictícios.</b> O texto final é escrito com a equipa do ginásio, na voz da casa.</div>
    <div class="note alt"><b>Cada toque pode levar uma oferta.</b> O ginásio já tem o que é preciso para abrir portas: batidos de proteína, águas, massagista, personal trainer. Três ofertas ativas de cada vez, uma por situação, renovadas de 3 em 3 meses para as mensagens nunca ficarem gastas. As combinações definem-se convosco; o sistema mede qual converte melhor.</div>
  </div>
</div>
''', 6))

# 7 — o que a receção vê
sample = [
    ("Exemplo A.", "Inativo 14 dias", "sim", "dia 3", "ligar hoje"),
    ("Exemplo B.", "Aula experimental", "depois", "dia 0", "toque reagendado · 5.ª feira"),
    ("Exemplo C.", "Lead novo", "sim", "dia 0", "ligar hoje"),
    ("Exemplo D.", "Pagamento em atraso", "—", "dia 7", "ligar hoje (fim da sequência)"),
    ("Exemplo E.", "Renovação", "sim", "dia −7", "ligar hoje"),
    ("Exemplo F.", "Inativo 14 dias", "PARA", "dia 3", "removido · sem ação"),
]
trs = "".join(f'<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td><span class="ans {c.lower().replace(" ","")}">{esc(c)}</span></td><td class="mono">{esc(d)}</td><td>{esc(e)}</td><td><span class="btns"><i>✓</i><i>↻</i><i>✕</i></span></td></tr>' for a, b, c, d, e in sample)
pages.append(page("", h("06 · O que a receção vê", "Uma lista por dia. Só quem vale a chamada.", "Em vez de 100 números para marcar, a receção abre uma lista curta, já ordenada, com o motivo e a resposta de cada pessoa. Marca o resultado com um toque. Nada de aprender software novo: pode viver numa folha partilhada ou num painel simples no telemóvel.") + f'''
<div class="panel">
  <div class="panel-top"><b>Lista de hoje · 2.ª feira</b><span class="mono">6 contactos · 4 chamadas a fazer</span></div>
  <table class="tbl compact">
    <thead><tr><th>Nome</th><th>Situação</th><th>Respondeu</th><th>Toque</th><th>Ação</th><th>Resultado</th></tr></thead>
    <tbody>{trs}</tbody>
  </table>
</div>
<div class="grid3 kpi">
  <div class="tile sm"><b>enviadas</b><span>quantas mensagens saíram esta semana, por situação</span></div>
  <div class="tile sm"><b>taxa de resposta</b><span>quantos responderam, e em que toque</span></div>
  <div class="tile sm"><b>recuperados</b><span>membros que voltaram e leads que se inscreveram</span></div>
</div>
<p class="fine">Nomes de exemplo. O painel real mostra os contactos do ginásio e nunca sai da conta do ginásio.</p>
''', 7))

# 8 — tecnologia, custos, RGPD
pages.append(page("", h("07 · Tecnologia e custos de funcionamento", "Peças conhecidas, sem nada por inventar.") + f'''
<table class="tbl stack">
  <thead><tr><th>Peça</th><th>O que faz</th><th>Porquê esta</th></tr></thead>
  <tbody>
    <tr><td><b>Motor de fluxo</b><br><span class="small">construído e gerido pela Pacheco Studios</span></td><td>Corre o esquema da página 4: lê contactos, decide, envia, espera, interpreta, regista.</td><td>Custo fixo por mês, não cresce com o número de contactos. Alojado na Europa, em servidores nossos. O ginásio não tem de instalar nem gerir nada.</td></tr>
    <tr><td><b>WhatsApp Business API</b><br><span class="small">canal oficial da Meta</span></td><td>Envia as mensagens a partir do número do ginásio, com selo de conta verificada.</td><td>É a via legal e estável. Sem apps de terceiros nem números pessoais, que a Meta bloqueia.</td></tr>
    <tr><td><b>Software do ginásio</b><br><span class="small">a confirmar</span></td><td>Origem das entradas, pagamentos e datas de plano.</td><td>Liga-se por exportação ou API. Se não exportar, uma folha partilhada faz o papel para os leads e aulas experimentais.</td></tr>
    <tr><td><b>Folha / painel</b><br><span class="small">Google Sheets ou Notion</span></td><td>A lista do dia da receção e o painel semanal.</td><td>Não obriga a aprender nada. Abre no telemóvel.</td></tr>
  </tbody>
</table>
<div class="cols2">
  <div>
    <h3>Custos de funcionamento</h3>
    <table class="tbl mini">
      <tr><td>Motor de fluxo (servidor, alojado na UE)</td><td class="r">incluído na mensalidade</td></tr>
      <tr><td>WhatsApp (Meta cobra por conversa)</td><td class="r">cêntimos por conversa; a orçamentar com o volume real</td></tr>
      <tr><td>Folha / painel</td><td class="r">incluído</td></tr>
    </table>
    <p class="fine">O servidor, a vigilância e a reparação prioritária estão dentro da mensalidade. Só as mensagens WhatsApp são pagas à Meta ao custo, em nome do ginásio; o valor por conversa confirma-se na tabela oficial antes de arrancar.</p>
  </div>
  <div>
    <h3>Dados e RGPD</h3>
    <ul class="ul">
      <li>Só recebem mensagens contactos que <b>deram o número ao ginásio</b> (inscrição, pedido de informação, aula experimental).</li>
      <li><b>PARA</b> em qualquer resposta remove a pessoa de imediato. A lista de exclusões é permanente.</li>
      <li>Os dados ficam em <b>servidores na União Europeia</b>, nas contas do ginásio. A Pacheco Studios não guarda cópias.</li>
      <li>Registo de cada envio e resposta, para poder mostrar a qualquer pessoa o que lhe foi enviado e quando.</li>
    </ul>
  </div>
</div>
<div class="note alt"><b>O motor de fluxo é trabalho nosso.</b> É montado, alojado e vigiado pela Pacheco Studios; o ginásio só vê o resultado: a lista da receção e o painel. Com {esc(C["chamadas_dia"])} contactos por dia, o custo não muda: é o mesmo com 50 ou com 500.</div>
''', 8))

# 9 — investimento e próximos passos
pages.append(page("", h("08 · Investimento e próximos passos", "Todos os Legends, a arrancar em Olhão.", "Monta-se uma vez, replica-se por ginásio: cada casa com o seu número, lista e painel, a mesma lógica. Faro e Lisboa entram depois do piloto de Olhão, sem nova montagem.") + f'''
<div class="cols2 price">
  <div class="pbox">
    <span class="mono">montagem · pagamento único</span>
    <b>{esc(C["setup"])} <small>{esc(C["setup_nota"])}</small></b>
    <ul class="ul tight">
      <li>Desenho e construção dos 5 fluxos no motor de fluxo, preparados para os três ginásios</li>
      <li>Escrita das mensagens com a equipa e registo dos modelos na Meta</li>
      <li>Ligação ao software do ginásio ou folha de contactos</li>
      <li>Lista da receção e painel semanal</li>
      <li>Formação das receções e piloto de 30 dias acompanhado</li>
    </ul>
  </div>
  <div class="pbox">
    <span class="mono">por mês · Olhão, Faro e Lisboa</span>
    <b>{esc(C["mensal"])} <small>{esc(C["mensal_nota"])}</small></b>
    <ul class="ul tight">
      <li>Um só valor para os três ginásios</li>
      <li>Todos os servidores a funcionar, vigiados 24/7, com reparação prioritária</li>
      <li>Ajustes sem limite e suporte direto por WhatsApp</li>
      <li>Relatório mensal por ginásio com os números e o que mudar</li>
      <li>Mensagens WhatsApp à parte, ao custo da Meta</li>
    </ul>
  </div>
</div>
<h3 class="mt">Como arrancamos</h3>
<ol class="ol">
  <li><b>Reunião de 30 minutos</b> com o dono e a receção: confirmar o software, a voz das mensagens, o número de WhatsApp e a exportação de contactos.</li>
  <li><b>Aprovação das mensagens</b> pelo ginásio. Nada sai sem ser lido pela casa.</li>
  <li><b>Arranque com um fluxo</b>, o dos membros inativos, em modo piloto de {esc(C["piloto_dias"])} dias.</li>
  <li><b>Revisão aos {esc(C["piloto_dias"])} dias</b> com o número que interessa: quantos membros voltaram e quantas chamadas a receção deixou de fazer. Só depois se ligam os outros quatro fluxos.</li>
</ol>
<h3 class="mt">Perguntas que costumam surgir</h3>
<div class="faq">
  <div><b>E quem não tem WhatsApp?</b><p>Fica na lista de chamadas como hoje. O sistema marca-o para a receção não perder tempo a perceber porque não respondeu.</p></div>
  <div><b>Isto não parece spam?</b><p>Não: sai do número verificado do ginásio, com modelos aprovados pela Meta, com nome próprio, e com saída num só toque. Três mensagens em sete dias, depois silêncio.</p></div>
  <div><b>Quem escreve as mensagens?</b><p>Nós, com a equipa do ginásio. Nada entra no sistema sem ser lido e aprovado pela casa.</p></div>
  <div><b>E se o software do ginásio não exportar dados?</b><p>Arranca-se com leads e aulas experimentais numa folha simples que a receção já preenche. Os fluxos de inativos e pagamentos entram quando houver exportação.</p></div>
</div>
<div class="callout final">
  <div><b>{esc(C["marca"])}</b><br><span>Web design e sistemas para negócios locais · Algarve</span><br><span class="pres">Assistência presencial: um subdiretor da Pacheco Studios desloca-se ao ginásio sempre que for necessário.</span></div>
  <div class="r"><span class="mono">{esc(C["email"])}</span></div>
</div>
''', 9))

CSS = f"""
{FONTS}
:root{{--navy:{NAVY};--gold:{GOLD};--paper:{PAPER};--ink:{INK};--muted:{MUTED};--teal:{TEAL};--line:{LINE};}}
*{{box-sizing:border-box;margin:0;padding:0}}
@page{{size:A4;margin:0}}
html,body{{background:#fff;color:var(--ink);font-family:Inter,system-ui,sans-serif;font-size:11pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;height:297mm;padding:16mm 16mm 14mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}}
.page:last-child{{page-break-after:auto}}
.ft{{position:absolute;left:16mm;right:16mm;bottom:9mm;display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:7.5pt;color:var(--muted);border-top:1px solid #E6E1D6;padding-top:6px}}
.kicker{{font-family:'JetBrains Mono',monospace;font-size:8.5pt;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:6px}}
h2{{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:30pt;line-height:1;color:var(--navy);margin-bottom:8px;letter-spacing:-.005em}}
h3{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:15.5pt;color:var(--navy);margin-bottom:6px;line-height:1.1}}
.lead{{font-size:11pt;color:#3A3F4B;max-width:150mm;margin-bottom:12px}}
.mono{{font-family:'JetBrains Mono',monospace;font-size:8.5pt;color:var(--muted)}}
.mt{{margin-top:14px}}
.small{{font-size:9pt;color:var(--muted)}}
.fine{{font-size:8.5pt;color:var(--muted);margin-top:8px}}
.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0}}
.tile{{background:var(--paper);border-radius:10px;padding:18px 16px 16px;border:1px solid #EAE5DA}}
.tile b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:26pt;line-height:1;color:var(--navy);margin-bottom:6px}}
.tile span{{display:block;font-size:9.5pt;color:#3A3F4B}}
.tile em{{display:block;font-style:normal;font-family:'JetBrains Mono',monospace;font-size:7.5pt;color:var(--muted);margin-top:5px}}
.tile.sm b{{font-size:15pt;color:var(--teal)}}
.cols2{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:8px}}
.ul{{list-style:none}}
.ul li{{position:relative;padding-left:16px;margin-bottom:8px;font-size:10.4pt}}
.ul li::before{{content:"";position:absolute;left:0;top:7px;width:7px;height:7px;border-radius:2px;background:var(--gold)}}
.ul.ok li::before{{background:var(--teal)}}
.ul.tight li{{margin-bottom:4px;font-size:9.5pt}}
.callout{{margin-top:14px;background:var(--navy);color:#fff;border-radius:10px;padding:14px 16px;font-size:10.5pt}}
.callout b{{color:var(--gold)}}
.rules .rule{{background:var(--paper);border-radius:10px;padding:18px 16px;border:1px solid #EAE5DA}}
.rule .num{{display:inline-block;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:22pt;color:var(--gold);line-height:1;margin-bottom:6px}}
.rule p{{font-size:10.2pt;color:#3A3F4B}}
.timeline{{border-left:2px solid var(--gold);margin-left:6px;padding-left:16px;margin-top:6px}}
.tl{{position:relative;margin-bottom:14px}}
.tl::before{{content:"";position:absolute;left:-21.5px;top:5px;width:9px;height:9px;border-radius:50%;background:#fff;border:2px solid var(--gold)}}
.tl .mono{{display:block;color:var(--navy);margin-bottom:1px}}
.tl p{{font-size:10.4pt;color:#3A3F4B}}
.diagram .lead{{margin-bottom:6px}}
.dg{{width:100%;height:222mm}}
.dg svg{{width:100%;height:100%;border-radius:12px;border:1px solid #EAE5DA}}
.tbl{{width:100%;border-collapse:collapse;font-size:9.8pt;margin-top:4px}}
.tbl th{{text-align:left;font-family:'JetBrains Mono',monospace;font-weight:500;font-size:7.8pt;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:6px 8px;border-bottom:1.5px solid var(--navy)}}
.tbl td{{padding:8px 8px;border-bottom:1px solid #E6E1D6;vertical-align:top}}
.tbl td.r{{text-align:right;white-space:nowrap}}
.tbl.mini td{{padding:6px 4px;font-size:9.4pt}}
.tbl.mini td.r{{white-space:normal;text-align:right;max-width:38mm}}
.tbl.compact td{{padding:7px 8px}}
.tbl.stack td{{font-size:9.3pt}}
.chip{{display:inline-block;background:var(--navy);color:#fff;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:10.5pt;padding:3px 10px;border-radius:20px;white-space:nowrap;letter-spacing:.02em}}
.note{{margin-top:10px;background:var(--paper);border-left:3px solid var(--gold);border-radius:6px;padding:10px 12px;font-size:9.5pt;color:#3A3F4B}}
.note.alt{{border-left-color:var(--teal)}}
.wa .phone{{background:#EFEAE2;border-radius:16px;padding:12px;border:1px solid #E1DACB}}
.phone-top{{display:flex;align-items:center;gap:10px;padding:2px 4px 10px;border-bottom:1px solid #DDD5C4;margin-bottom:10px}}
.phone-top b{{display:block;font-size:10pt;color:var(--navy)}}
.phone-top span{{font-size:8pt;color:var(--muted)}}
.avatar{{width:32px;height:32px;border-radius:50%;background:var(--navy);color:var(--gold);font-family:'Barlow Condensed',sans-serif;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:12pt}}
.bub{{background:#fff;border-radius:10px;border-top-left-radius:2px;padding:8px 10px 6px;margin:0 30px 8px 0;box-shadow:0 1px 0 rgba(0,0,0,.05)}}
.bub p{{font-size:10pt;color:#1F2430;margin-bottom:3px}}
.bub .mono{{display:block;text-align:right;font-size:7.5pt}}
.bub.me{{background:#D9F2E3;margin:0 0 8px 120px;border-top-left-radius:10px;border-top-right-radius:2px}}
.sys{{font-family:'JetBrains Mono',monospace;font-size:7.8pt;color:var(--teal);background:#fff;border:1px dashed var(--teal);border-radius:6px;padding:6px 8px}}
.panel{{border:1px solid #E6E1D6;border-radius:12px;overflow:hidden;margin-top:6px}}
.panel-top{{display:flex;justify-content:space-between;align-items:center;background:var(--navy);color:#fff;padding:9px 12px;font-size:10pt}}
.panel-top .mono{{color:var(--gold)}}
.panel .tbl{{margin:0}}
.panel .tbl th{{background:var(--paper)}}
.ans{{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:8.5pt;padding:2px 8px;border-radius:12px;background:#EEF0F4;color:var(--navy)}}
.ans.sim{{background:#D9F2E3;color:#155E45}}
.ans.depois{{background:#FBF3E1;color:#7A5A12}}
.ans.para{{background:#F7E0E0;color:#8A2B2B}}
.btns i{{display:inline-block;width:20px;height:20px;border-radius:6px;border:1px solid #D6D0C2;font-style:normal;text-align:center;line-height:18px;font-size:9pt;color:var(--muted);margin-right:3px}}
.kpi{{margin-top:12px}}
.price .pbox{{background:var(--paper);border:1px solid #EAE5DA;border-radius:12px;padding:14px 18px}}
.pbox b small{{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:9pt;color:var(--muted);margin-left:4px;letter-spacing:0}}
.pbox b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:32pt;line-height:1;color:var(--navy);margin:4px 0 8px}}
.ol{{padding-left:0;list-style:none;counter-reset:n}}
.ol li{{counter-increment:n;position:relative;padding-left:30px;margin-bottom:9px;font-size:10.4pt}}
.ol li::before{{content:counter(n);position:absolute;left:0;top:0;width:22px;height:22px;border-radius:50%;background:var(--navy);color:var(--gold);font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:12pt;text-align:center;line-height:22px}}
.callout.final{{display:flex;justify-content:space-between;align-items:center;margin-top:18px}}
.callout.final span{{color:#C9CFDA;font-size:9.5pt}}
.callout.final .pres{{color:#fff;display:inline-block;margin-top:4px}}
.callout.final .mono{{color:var(--gold);font-size:9.5pt}}
.tbl.cmp td{{padding:8px 6px;font-size:9.8pt}}
.tbl.cmp td:last-child{{white-space:nowrap;color:var(--teal);font-family:'JetBrains Mono',monospace;font-size:9pt}}
.faq{{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;margin-top:2px}}
.faq b{{display:block;font-size:10.4pt;color:var(--navy);margin-bottom:2px}}
.faq p{{font-size:9.5pt;color:#3A3F4B;line-height:1.4}}
.callout.final{{margin-top:12px;padding:11px 16px}}
/* capa */
.cover{{background:var(--navy);color:#fff;padding:18mm 18mm 16mm;display:flex;flex-direction:column}}
.cover-top{{display:flex;justify-content:space-between;align-items:baseline}}
.brand{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13pt;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}}
.cover .mono{{color:#B8BFCC}}
.cover-mid{{margin-top:auto}}
.cover-kicker{{font-family:'JetBrains Mono',monospace;font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:14px}}
h1{{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:66pt;line-height:.92;letter-spacing:-.01em;color:#fff}}
.cover-client{{font-family:'Barlow Condensed',sans-serif;font-weight:600;font-size:22pt;color:var(--gold);margin-top:16px}}
.cover-sub{{font-size:11.5pt;color:#C9CFDA;max-width:130mm;margin-top:12px;line-height:1.5}}
.cover-bot{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:auto;padding-top:26px}}
.cover-stat b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:40pt;line-height:1;color:#fff}}
.cover-stat span{{font-size:9.5pt;color:#B8BFCC}}
.cover-rule{{height:2px;background:var(--gold);margin:20px 0 10px}}
.cover-foot{{font-family:'JetBrains Mono',monospace;font-size:8pt;color:#8F97A8}}
"""

if __name__ == "__main__":
  doc = f"""<!DOCTYPE html>
<html lang="pt-PT"><head><meta charset="utf-8"><title>Follow-up &amp; Recuperação de Clientes · {esc(C["cliente"])} {esc(C["local"])}</title>
<style>{CSS}</style></head><body>{''.join(pages)}</body></html>"""
  (HERE / "proposta.html").write_text(doc, encoding="utf-8")
  print("proposta.html", len(doc) // 1024, "KB")
