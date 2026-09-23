# Dra. Angélica Lauermann — dentista · análise de prospeção (23/09/2026)

**Fontes pedidas pelo Tomás:** ficha Google Maps `maps.app.goo.gl/bAHQ47hZ5U6DDTRY9` · Instagram `@dra.angelicalauermann`.
**Estado das fontes nesta sessão:** Google Maps, Instagram e os motores de pesquisa externos estão **bloqueados pelo proxy de rede (política da organização)** — não é uma limitação minha, é um bloqueio a montante que não contorno. A pesquisa web disponível (WebSearch) não devolve nenhum resultado para o nome; o único rasto do apelido Lauermann em odontologia é no Brasil (RS), o que sugere uma profissional brasileira. **Tudo o que está abaixo sobre a clínica em si é hipótese até ver a ficha e o perfil.** Para a análise profunda, o Tomás envia capturas: ficha Maps (cabeçalho, horário, fotos, 10 primeiras avaliações e a resposta ou ausência de resposta), perfil Instagram (bio, link, contagens, últimos 9 posts, destaques).

**O que o caller viu (dados fiáveis):** sem site → os pacientes não verificam credenciais nem serviços; sem agendamento online → atrito para pacientes novos. Setor: odontologia.

## 1. O que uma dentista sem site nem agenda online perde, em concreto

1. **Pesquisa "dentista + zona"**: sem site, a ficha Google é a única porta. Sem link, sem fotos boas, sem respostas às avaliações, a ficha perde para as clínicas de cadeia (OralMED, Vitacentro) que dominam as pesquisas locais em Portugal.
2. **Verificação de credenciais**: em Portugal o paciente procura a **cédula da Ordem dos Médicos Dentistas (OMD)**; se for brasileira, o reconhecimento do diploma e a inscrição na OMD são a primeira pergunta. Um site que mostre cédula, formação e especialidades resolve a objeção antes da chamada.
3. **Marcação**: hoje a marcação passa pelo telefone ou pelo DM do Instagram. Uma chamada perdida em consulta = paciente perdido. DMs sem resposta em 1 h = paciente que marca noutro sítio.
4. **Faltas e desistências**: sem lembretes automáticos, uma agenda de dentista perde 10–20 % das consultas. É dinheiro direto.
5. **Instagram sem funil**: posts educativos e antes/depois geram interesse mas não há um caminho "post → marcar". O link da bio deve ir para a marcação, não para o perfil.

## 2. Workflows por prioridade (o que construir primeiro e porquê)

| # | Workflow | O que faz | Porquê primeiro | Ferramenta |
|---|---|---|---|---|
| 1 | **Ficha Google + motor de avaliações** | Ficha completa (categoria, serviços, horário, fotos, link), pedido de avaliação automático 2 h depois da consulta por SMS/WhatsApp, resposta a todas as avaliações | É a fonte nº 1 de pacientes novos numa profissão de confiança; custo quase zero; resultados em semanas | HighLevel Reputation (ou Make + Brevo) |
| 2 | **Site de ficheiro único** | Credenciais (cédula OMD, formação), serviços com preços "a partir de", antes/depois, FAQ (dor, orçamento, seguros/ADSE, parcelamento), botão "Marcar" e WhatsApp em todo o lado, JSON-LD `Dentist` | Responde ao que o caller detetou: verificar credenciais e serviços. Sem site não há onde apontar a ficha, o Instagram nem os anúncios | Engine Pacheco Studios (HTML único, Netlify) |
| 3 | **Agendamento online** | Calendário com tipos de consulta (avaliação, limpeza, urgência), confirmação automática, lembrete 24 h e 2 h, reagendamento por link | Tira o atrito de marcar; reduz faltas; liberta a dentista do telefone durante as consultas | HighLevel Calendars (ou Calendly + Make como fallback) |
| 4 | **Chamada perdida → SMS/WhatsApp automático** | "Estou em consulta. Marque aqui: [link] ou responda a esta mensagem" | Uma dentista sozinha perde chamadas por definição; recupera 30–50 % dos contactos | HighLevel Missed-Call Text-Back |
| 5 | **Instagram → marcação** | Link da bio para a página de marcação; resposta automática a DMs e comentários com palavra-chave ("orçamento", "clareamento") → link + pergunta de qualificação | Converte o público que já existe; sem isto os posts são só vaidade | HighLevel Conversations (IG DM) ou ManyChat |
| 6 | **Reativação de pacientes** | Aos 6 meses sem consulta: mensagem "está na altura da revisão" com link para marcar; campanhas sazonais (clareamento antes do verão, check-up de regresso às aulas) | Receita recorrente com a base que já existe; custo marginal zero | HighLevel Workflows + tags |
| 7 | **Pipeline de orçamentos** | Cada orçamento entregue entra num pipeline (enviado → seguimento 3 dias → aceite/perdido); seguimento automático | Em odontologia o dinheiro grande está nos tratamentos (implantes, ortodontia) que ficam "a pensar" | HighLevel Opportunities |

Ordem de venda sugerida: **2 + 3 juntos** (site com marcação) como pacote de entrada; 1 e 4 no primeiro mês de gestão; 5, 6 e 7 como mensalidade.

## 3. O que confirmar com as capturas / na chamada

- **Onde é a clínica** (zona, se é consultório próprio ou aluga gabinete numa clínica), horário real, telefone, se aceita seguros/ADSE.
- **Cédula OMD** e especialidades (estética, ortodontia, implantes, odontopediatria?). Se for brasileira, se já tem reconhecimento e inscrição.
- **Avaliações**: quantas, média, última data, se responde. Menos de 10 avaliações → workflow 1 é urgente.
- **Instagram**: seguidores, frequência, tipo de conteúdo (educativo, antes/depois, pessoal), link da bio, se responde a comentários. Se tem mais de 1 000 seguidores e zero funil, o workflow 5 tem retorno imediato.
- **Como marca hoje**: telefone? WhatsApp? DM? Quem atende quando ela está em consulta?
- **Software clínico** que já usa (se usa) para não duplicar agenda.

## 4. Pitch em duas frases (para a chamada)

"Hoje quem a encontra no Google não tem onde ver a sua cédula nem os seus serviços, e quem quer marcar tem de lhe ligar enquanto está em consulta. Eu monto-lhe o site com marcação online numa semana, e ligo-lhe a ficha Google e o Instagram para que marcar seja um clique — e as faltas caem com os lembretes automáticos."

## 5. Restrições HONEST-DATA para o site

Nada de ratings, número de pacientes, preços ou citações inventados. Cédula, formação e serviços vêm da dentista. Antes/depois só com consentimento escrito do paciente (RGPD e regras da OMD sobre publicidade em saúde — verificar o Regulamento de Publicidade da OMD antes de publicar promoções ou preços).
