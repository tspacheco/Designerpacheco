# Iași — densidade de negócios por zona (raio de 5 km), 29/09/2026

**Fonte:** Overture Maps, tema *places*, release 2026-09-23.1 (dados abertos, agregam OSM + Meta + Microsoft + BrightQuery). Extraídos 10 294 pontos na caixa de Iași; 9 350 com localidade "Iași" estão em `research/iasi-negocios-overture.csv` (nome, categoria, morada, telefone, site, rede social, coordenadas).

**Método:** 15 centros de bairro (posição = mediana das moradas com o nome da rua). Para cada centro, contagem de pontos num **raio de 600 m** (zona percorrível a pé numa tarde). "Negócios" exclui cacifos de encomendas, igrejas, escolas, universidades, hospitais, serviços públicos e monumentos. Todos os centros estão a menos de 5 km da Piața Unirii. **Google Maps, OSM e diretórios romenos estavam bloqueados** nesta sessão — o Overture é a única base numérica; as contagens são uma proporção fiável entre zonas, não um censo. Ratings e horários não estão nesta base (HONEST-DATA: continuam "a confirmar" negócio a negócio).

## Ranking (top 10, do 10.º ao 1.º)

| # | Zona | km do centro | Negócios | HORECA | Beleza | Saúde/ginásio | Sem site |
|---|---|---|---|---|---|---|---|
| 10 | Tătărași (Bd. Vasile Lupu · Ion Creangă) | 2,5 | 278 | 29 | 35 | 40 | 42 % |
| 9 | Alexandru cel Bun | 1,2 | 290 | 22 | 37 | 26 | 44 % |
| 8 | Păcurari · Canta (Șos. Păcurari) | 2,8 | 296 | 14 | 30 | 35 | 36 % |
| 7 | Sărărie · Târgu Cucu · Independenței | 0,7 | 361 | 45 | 39 | 44 | 37 % |
| 6 | Copou (Bd. Carol I · Universidade) | 1,2 | 398 | 50 | 18 | 50 | 32 % |
| 5 | Tudor Vladimirescu · Iulius Mall | 1,9 | 412 | 65 | 43 | 28 | 31 % |
| 4 | Podu Roș · Socola · Nicolae Iorga | 1,9 | 488 | 30 | 70 | 54 | 38 % |
| 3 | Gară · Arcu · Silvestru | 0,8 | 577 | 67 | 49 | 73 | 40 % |
| 2 | Centru (Piața Unirii · Ștefan cel Mare · Lăpușneanu) | 0,0 | 897 | 151 | 69 | 80 | 37 % |
| 1 | Palas · Sf. Lazăr · Anastasie Panu | 1,2 | 1 007 | 135 | 76 | 64 | 31 % |

Fora do top 10: Bularga · Chimiei (239) · Dacia · Tabacului (217, 49 % sem site) · Nicolina (178, 47 % sem site) · Bucium (123) · Galata · Poitiers · CUG (115).

## Leitura para prospeção

- **Palas e Centru** têm metade dos negócios da cidade nesta escala, mas Palas é mall + torres de escritórios (muitas cadeias e empresas de serviços; decisão não é local). Para porta-a-porta, o **Centru** (Lăpușneanu, Cuza Vodă, Ștefan cel Mare) é o melhor: 151 HORECA e 69 salões numa zona pedonal.
- **Gară · Arcu · Silvestru** (3.º) é a surpresa: 73 negócios de saúde/ginásio e 40 % sem site — zona de clínicas e consultórios à volta da Policlínica e da estação.
- **Podu Roș · Socola** (4.º) é a zona com mais **beleza** fora do centro (70 salões) — Lista B (ligar), terças e quartas.
- **Copou** (6.º) é o único bairro onde já estamos (Society Salon, Bistro Copou, Bolta Rece): HORECA forte (50) mas poucos salões (18).
- **Tudor Vladimirescu** (5.º): campus + Iulius Mall; muitos HORECA (65) para estudantes, ticket baixo — sites em RO/EN fazem sentido.
- **Dacia e Nicolina** têm a maior fração sem site (47–49 %), mas menos negócios por passeio. Bons para uma segunda ronda, não para a primeira.
- Cada zona tem sempre o mesmo pódio de categorias: **salão de beleza → clínica dentária → restaurante/café** (também na cidade inteira: 511 salões, 254 dentistas, 217 restaurantes + 167 cafés). O catálogo de demos para Iași devia seguir esta ordem.

## Como reutilizar

Filtrar o CSV por categoria e por `site` vazio dá a Lista A/B de cada zona sem nova pesquisa. Verificar sempre no Google Maps antes de investir tempo (rating, se está aberto, se já tem site) — o Overture não traz avaliações e a confiança média dos registos é 0,65.
