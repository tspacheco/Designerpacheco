# HighLevel — plano de 14 dias (Pacheco Studios)

**Objetivo único do trial:** sair com o snapshot **"Restaurante PT"** pronto a clonar para qualquer cliente em menos de 1 hora. Tudo o resto é distração.

**Regras do jogo**
- 1 hora por dia, à mesma hora. Cronómetro ligado.
- Cada dia tem um *entregável* e um teste de "está feito?". Se o teste falha, o dia repete-se antes de avançar.
- Trabalha sempre numa **sub-conta de teste** ("Restaurante Teste"), nunca na conta de agência.
- Tudo o que aprenderes de útil vai para a base "Aprendizagens" (no fim desta página) — é o que evita repetir erros com o cliente real.
- Fonte de verdade: **help.gohighlevel.com** (Support Portal) e a **HighLevel University** (gratuita). Nada de cursos pagos antes do dia 14.

**Antes do dia 1 (30 min):** criar o trial de 14 dias, ter um cartão para o Stripe em modo teste, um número de telemóvel que possas usar como "restaurante" para testar WhatsApp/SMS, e um e-mail de teste para receberes o que o cliente receberia.

---

## Semana 1 — construir

### Dia 1 · Agência e sub-contas
- **Objetivo:** perceber a diferença entre *Agency view* e *Sub-account view*, e criar a primeira sub-conta.
- **Tarefas:** criar a sub-conta "Pacheco Studios" (és o teu primeiro cliente) · criar a sub-conta "Restaurante Teste" · criar um utilizador com permissões de cliente e entrar com ele · anotar o que o cliente vê e o que não vê.
- **Entregável:** duas sub-contas criadas e um login de cliente testado.
- **Está feito quando:** consegues explicar em 3 frases a um cliente o que ele vai ver quando entrar.

### Dia 2 · Contactos, pipeline e etiquetas
- **Objetivo:** montar o CRM à medida da prospeção porta-a-porta do playbook.
- **Tarefas:** criar o pipeline **Vendas Pacheco** com as etapas *Lista A/B → Contactado → Demo vista → Proposta → Fechado → Mensalidade ativa* · criar campos personalizados *Zona*, *Tipo de negócio*, *Rating Google*, *Tem site?* · importar 10 contactos reais do playbook (Fuzeta, Altura, Quarteira) por CSV · criar etiquetas *restaurante*, *loja*, *cabeleireiro*.
- **Entregável:** pipeline com 10 oportunidades reais.
- **Está feito quando:** arrastas uma oportunidade de etapa e a lista de "próximo passo" faz sentido para amanhã de manhã.

### Dia 3 · Calendário de reservas
- **Objetivo:** o calendário que um restaurante usaria para reservas.
- **Tarefas:** criar o calendário "Reservas" (mesas, duração 90 min, horário 12–15 / 19–23, fecha à terça) · página pública de reserva · confirmação automática por e-mail e WhatsApp/SMS · fazer 2 reservas de teste a partir do telemóvel.
- **Entregável:** link público de reserva a funcionar.
- **Está feito quando:** a reserva feita no telemóvel aparece no calendário e recebes a confirmação nos dois canais.

### Dia 4 · Formulários e sites
- **Objetivo:** ligar os sites Pacheco ao HighLevel sem os refazer.
- **Tarefas:** criar o formulário "Contacto" igual ao dos sites (nome, telemóvel, mensagem) · obter o código de embed · testar num site de demonstração (ex.: `sites/mr-buffalo/index.html` local) · ver o contacto entrar no pipeline com a etiqueta certa · explorar o construtor de sites/funis e decidir: **não** substitui os sites de ficheiro único do playbook (o design é o nosso argumento de venda), serve para landing pages de campanha.
- **Entregável:** formulário embebido que cria contacto + oportunidade.
- **Está feito quando:** submetes o formulário no telemóvel e o contacto aparece em menos de 10 segundos.

### Dia 5 · Workflow "pedido de review"
- **Objetivo:** o primeiro workflow que um restaurante paga.
- **Tarefas:** criar workflow *Visita concluída → esperar 2 h → WhatsApp/SMS com link direto para a review Google → se não abrir em 2 dias, e-mail* · obter o link curto de review do Google Business do restaurante de teste · testar contigo próprio · escrever a mensagem em PT-PT com a voz do negócio (curta, sem emojis a mais).
- **Entregável:** workflow ativo e testado.
- **Está feito quando:** recebes a mensagem no teu telemóvel 2 h depois de marcares a visita como concluída.

### Dia 6 · Conversations (inbox unificada) + WhatsApp
- **Objetivo:** perceber o custo e o processo real do WhatsApp na Europa antes de o prometer.
- **Tarefas:** ligar Instagram DM e Facebook Messenger da sub-conta de teste · ler o guia oficial de WhatsApp para agências (help.gohighlevel.com) · ativar o WhatsApp na sub-conta de teste com o número de teste · registar: custo por conversa, tempo de aprovação da Meta, o que é preciso do cliente (Business Manager, verificação) · trocar 5 mensagens de teste.
- **Entregável:** inbox com Instagram + WhatsApp a receber.
- **Está feito quando:** tens escrito o custo mensal estimado de WhatsApp para um restaurante com 200 conversas/mês.

### Dia 7 · Reputação e widget de reviews
- **Objetivo:** fechar o ciclo das reviews e mostrá-las no site.
- **Tarefas:** ligar o Google Business Profile do restaurante de teste (ou o teu) · ativar *Reputation Management* · gerar o widget de reviews e embebê-lo na demo local · configurar resposta automática a reviews (rascunho, não automática — a voz é do dono).
- **Entregável:** widget de reviews a funcionar numa demo.
- **Está feito quando:** o widget mostra reviews reais e o pedido do dia 5 aponta para o sítio certo.

## Semana 2 — automatizar, cobrar, clonar

### Dia 8 · Missed-call text-back e lembretes
- **Objetivo:** os dois automatismos que um restaurante entende à primeira.
- **Tarefas:** *chamada perdida → WhatsApp/SMS automático "Vimos a sua chamada, quer reservar? [link]"* · *lembrete de reserva 3 h antes* · *cliente sem visita há 60 dias → mensagem com sugestão do menu* · testar as três com o número de teste.
- **Entregável:** três workflows ativos.
- **Está feito quando:** ligas para o número de teste, desligas, e recebes a mensagem em menos de 1 minuto.

### Dia 9 · E-mail marketing (o que substitui o Brevo)
- **Objetivo:** confirmar que o e-mail no HighLevel chega à caixa de entrada.
- **Tarefas:** configurar domínio de envio com DKIM/SPF para a sub-conta de teste · criar um template de newsletter simples no estilo Pacheco · enviar para 3 endereços teus (Gmail, Outlook, outro) · verificar onde cai (inbox/spam) · anotar limites e custos de envio do plano.
- **Entregável:** newsletter de teste entregue na inbox.
- **Está feito quando:** 3 de 3 chegam à caixa de entrada.

### Dia 10 · Redes sociais e conteúdo
- **Objetivo:** ver se o *Social Planner* substitui o que fazes hoje à mão para o Instagram.
- **Tarefas:** ligar o Instagram de teste · agendar 3 publicações (usa os destaques da Pacheco Studios de `social/`) · ver o que acontece com carrosséis e stories · decidir se entra no pacote "Pro" ou não.
- **Entregável:** decisão escrita: entra / não entra, e porquê.
- **Está feito quando:** a decisão tem uma frase que podes dizer a um cliente.

### Dia 11 · Pagamentos e mensalidades
- **Objetivo:** cobrar a mensalidade da Pacheco Studios sem tocar em nada.
- **Tarefas:** ligar Stripe (modo teste) · criar os produtos *Site 50 €/mês* e *Pro 90 €/mês* (valor a decidir) · criar um link de subscrição · pagar com cartão de teste · ver a fatura que o HighLevel gera e **confirmar que não é fatura fiscal portuguesa** (a fatura AT sai do Vendus/InvoiceXpress — ligação por Make no dia 13) · verificar se a Stripe da tua conta PT lista MB WAY.
- **Entregável:** link de subscrição a funcionar em teste.
- **Está feito quando:** a subscrição aparece ativa e sabes exatamente que documento fiscal ainda falta emitir.

### Dia 12 · Rebilling e custos ao cliente
- **Objetivo:** não perder dinheiro com SMS/WhatsApp/IA.
- **Tarefas:** ativar rebilling na sub-conta de teste · definir margem (ex.: custo ×1,5) · simular um mês de 200 conversas WhatsApp e 100 SMS · construir a tabela "o que custa ao cliente por mês" para pôr na proposta.
- **Entregável:** tabela de custos por cliente/mês.
- **Está feito quando:** consegues dizer a um restaurante "o WhatsApp custa-lhe X €/mês, incluído/não incluído" sem hesitar.

### Dia 13 · Snapshot "Restaurante PT" + ligação ao Make
- **Objetivo:** empacotar tudo.
- **Tarefas:** limpar a sub-conta de teste (dados de teste fora, templates dentro) · guardar como **snapshot "Restaurante PT v1"** · listar o que o snapshot contém (pipeline, calendário, formulário, 4 workflows, templates PT-PT, widget) · criar no Make o cenário `[PS] Mensalidade → fatura` com o webhook do HighLevel "pagamento recebido" → Vendus/InvoiceXpress (ou apenas o esqueleto, se ainda não tiveres o software de faturação).
- **Entregável:** snapshot guardado + lista do conteúdo.
- **Está feito quando:** o snapshot aparece na biblioteca da agência com a lista ao lado.

### Dia 14 · Clonar e cronometrar
- **Objetivo:** provar que o produto existe.
- **Tarefas:** criar a sub-conta **"Grupo Naval"** a partir do snapshot · cronometrar até estar operacional (nome, logótipo, horário, Google Business, número) · anotar tudo o que teve de ser feito à mão · decidir: **Starter agora, ou esperar pelo 3.º cliente em mensalidade?**
- **Entregável:** sub-conta do Grupo Naval pronta + tempo medido + decisão.
- **Está feito quando:** o tempo foi < 1 h. Se não foi, a lista do que fizeste à mão é o trabalho da v2 do snapshot.

---

## O que o snapshot "Restaurante PT v1" tem de conter

| Bloco | Conteúdo |
|---|---|
| Pipeline | Reserva pedida → Confirmada → Visita concluída → Review pedida → Cliente recorrente |
| Calendário | Reservas, 90 min, horário e dia de fecho configuráveis |
| Formulários | Contacto (igual ao site) · Reserva · Pedido de orçamento para grupos |
| Workflows | Review 2 h depois · Missed-call text-back · Lembrete 3 h antes · Cliente inativo 60 dias |
| Templates | 6 mensagens em PT-PT (confirmação, lembrete, review, chamada perdida, inativo, agradecimento) |
| Reputação | Google Business ligado, widget para o site |
| Campos | Zona, tipo de cozinha, dia de fecho, link de review |

## Custos a ter presentes

- Starter 97 $/mês (3 sub-contas) · Unlimited 297 $/mês (ilimitadas, API, white-label). Anual ≈ −17 %.
- Consumo (SMS, e-mail, WhatsApp, IA): 20–150 $/mês por cima, a confirmar nos dias 6, 9 e 12.
- Ponto de equilíbrio: 3 clientes em mensalidade. Detalhe em `research/sistemas-pacheco-studios.md`.

## Aprendizagens (preencher durante os 14 dias)

| Dia | O que aprendi | O que mudo no snapshot / na proposta |
|---|---|---|
| | | |
