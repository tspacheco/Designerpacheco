# Sistema à medida da Dra. Angélica — arquitetura (24/09/2026)

Decisão do Tomás: não usar a Clinicorp nem outro software de clínica. A Pacheco Studios constrói o sistema com workflows, APIs e IA, e a dona gere tudo sozinha.

## Limite legal: o prontuário fica fora

- O **prontuário clínico** (anamnese, odontograma, evolução) não entra no sistema. Um prontuário eletrónico sem papel exige certificação (CFO / SBIS) e assinatura digital ICP-Brasil. Continua em papel ou num sistema certificado. Requisito exato a confirmar com o CRO-SP.
- O nosso sistema guarda **só dados administrativos**: nome, telefone, e-mail, consentimentos, marcações, orçamentos (valor e estado), origem do contacto e avaliações. Isto ainda é dado pessoal ao abrigo da LGPD, mas não é dado de saúde detalhado.
- LGPD: consentimento registado no primeiro contacto, base de dados no Brasil (região São Paulo), acesso só da dona, exportar e apagar dados a pedido.

## Peças

| Peça | Ferramenta | Papel |
|---|---|---|
| Base de dados + login | Supabase (região sa-east-1, São Paulo) | Pacientes, marcações, horários, orçamentos, mensagens, consentimentos. Row Level Security. |
| Painel da dona | App web (PWA) instalável no telemóvel | Agenda do dia e da semana, pacientes, orçamentos, conversas, relatório. Um toque para confirmar, remarcar e marcar falta. |
| Marcação online | Página no site ligada ao Supabase | Mostra só horários livres reais; o paciente escolhe e recebe confirmação no WhatsApp. |
| WhatsApp | WhatsApp Business Cloud API (Meta), número dela | Confirmações, lembretes e assistente. Confirmar que o número pode ficar também na app WhatsApp Business (coexistência). |
| Automações | n8n (self-hosted num VPS) ou Make | Lembretes, pós-consulta, orçamentos, retornos, relatórios. |
| IA | API do Claude | Assistente de WhatsApp, transcrição de áudios, rascunhos, relatório mensal. |
| E-mail | Brevo | Lembretes por e-mail, relatório mensal e campanhas com consentimento. |
| Documentação | Notion | Manual da dona e painel interno da Pacheco Studios. Sem dados de pacientes. |

## A força da IA (o que mostra valor)

1. **Recepcionista no WhatsApp 24 h:** responde a dúvidas (tratamentos, localização, primeira consulta), consulta horários livres, marca e remarca, e percebe áudios. Regras fixas: nunca diagnostica, nunca dá preços, e em dor ou urgência passa logo à dona com alerta.
2. **Triagem de mensagens:** cada conversa chega ao painel com um resumo de uma linha e uma etiqueta (marcação, dúvida, urgência, orçamento).
3. **Orçamentos que fecham:** a dona dita um áudio depois da consulta → a IA escreve o orçamento em texto claro para o paciente (a dona aprova antes de enviar) → seguimento em D+3, D+7 e D+15.
4. **Relatório mensal em linguagem simples:** consultas, faltas, taxa de fecho de orçamentos, avaliações novas, horários mortos e 3 sugestões concretas.
5. **Resposta às avaliações Google:** rascunho de resposta a cada avaliação nova, que a dona aprova.

## Fases

| Fase | Entrega | Prazo estimado |
|---|---|---|
| 1. Núcleo | Supabase + painel da dona + marcação online + confirmação e lembrete por WhatsApp (D-1 e 2 h antes) | 3–4 semanas |
| 2. Assistente IA | Recepcionista no WhatsApp + triagem + transcrição de áudios | 2–3 semanas |
| 3. Retenção | Avaliação Google D+1, orçamentos, retorno aos 6 meses, aniversários, reativação aos 12 meses | 2 semanas |
| 4. Inteligência | Relatório mensal IA + respostas a avaliações | 1 semana |

A seguir, um mês de acompanhamento, o manual no Notion e vídeos curtos por tarefa.

## Custos de funcionamento (aproximados, a confirmar)

- Supabase: plano grátis no início; Pro ≈ US$ 25/mês quando entrar em produção (backups).
- VPS para o n8n: ≈ € 5–10/mês.
- WhatsApp Cloud API: a Meta cobra por mensagem de modelo (confirmações e lembretes); respostas dentro de uma conversa aberta pelo paciente são grátis. Ver a tabela de preços da Meta para o Brasil.
- API do Claude: poucos dólares por mês para este volume (~110 consultas por mês).
- Brevo: plano grátis chega para o volume dela.

## Preço para a cliente

- Âncora: a Clinicorp Premium custa ≈ R$ 410/mês + implantação e não tem assistente IA incluído (Clinicorp IA +R$ 299/mês).
- Modelo: **implementação** (valor único por fase) + **mensalidade** que cobre alojamento, custos das APIs, manutenção e suporte. Uma mensalidade abaixo de R$ 410 + 299 é fácil de justificar.
- O sistema fica com a Pacheco Studios (licença de uso). Os dados são da clínica, exportáveis a qualquer momento.

## Riscos a assumir

- **Somos o suporte:** se o sistema falha, a agenda dela para. É preciso monitorização (alerta quando um workflow falha), backups diários e um "modo papel" (agenda do dia exportável em PDF).
- **Verificação da Meta** (Business Manager + número) pode demorar dias: começar já na fase 1.
- **Nota fiscal / recibos:** fora de âmbito; continua com o contabilista ou o sistema da prefeitura.
