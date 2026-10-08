# Páginas por nicho e cidade (agente 5)

Páginas indexáveis para quem procura no Google «site frizerie Iași» ou «site para restaurante Algarve».
Cada página mostra as demos desse nicho (como uma rua de telemóveis, cada um com a placa da rua do negócio),
o que um site faz por esse tipo de negócio, os passos, perguntas e o botão **Cunoaște-ne / Conhece-nos**,
que abre o diagnóstico.

| Cidade | Língua | Endereço | Diagnóstico |
|---|---|---|---|
| Iași | RO | `ro.pachecost.com/site-uri/<nicho>-iasi/` e o índice `/site-uri/` | `ro.pachecost.com/?utm_content=diag-nisa-<página>#diagnostico` |
| Algarve | PT | `pachecost.com/sites/<nicho>-algarve/` e o índice `/sites/` | `pachecost.com/?utm_content=diag-nicho-<página>#diagnostico` |

As páginas PT juntam às demos do Algarve as demos de Iași que têm versão PT (`pt.html`), com o selo «Feito em Iași».

## Ficheiros

- `gerar.py` — lê a lista `DEMOS` de `sites/demos-pachecost/gerar.py` e o HTML de cada demo (nome, morada,
  cor, primeira foto) e escreve as páginas, os índices e `sitemap-nichos.xml`.
  `python3 gerar.py --out <pasta>`; `--embutir` mete as fotos no HTML (só para pré-visualizar).
- `nichos.py` — nichos, regras de arrumação, cidades e todos os textos. Uma página só nasce com 3 demos
  (pelo menos 1 da cidade) e texto escrito na língua da cidade. Nichos com texto à espera de demos:
  cabinete medicale, săli de fitness. `EXCLUIR` tira uma demo das páginas se o dono pedir.
- `integracao-demos.patch` — a mudança ao `gerar.py` das demos (ramo claude/dez-negocios-dez-websites-7gevwu).

## Como fica ligado (depois do patch)

1. As páginas vivem no projeto Netlify das demos e geram-se a cada push desse ramo, com as demos novas
   do Caçador diário já arrumadas no nicho certo. Sem zip.
2. O `_headers` das demos passa a pôr `noindex` só em `/<demo>/*`, para as páginas por nicho poderem ser indexadas.
3. O `pachecost-com-netlify.zip` ganha as regras: `ro.pachecost.com/site-uri/*` e `pachecost.com/sites/*`
   mostram as páginas do projeto das demos (200!, o endereço não muda), cada língua no seu domínio (301),
   e `/sitemap-nichos.xml`, que entra no `robots.txt`.
4. O contador das demos conta à parte, em `/nisa-demo/<demo>/`, quem abre uma demo vindo destas páginas
   (assim o tracker continua a medir só os donos).

Medição: GoatCounter em todas as páginas (`nisa/<página>/diagnostico-…`, `…/demo-<demo>`, `…/whatsapp`);
pixel da Meta só nas PT, com a mesma regra do site (desliga-se na página Cookies).

## O que fica para o Tomás (uma vez)

- Subir ao Netlify o `pachecost-com-netlify.zip` novo (com as regras).
- No Google Search Console: propriedade de domínio `pachecost.com` (cobre o `ro.`) e enviar
  `https://pachecost.com/sitemap-nichos.xml`.
