# Toda Chic — manual da loja

Guia para gerires a tua loja sozinha. Tudo se faz no mesmo sítio: **entras em `alojasite.pt/wp-admin`** com o teu utilizador e a tua palavra-passe.

Guarda esta página nos favoritos do telemóvel. Qualquer dúvida, liga ao Tomás.

---

## 1. Chegou uma encomenda. E agora?

Recebes um e-mail: **"Nova encomenda #1234"**.

1. Entra no painel → menu **WooCommerce → Encomendas**.
2. A encomenda nova está a **Processando** (amarelo). Isto quer dizer: **a cliente já pagou**. Podes enviar.
3. Clica na encomenda para veres o que ela comprou, a morada e o telemóvel.
4. Embala as peças.
5. Quando entregares o volume nos CTT, volta à encomenda e muda o estado para **Concluída**. A cliente recebe automaticamente um e-mail a dizer que já seguiu.

**As cores dos estados:**

| Estado | O que significa | O que fazes |
|---|---|---|
| **Pagamento pendente** | Ainda não pagou | Esperas. Ao fim de 1 hora a peça volta ao stock sozinha |
| **Processando** | **Já pagou** | Embalar e enviar |
| **Concluída** | Já enviaste | Nada |
| **Cancelada** | Não pagou a tempo | Nada. O stock já voltou |
| **Reembolsada** | Devolveste o dinheiro | Repor o stock à mão, se a peça voltou |

> ⚠️ **Nunca envies uma encomenda que esteja em "Pagamento pendente".** Só "Processando" quer dizer que o dinheiro entrou.

---

## 2. Mudar o stock de uma peça

É a coisa que mais vais fazer. Duas maneiras:

**A maneira rápida (uma peça):**
1. **Produtos** → procura a peça pelo nome
2. Passa o rato por cima → **Edição rápida**
3. Muda o número em **Stock**
4. **Atualizar**

**Se a peça tem várias cores:**
1. **Produtos** → clica na peça
2. Desce até **Variações**
3. Clica na cor que queres mudar
4. Muda a **Quantidade em stock** dessa cor
5. **Guardar alterações**

> **A regra mais importante de todas:** se venderes uma peça pelo Instagram, por mensagem ou na mão, **baixa o stock no site na mesma hora**. Se não o fizeres, o site vende uma peça que já não tens — e depois tens de devolver o dinheiro e perdes a cliente.

---

## 3. Pôr uma peça nova à venda

**Produtos → Adicionar novo**

1. **Nome:** simples e como tu dirias. *Top efeito barco*, não *TOP FEMININO MANGA COMPRIDA REF 4471*
2. **Descrição:** 1 ou 2 linhas. O tecido, o corte, como veste. Ex.: *"Malha canelada com pala a cair sobre os ombros. Tamanho único, veste do XS ao L."*
3. **Dados do produto → Geral → Preço normal:** o preço com IVA já incluído (o preço que a cliente paga)
4. **Inventário:**
   - **SKU:** o código da peça (ex.: `TC-085`)
   - ✅ **Gerir stock**
   - **Quantidade:** quantas tens
   - ✅ **Vendido individualmente** se só tens 1
5. **Imagem do produto** (à direita): a foto principal. **Galeria:** as outras fotos
6. **Categorias** (à direita): escolhe *Blusas & Tops*, *Calças & Pantalonas*, *Vestidos*, *Calções & Saias* ou *Conjuntos*
7. **Etiquetas:** a coleção — *Nova coleção*, *Inverno*, *Meia-estação* ou *Verão*
8. **Publicar**

**Se a peça tem várias cores:** em *Dados do produto* muda de **Produto simples** para **Produto variável**, cria o atributo **Cor** com as cores que tens, marca *Usado para variações*, e depois em **Variações** cria uma variação por cor — cada uma com a sua foto e o seu stock.

### As fotos

- **Sempre ao alto** (retrato), não deitadas
- Luz natural, fundo liso e claro
- **Sem preços nem texto escritos por cima** — o preço já aparece no site
- Se for para o Instagram, faz uma versão com a marca; para o site, a foto limpa

---

## 4. Fazer uma promoção

É o que faz aparecer o **preço antigo riscado e o preço novo a vermelho** — é isso que faz as clientes comprarem.

1. **Produtos** → a peça → **Edição rápida**
2. Deixa o **Preço normal** como está (é o preço antigo, o riscado)
3. Escreve o **Preço promocional** (o novo, mais baixo)
4. **Atualizar**

A peça passa a aparecer sozinha na página **Promoções**, com a percentagem de desconto.

Para a promoção acabar numa data: abre a peça, em *Geral* clica em **Agendar** ao lado do preço promocional e escolhe as datas. Acaba sozinha.

---

## 5. Peça esgotada

Não precisas de fazer nada: quando o stock chega a 0, o site escreve **"Esgotado"** e já não a deixa comprar.

Se voltares a ter a peça, mete o stock outra vez e ela volta a ficar à venda.

**Se a peça nunca mais volta:** Produtos → Edição rápida → **Estado: Rascunho**. Sai do site mas fica guardada, caso um dia queiras repetir.

---

## 6. Uma cliente tem dúvidas no tamanho

É a pergunta mais comum e é a que mais vendas fecha.

- Pede-lhe as medidas (peito, cintura, anca)
- Compara com o tamanho da peça
- Diz com honestidade: se achas que não lhe vai servir, diz. **Vale mais perder uma venda do que uma cliente chateada** — ainda por cima não aceitamos devoluções

Na loja há uma página **Guia de tamanhos**. Mede as peças que vendes muito e preenche a tabela: é trabalho de uma tarde e poupa-te dezenas de mensagens.

---

## 7. Todas as semanas (10 minutos)

- [ ] Ver se há encomendas paradas em "Processando" há mais de 2 dias
- [ ] Conferir o stock das peças que vendeste fora do site
- [ ] Pôr 2 ou 3 peças novas
- [ ] Ver se há promoções para acabar ou começar
- [ ] Partilhar uma peça nova no Instagram com o link do produto

---

## O que **não** deves mexer

Estas coisas partem o site e depois é preciso arranjar:

- ❌ Plugins (instalar, apagar ou atualizar)
- ❌ Aspeto → Editor / Temas
- ❌ Definições do WooCommerce (pagamentos, envios, impostos)
- ❌ Definições → Ligações permanentes
- ❌ Apagar páginas (Carrinho, Finalizar compra, Minha conta)

**Precisas de mudar alguma destas? Liga ao Tomás.** É para isso que serve a mensalidade.

---

## Números úteis

| | |
|---|---|
| **Painel da loja** | `alojasite.pt/wp-admin` |
| **Problemas no site** | Tomás — Pacheco Studios |
| **Pagamentos (MB WAY)** | Backoffice ifthenpay |
| **Faturas** | o teu contabilista |
