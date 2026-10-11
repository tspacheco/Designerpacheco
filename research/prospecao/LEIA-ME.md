# Prospeção por Instagram e e-mail (ligada ao n8n)

Base: guia «Pesquisa de Instagram e Prospecção Estratégica» do Tomás (10/10/2026). Quatro categorias, cada uma com a sua abordagem e o seu intuito; nota 0–10 que dá a prioridade 1–5; estados do pipeline.

## Onde está cada coisa
- **Base de dados (Excel):** `/mnt/project-files/prospecao/prospecao-base.xlsx` (pasta privada do projeto). Tem e-mails de negócios, por isso **nunca vai para este repositório** (é público).
- **Contas em bruto (JSON):** `/mnt/project-files/prospecao/contas-AAAA-MM-DD.json`.
- **Ferramentas (aqui):**
  - `mensagens.py` — modelos de mensagem por categoria e língua (RO, PT, EN): DM, e-mail com assunto e rodapé «STOP», follow-up, arranques de comentário. Em romeno fecha sempre com «Voi fi pregătit.»
  - `gerar_base.py` — JSON → Excel com abas Prospeção, Top 5, Comentários e Guia (nota e prioridade por fórmula, listas de Estado/Canal/Categoria).
  - `n8n/prospecao-n8n.json` — fluxo para importar no n8n (gerado por `n8n/gerar_workflow.py`).

## Campos de cada conta (JSON)
`categoria` (influenciador | grande | pme_parceiro | comunidade), `nome`, `nome_curto`, `instagram`, `url_instagram`, `fonte_instagram`, `cidade`, `site`, `linkedin`, `email`, `fonte_email`, `seguidores`, `lingua` (ro | pt | en), `sinais`, `foco`, `razao`, `evidencia`, `decisor`, `score_encaixe` 0–3, `score_acesso` 0–2, `score_complexidade` 0–3, `score_prova` 0–2, e para a mensagem: `gancho` (uma frase, na língua da conta, sobre algo público e concreto), `percurso` (percurso curto a validar), `tema` (comunidades).

Regras de dados: @ e e-mail só com prova pública (URL em `fonte_*`); e-mails só genéricos publicados pelo negócio; nunca seguidores inventados. O container não abre o Instagram: o @ vem do site oficial ou de resultados de pesquisa; o Tomás confirma no telemóvel antes de enviar.

## Análise que gera a mensagem (por conta)
1. Categoria → canal e abordagem do guia (passo 5): influenciador → DM; grande → e-mail/LinkedIn a pedir o dono do processo; PME → e-mail de complementaridade; comunidade → comentário primeiro, DM só depois de 2–3 interações.
2. `sinais` públicos → `percurso` (`entrada → contexto → decisão → handoff → entrega`) → `gancho` com um facto observável.
3. Modelo da categoria + gancho + percurso → mensagem. Linguagem do guia: hipótese a validar, nunca acusação; nada de «automação total».

## Fluxo no n8n (`n8n/prospecao-n8n.json`)
Dias úteis às 10h (hora de Iași):
- **E-mails:** lê a folha, envia até 15 por dia (prioridade 4–5, Estado «Validado», canal E-mail), **1 por minuto**, e marca «Contactado» com follow-up a 5 dias. No dia do follow-up envia-o uma vez e marca «Sem resposta».
- **Instagram:** o Instagram não deixa enviar DMs automáticas a quem não escreveu primeiro, por isso o n8n manda ao Tomás, por e-mail, a fila do dia: até 10 DMs com o texto pronto e o link `ig.me` que abre a conversa, os follow-ups vencidos e as comunidades a comentar. O Tomás envia do telemóvel (1 por minuto) e muda o Estado para «Contactado»; no dia seguinte o n8n põe a data e o follow-up.

### O que o Tomás faz do lado dele (uma vez)
1. Subir o `prospecao-base.xlsx` ao Google Drive e abrir com Google Sheets (fica uma folha «Prospeção»).
2. No n8n: Import from File → `prospecao-n8n.json`.
3. Nos 3 nós de Google Sheets: escolher a credencial Google e colar o URL da folha no lugar de `COLAR_URL_DA_FOLHA`.
4. Nos 2 nós de Gmail: escolher a credencial Gmail; no «Enviar fila ao Tomás» pôr o próprio e-mail no lugar de `COLAR_O_TEU_EMAIL`.
5. Testar com «Execute workflow» e só depois ativar.

Credenciais, URL da folha e e-mails ficam só no n8n, nunca aqui.

## Nova pesquisa
Lista longa de 15–25 por categoria (queries na secção «Biblioteca» do guia) → JSON → `python3 gerar_base.py contas.json saida.xlsx` → importar as linhas novas na folha (ID a continuar a numeração).
