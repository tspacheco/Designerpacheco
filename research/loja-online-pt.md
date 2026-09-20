# LOJA ONLINE EM PORTUGAL — o que é obrigatório, o que escolher, quanto custa

> Investigação de base (20/09/2026). Serve para qualquer cliente de e-commerce, não só o de roupa.
> **Aviso:** isto orienta decisões técnicas e de orçamento. A parte fiscal tem de ser confirmada pelo contabilista do cliente — não somos nós que assinamos as faturas dele.

## 1. Porque é que isto não é um site de 500 €

Um one-pager de restaurante mostra informação. Uma loja **recebe dinheiro**, emite faturas com valor fiscal, guarda dados pessoais e assume responsabilidade legal por devoluções. São cinco frentes novas:

1. Catálogo com stock, tamanhos e variantes
2. Carrinho e checkout com meios de pagamento portugueses
3. Faturação certificada pela AT (obrigatória, não opcional)
4. Páginas legais e políticas (RGPD, devoluções, RAL)
5. Envios, devoluções e o que acontece quando corre mal

Cada uma delas é trabalho recorrente depois do lançamento. **A mensalidade tem de refletir isso**, não pode ser os 50 €/mês de um site institucional.

## 2. Obrigatório por lei (tem de estar no site)

| Obrigação | O que significa na prática |
|---|---|
| **Identificação completa** | Nome/denominação, morada, NIF e registo comercial visíveis no site |
| **Preços com IVA incluído** | E os **portes visíveis antes** do checkout, não só no fim |
| **Livro de Reclamações Eletrónico** | Link visível (rodapé) para livroreclamacoes.pt. Reclamações respondidas em **15 dias úteis** |
| **Direito de livre resolução (14 dias)** | O cliente devolve em 14 dias **sem justificar**. Reembolso até 14 dias após receção, **no mesmo meio de pagamento** |
| **RAL** | Indicar a entidade de Resolução Alternativa de Litígios competente |
| **RGPD** | Política de privacidade, consentimento de cookies, base legal para os dados |
| **Condições gerais de venda** | Prazos de entrega, custos, política de trocas e devoluções |

Nada disto é decorativo: a falta de link do Livro de Reclamações ou de política de devoluções dá coima.

## 3. Faturação — a armadilha que apanha toda a gente

- Todas as faturas têm de sair de **software certificado pela AT** (Portaria 363/2010), com **ATCUD** e **QR Code** em cada documento.
- O ficheiro **SAF-T** tem de ser gerado e comunicado.
- PME podem emitir em PDF **até 31/12/2026**; a partir daí, formato estruturado **CIUS-PT**.
- Há indicação de **assinatura eletrónica qualificada (QES)** a partir de 01/01/2026 — **a confirmar com o contabilista**, as fontes públicas não são consistentes sobre a que casos se aplica.

**Consequência para nós:** a loja não emite faturas sozinha. Tem de ligar a um programa certificado (Vendus, InvoiceXpress, Moloni ou o que o contabilista do cliente já usa). **Perguntar isto ao cliente na primeira reunião** — muda a integração.

## 4. Pagamentos — MB WAY decide o negócio

Em Portugal, uma loja sem MB WAY perde vendas. Não é preferência, é hábito nacional.

| Gateway | Notas |
|---|---|
| **ifthenpay** | O mais usado por PME portuguesas, melhor reputação no Portal da Queixa (91,8/100). Plugins prontos para WooCommerce. MB WAY, Multibanco, cartão, Payshop |
| **Eupago** | 100% português, integra WooCommerce, Shopify e Magento |
| **Easypay** | Cobre todos os meios portugueses, boa documentação |
| **Stripe** | Excelente para cartão e cobre Multibanco, mas **não cobre MB WAY** *(a confirmar antes de propor)* |

**Shopify:** o Shopify Payments **não suporta MB WAY nativamente** em Portugal — é preciso app de parceiro certificado. Contar com isso no orçamento.

## 5. As três plataformas possíveis

### A. WooCommerce (WordPress) — **recomendada para cliente real com orçamento normal**
- **A favor:** plugins nativos de ifthenpay/Eupago; integração direta com software de faturação PT; custo mensal baixo (só alojamento); controlo total do design, que é exatamente o nosso argumento de venda
- **Contra:** segurança, atualizações e backups passam a ser responsabilidade nossa — tem de estar na mensalidade

### B. Shopify
- **A favor:** não falha, não precisa de manutenção técnica, o cliente gere sozinho o stock
- **Contra:** mensalidade da plataforma + comissões + app para MB WAY + app para faturação PT; o design personalizado obriga a trabalhar em Liquid

### C. Estático + Stripe/Snipcart
- **A favor:** rapidíssimo e lindo, encaixa no nosso engine de ficheiro único
- **Contra:** **sem MB WAY** e a faturação fica por resolver. Só serve para marcas que vendem sobretudo ao estrangeiro

**Recomendação:** A, salvo se o cliente disser explicitamente que não quer saber de manutenção — nesse caso B.

## 6. O que isto muda na tabela de preços

Itens que têm de ser orçamentados à parte do "website":

- Design e construção da loja (homepage, catálogo, página de produto, checkout)
- **Carregamento do catálogo** (fotos, descrições, tamanhos, stock) — cobrar por número de referências, é o que consome horas
- Integração de pagamentos + faturação certificada
- Páginas legais e políticas
- Formação do cliente para gerir encomendas sozinho

E a **mensalidade** tem de cobrir alojamento, atualizações de segurança, backups, e o suporte de quem vai ligar quando uma encomenda falhar — que numa loja acontece.

## 7. Perguntas a fazer ao cliente antes de desenhar

1. Que software de faturação usa hoje, e quem é o contabilista?
2. Quantas referências vai ter a loja no arranque (e quantas variantes por peça)?
3. Já tem fotografia de produto, ou é para produzirmos?
4. Vende só para Portugal ou também para Espanha/UE? (muda IVA e portes)
5. Quem vai gerir encomendas e stock no dia a dia?
6. Tem já marca definida (nome, logótipo, cores) ou desenhamos de raiz?
7. Transportadora e política de portes (grátis acima de X?)

## Fontes

- [Checklist legislação e-commerce 2026 — Tudo Sobre eCommerce](https://tsecommerce.com/blog/guia-rapido-legislacao-ecommerce-checklist/)
- [8 obrigações legais para lojas online em 2026](https://ecommerceparatodos.pt/8-obrigacoes-legais-que-todas-as-loja-online-em-portugal-tem-de-cumprir-em-2026/)
- [Livro de Reclamações Eletrónico — obrigatoriedade](https://inoveonline.com/pt/noticias/livro-de-reclamacoes-eletronico-obrigatorio-ou-nao)
- [Devoluções e reembolsos nas lojas online](https://inoveonline.com/pt/noticias/devolucoes-e-reembolsos-nas-lojas-online-o-que-diz-a-lei)
- [Faturação eletrónica e ATCUD em 2026](https://grupoyour.com/pt/blog/faturacao-eletronica-atcud-2026)
- [Elementos obrigatórios nas faturas — InvoiceXpress](https://invoicexpress.com/blog/elementos-obrigatorios-faturas/)
- [Aceitar MB WAY na loja online: taxas e opções (2026)](https://shelf.pt/blog/aceitar-mbway-loja-online)
- [ifthenpay](https://ifthenpay.com/)
