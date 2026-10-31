# WashUp Laundromat · Análise (estudo de mercado curto, diagnóstico, bottlenecks)

**Pacheco Studios · AI Consultant · 31 out 2026 · tópico «Analisar WashUp Laundromat e criar CRM»**
Cliente: WashUp Laundromat, Bulevardul Carol I 26-28, 700505 Iași · 0766 971 785 · fecha às 20:00 · Google 4,9★ com 78 avaliações (P, print do Google Maps de 31 out).

Marcas: **P** publicado · **O** observado · **E** estimativa com base em dados de mercado e referências do setor. Nenhum número da WashUp foi medido ainda: tudo o que é «da WashUp» é E até o dono confirmar.

---

## 1. O que o dono disse (ponto de partida)

1. O maior gasto hoje é **água, gás e luz**.
2. **Não sabe quanto gasta exatamente**: recebe faturas, mas não liga o gasto aos ciclos, às máquinas nem aos dias.
3. Quer uma aplicação que lhe dê **todas as estatísticas da lavandaria**.
4. Website: começar já, em paralelo.

Restrição principal (regra de 01-diagnóstico: uma só): **o custo variável é invisível**. Sem saber o custo por ciclo, o dono não sabe a margem real de cada lavagem e secagem, não vê fugas (água a correr, secador mal regulado, máquina avariada a gastar) e não consegue decidir preços.

---

## 2. Estudo de mercado curto (lavandarias self-service, Iași / RO)

### 2.1 Quem compra (situações de compra)
| Segmento | Situação | Peso para a WashUp |
|---|---|---|
| Estudantes (UAIC fica no mesmo bulevar, Carol I 11) | casa partilhada ou lar sem máquina; lavagem semanal | Alto (O: localização) |
| Estudantes estrangeiros de Medicina (UMF Iași) e Erasmus | não falam romeno; procuram em inglês no Google | Alto: justifica o site **EN** (E) |
| Anfitriões Airbnb / apartamentos de curta duração | lençóis e toalhas, volume semanal, pagam por conveniência | Médio-alto (E) |
| Famílias | edredões, cobertores, tapetes pequenos (máquinas grandes) | Médio, sazonal (outono/primavera) (E) |
| Pequenos negócios (salões, ginásios, restaurantes) | toalhas e panos, volume regular | Médio; possível conta mensal (E) |

### 2.2 Preço de mercado
- Roménia: «la 10 kg de rufe, prețul e 30 de lei» (P, Observator, reportagem sobre self-service).
- Faixa usada no modelo: **lavagem 10 kg 20–30 lei, secagem 15–25 lei** (E).

### 2.3 Custos de utilidades em Iași (2026)
| Utilidade | Preço usado | Marca |
|---|---|---|
| Água potável ApaVital | 23,50 lei/m³ desde 1 jan 2026 | P (bzi.ro) |
| Água + canalização (total na fatura) | ≈ 30 lei/m³ | E |
| Eletricidade, cliente não doméstico | ≈ 1,3 lei/kWh com tudo incluído | E (ofertas domésticas 2026: 1,07–2,21 lei/kWh, P capital.ro) |
| Gás natural, cliente não doméstico | ≈ 0,32 lei/kWh (≈ 3,4 lei/m³) | E |

### 2.4 Leitura
O self-service é um negócio de **margem por ciclo**: a receita é fixa por ciclo e o custo de água, gás e luz é a maior parte do custo variável. Quem sabe o custo por ciclo ganha duas alavancas: corta fugas e ajusta preços por máquina e por hora. Em Iași a concorrência confirma-se no Google Maps na reunião (não conseguimos ler o Maps a partir da cloud).

---

## 3. Diagnóstico (Ficha resumida)

- **Escala:** E1 (balcão único, self-service, provavelmente sem funcionário permanente) (E).
- **Pontos fortes:** 4,9★ com 78 avaliações (P), localização universitária (O), máquinas industriais em inox de aspeto recente (O, foto).
- **Ponto fraco principal:** gasto de utilidades sem registo nem ligação aos ciclos.
- **Pontos a confirmar:** número e marca das máquinas, sistema de pagamento (moedas, fichas, cartão, app), se há casa de marcat com relatório Z, quem lê os contadores, contratos de luz/gás e fornecedor, se tem website/Instagram.

### 3.1 Exemplo de cálculo (demonstração, todos E)
Hipótese de trabalho para mostrar a lógica, não a faturação da WashUp: 6 máquinas de lavar 10 kg, 4 secadores a gás; 25 lavagens e 18 secagens por dia; lavagem 25 lei, secagem 20 lei.

| Por ciclo | Consumo (referência do setor) | Custo | % do preço |
|---|---|---|---|
| Lavagem 10 kg | 70 L água + 1,6 kWh luz | 2,1 + 2,1 = **4,2 lei** | 17 % (E) |
| Secagem 30 min, gás | 9,5 kWh gás + 0,3 kWh luz | 3,0 + 0,4 = **3,4 lei** | 17 % (E) |

Por mês: receita ≈ 29.550 lei; utilidades variáveis ≈ 5.000 lei + base fixa (iluminação, aquecimento de água em espera, standby) ≈ 1.000 lei → **≈ 6.000 lei/mês, ≈ 20 % da receita** (E).

Poupança típica quando o consumo passa a ser medido e comparado por ciclo: **8–15 % das utilidades** (E, referências de submedição em lavandarias e pequenos negócios: fugas, secadores com filtro sujo ou tempo a mais, tarifa mal escolhida, aquecimento de água fora de horas). Neste exemplo: 480–900 lei/mês.

---

## 4. Bottlenecks (por prioridade)

| # | Bottleneck | Motor | Impacto | Viabilidade | Ação |
|---|---|---|---|---|---|
| ★ B1 | Custo de água, gás e luz invisível; sem custo por ciclo nem margem | Entrega/Economia | Alto | Alta (começa com fotos no WhatsApp) | **WashUp Control** (piloto) |
| B2 | Sem estatísticas: ciclos e receita por máquina, horas de pico, máquinas paradas | Entrega | Alto | Média (depende do sistema de pagamento) | Painel + relatório Z / contadores de ciclos |
| B3 | Avarias e manutenção sem registo (máquina parada = receita perdida e consumo anormal) | Suporte | Médio | Alta | Alerta «consumo anormal» + registo de avarias |
| B4 | Aquisição: sem site próprio visível; estrangeiros procuram em inglês | Aquisição | Médio | Alta | Website RO + EN |
| B5 | Perguntas repetidas (preço, horário, detergente, «há máquinas livres?») | Suporte | Baixo-médio | Alta | Mais tarde: rececionista WhatsApp em modo sombra |

---

## 5. Como captar os dados (do mais barato ao mais automático)

| Nível | O que capta | Como | Custo | Quando |
|---|---|---|---|---|
| 1 | Contadores de água, gás e luz | Ao fechar (20:00) o dono manda **3 fotos** no WhatsApp → a IA lê o número → rascunho «Água 1.234,5 m³ · OK/X» → OK grava | 0 € em hardware | Semana 1 |
| 1 | Preço real de cada utilidade | Foto ou PDF da fatura (ApaVital, gás, luz) → a IA extrai lei/m³ e lei/kWh e o período → OK/X | 0 € | Semana 1 |
| 1 | Receita e ciclos do dia | Foto do **raport Z** da casa de marcat, ou do ecrã do sistema de pagamento → OK/X | 0 € | Semana 1 |
| 2 | Ciclos por máquina | Contador de ciclos de cada máquina (fotografado 1×/semana) ou export do sistema de pagamento | 0 € | Semana 2 |
| 3 | Luz em tempo real, por máquina | Medidor no quadro (tipo Shelly Pro 3EM) e tomadas/relés de medição por máquina → n8n | ≈ 120–400 € (E) | Mês 2 |
| 3 | Água e gás em tempo real | Leitor de impulsos no contador (se o contador tiver saída) | ≈ 60–150 € por contador (E) | Mês 2 |
| 4 | Dados diretos das máquinas | Plataforma do fabricante (ex. Electrolux, Primus, Miele, Speed Queen têm sistemas ligados) se as máquinas suportarem | depende da marca | Mês 3 |

Os fornecedores de luz, gás e água em RO não dão API pública aos clientes (O): a fatura em PDF por email é a via fiável; o n8n lê a caixa e extrai.

**Regras:** a IA nunca grava sem o OK do dono (modo sombra, como no Magic Key); tudo fica numa base no servidor Hetzner (n8n + Postgres); o dono vê o painel no telemóvel.

---

## 6. O que entregamos agora

1. **Protótipo WashUp Control** (HTML, dados de demonstração): `crm/washup-control.html`. Painel do dia, utilidades (água, gás, luz, custo por ciclo), máquinas, horas de pico, margem, alertas, e o fluxo «foto no WhatsApp → OK/X».
2. **Website RO + EN** (hero vertical, ref. Borda d'Água): `site/index.html` e `site/en/index.html`, pronto para pachecost.com/p/washup/.
3. **Proposta** 1–2 páginas RO + PT, 500 € + TVA «în caz de factură»: `proposta/`.

## 7. Perguntas para o dono (primeira reunião)
1. Quantas máquinas de lavar e secadores, de que marca e capacidade?
2. Como pagam os clientes (moedas, fichas, cartão, app)? Há casa de marcat com raport Z?
3. Onde estão os contadores de água, gás e luz? São só da lavandaria?
4. Fornecedores e valores das 3 últimas faturas de cada utilidade.
5. A água quente vem de caldeira a gás ou as máquinas aquecem a eletricidade?
6. Preços atuais por ciclo; horário de abertura (sabemos que fecha às 20:00).
7. Tem fotos/vídeo do espaço para o site? Instagram/Facebook?
8. CUI/NIF para a proposta e acordo RGPD (se houver dados de clientes).
