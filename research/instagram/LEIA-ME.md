# Prospeção no Instagram

Base: guia «Pesquisa de Instagram e Prospecção Estratégica» do Tomás (10/10/2026). Este thread trata do Instagram; os e-mails ficam no thread «Pesquisa de e-mails com n8n» (`research/prospecao/`, outro ramo). As categorias usam os mesmos ids (`influenciador`, `grande`, `pme_parceiro`, `comunidade`) para as duas bases se juntarem.

## Ficheiros
- `prospecao-instagram.xlsx` — base de dados. Folhas: Prospeção (nota e prioridade por fórmula, listas de Categoria, Estado, Canal e Língua), Categorias, Mensagens, Percursos, Queries, Estados, Linguagem.
- `gerador.html` — página para o telemóvel: escolher o tipo de conta e o tipo de negócio, escrever o gancho, e sai o Micro System Print de uma página, a DM com a isca, a cadência D4, D7 e D12, a «Triagem», a «Parceria» e o «Testemunho» (e os comentários, nas comunidades), já com as regras. Botão «Copiar linha p/ Excel».
- `MENSAGENS.md` — todos os modelos, por categoria e língua.
- `contas.json` — contas da pesquisa (entrada do `gerar.py`).
- `dados.py` — fonte única de modelos, percursos e queries. Mudar aqui e correr `python3 gerar.py`.

## Análise que gera a mensagem (por conta)
1. **Categoria numa frase.** Se não consigo explicar porque está nesta categoria, não entra.
2. **Sinais públicos.** Bio, posts, destaques, link na bio, site, LinkedIn. Procurar os termos da folha Queries (`programări`, `rezervări`, `app`, `locations`, `team`...). Duas fontes no mínimo.
3. **Percurso.** Escolher o tipo de negócio no gerador (12 tipos, incluindo restauração, marcações e construção, os 3 setores prioritários do playbook) e ajustar ao que a conta mostra: só canais observados.
4. **Pergunta de hipótese.** O handoff com mais pessoas ou mais contexto vira pergunta («Quando entra uma reserva, existe um único dono até à confirmação?»). Nunca afirmar um problema.
4b. **Isca.** O que já é possível hoje, em pergunta, nas palavras do Tomás adaptadas ao nicho: «Hoje tem uma IA que responde às FAQ da sua diretriz?», «O seu sistema capta, qualifica e filtra e só pede a sua decisão no que importa?», «O atendimento custa-lhe menos de 1 hora por dia?». A DM fecha com «se não, faça uma triagem connosco».
4c. **Micro System Print.** O gerador monta a página com o tipo de negócio (título, passo a validar, 3 validações, métrica, 1 quick win). Rever antes de enviar; no Instagram vai como captura de ecrã.
5. **Gancho.** Um facto concreto e recente da conta: um post, um serviço novo, um evento, uma abertura. É o que prova que a mensagem não é em massa.
6. **Nota 0–10.** Encaixe 0–3, acesso 0–2, complexidade 0–3, prova 0–2. 8–10 → prioridade 5; 6–7 → 4; 4–5 → 3; 2–3 → 2; 0–1 → observar.
7. **Tom e língua.** Influenciadores e comunidades: «tu». Grandes negócios e agências: formal. Língua da conta.
8. **Mensagem.** O gerador junta saudação (roda), gancho, percurso, pergunta e o pedido proporcional da categoria. Verifica campos em falta e palavras a evitar.

## Ângulo (11/10)
A mudança da IA está a acontecer agora: empresas dos EUA e da China já conduzem operações com sistemas de IA com regras claras e uma pessoa na decisão; na Roménia só 5% das empresas usam IA (Eurostat, 2025). Damos clareza, caminho e estrutura a partir da situação de hoje.

## Triagem proativa (playbook de 11/10, secção A.14)
A triagem é a isca e é conduzida por nós: observar o percurso público, levar uma hipótese concreta e um Micro System Print de uma página (com pelo menos 1 quick win à vista) e pedir só a validação com o decisor. Nunca formulário, nunca minutos, nunca afirmar falhas internas sem dados. Cadência: D0 DM → D4 observação nova → D7 pergunta sim ou não → D12 fecho limpo. Original em `/mnt/project-files/playbook/pacheco-studios-playbook-triagem-proativa.pdf`. Prova: `autoridade/saida/brief-ro.pdf` (números com fonte) e `autoridade/GUIAO-MESA.md` (caminho até ao decisor, objeções, checklist para as próximas empresas).

## Primeiro passo por categoria
| Categoria | Canal | Ativo | Pedido |
|---|---|---|---|
| Influenciador / operador | DM | Micro System Print com 1 quick win à vista; 3 quick wins sem custo depois da validação | «Faz uma triagem connosco» → validação → auditoria |
| Grande negócio | DM + LinkedIn do decisor | Micro System Print de um percurso público do cliente | Quem valida (operações, CX, transformação) → validação → 3 quick wins → auditoria |
| PME / parceiro | DM ao fundador | Micro System Print de um cliente-tipo; 3 quick wins sem custo na operação da agência | «Façam uma triagem connosco» → validação → auditoria |
| Página / comunidade | Comentários em 2–3 posts, depois DM | Contribuição pública útil | Tema para artigo, workshop ou evento |

## Escada comercial (playbook de consultoria, 11/10)
Triagem conduzida por nós (print + validação) → 3 quick wins sem custo → Auditoria de Sistemas com IA (porta de entrada; **creditada na implementação**: grátis na execução, paga quando vira prova e início de trabalho) → sprint de desenho → piloto controlado → otimização. Ticket 2.000 € (3 quick wins sobre problemas atuais) a 100.000 € (acompanhamento de crescimento 3x a 10x, pago pelo valor agregado); foco na prova de valor, nunca escrito numa DM. Sites e mensalidades só existem dentro da implementação. Parceiros (decisões 14h38 e 14h44): 3 quick wins sem custo; 15 % do valor da implementação do negócio indicado e, no fim de cada trimestre, 5 % dos nossos ganhos com ele enquanto trabalharmos juntos; primeiro o incentivo e a proposta assinada (mensagem «Parceria», antes de aplicar os quick wins); contrapartida por ordem: testemunho online e recomendação no dia em que os quick wins funcionam (mensagem «Testemunho»), boca a boca, 1 menção por mês. Nada se envia a influenciadores sem o Tomás confirmar os @ e o texto. Detalhe em `COMISSAO-PARCEIROS.md`. Playbook: `/mnt/project-files/playbook/`.

## Regras de envio
- 1 minuto entre mensagens; saudação diferente em cada uma; sem emojis; sem preço; em romeno fecha com «Voi fi pregătit.»
- Cadência D4, D7, D12, sempre com uma coisa nova (observação, pergunta de sim ou não, fecho limpo). Sem resposta depois do D12 → Estado «Sem resposta» e parar. A folha calcula as três datas.
- DM até 1000 caracteres (limite do Instagram); o gerador avisa. O print vai como imagem.
- Comunidades: 7 dias entre interações; nada de proposta nos comentários.
- Pedido: «uma reunião», «uma validação» ou «uma conversa curta», sem minutos (regra das mensagens de 10/10, reforçada a 11/10). Nunca pedir que preencham uma triagem ou um formulário.
- Saúde, banca, seguros: fora da proposta inicial qualquer decisão clínica, de crédito ou jurídica.

## Pesquisa
O Instagram não abre a partir das sessões: o @ vem do site oficial, do Google ou de notícias, e fica «a confirmar» até o Tomás o ver no telemóvel. Primeira ronda (11/10): 17 contas, todas com @ a confirmar (ver `contas.json`). Próxima ronda: pesquisa por nome («<nome> instagram») ou ler o rodapé do site oficial pela PONTE (`pagina <url>`).

Para pedir a análise de uma conta a um thread: mandar o @ e 2–3 capturas (bio, um post recente, destaques). O thread devolve a linha da folha e a mensagem.

## n8n (mais à frente)
O Instagram não permite DMs automáticas a quem não escreveu primeiro, por isso o n8n não envia a 1.ª mensagem. O que faz: ler a folha (Google Sheets), mandar ao Tomás a fila do dia com o texto pronto e o link `ig.me/m/<conta>`, lembrar follow-ups vencidos e as comunidades a comentar. O fluxo base já existe em `research/prospecao/n8n/` no ramo dos e-mails.
