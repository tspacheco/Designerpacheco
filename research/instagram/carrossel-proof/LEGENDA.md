# Carrossel 2 · Proof: a real system breakdown (EN e RO, 10 slides)

Ficheiros: EN em `saida/en/pacheco-proof-01.jpg` a `10.jpg` e `saida/carrossel-proof-en.zip`; RO (12/10 22h58) em `saida/ro/pacheco-proof-ro-01.jpg` a `10.jpg` e `saida/carrossel-proof-ro.zip`. As traduções estão em TXT_RO no gerar.py (por frase inglesa).
Fonte: `gerar.py` (estilo do carrossel 1, em `../carrossel-audit/gerar.py`). Voltar a gerar:
`python3 gerar.py && NODE_PATH=$(npm root -g) node ../carrossel-audit/fotografar.js saida/carrossel-proof-en.html saida/en pacheco-proof && NODE_PATH=$(npm root -g) node ../carrossel-audit/fotografar.js saida/carrossel-proof-ro.html saida/ro pacheco-proof-ro`

## Ordem (10 slides desde 12/10 22h56)

1 Capa com gráfico ilustrativo · 2 O que a IA faz + Klarna (01 / AI LAYER) · 3 O que fica humano + Gartner (02) ·
4 A primeira hora decide o lead (60×) · 5 Pergunta da auditoria (03) · 6 A regra (04) · 7 Percurso antes (05 / BEFORE) ·
8 Sem IA vs. com IA (barras) · 9 Caso real do Brasil (06 / EVIDENCE) · 10 CTA «DM AUDIT».
Saíram o sintoma («slow replies») e o percurso depois («Same doors. One clear path.»).

## Fontes dos números (verificadas a 12/10/2026)

- Slide 8 (Tomás, 12/10 22h12: reforçar faturação e a diferença da IA no atendimento): 50 → 500 pedidos de orçamento respondidos por dia (caso real, bebidas para eventos, Brasil) e +10 % de faturação mensal depois da implementação (caso real, clínica de imagem, Brasil; o caso não diz que cresce 10 % todos os meses), ambos do site (`conteudo/casos.json`); +15 % de pedidos resolvidos por hora com assistente de IA, média de 5.172 agentes de apoio (Brynjolfsson, Li e Raymond, «Generative AI at Work», Quarterly Journal of Economics, 2025; https://www.nber.org/papers/w31161). Cada painel tem a sua escala e as barras começam no zero.
- Slide 4: Oldroyd, McElheran e Elkington, «The Short Life of Online Sales Leads», Harvard Business Review, março de 2011 (https://hbr.org/2011/03/the-short-life-of-online-sales-leads). Análise de 1,25 milhões de leads de 42 empresas: contacto em 1 hora ≈ 7× mais probabilidade de qualificar do que 1 hora depois e mais de 60× do que após 24 horas.
- Slide 2: comunicado da Klarna de 27/02/2024 (https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/): 2/3 das conversas de apoio no 1.º mês, tempo médio de resolução de 11 min para menos de 2 min. Números da própria empresa, e o slide diz isso.
- Slide 3: Gartner, comunicado de 04/08/2026 (https://www.gartner.com/en/newsroom/press-releases/2026-08-04-gartner-survey-finds-87-percent-of-customers-say-companies-using-genai-for-customer-service-must-provide-access-to-a-human-agent0): inquérito a 3.566 clientes (fev.–mar. 2026), 87 % consideram essencial poder falar com uma pessoa quando a empresa usa IA.
- Slide 9: caso público do Brasil que já está no site (clínica de imagem; fonte interna em `sites/pacheco-studios/conteudo/casos.json` do ramo do site, verificada a 02/10). No slide aparece só «Real case» (decisão do Tomás, 12/10 21h39), sem «public case» nem «nós fizemos». Quando houver um caso nosso com números confirmados, troca-se `caso_real()`.

Nota: os números 100× / 21× (5 vs. 30 minutos) que circulam na internet são de outro estudo (InsideSales, 2007) e muitas vezes são atribuídos à HBR por engano. Não entraram.

## Legenda EN (copiar a partir daqui)

Versão curta de 12/10 23h04 (Tomás: só o fruto, o motivo para aderir, abrir os olhos e avançar). Público: donos
que faturam 10 mil a 500 mil €/mês, ainda sem IA, à procura de alguém em quem confiar. Caso só «real case».

The business that chose AI before the market forced it to.

It didn't start with a tool. It started with one next action after every enquiry.

The result: 50 to 500 quotes answered a day. +10% monthly revenue after the system went live.

Your business already works. But every request with no owner is money leaking out, at 10k a month or at 500k. The market will force this change anyway. Moving first is the only part you control.

We start with a triage, not a tool. AI inside your rules, a person for every exception, your data stays yours.

DM "AUDIT" and tell us what your business does.

#AISystems #AIConsulting #BusinessSystems #CustomerService #BusinessGrowth

## Legenda RO (copiar a partir daqui)

Afacerea care a ales AI înainte să o oblige piața.

Nu a început cu un tool. A început cu un pas următor după fiecare cerere.

Rezultatul: de la 50 la 500 de oferte răspunse pe zi. +10% venit lunar după ce sistemul a intrat în funcțiune.

Afacerea ta funcționează deja. Dar fiecare cerere fără responsabil e bani care se scurg, la 10 mii pe lună sau la 500 de mii. Piața va forța oricum schimbarea. Singurul lucru pe care îl controlezi e dacă te miști primul.

Începem cu o triere, nu cu un tool. AI în interiorul regulilor tale, un om pentru fiecare excepție, datele rămân ale tale.

Trimite „AUDIT” în privat și spune-ne ce face afacerea ta.

#AISystems #AIConsulting #AutomatizareAfaceri #AntreprenoriRomania #RelatiiCuClientii
