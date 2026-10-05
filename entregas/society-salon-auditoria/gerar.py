# Guião da auditoria de IA ao Society Salon (método em research/execucao-video.md).
# Gera guiao.html e Society-Salon-guiao-auditoria.pdf com o Chromium do Playwright.
# Uso: python3 gerar.py
import html, pathlib, subprocess, sys

AQUI = pathlib.Path(__file__).parent
FONTES = (AQUI / "../../marca/fontes").resolve()

# (essencial?, pergunta PT, pergunta RO, nota para o Tomás)
BLOCOS = [
  ("1", "O objetivo", "Dono · 10 min", "Transformar desejos em números: estado atual → alvo → valor em lei.", [
    (1, "Qual é o problema que mais dinheiro te custa hoje?",
        "Care e problema care te costă cei mai mulți bani acum?", "Deixa-o falar. Não sugiras nada."),
    (1, "Se resolvêssemos uma só coisa que mexesse na faturação, qual era?",
        "Dacă am rezolva un singur lucru care să crească încasările, care ar fi?", ""),
    (0, "Onde sabes que perdes dinheiro mas ainda não tiveste tempo de resolver?",
        "Unde știi că pierzi bani, dar încă n-ai apucat să rezolvi?", ""),
    (1, "Daqui a 12 meses, o que tem de ser verdade para dizeres que foi um bom ano?",
        "Peste 12 luni, ce trebuie să fie adevărat ca să spui că a fost un an bun?",
        "Puxa por um número: faturação, cadeiras cheias, mais barbeiros, 2.º salão."),
    (0, "Se a equipa ganhasse mais 20 % de tempo, onde o punhas?",
        "Dacă echipa ar avea cu 20 % mai mult timp, unde l-ai folosi?", ""),
  ]),
  ("2", "O dia de ontem", "Dono, depois cada barbeiro", "A pergunta-mãe do método. Sobre ontem contam o que acontece, não o que devia acontecer.", [
    (1, "Conta-me ontem, desde que abriste a porta. O que fizeste primeiro? E depois? E depois?",
        "Povestește-mi ziua de ieri, de când ai deschis ușa. Ce ai făcut prima dată? Și apoi? Și după aceea?",
        "Repete «e depois?» até não dar para partir mais. Aponta o tempo de cada passo."),
    (0, "Ontem, quantas mensagens e chamadas atendeste? Por onde chegaram e quanto tempo levaram?",
        "Ieri, câte mesaje și apeluri ai primit? Pe unde au venit și cât timp ți-au luat?", ""),
    (0, "E depois de fechar, o que ficou para fazer?",
        "Și după închidere, ce a mai rămas de făcut?", "Caixa, comissões, Instagram, encomendas."),
  ]),
  ("3", "Motor de aquisição", "Como chega um cliente novo", "", [
    (1, "De onde vêm os clientes novos? MERO, Google, Instagram, quem passa na rua, recomendação… Em percentagem, mais ou menos.",
        "De unde vin clienții noi? MERO, Google, Instagram, trecători, recomandări… Cam în ce procent?", ""),
    (0, "Quantos clientes novos têm por mês? Onde vês esse número?",
        "Câți clienți noi aveți pe lună? Unde vezi cifra asta?", "Se não souber, já é um achado."),
    (1, "Quando alguém pergunta preço ou vaga por mensagem ou telefone, quem responde e quanto tempo demora? E à noite ou ao domingo?",
        "Când cineva întreabă de preț sau de un loc liber pe mesaj sau la telefon, cine răspunde și în cât timp? Dar seara sau duminica?", ""),
    (0, "Quantos pedidos ficam sem resposta ou chegam quando a agenda já está cheia? O que acontece a essas pessoas?",
        "Câte cereri rămân fără răspuns sau vin când agenda e deja plină? Ce se întâmplă cu oamenii ăștia?", ""),
    (0, "Quem trata do Instagram e quanto tempo leva por semana?",
        "Cine se ocupă de Instagram și cât timp îi ia pe săptămână?", ""),
    (0, "Quantos clientes estrangeiros têm (estudantes de Medicina, por exemplo)? A língua atrapalha?",
        "Câți clienți străini aveți (studenți la Medicină, de exemplu)? Limba e o problemă?", ""),
  ]),
  ("4", "Motor de entrega", "Da marcação à cadeira e à caixa", "", [
    (1, "Como entra uma marcação: MERO, telefone, Instagram, porta? Quem passa para o MERO as que não vêm por lá?",
        "Cum intră o programare: MERO, telefon, Instagram, direct la ușă? Cine le trece în MERO pe cele care nu vin de acolo?", ""),
    (1, "Faltas e cancelamentos à última hora: quantos por semana? O que fazem quando acontece?",
        "Neprezentări și anulări de ultim moment: câte pe săptămână? Ce faceți când se întâmplă?",
        "Cada falta é dinheiro perdido: preço médio × faltas × 52."),
    (0, "Em que dias e horas a agenda tem buracos? Numa semana normal, quantas horas de cadeira ficam vazias?",
        "În ce zile și la ce ore agenda are goluri? Într-o săptămână obișnuită, câte ore rămân scaunele libere?", ""),
    (0, "Como fecham a caixa e fazem as contas das comissões dos barbeiros? Quem faz e quanto tempo leva?",
        "Cum închideți casa și calculați comisioanele frizerilor? Cine face asta și cât durează?", ""),
    (0, "Vendem produtos? Como controlam o stock e as encomendas?",
        "Vindeți produse? Cum țineți evidența stocului și a comenzilor?", ""),
    (0, "Onde costuma haver erros: marcação a dobrar, barbeiro errado, preço errado?",
        "Unde apar de obicei greșeli: programări duble, frizer greșit, preț greșit?", "Marca a vermelho no mapa (risco de qualidade)."),
  ]),
  ("5", "Motor de retorno", "Depois do corte: voltar, recomendar, avaliar", "", [
    (1, "De quanto em quanto tempo volta um cliente? Sabem quem deixou de vir?",
        "La cât timp revine un client? Știți cine a încetat să mai vină?", ""),
    (0, "Fazem alguma coisa para trazer de volta quem não vem há 5 ou 6 semanas?",
        "Faceți ceva ca să-i aduceți înapoi pe cei care n-au mai venit de 5–6 săptămâni?", ""),
    (0, "O 6.º corte grátis: como é que o controlam? Cartão de papel, MERO, de cabeça?",
        "A șasea tunsoare gratuită: cum o țineți evidența? Card de hârtie, MERO, din memorie?", ""),
    (1, "No MERO têm mais de 1 600 avaliações e no Google cerca de 70. Pedem avaliação no Google? Porque acham que há esta diferença?",
        "Pe MERO aveți peste 1.600 de recenzii, iar pe Google în jur de 70. Cereți recenzii pe Google? De ce credeți că e diferența asta?",
        "Confirmar os números no dia, no telemóvel."),
    (0, "Quando um cliente se queixa, por onde chega e quem trata?",
        "Când un client se plânge, pe unde ajunge plângerea și cine se ocupă?", ""),
  ]),
  ("6", "A equipa", "Cada barbeiro, 10 min, se possível sem o dono ao lado", "Quem faz o trabalho conhece os buracos da estrada.", [
    (1, "Que parte do teu dia é mais repetitiva?",
        "Ce parte din ziua ta e cea mai repetitivă?", ""),
    (1, "Que tarefa nunca mais querias fazer?",
        "Ce sarcină n-ai mai vrea s-o faci niciodată?", ""),
    (0, "Onde gastas tempo em coisas que não precisam das tuas mãos?",
        "Unde pierzi timp cu lucruri care nu au nevoie de mâinile tale?", ""),
    (0, "Que perguntas te fazem os clientes sempre, todas as semanas?",
        "Ce întrebări îți pun clienții mereu, în fiecare săptămână?", "Matéria-prima para respostas automáticas."),
  ]),
  ("7", "Sistemas", "O que já usam", "", [
    (1, "Que ferramentas usam hoje? MERO (que plano, lembretes por SMS ligados?), WhatsApp, Instagram, caixa, faturação, contabilista, Excel…",
        "Ce instrumente folosiți acum? MERO (ce abonament, aveți remindere SMS activate?), WhatsApp, Instagram, casa de marcat, facturare, contabil, Excel…", ""),
    (0, "Onde copiam dados à mão de um sítio para outro? Que sistemas deviam falar uns com os outros e não falam?",
        "Unde copiați date de mână dintr-un loc în altul? Ce sisteme ar trebui să comunice între ele și nu o fac?", ""),
    (0, "O que já experimentaram e não resultou?",
        "Ce ați încercat deja și n-a mers?", "Evita repetir o que já falhou."),
  ]),
  ("8", "Fecho e validação", "Dono · 5 min", "", [
    (1, "De tudo o que falámos, o que te tira mais o sono?",
        "Din tot ce am vorbit, ce te frământă cel mai mult?", "É este o 1.º problema do PDF."),
    (0, "Como costuma a equipa reagir a ferramentas novas?",
        "Cum reacționează de obicei echipa la instrumente noi?", ""),
    (0, "Há mais alguém que eu deva ouvir?",
        "Mai e cineva cu care ar trebui să vorbesc?", ""),
    (1, "Posso voltar daqui a uma semana para te mostrar o mapa do salão, onde se perde tempo e dinheiro e o que vale a pena fazer primeiro, com as contas?",
        "Pot să revin peste o săptămână să-ți arăt harta salonului, unde se pierd timp și bani și ce merită făcut mai întâi, cu cifrele?",
        "Marca a data antes de saíres."),
  ]),
]

NUMEROS = [
  ("Preço médio de um serviço", "lei", "Google: 80–120 lei (a confirmar)"),
  ("Barbeiros a trabalhar", "pessoas", "MERO: 5 (a confirmar)"),
  ("Marcações por semana", "marcações", ""),
  ("Faltas + cancelamentos de última hora por semana", "por semana", ""),
  ("Horas de cadeira vazias por semana", "horas", ""),
  ("Tempo a responder a mensagens e chamadas", "h / semana", ""),
  ("Tempo a fechar caixa e comissões", "h / semana", ""),
  ("Clientes novos por mês", "clientes", ""),
  ("Dos clientes novos, quantos voltam", "%", ""),
  ("Intervalo médio entre cortes", "semanas", ""),
  ("Custo de 1 hora de trabalho (comissão / salário)", "lei / h", ""),
  ("Pedidos sem resposta ou perdidos por semana", "pedidos", ""),
]

HIPOTESES = [
  ("Avaliações", "Mais de 1 600 no MERO e cerca de 70 no Google. Um pedido automático de avaliação depois de cada corte pode puxar o Google para as centenas."),
  ("Voltar a marcar", "Um corte dura 3–4 semanas. Lembrete por volta do dia 21–28 com o link do MERO já com o barbeiro escolhido."),
  ("Faltas", "Confirmação na véspera e lista de espera que preenche o buraco."),
  ("Mensagens fora de horas", "Respostas imediatas às perguntas de sempre (preço, vaga, onde fica a porta), em RO e EN, e o resto passa para uma pessoa."),
  ("Society Membership", "Assinatura mensal com cortes a preço fixo. Receita certa todos os meses."),
]

def e(s): return html.escape(s)

def bloco_html(num, titulo, quem, nota, perguntas, contador):
    linhas = []
    for ess, pt, ro, dica in perguntas:
        contador[0] += 1
        n = contador[0]
        linhas.append(f"""
      <li class="q{' ess' if ess else ''}">
        <span class="n">{n:02d}</span>
        <div class="corpo">
          <p class="pt">{e(pt)}</p>
          <p class="ro" lang="ro">{e(ro)}</p>
          {f'<p class="dica">{e(dica)}</p>' if dica else ''}
          <div class="linhas" aria-hidden="true"><i></i><i></i></div>
        </div>
      </li>""")
    return f"""
  <section class="bloco">
    <header class="bloco-cab">
      <span class="bn">{num}</span>
      <div><h2>{e(titulo)}</h2><p class="quem">{e(quem)}</p></div>
    </header>
    {f'<p class="bnota">{e(nota)}</p>' if nota else ''}
    <ol class="qs">{''.join(linhas)}</ol>
  </section>"""

def gerar():
    contador = [0]
    blocos = "".join(bloco_html(*b, contador) for b in BLOCOS)
    total = contador[0]
    essenciais = sum(q[0] for b in BLOCOS for q in b[4])
    numeros = "".join(f"<tr><td>{e(a)}</td><td class='un'>{e(u)}</td><td class='val'></td><td class='ja'>{e(j)}</td></tr>" for a, u, j in NUMEROS)
    hip = "".join(f"<li><b>{e(a)}.</b> {e(b)}</li>" for a, b in HIPOTESES)
    css = (AQUI / "estilo.css").read_text(encoding="utf-8").replace("FONTES/", FONTES.as_uri() + "/")
    doc = f"""<!doctype html>
<html lang="pt-PT"><head><meta charset="utf-8">
<title>Society Salon — guião da auditoria</title>
<style>{css}</style></head><body>

<section class="capa">
  <div class="marca">PACHECO STUDIOS<span class="ponto"></span></div>
  <div class="capa-meio">
    <p class="kicker">Auditoria de IA · guião da conversa</p>
    <h1>Society Salon<br>Barbershop</h1>
    <p class="sub">Iași · Bulevardul Carol I 26–28</p>
  </div>
  <dl class="capa-dados">
    <div><dt>Para</dt><dd>Tomás Pacheco (uso interno)</dd></div>
    <div><dt>Data</dt><dd>outubro de 2026</dd></div>
    <div><dt>Perguntas</dt><dd>{total} · {essenciais} essenciais ★</dd></div>
    <div><dt>Duração</dt><dd>45 min com o dono + 10 min por barbeiro</dd></div>
  </dl>
</section>

<section class="pagina intro">
  <h2 class="titulo">Como corre a conversa</h2>
  <div class="duas">
    <div>
      <h3>O objetivo</h3>
      <p>Sair com o mapa de como o salão funciona de verdade e com números suficientes para fazer as contas. Não se vende nada nesta conversa. A proposta vem depois, no PDF da auditoria.</p>
      <h3>Antes de ir</h3>
      <ul class="pts">
        <li>Pedir ao dono, com antecedência, o relatório do MERO dos últimos 3 meses: marcações, faltas, cancelamentos, clientes novos e recorrentes.</li>
        <li>Confirmar no telemóvel as avaliações do Google e do MERO no próprio dia.</li>
        <li>Imprimir este guião ou levá-lo no tablet. As linhas por baixo de cada pergunta são para as respostas.</li>
      </ul>
      <h3>Regras</h3>
      <ul class="pts">
        <li><b>Pedir para gravar</b> (com autorização) e transcrever depois. Assim ouves em vez de escrever.</li>
        <li><b>Perguntar sempre «e depois?»</b> até a tarefa não dar para partir mais.</li>
        <li><b>Não sugerir soluções</b> durante a conversa. Só ouvir e anotar tempos.</li>
        <li><b>Cada problema sai com um número:</b> estado atual, alvo e quanto vale em lei.</li>
        <li>Pouco tempo? Faz só as perguntas com ★.</li>
      </ul>
    </div>
    <div>
      <h3>Abertura (dizer assim)</h3>
      <blockquote>
        <p>«Isto não é uma venda. Durante uns 45 minutos vou fazer-te perguntas sobre como o salão funciona no dia a dia. Daqui a uma semana volto com o mapa do salão, onde se perde tempo e dinheiro, e o que vale a pena fazer primeiro, com as contas. Depois decides tu.»</p>
        <p lang="ro" class="ro">„Nu e o vânzare. Timp de vreo 45 de minute o să-ți pun întrebări despre cum funcționează salonul zi de zi. Peste o săptămână revin cu harta salonului, unde se pierd timp și bani și ce merită făcut mai întâi, cu cifrele. Apoi decizi tu."</p>
      </blockquote>
      <h3>O que vais desenhar a seguir</h3>
      <div class="motores">
        <div><b>Aquisição</b><span>como chega um cliente novo</span></div>
        <div><b>Entrega</b><span>da marcação à cadeira e à caixa</span></div>
        <div><b>Retorno</b><span>voltar, recomendar, avaliar</span></div>
      </div>
      <p class="leg"><span class="tag t">Tempo</span> tarefa manual e repetitiva · <span class="tag r">Risco</span> passo onde acontecem erros</p>
    </div>
  </div>
</section>

{blocos}

<section class="pagina">
  <h2 class="titulo">Números para as contas</h2>
  <p class="lead">Preencher na conversa ou a partir do relatório do MERO. Se for estimativa do dono, escrever «est.» ao lado.</p>
  <table class="num">
    <thead><tr><th>O quê</th><th>Unidade</th><th>Valor</th><th>O que já sabemos</th></tr></thead>
    <tbody>{numeros}</tbody>
  </table>
  <div class="formula">
    <p class="k">A conta de cada problema</p>
    <p class="f">horas perdidas por semana × pessoas × 52 semanas × custo de 1 hora = <b>custo por ano</b></p>
    <p class="f">faltas por semana × preço médio × 52 = <b>receita perdida por ano</b></p>
  </div>
</section>

<section class="pagina">
  <h2 class="titulo">Depois da conversa</h2>
  <div class="duas">
    <div>
      <h3>1. Filtro das 4 perguntas</h3>
      <p>Para cada passo do mapa. Quatro «sim» = candidato a automatizar.</p>
      <ol class="filtro">
        <li>A entrada é estruturada? (formulário, mensagem, marcação)</li>
        <li>A saída é previsível? (resposta padrão, lembrete)</li>
        <li>A decisão segue regras? (se… então…)</li>
        <li>Repete-se todos os dias ou todas as semanas?</li>
      </ol>
      <h3>2. Hipóteses a confirmar</h3>
      <p class="aviso">Não dizer ao dono antes de ele falar. Servem só para saberes onde escavar.</p>
      <ul class="pts">{hip}</ul>
    </div>
    <div>
      <h3>3. Matriz de oportunidades</h3>
      <div class="matriz">
        <span class="eixo y">valor para o salão ↑</span>
        <div class="q1"><b>Vitórias rápidas</b><span>fácil · valor alto · começar aqui</span></div>
        <div class="q2"><b>Grandes apostas</b><span>difícil · valor alto · fase 2</span></div>
        <div class="q3"><b>Extras</b><span>fácil · valor baixo · mais tarde</span></div>
        <div class="q4"><b>Evitar</b><span>difícil · valor baixo</span></div>
        <span class="eixo x">dificuldade →</span>
      </div>
      <h3>4. O que o dono recebe (PDF, 1 semana depois)</h3>
      <ol class="entrega">
        <li>O que nos pediste para ver</li>
        <li>O mapa do salão, com o tempo e os erros marcados</li>
        <li>A matriz de oportunidades</li>
        <li>As 3 vitórias rápidas: antes e depois, tempo poupado, contas</li>
        <li>Quanto vale tudo junto por ano</li>
        <li>Plano de 90 dias</li>
      </ol>
      <p>Antes de entregar, 15 min de validação com o dono: «Destas três, qual bate mais com o que a equipa contou?»</p>
    </div>
  </div>
</section>

</body></html>"""
    (AQUI / "guiao.html").write_text(doc, encoding="utf-8")
    return total, essenciais

def pdf():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = b.new_page()
        pg.goto((AQUI / "guiao.html").as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(AQUI / "Society-Salon-guiao-auditoria.pdf"), format="A4", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, prefer_css_page_size=True)
        b.close()

if __name__ == "__main__":
    print(gerar())
    pdf()
