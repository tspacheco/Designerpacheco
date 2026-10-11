# Guião para a mesa · autoridade da Pacheco Studios

Para chegar ao decisor das empresas do lote 1 e das próximas. Ficheiros: `saida/brief-ro.pdf` (o que se envia), `saida/brief-pt.pdf` (para ler), `gerar.py --pentru "Nome"` (brief com o nome da empresa na capa).

## A ideia em 3 frases (dizer sempre igual)
1. A mudança da IA está a acontecer agora: empresas dos EUA e da China já conduzem operações com sistemas de IA com regras claras e uma pessoa na decisão.
2. Na Roménia só 5% das empresas usam IA (Eurostat, 2025). Quem começa hoje fica à frente dos outros 95%.
3. Nós damos clareza, caminho e estrutura a partir da situação de hoje: um mapa, 3 soluções rápidas sem custo e, depois, a auditoria com um piloto de 30 dias medido.

## As 3 provas que levas
1. **O brief** (2 páginas, RO). Só números com fonte: Stanford AI Index 2025, Eurostat 2025, Klarna fev. 2024. Envia-se quando respondem ou quando pedem «o documento».
2. **O mini-mapa da empresa** (1 página). Percurso público → hipótese em pergunta → limite humano → prioridade 30 dias. Faz-se em 30 minutos antes da reunião, com o gerador (`gerador.html`, tipo de negócio) e a secção 02 do brief como modelo.
3. **Um quick win feito à frente deles.** Exemplos: cartaz QR de avaliações gerado na hora (/afis), as 5 respostas rápidas escritas em 10 minutos, o formulário de pedido com as perguntas certas. Prova que «implementamos em dias» é verdade.

## O caminho até à mesa numa empresa grande
1. **Hoje:** DM no Instagram à conta (lote 1). Pede sempre um nome ou um endereço.
2. **Dias 2–3, em paralelo:** LinkedIn ao dono da função. Funções a procurar: Director Operațiuni, Head of Customer Experience, Director Transformare Digitală, Head of E-commerce, Head of Marketplace; nas agências, fundador ou COO. Mensagem de 4 linhas (abaixo) com o brief anexado.
3. **Resposta:** enviar o mini-mapa e pedir uma hora com quem conhece o percurso.
4. **Reunião (45 min):** 10 min a ouvir («conta-me como foi ontem um pedido típico», e depois «e depois?»), 10 min do mapa, 15 min a escolher os 3 quick wins, 5 min a combinar o dia 0 e quem é o responsável do lado deles.
5. **Até 10 dias:** 3 quick wins entregues e medidos. Só então a proposta da AI Systems Audit com preço, e o piloto de 30 dias.

### Mensagem de LinkedIn (RO, 4 linhas)
> Bună ziua, [Nume]! Sunt Tomás, de la Pacheco Studios, din Iași. Am parcurs traseul public al unui client [Companie] ([percurso]) și am o ipoteză de diagnostic, nu o concluzie: [pergunta]. Am pus-o pe o mini-hartă de o pagină și pot implementa fără cost 3 soluții rapide ca să o testăm. Atașez un document scurt despre ce înseamnă un sistem AI în operațiuni, azi. Ați fi deschis la o întâlnire scurtă? Voi fi pregătit.

## Os primeiros 90 segundos na reunião
**RO:** «Mulțumesc pentru timp. Pe scurt: companiile din SUA și China își conduc deja operațiunile cu sisteme AI cu reguli clare și cu un om la decizie. În România, 5% dintre firme folosesc AI. Nu am venit să vă spun că aveți o problemă. Am desenat traseul public al unui client de-al vostru și am o ipoteză. Vreau să o validăm împreună și să implementăm 3 soluții rapide, fără cost, ca să vedeți cum lucrăm. Apoi decideți voi.»

**PT:** «Obrigado pelo tempo. Em resumo: as empresas dos EUA e da China já conduzem as operações com sistemas de IA com regras claras e uma pessoa na decisão. Na Roménia, 5% das empresas usam IA. Não vim dizer que têm um problema. Desenhei o percurso público de um cliente vosso e tenho uma hipótese. Quero validá-la convosco e implementar 3 soluções rápidas, sem custo, para verem como trabalhamos. Depois decidem.»

## Objeções e respostas (RO)
| Objeção | Resposta |
|---|---|
| «Avem departament IT / un integrator.» | «Nu înlocuim IT-ul. Noi desenăm predările și regulile; implementează IT-ul sau implementăm noi împreună cu ei. Harta e utilă oricum.» |
| «Suntem într-un sector reglementat.» | «Nu atingem decizii clinice, de credit sau juridice. Lucrăm pe partea administrativă, cu om la limită și cu trasabilitate.» |
| «De ce o firmă mică din Iași?» | «Pentru că pornim de la traseul vostru public, arătăm în 10 zile, nu în 10 luni, și nu cerem nimic până atunci. Nu promitem. Arătăm.» |
| «Cât costă?» | «Prima lună, harta și cele 3 soluții, nu costă. Auditul are preț și vi-l spun după ce vedeți cele 3 soluții.» (Nunca preço por DM.) |
| «Trimiteți un e-mail.» | «Trimit, cu harta. Cui ar fi cel mai util să ajungă?» (obter o nome) |
| «Folosim deja AI.» | «Perfect. Atunci întrebarea e unde se pierde contextul între unelte și echipe. Exact asta arată harta.» |
| «Nu e momentul.» | «Înțeleg. Vă las documentul. Când apare un proiect nou, harta se face în câteva zile.» |

## Para as próximas empresas (30 minutos por empresa)
1. Percorrer o percurso público como cliente: site, app, Instagram, telefone. Escrever 5 ou 6 passos.
2. Hipótese em forma de pergunta (gerador: escolher o tipo de negócio e ajustar).
3. Escolher 3 quick wins do menu (secção 04 do brief ou `COMISSAO-PARCEIROS.md`).
4. Decisor: função e nome no LinkedIn. Guardar na coluna Notas da folha.
5. Brief com o nome da empresa: `python3 autoridade/gerar.py --pentru "Nome"`.
6. DM pelo gerador, linha no Excel, follow-up em 4 dias.

## Regras que não se quebram
- Sem preço e sem minutos na 1.ª mensagem; sem emojis; em romeno «Voi fi pregătit.»
- Hipótese, nunca acusação. Só números com fonte e data.
- Sector regulado: nada de decisões clínicas, de crédito ou jurídicas na proposta.
- Um follow-up e parar. Voltar só com motivo novo.
