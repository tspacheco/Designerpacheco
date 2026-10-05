# Briefs dos 10 sites (lote Algarve, 05/10/2026)

Regras comuns: PLAYBOOK §3, §3-A (nível 10K), §4. Dados em `research/algarve-10-negocios-out26.md` e nas fichas `ponte/ficha-*.txt`. Fotos reais em `sites/<slug>/media/g/NN.webp` (vistas uma a uma, escolhidas, renomeadas com nomes que dizem o que são; as não usadas apagam-se).

Estrutura de cada site (ficheiro único `index.html`, gerado por `ferramentas/build.py` a partir de `index.src.html`, fontes embutidas em base64 como em `sites/jj-restaurante` / `sites/society-salon`):
- **Subpáginas por `#/`** dentro do ficheiro: Início · (Carta | Serviços | Catálogo) · A casa · Galeria · Visitar/Contactos. Cada página com título próprio no `<title>`, scroll ao topo, foco no `<h2>` da página, botão voltar do browser a funcionar, links diretos (`#/carta`) a abrir a página certa.
- Telemóvel primeiro (o Tomás apresenta no telemóvel). CTA fixo em baixo no telemóvel: Ligar + WhatsApp (wa.me/351<número>).
- Banner `APRESENTAÇÃO PACHECO STUDIOS · …` no topo. Livro de Reclamações no rodapé. JSON-LD do tipo certo (Restaurant, BarberShop, Florist, Bakery, AutoRepair).
- Dados não confirmados → selo "a confirmar". Sem notas sobre a origem dos dados. Nota do Google só com nº de avaliações quando se conhece.
- Fotos: fundo SVG desenhado por baixo + `<img src="media/…" onerror>` por cima.
- `media/LEIA-ME.txt`, `netlify.toml`, zips `<slug>-netlify.zip` (com toml) e `<slug>-hostinger.zip` (sem toml), ambos com `index.html` + `media/`.

| Site | Slug | Fonte display (nova) | Assinatura visual (nova) | Língua | Funcionalidade que vende |
|---|---|---|---|---|---|
| Tasquinha do Bruno | `tasquinha-do-bruno` | Caprasimo | **Alcatruzes na corda**: os potes de barro do polvo de Santa Luzia pendurados numa corda que desce com o scroll; cada secção "sobe" um alcatruz | PT/EN | carta de tapas filtrável (peixe, polvo, carne, vegetariano) + "monta a tua mesa" → mensagem WhatsApp |
| O António | `o-antonio` | Hepta Slab | **Toalha de papel da mesa**: a carta escrita a lápis numa toalha de papel quadriculada, com a conta a somar-se na margem | PT/EN | pratos do dia em destaque + reserva por WhatsApp com dia/hora/pessoas |
| Restaurante Colibri | `restaurante-colibri` | Petrona | **O colibri que paira**: um beija-flor em SVG (asas em blur) que voa até ao link/prato em hover/toque e paira | PT | carta + reserva WhatsApp; almoço de dia de semana |
| Tasca do Tó | `tasca-do-to` | Kufam | **Telhados de tesoura**: a linha dos telhados de quatro águas de Tavira desenha-se e emoldura o herói e as secções | PT/EN | petiscos + aberto até às 23h ("ainda está aberto?" ao vivo) |
| Barber's Touch | `barbers-touch` | Rye | **Toalha quente**: vapor em canvas que se dissipa e revela o título; a navalha abre como cursor de progresso | PT/EN | marcação: serviço → dia → hora → WhatsApp pré-escrito |
| Barbearia Sr. Bonifácio | `barbearia-sr-bonifacio` | Holtwood One SC | **Cartão de cliente carimbado**: o scroll carimba o cartão (10 carimbos), cada secção um carimbo | PT | marcação WhatsApp + cartão de fidelização a propor |
| Flor Mimosa | `flor-mimosa` | Imbue | **Papel kraft a abrir**: o embrulho abre-se e os caules juntam-se num ramo à medida que se desce | PT/EN | catálogo por ocasião (aniversário, casamento, funeral, empresa) → encomenda guiada WhatsApp |
| Faisca & Henriques | `faisca-henriques` | Shrikhand | **Bolo em corte**: as secções empilham-se como camadas de bolo (pão-de-ló, recheio, cobertura) | PT | construtor de encomenda de bolo (massa, recheio, cobertura, pessoas, data) → WhatsApp |
| SOS CAR | `sos-car` | Tilt Warp | **Painel de instrumentos**: as luzes de aviso do tablier acendem-se uma a uma; cada luz é um serviço | PT | "Que luz acendeu?" → pedido de orçamento WhatsApp com marca/modelo/matrícula |
| MB Cakes Brunch & Coffee | `mb-cakes` | Calistoga | **Açúcar em pó pela peneira**: o título aparece como açúcar polvilhado através de um stencil | PT/EN | brunch + encomendas de bolos (WhatsApp) |
