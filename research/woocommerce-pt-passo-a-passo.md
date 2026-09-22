# WOOCOMMERCE EM PORTUGAL — montagem, pagamentos e stock

> Guia de montagem para a Pacheco Studios (21/09/2026). Serve para a Toda Chic e para qualquer loja seguinte.
> **Fazer primeiro numa conta de teste tua.** Só depois repetir na conta da cliente, já com o caminho decorado.
> A parte fiscal tem de ser confirmada pelo contabilista da cliente — não somos nós que assinamos as faturas dela.

---

## PARTE A — Montagem (tu, uma vez por loja)

### A1. Alojamento e WordPress (30 min)

1. Alojamento com **PHP 8.1+, MySQL 8, SSL grátis e backups diários**. Em Portugal: Hostinger, Amen ou PTisp. Não uses o plano mais barato partilhado se a loja tiver 70+ produtos com fotos.
2. Instalar WordPress pelo painel do alojamento (1 clique).
3. **Antes de tudo:** Definições → Gerais → idioma **Português (Portugal)**, fuso **Lisboa**, formato de data `d/m/Y`.
4. Ligações permanentes → **Nome do artigo** (senão os URLs ficam `?p=123`).
5. Forçar HTTPS (o alojamento tem um botão; se não, plugin *Really Simple SSL*).

### A2. WooCommerce (20 min)

1. Plugins → Adicionar → **WooCommerce** → Instalar → Ativar.
2. Assistente de configuração:
   - Morada da loja: a morada fiscal da cliente
   - Setor: **Moda e vestuário**
   - Tipo de produtos: **Produtos físicos**
   - **Não** instalar as extensões sugeridas (Jetpack, MailPoet, etc.) — só pesam.
3. WooCommerce → Definições → **Geral**:
   - Moeda **Euro (€)**, símbolo à direita, **vírgula decimal**, ponto nos milhares, 2 casas
   - Vender apenas para **Portugal** (por agora; muda o IVA se vender para a UE)
   - Ativar a morada de faturação e envio
4. WooCommerce → Definições → **Impostos**:
   - Ativar impostos
   - **Preços inseridos com IVA incluído** ← obrigatório em B2C; é assim que a cliente pensa os preços
   - Taxa padrão: PT, 23 %
   - Se ela não tem atividade aberta / está isenta, **desativar impostos** e usar a menção de isenção que o contabilista indicar

### A3. Páginas legais (15 min)

O WooCommerce cria Loja, Carrinho, Finalizar compra e Minha conta. Faltam estas, que já estão escritas na demo e é só copiar:

- Sobre nós · Contactos · Perguntas frequentes · **Guia de tamanhos**
- Política de Privacidade · Termos e Condições · Trocas e devoluções
- No rodapé: **link para livroreclamacoes.pt** (obrigatório) e a identificação completa (nome/denominação, morada, NIF)

> ⚠️ A cláusula "não aceito trocas nem devoluções" é **nula** em venda à distância e a falta de informação estende o prazo de 14 dias para 12 meses. Está registado em `sites/toda-chic/REGISTO-devolucoes.md`. Construir como a cliente pediu, mas com o registo assinado.

### A4. Pagamentos — MB WAY com a ifthenpay (45 min)

**Porquê ifthenpay:** é a mais usada por PME portuguesas, tem plugin oficial para WooCommerce e cobre MB WAY, Multibanco, Payshop e cartão. Sem MB WAY perdes vendas em Portugal — não é preferência, é hábito.

**Passo 1 — Aderir (faz-se uma vez, demora 1-3 dias úteis)**
1. `ifthenpay.com` → Aderir. É preciso: NIF, certidão permanente ou cartão de cidadão do empresário, **IBAN da conta onde entra o dinheiro** e comprovativo de IBAN.
2. Recebes acesso ao **Backoffice ifthenpay**.
3. No backoffice, em *Chaves/Contas*, anota:
   - **Chave MB WAY** (formato `XXXX-XXXXXX`)
   - **Entidade + Subentidade** (Multibanco)
   - **Chave Payshop**, se quiseres
   - **Chave anti-phishing** (Backoffice → *Callback* → gerar) — é o que autoriza o site a receber a confirmação de pagamento

**Passo 2 — Plugin**
1. Plugins → Adicionar → procurar **"ifthenpay"** → instalar o *IfthenPay Payment Gateway for WooCommerce* → Ativar.
2. WooCommerce → Definições → **Pagamentos**. Aparecem os métodos ifthenpay.

**Passo 3 — MB WAY**
1. Clicar em **MB WAY → Gerir**.
2. Colar a **chave MB WAY** e a **chave anti-phishing**.
3. Título que a cliente vê: `MB WAY` · Descrição: *"Pague pelo telemóvel. Recebe um pedido na app MB WAY e confirma em segundos."*
4. **Tempo de espera:** 5 minutos (é o que a app dá para confirmar).
5. Ativar o **callback** (o plugin mostra o URL; copiar e colar no backoffice ifthenpay em *Callback*). **Sem isto, o pagamento entra na conta mas a encomenda fica eternamente "a aguardar".** É o erro nº 1.
6. Guardar.

**Passo 4 — Multibanco (referência)**
Mesma coisa com **Entidade + Subentidade**. Vale a pena ter: quem não tem MB WAY paga por referência, e a referência não caduca no mesmo dia.

**Passo 5 — Testar a sério**
1. Modo de teste ligado no plugin → fazer uma encomenda → confirmar que o estado muda sozinho para **Processando**.
2. Desligar o modo de teste e fazer **uma compra real de 1 €** com o teu telemóvel.
3. Verificar três coisas: o dinheiro entra no IBAN · a encomenda fica *Processando* sozinha · a cliente recebe o e-mail de confirmação.
4. Reembolsar-te a ti próprio para veres como é feito um reembolso.

**Custos:** a ifthenpay cobra por transação (valor fixo por operação MB WAY/Multibanco, mais barato que os 2,9 % + 0,25 € típicos de cartão). Confirmar a tabela no contrato antes de prometer margens à cliente.

### A5. Faturação certificada pela AT (30 min) — **não é opcional**

O WooCommerce **não emite faturas com valor fiscal em Portugal**. O "recibo" que ele manda por e-mail não serve. É preciso software certificado (Portaria 363/2010) com **ATCUD e QR Code** em cada documento.

1. Perguntar à cliente **que software usa o contabilista dela**. Se não usa nenhum: **Vendus** (mais barato, bom para lojas pequenas) ou **InvoiceXpress**.
2. Instalar o plugin da marca escolhida (ambos têm plugin oficial de WooCommerce).
3. Ligar com a chave de API da conta dela.
4. Configurar: emitir **fatura-recibo** automaticamente quando a encomenda passa a **Processando**, enviar por e-mail à cliente, série de documentos para a loja online.
5. Testar com uma encomenda real e **confirmar com o contabilista** que o documento está correto antes do lançamento.

> Nota de 2026: PME podem emitir em PDF até 31/12/2026; a partir daí é formato estruturado CIUS-PT. Há indicação de assinatura eletrónica qualificada — **a confirmar com o contabilista**, as fontes públicas não são consistentes.

### A6. Envios (20 min)

1. WooCommerce → Definições → **Envio** → Zona "Portugal Continental".
2. Método: **Taxa fixa** com o valor real dos CTT/transportadora. Se ela ainda não decidiu, põe um valor e marca para rever — **não lançar sem portes definidos**, porque os portes têm de estar visíveis *antes* do checkout (é obrigação legal).
3. Criar também "Ilhas" se enviar para Madeira/Açores (portes diferentes).
4. Opcional e bom para as vendas: **portes grátis acima de X €** (ex.: 40 €). Faz subir o valor médio da encomenda.

### A7. Produtos e stock — as definições que decidem tudo (15 min)

WooCommerce → Definições → **Produtos → Inventário**:

| Definição | Valor | Porquê |
|---|---|---|
| Gerir stock | ✅ Ligado | Sem isto, a loja vende o que não existe |
| Reter stock (minutos) | **60** | Segura a peça 60 min enquanto a cliente paga o MB WAY; se não pagar, volta ao stock |
| Notificações de stock baixo / esgotado | ✅ para o e-mail dela | Ela é avisada sem ter de ir ver |
| Limiar de stock baixo | **1** | Na Toda Chic quase tudo é unidade única |
| Ocultar produtos esgotados | ❌ **Desligado** | Melhor mostrar "Esgotado" — cria desejo e a cliente pergunta se volta |

### A8. Catálogo — carregar as 72 peças

O catálogo já está transcrito e as fotos já estão limpas: `sites/toda-chic/catalogo.json` + `media/produtos/`. Duas maneiras:

- **Importação CSV** (recomendado): converter o `catalogo.json` para o formato de importação do WooCommerce (Produtos → Importar). Poupa horas. *Nota para mim: escrever `ferramentas/woo-csv.py` quando o WordPress estiver de pé.*
- **À mão**, se forem poucas.

**Como modelar as peças da Toda Chic:**
- Peça de **uma cor só** → *Produto simples*, gerir stock, quantidade 1
- Peça em **várias cores** (ex.: body cavas em 4 cores) → *Produto variável* com o atributo **Cor**, usado para variações, e **stock por variação** (1 de cada). É assim que a loja esgota só a cor que acabou
- Tamanhos: a maioria é "tamanho único" → não criar atributo. Só nas calças de ganga e calçado é que há numeração → atributo **Tamanho**
- **SKU** sempre (ex.: `TC-039`). Sem SKU, gerir stock ao telefone é impossível
- "Vendido individualmente" ✅ nas peças de unidade única (impede levar 2 no carrinho)

### A9. Conta da cliente (5 min) — **o passo que evita desastres**

Utilizadores → Adicionar → perfil **Gestor da loja** (*Shop manager*), **nunca Administrador**.

O Gestor da loja pode: ver e processar encomendas, criar/editar produtos, mudar stock e preços, fazer cupões, ver relatórios.
Não pode: instalar/apagar plugins, mudar o tema, apagar o site. É exatamente o que queremos.

### A10. Antes de lançar — lista de verificação

- [ ] Compra real de 1 € por MB WAY, do princípio ao fim
- [ ] Fatura certificada emitida e aprovada pelo contabilista
- [ ] Portes definidos e visíveis antes do checkout
- [ ] Identificação da empresa (nome, NIF, morada) no rodapé
- [ ] Link do Livro de Reclamações no rodapé
- [ ] E-mails da loja a sair com o domínio dela (plugin SMTP + DKIM), não para spam
- [ ] Backup automático ligado
- [ ] Testar no telemóvel: adicionar ao carrinho, pagar, receber o e-mail
- [ ] Google Analytics ou equivalente (opcional)

---

## PARTE B — O dia a dia (ela)

O manual escrito na linguagem dela está em `sites/toda-chic/MANUAL-DONA.md`. Resumo do que tem de saber fazer, por ordem de importância:

1. **Ver uma encomenda nova e enviá-la** (e-mail → Encomendas → Processando → embalar → Concluída)
2. **Atualizar o stock** de uma peça
3. **Pôr uma peça nova à venda** (foto, nome, preço, stock, categoria, coleção)
4. **Fazer uma promoção** (preço promocional — é o que faz aparecer o preço antigo riscado)
5. **Esgotar / repor** uma peça
6. **Responder a uma cliente** que tem dúvidas no tamanho

**Regra de ouro para ela:** *o stock do site é a verdade.* Se vender uma peça pelo Instagram ou na mão, tem de baixar o stock no site nesse momento — senão o site vende o que já não existe, e aí é devolver dinheiro e perder a cliente.

---

## Perguntas em aberto para a reunião com a dona

1. Tem atividade aberta e NIF? Qual o nome/denominação e morada para as páginas legais?
2. Que software de faturação usa o contabilista?
3. IBAN para a ifthenpay (a adesão precisa dele).
4. Transportadora e valor dos portes. Portes grátis acima de quanto?
5. E-mail da loja (ainda por criar).
6. Envia para as ilhas? Para Espanha?
7. Quem escreve as descrições das peças novas — ela ou nós?

## Fontes

- [ifthenpay](https://ifthenpay.com/)
- [WooCommerce — documentação de inventário e stock](https://woocommerce.com/document/managing-products/)
- `research/loja-online-pt.md` (obrigações legais, plataformas, custos)
