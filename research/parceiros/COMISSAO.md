# Comissão dos parceiros — proposta por omissão (08/10/2026)

A decisão é do Tomás. Até ele dizer outra coisa, a proposta usa isto (valores em `proposta/gerar.py`, `VALORES`).

## A regra

**20 % da primeira fatura, paga até 7 dias depois de o cliente pagar.**

| | Iași (lei) | Algarve (€) |
|---|---|---|
| Por cada site vendido | 500 lei | 100 € |
| Por cada sistema de IA vendido ao mesmo cliente | 250 lei | 50 € |
| Oferta ao cliente indicado: 1.º mês de manutenção grátis | 375 lei | 75 € |

## A conta de um cliente indicado (Iași, 1.º ano)

- O cliente paga: 2.500 lei (site) + 11 × 375 lei (o 1.º mês é grátis) = **6.625 lei**
- Comissão ao parceiro: **− 500 lei**
- Fica para a Pacheco Studios: **6.125 lei** (≈ 1.225 €)
- Custo total de angariação: 500 + 375 = 875 lei, 12,5 % do que um cliente normal paga no 1.º ano (7.000 lei).

No Algarve é a mesma conta em euros: 500 + 11 × 75 = 1.325 €; − 100 € → **1.225 €** para nós.

## Se correr bem

6 parceiros ativos, cada um com 1 cliente por mês:

- Comissões: 6 × 500 = **3.000 lei/mês** pagos aos parceiros
- Entradas de sites: 6 × 2.500 = **15.000 lei/mês**
- Mensalidades: sobem 6 × 375 = **+2.250 lei/mês** a cada mês (ao fim de 6 meses, 36 clientes → 13.500 lei/mês, menos os meses grátis)

## Porquê esta e não outra

- **Valor fixo e redondo.** «500 de lei pe client» diz-se numa frase ao balcão. Uma percentagem da mensalidade obriga o parceiro a fazer contas e a confiar em relatórios.
- **Só depois de o cliente pagar.** Nunca sai dinheiro sem entrar primeiro.
- **O mês grátis ao cliente** faz da indicação um favor do parceiro ao cliente dele, não uma venda. É o que o contabilista quer: parecer bem com o cliente.
- **Alternativa mais agressiva**, se ao fim de 30 dias nenhum parceiro tiver indicado ninguém: 500 lei + 10 % da mensalidade durante 12 meses (+450 lei por cliente). Fica 5.675 lei para nós; continua a fechar positivo.

## Pagamento

Transferência bancária. Parceiro com firma: fatura de «servicii de intermediere / comision de recomandare». Pessoa singular: contrato de colaboração simples. O registo de cada indicação e de cada comissão fica em `comissoes.tsv`.
