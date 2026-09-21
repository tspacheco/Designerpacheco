# SISTEMAS INTERNOS DA PACHECO STUDIOS — Make, Notion, Slack, Brevo e HighLevel

> Investigação de 21/09/2026. Preços vêm de fontes públicas de 2026 (lista no fim) e mudam: confirmar na página de preços antes de pagar. Regra de ouro pedida pelo Tomás: **cada ferramenta tem de suportar "secções por cliente"**, senão não entra.

## 1. A decisão, em uma frase

**Não montes os dois mundos ao mesmo tempo.** Ou (A) Notion + Slack + Make + Brevo — barato, flexível, mas és tu a colar tudo; ou (B) HighLevel como centro (CRM, pipeline, e-mail, WhatsApp, agenda, reviews, sites, faturação de mensalidades) com Notion para documentação e Make só para o que o HighLevel não fala (faturação AT, MB WAY, WooCommerce). Para uma agência que vende **mensalidade** a restaurantes e lojas pequenas, **B ganha**: o modelo de sub-contas + snapshots é literalmente "uma secção por cliente", e é isso que dá para revender.

Caminho recomendado: **arrancar com Notion + Make (Core) hoje, e um trial de 14 dias do HighLevel esta semana com um único objetivo: construir o snapshot "Restaurante PT".** Se ao fim do trial o snapshot faz o que o playbook promete aos clientes (reviews, reservas, WhatsApp, lembretes), passa a Starter. Brevo e Slack ficam em espera — ver porquê abaixo.

## 2. Ferramenta a ferramenta — "secções por cliente" sim ou não

| Ferramenta | Como se separa por cliente | Plano necessário | Veredicto |
|---|---|---|---|
| **HighLevel** | **Sub-conta por cliente**, criada a partir de um **snapshot** (modelo com pipeline, calendário, formulários, workflows, templates). Cada cliente tem login próprio, dados isolados, e podes revender. | Starter 97 $/mês = 3 sub-contas · Unlimited 297 $/mês = ilimitadas + API + domínio white-label. Anual ≈ −17 %. Mais 20–150 $/mês de consumo (SMS, e-mail, WhatsApp, IA). | **Sim, é o desenho nativo.** É a única das cinco em que "secção por cliente" é a unidade base do produto. |
| **Notion** | Uma base de dados "Clientes"; cada cliente é uma página com sub-bases (tarefas, conteúdos, entregas, reuniões). O cliente entra como **convidado** só na página dele. | Plus (~12 $/lugar/ano-mês) — convidados ilimitados. *Teamspaces privados* só no Business; não precisas deles se usares página-por-cliente + convidados. | **Sim.** Fica com o playbook, a documentação e o portal do cliente. |
| **Slack** | Canal por cliente (`#c-todachic`, `#c-naval`). Para meter o cliente dentro é preciso Slack Connect. | Free: histórico 90 dias, 10 apps, Slack Connect **só 1:1 por DM**. Canais partilhados com clientes exigem plano pago (~8,75 $/utilizador). | **Só interno, e só quando tiveres equipa.** Os teus clientes (restaurantes do Algarve, a dona da Toda Chic) vivem no WhatsApp; não vão instalar Slack. Sozinho, Slack é um sítio a mais para olhar. |
| **Brevo** | "Sub-accounts" com admin central, IP e API próprios por cliente. | **Só Enterprise** (~449 $/mês). Nos planos normais a alternativa é **uma conta Brevo por cliente** (free 300 e-mails/dia, com o domínio do cliente) e tu como utilizador convidado. | **Não como plataforma de agência.** Ou uma conta por cliente (gratuita, funciona, mas são N logins), ou o e-mail passa para o HighLevel. |
| **Make** | Cenários e ligações separadas por cliente. Pastas por cliente e permissões por membro **só no plano Teams**. | Free 1.000 créditos · Core ~16 $/mês (10 k) · Pro ~28 $ · Teams ~51 $ (mensal; anual mais barato). | **Sim, com disciplina de nomes** no Core (`[TODA CHIC] Encomenda → fatura`), Teams quando houver colaborador. |

## 3. O que o HighLevel substitui, e o que não substitui em Portugal

**Substitui:** CRM e pipeline de vendas (a tua prospeção porta-a-porta cabe aqui: Lista A/Lista B, estado, próximo passo), agenda de reservas/marcações, formulários dos sites, e-mail marketing (adeus Brevo), inbox unificada (Instagram DM, Messenger, e-mail, WhatsApp, SMS), workflows (grande parte do Make), pedidos de review Google, planeador de redes sociais, sites/funis simples, faturação de **mensalidades** por Stripe, memberships/cursos, IA de conversação.

**Não substitui (e é aqui que o Make continua a valer):**
- **Faturação certificada pela AT** (ATCUD, QR, SAF-T). O HighLevel emite "invoices" por Stripe que **não são faturas fiscais portuguesas**. A fatura sai do Vendus/InvoiceXpress/Moloni — Make liga "pagamento recebido" → "emitir fatura".
- **MB WAY.** Pagamentos no HighLevel = Stripe. A página da Stripe lista MB WAY como método de pagamento em 2026 (fonte abaixo) — **a confirmar se está ativo em contas portuguesas e a que taxa**; se estiver, muda a recomendação da loja Toda Chic (ver `research/loja-online-pt.md`, que assumia o contrário). Até confirmar: ifthenpay/Eupago continuam a ser o caminho seguro.
- **WhatsApp a custo previsível.** O WhatsApp no HighLevel é add-on por sub-conta, cobrado por conversa e rebilling ao cliente; SMS em Portugal exige registo de remetente. Orçamentar 20–150 $/mês de consumo por cima do plano e testar no trial com o teu próprio número antes de prometer a clientes.
- **Documentação e playbook.** Isso é Notion (e este repositório).
- **Comunicação interna.** Slack ou simplesmente WhatsApp contigo próprio até haver equipa.

## 4. Como aprender a gerir o HighLevel (plano de 14 dias, 1 h/dia)

1. **Dias 1–2 — Agência e sub-contas.** Cria a sub-conta "Pacheco Studios" (és o teu primeiro cliente). Aprende: Agency view vs Sub-account view, utilizadores, permissões, domínio white-label (só no Unlimited — ignora por agora).
2. **Dias 3–5 — Snapshot "Restaurante PT".** Numa sub-conta de teste monta: pipeline (Contactado → Demo vista → Proposta → Fechado → Mensalidade), calendário de reservas, formulário de contacto igual ao dos sites, workflow "pedido de review 2 h depois da visita", template de WhatsApp "a sua mesa está confirmada". Guarda como **snapshot**. É o produto que vais clonar por cliente.
3. **Dias 6–8 — Conversations + Reputation.** Liga Instagram e WhatsApp da sub-conta de teste, testa o inbox unificado, ativa o pedido de reviews Google e o widget de reviews para pôr nos sites que fazes.
4. **Dias 9–10 — Automations.** Missed-call text-back (chamada perdida → WhatsApp automático), lembrete de reserva, aniversário/cliente inativo. São os três workflows que um restaurante entende e paga.
5. **Dias 11–12 — Dinheiro.** Stripe, produtos de subscrição (a tua mensalidade de 50 €), rebilling de SMS/WhatsApp ao cliente com margem.
6. **Dias 13–14 — Clonar.** Cria a sub-conta "Grupo Naval" a partir do snapshot, mede quanto tempo demora a ficar operacional (meta: < 1 h). Se for mais, o snapshot não está pronto.

Fontes de aprendizagem que valem o tempo: **HighLevel Support Portal** (help.gohighlevel.com — artigos oficiais, incluindo o guia de WhatsApp para agências) e a **HighLevel University** (gratuita). Evitar cursos pagos de "gurus" até ter feito os 14 dias.

## 5. Os primeiros cenários a montar no Make (por ordem de retorno)

1. **`[PS] Lead do site → CRM`** — formulário dos sites (Netlify Forms ou WhatsApp click) → Notion "Leads" (ou HighLevel) → notificação no telemóvel. Um cenário, serve todos os sites.
2. **`[PS] Mensalidade → fatura`** — todo o dia 1: lê a base "Clientes" no Notion, para cada mensalidade ativa cria a fatura no Vendus/InvoiceXpress e envia por WhatsApp/e-mail. É o cenário que te poupa mais horas por mês.
3. **`[TODA CHIC] Encomenda → fatura + aviso`** — WooCommerce "encomenda paga" → fatura certificada → mensagem à dona → stock a 0 marca a peça esgotada.
4. **`[cliente] Review pedida`** — se não usares HighLevel: reserva/visita → 2 h depois → WhatsApp com link direto para a review Google.
5. **`[PS] Faturas por WhatsApp`** — o blueprint da secção 9 do playbook (Twilio → OCR do QR da AT → Supabase) pode viver no Make em vez do n8n, se preferires uma só ferramenta.

Convenção obrigatória: prefixo `[CLIENTE]` no nome do cenário, uma ligação (connection) por cliente com o nome do cliente, e um cenário nunca mistura dados de dois clientes.

## 6. Custo mensal realista

| Cenário | Mensal aprox. |
|---|---|
| **Arranque** (Notion Plus 1 lugar + Make Core + Slack Free + Brevo Free por cliente) | ~30 $ |
| **HighLevel Starter** (3 sub-contas: Pacheco + 2 clientes) + Notion + Make Core | ~125 $ + consumo (20–150 $) |
| **HighLevel Unlimited** (quando passares de 3 clientes pagantes em mensalidade) | ~325 $ + consumo |

Regra: o HighLevel só se paga quando **3 clientes pagam mensalidade**. Com a tabela atual (50 €/mês) são 150 €/mês de receita contra ~100–150 $ de custo — é o ponto de equilíbrio. A partir do 4.º cliente é margem. Isto é mais um argumento para a mensalidade "Pro" (reviews + WhatsApp + reservas) custar mais do que a mensalidade "site".

## 7. Perguntas que ainda não têm resposta (verificar antes de decidir)

- Stripe com MB WAY está disponível para contas de Portugal e a que taxa? (Muda a recomendação da Toda Chic.)
- Custo real de uma conversa WhatsApp via HighLevel em Portugal em 2026, e se o rebilling ao cliente é aceite na fatura portuguesa.
- O HighLevel aceita domínio de e-mail próprio com DKIM sem custo extra no Starter? (Sim segundo a documentação, mas confirmar no trial.)
- Make Core: as pastas de cenários existem ou é só no Teams? As fontes divergem — ver no próprio plano.

## Fontes

- [HighLevel — página oficial de preços](https://www.gohighlevel.com/pricing)
- [GoHighLevel Pricing 2026: $97 vs $297 vs $497 (Ruzuku)](https://www.ruzuku.com/compare/gohighlevel-pricing)
- [GoHighLevel Sub-Accounts & Snapshots — guia para agências](https://globalhighlevel.com/blog/gohighlevel-sub-accounts-snapshots-agency-guide/)
- [GoHighLevel Pricing for Agencies (2026)](https://digitalmarketingsnapshotforghl.com/blog/gohighlevel-pricing-plans-for-agencies/)
- [WhatsApp Pricing, Billing & Rebilling Guide — HighLevel Support Portal](https://help.gohighlevel.com/support/solutions/articles/155000001428-whatsapp-pricing-billing-and-rebilling-guide)
- [WhatsApp Full Setup Guide for Agency — HighLevel Support Portal](https://help.gohighlevel.com/support/solutions/articles/48001206216-whatsapp-full-setup-guide-for-agency)
- [Stripe — MB WAY como método de pagamento](https://stripe.com/ie/payment-method/mb-way)
- [Brevo — Sub-Account Management](https://www.brevo.com/features/sub-account-management/)
- [Brevo — O que é a gestão de sub-contas (Enterprise)](https://help.brevo.com/hc/en-us/articles/9003097317138-Classic-Admin-account-What-is-sub-accounts-management)
- [Brevo Pricing 2026 (emailsoftwareinsights)](https://www.emailsoftwareinsights.com/reviews/brevo/pricing/)
- [Make — Pricing](https://www.make.com/en/pricing)
- [Make.com Teams vs Enterprise — quando faz sentido](https://thestackarchitects.com/make-com-teams-vs-enterprise-plans/)
- [Make.com Pricing 2026 (trackstack)](https://trackstack.tech/en/make-com-pricing-2026/)
- [Slack — limitações da versão gratuita](https://slack.com/help/articles/27204752526611-Feature-limitations-on-the-free-version-of-Slack)
- [Slack — Slack Connect com equipas gratuitas](https://slack.com/help/articles/4409350616467-Use-Slack-Connect-with-free-teams)
- [Notion Pricing 2026 (TinyCommand)](https://tinycommand.com/blogs/notion-pricing-2026)
- [Notion Agency 2026: workspace que escala (Hack'celeration)](https://hackceleration.com/agency/notion)
