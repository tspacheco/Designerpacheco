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
