# Caçador diário de Iași (agente 1)

Pedido do Tomás (08/10/2026): todas as manhãs, às 8h00 de Iași, procurar **50 negócios sem site** e construir a demo de **25**; às 11h30 construir as **outras 25**. Este ficheiro é o guião das duas corridas. Ramo de trabalho: `claude/cacador-diario-nkiz36`. As demos publicam-se no ramo das demos (`claude/dez-negocios-dez-websites-7gevwu`, pasta `sites/<pasta>/` + linha em `DEMOS` do `sites/demos-pachecost/gerar.py`); o projeto Netlify «pachecost-demos» publica sozinho a cada push em `pachecost.com/demo/<slug>/`.

Ler antes da 1.ª corrida de cada dia: `PLAYBOOK.md` (§3, §3-A, §5, §6, §11), `research/iasi-lote4-briefs.md` (estrutura dos sites dos lotes) e este ficheiro.

## Ficheiros

| Ficheiro | Para quê |
|---|---|
| `research/cacador/vistos.tsv` | Todas as fichas abertas, com ou sem site. Nunca abrir duas vezes o mesmo negócio. |
| `research/cacador/AAAA-MM-DD.tsv` | Os 50 do dia: corrida A (25) e B (25), contacto, WhatsApp, estado. |
| `research/cacador/AAAA-MM-DD.md` | Lista para o Tomás, gerada: `python3 research/cacador/mensagens.py research/cacador/AAAA-MM-DD.tsv > research/cacador/AAAA-MM-DD.md` |
| `research/cacador/briefs-AAAA-MM-DD.md` | Fonte display, assinatura visual e funcionalidade de cada site do dia. |
| `research/cacador/fontes-assinaturas.md` | Fontes e assinaturas já usadas pelo caçador (somam-se ao PLAYBOOK §5 e §6 e aos briefs dos lotes 1 a 4). |

## Modo economia (pedido do Tomás, 09/10)

A pesquisa gasta o mínimo; a construção continua com execução completa (nível 10K, skills, crítica). Na pesquisa:

1. Tudo por `cacar.py`, que só imprime contagens. **Nunca** abrir à mão `.html`/`.txt` da ponte, nem imprimir `vistos.tsv`, TSV do dia ou listas inteiras (usar `wc -l`, `cut`, `head -3` quando for mesmo preciso).
2. Pesquisas: `python3 research/cacador/cacar.py pesquisas AAAAMMDD 12` (tira da fila `pesquisas.txt`, com `listamaps`) → commit + push → `bash research/cacador/esperar.sh` (uma chamada, sem sondagens repetidas).
3. `cacar.py lista AAAAMMDD`: lê os cartões das listas (nota, avaliações, categoria, telefone e o botão «Site»). Quem tem domínio próprio sai **sem abrir a ficha**; cadeias, hotéis, farmácias etc. também.
4. `cacar.py fichas AAAAMMDD 25` (op `fichamaps`: ficha **e** fotos num só pedido) → push → `esperar.sh`. Repetir até `cacar.py dia AAAAMMDD` dizer «faltam 0». O `dia` lê o campo «Site» de cada ficha (regra do Gist e do Salon Monne), junta ao `vistos.tsv` e escreve o `AAAA-MM-DD.tsv` com 25 A + 25 B por força.
5. `cacar.py fotos AAAAMMDD A` → push → `esperar.sh`. As fotos ficam diretamente em `sites/<slug>/media/g-NN.webp` (o motor das demos não copia subpastas).
6. Briefs curtos (uma linha por site: fonte, assinatura, funcionalidade) e construtores com `research/cacador/trabalhador.md` por caminho, sem colar regras longas no prompt.
7. Mensagens no thread: só a entrega final de cada corrida, curta. Estado no checklist.

## Corrida A (8h00): pesquisar 50, construir 25

Os passos 2 a 6 abaixo fazem-se com os comandos do modo economia; o texto fica como referência do que cada passo tem de garantir.

1. **Preparar.** `git fetch origin claude/cacador-diario-nkiz36 claude/dez-negocios-dez-websites-7gevwu`; ficar no ramo do caçador e fazer `git merge origin/claude/dez-negocios-dez-websites-7gevwu` (merge, nunca rebase/force). Lista de exclusão: slugs e pastas de `DEMOS`, nomes em `research/iasi-*.md` (lotes 1 a 4) e todo o `vistos.tsv`.
2. **Escolher as pesquisas.** 10 a 14 pesquisas no Maps em categorias **ainda não feitas** (ver `ponte/iasi-*.txt` e a coluna categoria de `vistos.tsv`). As categorias habituais estão quase esgotadas no centro: variar por nicho (ex.: ortopedie, optică, croitorie de mireasă, atelier biciclete, tâmplărie, gresie-faianță, saltele, flori de nuntă, fotograf, cofetărie de nuntă, croitorie, curățătorie, autoșcoală, centru de copiat, vulcanizare, tapițerie auto, laborator dentar, kinetoterapie, sală de fitness mică, pensiune) e por bairro ou comuna à volta (Tătărași, Nicolina, Alexandru cel Bun, Dacia, Galata, Păcurari, Valea Lupului, Miroslava, Tomești, Bucium, Holboca, Popricani, Lunca Cetățuii). URL: `https://www.google.com/maps/search/<termo>+<zona>+Iași?hl=ro`, nome `ponte/cc-AAAAMMDD-<termo>`.
3. **PONTE, ronda 1 (pesquisas).** Escrever os pedidos `pagina` em `.github/ponte.txt`, commit, push no ramo do caçador, esperar o commit «Ponte: …» (1–4 min; ver `ponte/relatorio.txt`). Tirar das listas: nome, nota, nº de avaliações, link da ficha. Filtrar: nota ≥ 4,3, dezenas de avaliações ou mais, sem cadeias/franchisings, fora da lista de exclusão.
4. **PONTE, rondas 2 a 4 (fichas).** Abrir as candidatas em pedidos de **até 25 páginas** (79 de uma vez passou dos 45 min), nome `ponte/cc-AAAAMMDD-f-<slug>`. Em **todas**, ler o campo «Site» (`aria-label="Site: …"` no `.html`): domínio próprio → sai; Facebook, Instagram, MERO, diago, linktree ou nada → fica (presença anotada). Juntar cada ficha aberta ao `vistos.tsv`. Repetir até ter **50 sem site** (contar com ~2 fichas abertas por cada uma que fica). Ler também: telefone, morada, horário, prova de WhatsApp (botão wa.me na ficha; o Facebook pela ponte quando existe). WhatsApp «sim» só com prova pública; senão «?»; fixo (02…/03…) → «não (fixo)».
5. **Dividir.** Ordenar os 50 por força (nota × avaliações, fotos boas). Os 25 melhores são a corrida A, os outros a B. Escrever `AAAA-MM-DD.tsv` (todos com estado «por fazer») e fazer commit + push logo, para a corrida B ter a lista mesmo que a A pare a meio.
6. **Fotos.** Pedidos `fotosmaps cc-AAAAMMDD-fotos-<slug> <link da ficha>` para os 25 (uma ronda), depois `imagem sites/<slug>/media/g/NN.webp <url>=w1600` das melhores 4 a 8 de cada (outra ronda). Sem fotos → site ilustrado, nunca fotos falsas; Higgsfield só para ambiente, marcado «Imagine ilustrativă».
7. **Briefs.** Para cada site: fonte display nova com ă â î ș ț (verificar com fontTools; fora do PLAYBOOK §6, dos briefs dos lotes e de `fontes-assinaturas.md`), assinatura visual nova ligada ao ofício do negócio, funcionalidade que vende. Negócios da mesma categoria têm de ficar claramente diferentes. Gravar em `briefs-AAAA-MM-DD.md` e somar a `fontes-assinaturas.md`.
8. **Construir em paralelo.** Lançar 5 trabalhadores (Agent), 5 sites cada, com o brief, as regras do PLAYBOOK §3/§3-A, a estrutura dos lotes anteriores (RO com botão EN, `pt.html`, ANPC SAL + ODR, banner de apresentação, JSON-LD, um só `<h1>`, HONEST-DATA: o que não está na ficha fica «de confirmat»; sem notas sobre a origem dos dados) e o CTA: «Sună» + pedido por WhatsApp ou SMS quando o WhatsApp é «?»; só «Sună» quando é fixo. Dizer-lhes que não usam ferramentas `mcp__hearthbot__` nem fazem push. Usar os skills `frontend-design` e `ui-ux-pro-max` como manda o CLAUDE.md.
9. **Validar.** Script do PLAYBOOK §4 em cada site; abrir cada página em Chromium (Playwright local, `/opt/pw-browsers/chromium`) a 390 px e a 1280 px, sem erros de consola nem scroll horizontal; crítica final «isto podia ser um template?».
10. **Publicar.** Commit no ramo do caçador. Depois, numa worktree do ramo das demos: copiar só as pastas `sites/<pasta>/` do dia e juntar as linhas a `DEMOS` sob `# caçador AAAA-MM-DD`; um commit; `git pull --rebase origin claude/dez-negocios-dez-websites-7gevwu` e push (até 4 tentativas). Nunca reescrever história desse ramo nem mexer noutros ficheiros dele: é do thread «Dez negócios, dez websites». Em conflito no `gerar.py`, manter as duas listas.
11. **Confirmar no ar.** Pedido `testar https://pachecost-demos.netlify.app/<slug>/` pela ponte para cada demo (o proxy daqui não chega ao netlify.app). Só as que dão 200 passam a «publicada» no `.tsv`.
12. **Entregar.** Gerar `AAAA-MM-DD.md`, commit + push no ramo do caçador e responder no thread com: quantas demos ficaram no ar, o link da lista (`https://github.com/tspacheco/Designerpacheco/blob/claude/cacador-diario-nkiz36/research/cacador/AAAA-MM-DD.md`, abre no telemóvel com os botões a funcionar), as que caíram e porquê, e o que passa para a corrida B.

## Corrida B (11h30): construir as outras 25

1. Passo 1 da corrida A. Se a corrida A ainda não terminou, terminá-la primeiro.
2. Ler `AAAA-MM-DD.tsv`: as linhas B com estado «por fazer», mais as A que tenham ficado por fazer.
3. Passos 6 a 12 da corrida A para essas.
4. Se faltarem negócios B (ex.: saíram por terem site), completar com novas fichas (passo 4) até 25.

## Quando não chega

Se uma corrida não fechar as 25, as que faltarem ficam «por fazer» no `.tsv` e passam para a corrida seguinte; a resposta no thread diz quantas ficaram e porquê. Baixar a meta é decisão do Tomás.

## O que nunca fazer

- Construir sem ler o campo «Site» da ficha (Gist e Salon Monne, 07/10).
- Inventar notas, preços, horários, citações ou provas de WhatsApp.
- Mudar o texto da mensagem: é o de `mensagens.py` (10% a 30% mais clientes, desde 08/10), igual ao do `LOTE4-IASI.md`. Só a saudação roda entre 4 variantes.
- Esquecer a regra de envio na lista: **mínimo 1 minuto entre mensagens** e textos não idênticos seguidos (09/10: o WhatsApp bloqueou o Tomás um dia por spam, a enviar de 10 em 10 s). O `mensagens.py` já põe o aviso e varia a saudação.
- Pôr preço na mensagem (o preço fala-se depois: 500 € ≈ 2.500 lei + 75 €/mês ≈ 375 lei, auditoria grátis incluída).
- Push noutro ramo que não o do caçador, exceto a publicação descrita no passo 10.

## Lições da 1.ª corrida (09/10)

- Ferramentas no ramo: `excluir.py` (lista de exclusão), `fichas.py` (lê as fichas da ponte → TSV), `fotos.py` (pedidos `imagem` a partir de `fotosmaps`), `publicar.sh` (copia para o ramo das demos e junta a `DEMOS`), `trabalhador.md` (brief dos construtores).
- A ponte deste ramo aceita pedidos em paralelo (push de vários `.github/ponte.txt` seguidos) e tem `listamaps`, que desce a lista do Maps (até ~60 resultados em vez de 7).
- Rendimento: ~45 % das fichas abertas não têm site; para 50 abrir ~115. Sobram os de reserva no `vistos.tsv` («sem site (reserva)»): usar primeiro no dia seguinte.
- 7 construtores em paralelo (3 a 4 sites cada) fizeram as 25 em ~45 min depois das fotos; a corrida A demorou ~3 h no total.
- O motor das demos não copia subpastas de `media/`: o HTML só pode usar `media/<ficheiro>` (`sem-subpastas.sh` corrige).
