# Carrossel 2 · Proof: a real system breakdown (EN, 12 slides)

Ficheiros: `saida/en/pacheco-proof-01.jpg` a `12.jpg` (1080x1350) e `saida/carrossel-proof-en.zip`.
Fonte: `gerar.py` (estilo do carrossel 1, em `../carrossel-audit/gerar.py`). Voltar a gerar:
`python3 gerar.py && NODE_PATH=$(npm root -g) node ../carrossel-audit/fotografar.js saida/carrossel-proof-en.html saida/en pacheco-proof`

## Ordem

1 Capa com gráfico ilustrativo (crescimento linear vs. sistemas com IA, sem números nos eixos) · 2 Sintoma · 3 Sem IA vs. com IA no atendimento (barras: pedidos de orçamento, faturação, resolução) · 4 Percurso antes ·
5 DADOS: a primeira hora decide o lead (60×) · 6 Pergunta da auditoria · 7 A regra ·
8 O que a IA faz + Klarna · 9 O que fica humano + Gartner · 10 Percurso depois ·
11 Caso real do Brasil (R$40k, +10 %) · 12 CTA «DM AUDIT».

## Fontes dos números (verificadas a 12/10/2026)

- Slide 3 (Tomás, 12/10 22h12: reforçar faturação e a diferença da IA no atendimento): 50 → 500 pedidos de orçamento respondidos por dia (caso real, bebidas para eventos, Brasil) e +10 % de faturação mensal depois da implementação (caso real, clínica de imagem, Brasil; o caso não diz que cresce 10 % todos os meses), ambos do site (`conteudo/casos.json`); +15 % de pedidos resolvidos por hora com assistente de IA, média de 5.172 agentes de apoio (Brynjolfsson, Li e Raymond, «Generative AI at Work», Quarterly Journal of Economics, 2025; https://www.nber.org/papers/w31161). Cada painel tem a sua escala e as barras começam no zero.
- Slide 5: Oldroyd, McElheran e Elkington, «The Short Life of Online Sales Leads», Harvard Business Review, março de 2011 (https://hbr.org/2011/03/the-short-life-of-online-sales-leads). Análise de 1,25 milhões de leads de 42 empresas: contacto em 1 hora ≈ 7× mais probabilidade de qualificar do que 1 hora depois e mais de 60× do que após 24 horas.
- Slide 8: comunicado da Klarna de 27/02/2024 (https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/): 2/3 das conversas de apoio no 1.º mês, tempo médio de resolução de 11 min para menos de 2 min. Números da própria empresa, e o slide diz isso.
- Slide 9: Gartner, comunicado de 04/08/2026 (https://www.gartner.com/en/newsroom/press-releases/2026-08-04-gartner-survey-finds-87-percent-of-customers-say-companies-using-genai-for-customer-service-must-provide-access-to-a-human-agent0): inquérito a 3.566 clientes (fev.–mar. 2026), 87 % consideram essencial poder falar com uma pessoa quando a empresa usa IA.
- Slide 11: caso público do Brasil que já está no site (clínica de imagem; fonte interna em `sites/pacheco-studios/conteudo/casos.json` do ramo do site, verificada a 02/10). No slide aparece só «Real case» (decisão do Tomás, 12/10 21h39), sem «public case» nem «nós fizemos». Quando houver um caso nosso com números confirmados, troca-se `caso_real()`.

Nota: os números 100× / 21× (5 vs. 30 minutos) que circulam na internet são de outro estudo (InsideSales, 2007) e muitas vezes são atribuídos à HBR por engano. Não entraram.

## Legenda (copiar a partir daqui)

The problem did not start with a lack of tools.

It started with a request entering the business and nobody owning the next action.

With AI in customer service, one business went from 50 to 500 quotes answered a day.

We map:

→ where the request enters
→ what context is available
→ who has to decide
→ what can be handled by a system
→ where a human needs to take over

The result is not another generic automation.

It is a clearer operational path: trigger → owner → rule → next action → human.

Sources are on each slide.

If your team is still rebuilding context, chasing follow-ups or deciding the same things twice, DM "AUDIT" and tell us where the first break happens.

#AISystems #AIConsulting #BusinessSystems #Operations #BusinessAutomation
