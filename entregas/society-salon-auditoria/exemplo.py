# Exemplo do PDF final da auditoria (o que o dono recebe), com números FICTÍCIOS
# baseados na estrutura real do Society Salon (5 barbeiros, MERO, 80–120 lei).
# Gera exemplo-ro.html/.pdf (para o dono) e exemplo-pt.html/.pdf (para o Tomás).
# Uso: python3 exemplo.py
import html, pathlib

AQUI = pathlib.Path(__file__).parent
FONTES = (AQUI / "../../marca/fontes").resolve()

# ---------- o cenário (tudo fictício, plausível para uma barbearia de 5 cadeiras) ----------
PRECO = 95            # lei, preço médio de um serviço
SEMANAS = 50          # semanas de trabalho por ano
HORA = 50             # lei, custo de 1 hora de quem atende mensagens

A_faltas_sem = 12                                  # faltas + cancelamentos tardios por semana
A_perda = A_faltas_sem * PRECO * SEMANAS           # 57 000
A_recupera = 0.5
A_ganho = round(A_perda * A_recupera)              # 28 500

B_novos_mes, B_hoje, B_alvo = 40, 0.45, 0.60
B_extra_mes = round(B_novos_mes * (B_alvo - B_hoje))   # 6 clientes fixos a mais por mês
B_visitas = 9                                          # visitas por ano de um cliente fixo
B_ganho = round(B_extra_mes * 12 * B_visitas * PRECO * 0.5)  # 1.º ano: metade do efeito → 30 780

C_horas_sem, C_auto = 9, 0.7
C_tempo = round(C_horas_sem * C_auto * SEMANAS * HORA)      # 15 750
C_perdidos_sem, C_conv = 5, 0.5
C_receita = round(C_perdidos_sem * C_conv * PRECO * SEMANAS)  # 11 875
C_ganho = C_tempo + C_receita                                 # 27 625

TOTAL = A_ganho + B_ganho + C_ganho
SETUP, MENSAL = 1250, 250          # lei por sistema (exemplo, alinhado com a tabela da secção 2 do PLAYBOOK)
INVEST = 3 * SETUP + 3 * MENSAL * 12
ROI = round((TOTAL - INVEST) / INVEST * 100)
RETORNO_MESES = round(INVEST / (TOTAL / 12), 1)

def lei(n): return f"{n:,.0f}".replace(",", ".") + " lei"
def num(n): return f"{n:,.0f}".replace(",", ".")

T = {
 "ro": dict(
  lang="ro", titulo="Society Salon — audit AI (exemplu)",
  faixa="EXEMPLU · cifre ilustrative, nu sunt datele salonului",
  kicker="Audit AI · rezultate", sub="Ce primești la o săptămână după discuție",
  total_rot="Cât poate valora pe an", total_nota="în primul an, cu cele 3 câștiguri rapide",
  p_cerut="Ce ne-ai cerut", obj="Mai multe programări și clienți care revin, fără ore de muncă în plus.",
  feito=[("45 min", "discuție cu proprietarul"), ("5 × 10 min", "cu fiecare frizer"), ("3 luni", "de programări din MERO"), ("12", "pași analizați")],
  p_mapa="Harta salonului", mapa_lead="Cum funcționează azi, de la primul mesaj până la următoarea vizită.",
  mot=[("Atragere", "cum vine un client nou",
        [("Găsește salonul pe Google, Instagram sau MERO", ""), ("Întreabă de preț sau de un loc pe mesaj", "t"), ("Răspunsul vine după ore, seara deloc", "r")]),
       ("Servire", "de la programare la casă",
        [("Programare în MERO sau la telefon", ""), ("Programările de la telefon trecute de mână", "t"), ("Neprezentări fără înlocuitor", "r"), ("Casa și comisioanele calculate seara", "t")]),
       ("Revenire", "după tunsoare",
        [("Clientul pleacă fără următoarea programare", "r"), ("Nimeni nu observă cine n-a mai venit", "r"), ("Recenzie pe Google doar dacă își amintește", "t")])],
  leg_t="timp pierdut", leg_r="bani sau clienți pierduți",
  p_matriz="Ce merită făcut mai întâi", eixo_y="valoare pentru salon", eixo_x="dificultate",
  q=[("Câștiguri rapide", "începem aici", ["Neprezentări", "Clienți care revin", "Răspuns la mesaje"]),
     ("Pariuri mari", "faza 2", ["Society Membership (abonament lunar)", "Site nou cu programare în RO + EN"]),
     ("Extra", "mai târziu", ["Comisioane calculate automat", "Calendar de postări Instagram"]),
     ("De evitat", "", ["Aplicație proprie a salonului", "Robot care răspunde la telefon"])],
  qw=[
   dict(id="1", nome="Neprezentări", dor=f"{A_faltas_sem} programări pe săptămână se pierd: neprezentări și anulări în ultimul moment. Scaunul rămâne gol.",
        antes=["Clientul uită și nu vine", "Locul rămâne liber", "Nimeni de pe lista de așteptare nu află"],
        depois=["Confirmare cu o zi înainte, cu răspuns DA / ANULEZ", "Dacă anulează, locul pleacă singur la lista de așteptare", "Frizerul vede scaunul ocupat din nou"],
        conta=[(f"{A_faltas_sem} pe săpt. × {PRECO} lei × {SEMANAS} săpt.", lei(A_perda), "pierdut azi pe an"),
               (f"recuperăm {int(A_recupera*100)} %", lei(A_ganho), "câștig pe an")]),
   dict(id="2", nome="Clienți care revin", dor=f"Din {B_novos_mes} clienți noi pe lună, doar {int(B_hoje*100)} % mai revin. Restul pleacă fără să-i întrebe nimeni.",
        antes=["Tunsoarea ține 3–4 săptămâni", "Nimeni nu-i amintește clientului", "Recenzia pe Google depinde de noroc"],
        depois=["În ziua 25: «E timpul pentru tunsoare», cu linkul MERO și frizerul lui", "La 6 săptămâni fără vizită: un mesaj de revenire", "După fiecare tunsoare: link direct pentru recenzie pe Google"],
        conta=[(f"{int(B_hoje*100)} % → {int(B_alvo*100)} % din {B_novos_mes} pe lună", f"+{B_extra_mes} clienți", "ficși în plus pe lună"),
               (f"× {B_visitas} vizite × {PRECO} lei, jumătate în primul an", lei(B_ganho), "câștig în primul an")],
        extra="Recenziile Google în plus nu intră în calcul. Sunt un bonus."),
   dict(id="3", nome="Răspuns la mesaje", dor=f"Echipa pierde {C_horas_sem} ore pe săptămână răspunzând la aceleași întrebări. Seara și duminica nu răspunde nimeni.",
        antes=["Preț, loc liber, unde e ușa: mereu aceleași întrebări", "Frizerul răspunde între doi clienți", "Cererile de seară se pierd"],
        depois=["Asistentul răspunde imediat, în română și engleză, și spune că e asistent", "Trimite linkul MERO cu serviciul ales", "Ce nu știe ajunge la un om din echipă"],
        conta=[(f"{C_horas_sem} h × {int(C_auto*100)} % × {SEMANAS} săpt. × {HORA} lei", lei(C_tempo), "timp eliberat pe an"),
               (f"{C_perdidos_sem} cereri pierdute pe săpt. × {int(C_conv*100)} % × {PRECO} lei × {SEMANAS}", lei(C_receita), "încasări recuperate"),
               ("total", lei(C_ganho), "câștig pe an")]),
  ],
  antes_rot="Azi", depois_rot="Cu sistemul",
  p_dinheiro="Cât valorează totul", col=["Câștig rapid", "Pe an"],
  invest_rot="Investiție (exemplu)", invest_txt=f"3 sisteme × {lei(SETUP)} instalare + {lei(MENSAL)}/lună",
  roi_rot="Rentabilitate în primul an", ret_rot="Se plătește în", ret_un="luni",
  p_plano="Planul pe 90 de zile",
  plano=[("Zilele 1–30", "Neprezentări", "Ziua 0: măsurăm câte neprezentări sunt acum. Pornim confirmările și lista de așteptare."),
         ("Zilele 31–60", "Clienți care revin", "Mesajul din ziua 25, revenirea la 6 săptămâni și linkul pentru recenzii."),
         ("Zilele 61–90", "Răspuns la mesaje", "Tu aprobi răspunsurile. Asistentul pornește și predă omului tot ce iese din rutină.")],
  medir_rot="Ce măsurăm în fiecare lună", medir=["neprezentări pe săptămână", "% clienți noi care revin", "timp de răspuns la mesaje", "recenzii noi pe Google"],
  tu_rot="Ce decizi tu", tu=["aprobi fiecare text înainte să plece", "poți opri orice sistem cu un singur mesaj", "totul rulează în conturile tale (MERO, WhatsApp, Google)"],
  prox="Următorul pas: alegem împreună cu ce câștig rapid începem.",
  rodape="Pacheco Studios · pachecost.com",
 ),
 "pt": dict(
  lang="pt-PT", titulo="Society Salon — auditoria de IA (exemplo)",
  faixa="EXEMPLO · números ilustrativos, não são os dados do salão",
  kicker="Auditoria de IA · resultados", sub="O que recebes uma semana depois da conversa",
  total_rot="Quanto pode valer por ano", total_nota="no 1.º ano, com as 3 vitórias rápidas",
  p_cerut="O que nos pediste", obj="Mais marcações e clientes que voltam, sem mais horas de trabalho.",
  feito=[("45 min", "conversa com o dono"), ("5 × 10 min", "com cada barbeiro"), ("3 meses", "de marcações do MERO"), ("12", "passos analisados")],
  p_mapa="O mapa do salão", mapa_lead="Como funciona hoje, da primeira mensagem à visita seguinte.",
  mot=[("Aquisição", "como chega um cliente novo",
        [("Encontra o salão no Google, Instagram ou MERO", ""), ("Pergunta preço ou vaga por mensagem", "t"), ("A resposta vem horas depois; à noite, nunca", "r")]),
       ("Entrega", "da marcação à caixa",
        [("Marcação no MERO ou por telefone", ""), ("As do telefone passadas à mão", "t"), ("Faltas sem ninguém para o lugar", "r"), ("Caixa e comissões feitas à noite", "t")]),
       ("Retorno", "depois do corte",
        [("O cliente sai sem a próxima marcação", "r"), ("Ninguém nota quem deixou de vir", "r"), ("Avaliação no Google só se se lembrar", "t")])],
  leg_t="tempo perdido", leg_r="dinheiro ou clientes perdidos",
  p_matriz="O que vale a pena fazer primeiro", eixo_y="valor para o salão", eixo_x="dificuldade",
  q=[("Vitórias rápidas", "começar aqui", ["Faltas", "Clientes que voltam", "Resposta a mensagens"]),
     ("Grandes apostas", "fase 2", ["Society Membership (assinatura mensal)", "Site novo com marcação em RO + EN"]),
     ("Extras", "mais tarde", ["Comissões calculadas sozinhas", "Calendário de publicações no Instagram"]),
     ("Evitar", "", ["App própria do salão", "Robô que atende o telefone"])],
  qw=[
   dict(id="1", nome="Faltas", dor=f"Perdem-se {A_faltas_sem} marcações por semana entre faltas e cancelamentos à última hora. A cadeira fica vazia.",
        antes=["O cliente esquece-se e não vem", "O lugar fica vazio", "Ninguém na lista de espera sabe"],
        depois=["Confirmação na véspera, com resposta SIM / CANCELO", "Se cancelar, o lugar vai sozinho para a lista de espera", "O barbeiro volta a ter a cadeira ocupada"],
        conta=[(f"{A_faltas_sem} por sem. × {PRECO} lei × {SEMANAS} sem.", lei(A_perda), "perdido hoje por ano"),
               (f"recuperar {int(A_recupera*100)} %", lei(A_ganho), "ganho por ano")]),
   dict(id="2", nome="Clientes que voltam", dor=f"Dos {B_novos_mes} clientes novos por mês, só {int(B_hoje*100)} % voltam. Os outros vão-se sem ninguém perguntar.",
        antes=["Um corte dura 3–4 semanas", "Ninguém lembra o cliente", "A avaliação no Google depende da sorte"],
        depois=["Ao dia 25: «Está na hora do corte», com o link do MERO e o barbeiro dele", "6 semanas sem vir: uma mensagem de regresso", "Depois de cada corte: link direto para avaliar no Google"],
        conta=[(f"{int(B_hoje*100)} % → {int(B_alvo*100)} % de {B_novos_mes} por mês", f"+{B_extra_mes} clientes", "fixos a mais por mês"),
               (f"× {B_visitas} visitas × {PRECO} lei, metade no 1.º ano", lei(B_ganho), "ganho no 1.º ano")],
        extra="As avaliações a mais no Google não entram na conta. São um bónus."),
   dict(id="3", nome="Resposta a mensagens", dor=f"A equipa gasta {C_horas_sem} horas por semana a responder às mesmas perguntas. À noite e ao domingo ninguém responde.",
        antes=["Preço, vaga, onde fica a porta: sempre as mesmas perguntas", "O barbeiro responde entre dois clientes", "Os pedidos da noite perdem-se"],
        depois=["O assistente responde logo, em romeno e inglês, e diz que é assistente", "Envia o link do MERO com o serviço escolhido", "O que não sabe passa para uma pessoa da equipa"],
        conta=[(f"{C_horas_sem} h × {int(C_auto*100)} % × {SEMANAS} sem. × {HORA} lei", lei(C_tempo), "tempo libertado por ano"),
               (f"{C_perdidos_sem} pedidos perdidos por sem. × {int(C_conv*100)} % × {PRECO} lei × {SEMANAS}", lei(C_receita), "receita recuperada"),
               ("total", lei(C_ganho), "ganho por ano")]),
  ],
  antes_rot="Hoje", depois_rot="Com o sistema",
  p_dinheiro="Quanto vale tudo junto", col=["Vitória rápida", "Por ano"],
  invest_rot="Investimento (exemplo)", invest_txt=f"3 sistemas × {lei(SETUP)} de instalação + {lei(MENSAL)}/mês",
  roi_rot="Retorno no 1.º ano", ret_rot="Paga-se em", ret_un="meses",
  p_plano="O plano de 90 dias",
  plano=[("Dias 1–30", "Faltas", "Dia 0: medimos quantas faltas há hoje. Ligamos as confirmações e a lista de espera."),
         ("Dias 31–60", "Clientes que voltam", "A mensagem do dia 25, o regresso às 6 semanas e o link das avaliações."),
         ("Dias 61–90", "Resposta a mensagens", "Tu aprovas as respostas. O assistente arranca e passa a uma pessoa tudo o que sai da rotina.")],
  medir_rot="O que medimos todos os meses", medir=["faltas por semana", "% de clientes novos que voltam", "tempo de resposta às mensagens", "avaliações novas no Google"],
  tu_rot="O que decides tu", tu=["aprovas cada texto antes de sair", "desligas qualquer sistema com uma mensagem", "tudo corre nas tuas contas (MERO, WhatsApp, Google)"],
  prox="Próximo passo: escolhemos juntos por que vitória rápida começar.",
  rodape="Pacheco Studios · pachecost.com",
 ),
}

def e(s): return html.escape(str(s))

def pagina(t, n, titulo, corpo, cls=""):
    return f"""<section class="sl {cls}">
  <div class="faixa">{e(t['faixa'])}</div>
  <header class="sl-cab"><span class="sl-n">{n:02d}</span><h2>{e(titulo)}<span class="ponto"></span></h2></header>
  <div class="sl-corpo">{corpo}</div>
  <footer class="rod"><span>{e(t['rodape'])}</span><span>{n:02d} / 08</span></footer>
</section>"""

def gerar(L):
    t = T[L]
    capa = f"""<section class="sl capa">
  <div class="faixa">{e(t['faixa'])}</div>
  <div class="capa-top"><span class="marca">PACHECO STUDIOS<span class="ponto"></span></span><span class="mono">{e(t['kicker'])}</span></div>
  <div class="capa-grid">
    <div><h1>Society<br>Salon</h1><p class="capa-sub">{e(t['sub'])}</p></div>
    <div class="capa-num"><p class="mono lar">{e(t['total_rot'])}</p><p class="grande">{num(TOTAL)}<small> lei</small></p><p class="cinza">{e(t['total_nota'])}</p></div>
  </div>
</section>"""
    feito = "".join(f"<div><b>{e(a)}</b><span>{e(b)}</span></div>" for a, b in t["feito"])
    p1 = pagina(t, 1, t["p_cerut"], f"""<p class="obj">«{e(t['obj'])}»</p><div class="feito">{feito}</div>""")
    cols = ""
    for nome, sub, passos in t["mot"]:
        ps = "".join(f"<li class='{c}'>{e(p)}</li>" for p, c in passos)
        cols += f"<div class='motor'><h3>{e(nome)}</h3><p class='mono cinza'>{e(sub)}</p><ol>{ps}</ol></div>"
    p2 = pagina(t, 2, t["p_mapa"], f"""<p class="lead">{e(t['mapa_lead'])}</p><div class="motores">{cols}</div>
      <p class="leg"><span class="tag t">■</span> {e(t['leg_t'])} &nbsp; <span class="tag r">■</span> {e(t['leg_r'])}</p>""")
    qs = "".join(f"<div class='mq m{i}'><b>{e(a)}</b><span class='mono'>{e(b)}</span><ul>{''.join(f'<li>{e(x)}</li>' for x in itens)}</ul></div>"
                 for i, (a, b, itens) in enumerate(t["q"], 1))
    p3 = pagina(t, 3, t["p_matriz"], f"""<div class="matriz"><span class="eixo y">{e(t['eixo_y'])} →</span>{qs}<span class="eixo x">{e(t['eixo_x'])} →</span></div>""")
    qws = []
    for i, w in enumerate(t["qw"]):
        contas = "".join(f"<tr class='{'fim' if j == len(w['conta'])-1 else ''}'><td class='mono'>{e(a)}</td><td class='v'>{e(b)}</td><td class='cinza'>{e(c)}</td></tr>" for j, (a, b, c) in enumerate(w["conta"]))
        corpo = f"""<p class="dor">{e(w['dor'])}</p>
        <div class="ad">
          <div class="antes"><p class="mono">{e(t['antes_rot'])}</p><ol>{''.join(f'<li>{e(x)}</li>' for x in w['antes'])}</ol></div>
          <div class="seta">→</div>
          <div class="depois"><p class="mono">{e(t['depois_rot'])}</p><ol>{''.join(f'<li>{e(x)}</li>' for x in w['depois'])}</ol></div>
        </div>
        <table class="conta">{contas}</table>{f'<p class="extra">{e(w["extra"])}</p>' if w.get('extra') else ''}"""
        qws.append(pagina(t, 4 + i, f"{w['id']} · {w['nome']}", corpo, "qw"))
    mx = max(A_ganho, B_ganho, C_ganho)
    linhas = "".join(f"<tr><td>{e(w['nome'])}</td><td class='barra'><i style='width:{v/mx*100:.0f}%'></i></td><td class='v'>{lei(v)}</td></tr>"
                     for w, v in zip(t["qw"], (A_ganho, B_ganho, C_ganho)))
    p7 = pagina(t, 7, t["p_dinheiro"], f"""<div class="din">
      <table class="tot"><thead><tr><th>{e(t['col'][0])}</th><th></th><th>{e(t['col'][1])}</th></tr></thead><tbody>{linhas}
      <tr class="soma"><td>Total</td><td></td><td class="v">{lei(TOTAL)}</td></tr></tbody></table>
      <div class="kpis">
        <div><p class="mono">{e(t['invest_rot'])}</p><p class="k">{lei(INVEST)}</p><p class="cinza">{e(t['invest_txt'])}</p></div>
        <div class="lar-bg"><p class="mono">{e(t['roi_rot'])}</p><p class="k">{ROI} %</p></div>
        <div><p class="mono">{e(t['ret_rot'])}</p><p class="k">{str(RETORNO_MESES).replace('.', ',')} {e(t['ret_un'])}</p></div>
      </div></div>""")
    plano = "".join(f"<div class='fase'><p class='mono lar'>{e(a)}</p><h3>{e(b)}</h3><p>{e(c)}</p></div>" for a, b, c in t["plano"])
    p8 = pagina(t, 8, t["p_plano"], f"""<div class="plano">{plano}</div>
      <div class="duas"><div><p class="mono">{e(t['medir_rot'])}</p><ul class="pts">{''.join(f'<li>{e(x)}</li>' for x in t['medir'])}</ul></div>
      <div><p class="mono">{e(t['tu_rot'])}</p><ul class="pts">{''.join(f'<li>{e(x)}</li>' for x in t['tu'])}</ul></div></div>
      <p class="prox">{e(t['prox'])}</p>""")
    css = (AQUI / "exemplo.css").read_text(encoding="utf-8").replace("FONTES/", FONTES.as_uri() + "/")
    doc = f"""<!doctype html><html lang="{t['lang']}"><head><meta charset="utf-8"><title>{e(t['titulo'])}</title>
<style>{css}</style></head><body>{capa}{p1}{p2}{p3}{''.join(qws)}{p7}{p8}</body></html>"""
    (AQUI / f"exemplo-{L}.html").write_text(doc, encoding="utf-8")

def pdf(L):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = b.new_page()
        pg.goto((AQUI / f"exemplo-{L}.html").as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(AQUI / f"Society-Salon-auditoria-exemplo-{L}.pdf"), print_background=True, prefer_css_page_size=True)
        b.close()

if __name__ == "__main__":
    print(dict(A=A_ganho, B=B_ganho, C=C_ganho, total=TOTAL, invest=INVEST, roi=ROI, meses=RETORNO_MESES))
    for L in ("ro", "pt"):
        gerar(L); pdf(L)
