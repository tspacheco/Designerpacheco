# Prospeção no Instagram

Base: guia «Pesquisa de Instagram e Prospecção Estratégica» do Tomás (10/10/2026). Este thread trata do Instagram; os e-mails ficam no thread «Pesquisa de e-mails com n8n» (`research/prospecao/`, outro ramo). As categorias usam os mesmos ids (`influenciador`, `grande`, `pme_parceiro`, `comunidade`) para as duas bases se juntarem.

## Ficheiros
- `prospecao-instagram.xlsx` — base de dados. Folhas: Prospeção (nota e prioridade por fórmula, listas de Categoria, Estado, Canal e Língua), Categorias, Mensagens, Percursos, Queries, Estados, Linguagem.
- `gerador.html` — página para o telemóvel: escolher o tipo de conta, escrever o gancho, e sai a DM, o follow-up (e os comentários, nas comunidades) já com as regras. Botão «Copiar linha p/ Excel».
- `MENSAGENS.md` — todos os modelos, por categoria e língua.
- `contas.json` — contas da pesquisa (entrada do `gerar.py`).
- `dados.py` — fonte única de modelos, percursos e queries. Mudar aqui e correr `python3 gerar.py`.

## Análise que gera a mensagem (por conta)
1. **Categoria numa frase.** Se não consigo explicar porque está nesta categoria, não entra.
2. **Sinais públicos.** Bio, posts, destaques, link na bio, site, LinkedIn. Procurar os termos da folha Queries (`programări`, `rezervări`, `app`, `locations`, `team`...). Duas fontes no mínimo.
3. **Percurso.** Escolher o tipo de negócio no gerador e ajustar ao que a conta mostra: `entrada → contexto → decisão → handoff → entrega → próxima ação`.
4. **Pergunta de hipótese.** O handoff com mais pessoas ou mais contexto vira pergunta («Ce context trebuie să ajungă...?»). Nunca afirmar um problema.
5. **Gancho.** Um facto concreto e recente da conta: um post, um serviço novo, um evento, uma abertura. É o que prova que a mensagem não é em massa.
6. **Nota 0–10.** Encaixe 0–3, acesso 0–2, complexidade 0–3, prova 0–2. 8–10 → prioridade 5; 6–7 → 4; 4–5 → 3; 2–3 → 2; 0–1 → observar.
7. **Tom e língua.** Influenciadores e comunidades: «tu». Grandes negócios e agências: formal. Língua da conta.
8. **Mensagem.** O gerador junta saudação (roda), gancho, percurso, pergunta e o pedido proporcional da categoria. Verifica campos em falta e palavras a evitar.

## Primeiro passo por categoria
| Categoria | Canal | Ativo | Pedido |
|---|---|---|---|
| Influenciador / operador | DM | Partner Systems Opportunity Map (3–5 handoffs, 1 hipótese, limite humano, prioridade 30 dias), sem custo | Conversa curta |
| Grande negócio | DM + LinkedIn do decisor | Mini-mapa de uma página de um percurso público | Quem na equipa valida (operações, CX, transformação) |
| PME / parceiro | DM ao fundador | Mini-mapa de um cliente-tipo da agência | Reunião de complementaridade |
| Página / comunidade | Comentários em 2–3 posts, depois DM | Contribuição pública útil | Tema para artigo, workshop ou evento |

## Regras de envio
- 1 minuto entre mensagens; saudação diferente em cada uma; sem emojis; sem preço; em romeno fecha com «Voi fi pregătit.»
- Follow-up 4 dias depois, uma vez, sempre com uma coisa nova. Sem resposta → Estado «Sem resposta» e parar.
- Comunidades: 7 dias entre interações; nada de proposta nos comentários.
- Pedido: «uma reunião» ou «uma conversa curta», sem minutos (regra das mensagens de 10/10).
- Saúde, banca, seguros: fora da proposta inicial qualquer decisão clínica, de crédito ou jurídica.

## Pesquisa
O Instagram não abre a partir das sessões: o @ vem do site oficial, do Google ou de notícias, e fica «a confirmar» até o Tomás o ver no telemóvel. Primeira ronda (11/10): 17 contas, todas com @ a confirmar (ver `contas.json`). Próxima ronda: pesquisa por nome («<nome> instagram») ou ler o rodapé do site oficial pela PONTE (`pagina <url>`).

Para pedir a análise de uma conta a um thread: mandar o @ e 2–3 capturas (bio, um post recente, destaques). O thread devolve a linha da folha e a mensagem.

## n8n (mais à frente)
O Instagram não permite DMs automáticas a quem não escreveu primeiro, por isso o n8n não envia a 1.ª mensagem. O que faz: ler a folha (Google Sheets), mandar ao Tomás a fila do dia com o texto pronto e o link `ig.me/m/<conta>`, lembrar follow-ups vencidos e as comunidades a comentar. O fluxo base já existe em `research/prospecao/n8n/` no ramo dos e-mails.
