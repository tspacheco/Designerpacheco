# Agenda para a Dra. Angélica (consultório odontológico, Brasil) — 24/09/2026

Pesquisa feita por motor de busca: os sites dos fornecedores estão bloqueados nesta sessão. Preços a confirmar na página de cada um antes de propor.

| Sistema | Preço visto | Link de marcação online | Confirmação automática por WhatsApp | API para Make/n8n |
|---|---|---|---|---|
| **Clinicorp** | R$ 159,90 a 369,90/mês (fonte: comparativo de terceiros) | Sim, nos planos Standard e Premium, sem custo extra | Sim, automática (também SMS e e-mail) | Sim: API REST com OAuth2, já usada com n8n (anúncio na Workana, integração Cloudia) |
| **Codental** | R$ 89,90/mês | Sim | Sim, automática e manual | Não encontrada |
| **Simples Dental** | não visível (planos Essencial, Plus, Pro; 7 dias grátis) | Sim, link personalizado | Sim, 24 h antes e 2 h antes; aparece com asterisco (serviço pago à parte) | **Não tem API** (Central de Ajuda) |
| Odontiva | desde R$ 60/mês (1 consultório, 1 utilizador) | — | Sim | Não encontrada |
| Simples Agenda | desde R$ 39,90/mês (anual) | — | Sim | Não encontrada |

## Recomendação

- **Clinicorp**, se a Pacheco Studios vai gerir as automações. A agenda já faz a confirmação por WhatsApp, o que substitui o nosso workflow 1. A API permite ligar os workflows 2 e 3 (avaliações Google, revisão aos 6 meses, orçamentos) por Make ou n8n.
- **Codental**, se ela quiser só agenda e confirmações pelo preço mais baixo. Perde-se a ligação aos nossos workflows.
- Evitar o Simples Dental para este plano: não tem API.

Antes de fechar: confirmar com a Clinicorp em que plano está o acesso à API e se tem webhooks (marcação criada ou cancelada) ou só consulta.

## Custo da Clinicorp (pesquisa 24/09/2026, a confirmar com a Clinicorp)

| Item | Valor | Nota |
|---|---|---|
| Plano Premium | R$ 369,90/mês | Necessário: a integração WhatsApp só existe a partir do Premium. Há opção trimestral com desconto. |
| Plano Standard | R$ 159,90/mês | Agenda, prontuário, financeiro, marcação online. Sem WhatsApp. |
| Mensagens WhatsApp | R$ 0,12 por mensagem enviada | API oficial da Meta. Estimativa: ~110 consultas × 3 mensagens ≈ R$ 40/mês. |
| Implantação | obrigatória, preço não público | Pedir orçamento. |
| Clinicorp IA (opcional) | R$ 299/mês, sem fidelidade | Não recomendado no início. |
| Cloudia (opcional) | preço à parte | Chatbot de marcação 24 h (WhatsApp, Instagram, site) e NPS. |

Total provável: **≈ R$ 410/mês** (Premium + mensagens) + implantação.

## Divisão de trabalho: a dona gere, a Pacheco Studios constrói

**Nativo da Clinicorp Premium (só configurar):** marcação online, confirmação e lembrete por WhatsApp, remarcação e cancelamento que atualizam a agenda, programação de retornos, aniversariantes, orçamentos em aberto, régua de cobrança, recibos e nota fiscal, assinatura eletrónica.

**Construído por nós (Make ou n8n, via API):**
1. Pedido de avaliação Google no dia seguinte à consulta.
2. Sequência de seguimento de orçamentos, se a nativa não chegar.
3. Relatório mensal automático para a dona (consultas, faltas, orçamentos fechados, avaliações novas).
4. Site ligado ao link de marcação da Clinicorp.

**Entregável para ela ser autónoma:** manual curto com rotina diária e semanal, vídeos de 2 min por tarefa, e um mês de acompanhamento.

## Notion e Brevo com a Clinicorp

- **Clinicorp** passa a ser a única fonte dos dados dos pacientes (agenda, prontuário, orçamentos). Não se duplicam pacientes noutro sistema: dados de saúde (LGPD) e risco de dados desatualizados.
- **Notion:** sai da operação da clínica. Fica para o manual da dona e para o painel interno da Pacheco Studios (estado das automações, pedidos de alteração).
- **Brevo:** opcional. O WhatsApp, o SMS e os lembretes por e-mail ficam na Clinicorp. Só se usa o Brevo se ela quiser e-mail marketing (dicas mensais, reativação de pacientes sem consulta há 12 meses), com consentimento.

Fontes: clinicasyspro.com.br/clinicasyspro-vs-clinicorp.html · clinicorp.com/planos · clinicorp.com/post/notificacoes-whatsapp · clinicorp.com/post/agenda-online-clinicorp · clinicorp.com/clinicorp-ia · clinicorp.com/post/lembretes-de-cobranca · cloudia.com.br/integracao/clinicorp · sistema.clinicorp.com/api-docs
