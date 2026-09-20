# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

WooCommerce (WordPress) + ifthenpay como gateway de pagamentos. Decisão do Tomás em 20/09/2026, com base em `research/loja-online-pt.md`: MB WAY nativo, ligação a software de faturação certificado pela AT, custo mensal baixo e controlo total do design.

## Users

**Primária:** mulheres em Portugal a comprar roupa, bijuteria, cosméticos e artigos de casa, quase sempre no telemóvel, vindas do Instagram da loja (@_toda.chiic). Navegam por categoria e por estação, verificam tamanho e cor disponíveis, e querem saber se a peça ainda existe em stock antes de decidir.

**Secundária:** a dona da loja, que gere catálogo, stock e encomendas no dia a dia. *(A confirmar se é ela ou o Tomás a gerir.)*

## Product Purpose

Vender o stock da Toda Chic online, substituindo e alargando as vendas que hoje acontecem por mensagem no Instagram. Sucesso = encomenda feita e paga sem a cliente ter de mandar DM a perguntar preço, tamanho ou disponibilidade.

## Positioning

Loja portuguesa pequena e multi-categoria: roupa, bijuteria, cosméticos e artigos de casa sob a mesma marca, organizados por estação. O diferenciador é a curadoria e a voz da dona, não o preço nem a variedade.

## Operating Context

- As clientes chegam sobretudo do Instagram (@_toda.chiic)
- Pagamento: **MB WAY** (requisito confirmado pela dona)
- Contacto: **933 668 148**; e-mail da loja ainda por criar
- Encomendas e stock geridos pela dona

## Capabilities and Constraints

**Famílias de produto e categorias** (confirmadas pela dona):

- **Roupa** — Blusas & Tops · Calças & Pantalonas · Vestidos · Calções & Saias · Conjuntos
- **Bijuteria**
- **Cosméticos**
- **Artigos de casa**

**Transversal:** coleções por estação (nova coleção, inverno, meia-estação, verão) e uma secção de promoções. Implementa-se como categorias no menu + estação como filtro, não como menus separados — cruzar as duas dimensões em menus faria explodir a navegação.

**Por produto:** nome, preço, tamanhos disponíveis, cores disponíveis, guia de tamanhos e **quantidade em stock visível**.

**Funcionalidades pedidas:** favoritos (wishlist) e bloco "SEGUE-NOS NO INSTAGRAM".

**Páginas pedidas:** Sobre Nós · Contactos · Perguntas Frequentes · Política de Privacidade · Termos e Condições · Trocas e Devoluções.

**Consequências técnicas a assumir:**
- Stock visível obriga a gestão de stock rigorosa: se a dona não atualizar, a loja vende o que não tem
- Favoritos precisam de conta de cliente para persistirem entre dispositivos; sem conta, ficam só naquele telemóvel

### Política de devoluções — imposta pela cliente, não conforme à lei

A dona exige **"não aceito trocas nem devoluções"**. Decisão dela, registada a 20/09/2026 depois de a posição legal ter sido explicada — ver `sites/toda-chic/REGISTO-devolucoes.md`.

Para constar: na venda à distância a consumidores em Portugal, o direito de livre resolução de 14 dias é imperativo e não pode ser afastado por cláusula; a cláusula é nula e a falta de informação estende o prazo para 12 meses e 14 dias. **Construído conforme instruído; a responsabilidade é da dona.**

### Decisões em aberto

- **Faturação:** se a dona tem atividade aberta/NIF e que software certificado usa — desconhecido, o Tomás vai perguntar
- **Identificação da empresa** (nome/denominação, morada, NIF) para as páginas legais — ainda não disponível
- **E-mail da loja** — por criar
- Vende para fora de Portugal? — desconhecido (muda IVA e portes)
- Número de referências no arranque — desconhecido
- Transportadora e política de portes — por decidir

## Brand Commitments

- **Nome:** Toda Chic
- **Assinatura:** "Embeleza-te connosco" (já existe no logótipo, é portuguesa e tem voz — manter)
- **Instagram:** @_toda.chiic
- **Cor fixada pela dona:** tons de rosa, a condizer com o logótipo ("quero em tons de rosa como o logo")
- **Logótipo atual** (`marca/logo-atual.jpg`) vai ser **refeito**, por decisão do Tomás e a pedido da dona. Motivos técnicos: o gradiente rose gold não reproduz a uma cor (etiqueta, carimbo, saco, fatura) e o aro fino com a assinatura fica ilegível a tamanho de favicon ou de etiqueta cosida. Nome e assinatura mantêm-se.

## Evidence on Hand

- Briefing escrito da dona, reencaminhado por WhatsApp — `marca/briefing-dona-whatsapp.jpg`
- Logótipo atual — `marca/logo-atual.jpg` (1254×1254)
- Investigação legal e de pagamentos para e-commerce em PT — `research/loja-online-pt.md`
- Fotografia de produto — prometida pelo Tomás, ainda não recebida
