# Checklist de execução — sistema da Dra. Angélica

Do passo 1 até à entrega. Arquitetura em `research/dra-angelica-sistema.md`. Marca `[x]` à medida que avanças.

## 0. Venda e acordo
- [ ] 1. Apresentar a demo do site e a proposta do sistema (comparar com a Clinicorp: ≈ R$ 410 + R$ 299 de IA por mês).
- [ ] 2. Proposta escrita: preço por fase + mensalidade, prazos, âmbito (fora: prontuário e nota fiscal).
- [ ] 3. Contrato: licença de uso do sistema, os dados são da clínica, suporte e tempo de resposta, cláusula de operador de dados (LGPD).
- [ ] 4. Receber o sinal.
- [ ] 5. Recolher com ela:
  - fotos originais;
  - validação dos textos do site;
  - horário semanal e folgas;
  - duração de cada tipo de consulta;
  - convénios e formas de pagamento;
  - o que conta como urgência;
  - link de avaliação do Google;
  - lista de pacientes atuais com telefone (só com consentimento).

## 1. Contas e infraestrutura (começar já: a Meta demora)
- [ ] 6. Meta Business Manager **em nome da clínica** + verificação da empresa.
- [ ] 7. Decidir o número: o atual em coexistência com a app WhatsApp Business, ou um número novo.
- [ ] 8. App no Meta for Developers → WhatsApp Cloud API → token permanente (utilizador de sistema) → webhook.
- [ ] 9. Submeter os modelos de mensagem em pt-BR:
  - confirmação;
  - lembrete D-1 com botões;
  - lembrete 2 h antes;
  - avaliação;
  - seguimento de orçamento;
  - retorno aos 6 meses;
  - aniversário;
  - reativação.
- [ ] 10. VPS Hostinger KVM 2 em São Paulo com o template do n8n, subdomínio com HTTPS, 2FA e backups semanais do VPS.
- [ ] 11. Projeto Supabase na região sa-east-1 (São Paulo).
- [ ] 12. Chave da API do Claude com limite de gasto mensal.
- [ ] 13. Serviço de transcrição de áudio (a API do Claude não recebe áudio; por exemplo, Whisper).
- [ ] 14. Brevo: conta e domínio de envio autenticado (SPF, DKIM, DMARC).
- [ ] 15. Domínio do site + Netlify.
- [ ] 16. Cofre de palavras-passe com todos os acessos; contas em nome da clínica sempre que possível.

## 2. Base de dados (Supabase)
- [ ] 17. Tabelas:
  - pacientes, consentimentos;
  - tipos_consulta, horario_semana, bloqueios;
  - marcacoes;
  - orcamentos, orcamento_eventos;
  - conversas, mensagens;
  - avaliacoes;
  - alertas, log_automacoes.
- [ ] 18. Regra na base de dados que impede duas marcações sobrepostas.
- [ ] 19. Função "horários livres" (tipo de consulta + dia → lista de horas).
- [ ] 20. RLS: só a dona e o serviço têm acesso. Sem dados clínicos.
- [ ] 21. Backup diário + exportação em CSV.
- [ ] 22. Dados de teste.

## 3. Fase 1 — Núcleo
- [ ] 23. Painel no Lovable ligado ao Supabase:
  - login da dona;
  - agenda do dia e da semana;
  - marcar, remarcar, cancelar;
  - "compareceu" e "faltou";
  - pacientes;
  - folgas.
- [ ] 24. Painel instalável no telemóvel (PWA) + código exportado para o GitHub.
- [ ] 25. Marcação no site: tratamento → horário livre → nome, telefone e consentimento → marcação criada.
- [ ] 26. n8n: confirmação imediata por WhatsApp.
- [ ] 27. n8n: lembrete D-1 com botões Confirmar / Remarcar; a resposta atualiza a agenda.
- [ ] 28. n8n: lembrete 2 h antes.
- [ ] 29. n8n: aviso à dona quando alguém cancela ou pede para remarcar.
- [ ] 30. Workflow de erros: qualquer falha avisa-te por WhatsApp ou e-mail.
- [ ] 31. Agenda do dia exportável em PDF (o "modo papel", se algo falhar).
- [ ] 32. Teste ponta a ponta com números de teste → a dona experimenta → correções.

## 4. Fase 2 — Recepcionista IA
- [ ] 33. Base de conhecimento: tratamentos, primeira consulta, medo, dor, morada, horário, convénios (só dados confirmados).
- [ ] 34. Prompt em pt-BR com a voz da Dra. Regras:
  - apresenta-se como assistente virtual;
  - nunca diagnostica;
  - nunca dá preços;
  - dor ou urgência → passa logo à dona;
  - pede consentimento no primeiro contacto.
- [ ] 35. Ferramentas do agente: ver_horarios, criar_marcacao, remarcar, cancelar, passar_a_dona.
- [ ] 36. Memória da conversa no Supabase; respeitar a janela de 24 h do WhatsApp.
- [ ] 37. Áudios: transcrever → o agente responde ao texto.
- [ ] 38. Triagem: cada conversa aparece no painel com um resumo de uma linha e uma etiqueta.
- [ ] 39. Botão "eu assumo" no painel: pausa a IA naquela conversa.
- [ ] 40. Bateria de 40 conversas simuladas:
  - paciente com medo;
  - dor forte;
  - pedido de preço;
  - fora de horas;
  - áudio;
  - remarcação;
  - spam.
- [ ] 41. A Dra. revê as respostas e aprova o tom.
- [ ] 42. Uma semana em modo rascunho (a IA sugere, a dona envia) → depois modo automático.

## 5. Fase 3 — Retenção
- [ ] 43. Pedido de avaliação no Google no dia seguinte a "compareceu".
- [ ] 44. Orçamentos:
  - a dona dita um áudio;
  - a IA escreve o orçamento;
  - a dona aprova e é enviado;
  - seguimentos em D+3, D+7 e D+15;
  - estado aceite ou recusado.
- [ ] 45. Retorno aos 6 meses.
- [ ] 46. Aniversários.
- [ ] 47. Reativação aos 12 meses sem consulta (WhatsApp + e-mail Brevo, só com consentimento).
- [ ] 48. "Responda SAIR" em todas as mensagens de marketing, e a saída fica registada.

## 6. Fase 4 — Relatórios
- [ ] 49. Relatório mensal no dia 1:
  - consultas, faltas, orçamentos fechados, avaliações novas e horários vazios;
  - resumo pela IA + 3 sugestões concretas;
  - enviado por e-mail pelo Brevo.
- [ ] 50. Respostas a avaliações: rascunho pela IA, aprovado pela dona. A API do Perfil de Empresa da Google precisa de pedido de acesso; sem ele, a dona cola a avaliação no painel.

## 7. LGPD e entrega
- [ ] 51. Política de privacidade no site + termo de consentimento + registo das operações de tratamento.
- [ ] 52. Importar os pacientes atuais (só com consentimento).
- [ ] 53. Manual no Notion com a rotina diária e semanal + vídeos de 2 min por tarefa.
- [ ] 54. Sessão de formação com a dona.
- [ ] 55. Ida ao ar: site com marcação real, WhatsApp no número oficial, remover o banner de demonstração.
- [ ] 56. 30 dias de acompanhamento: rever as conversas da IA todas as semanas e afinar o prompt.
- [ ] 57. Entregar à clínica a lista de acessos e registar tudo no PLAYBOOK.

## 8. Operação contínua (mensalidade)
- [ ] 58. Todos os meses: rever os alertas de erro, as conversas da IA e os custos das APIs; atualizar o n8n.
- [ ] 59. A cada trimestre: testar a reposição de um backup.
- [ ] 60. Pedir à dona feedback e novas automações → propor como extra.
