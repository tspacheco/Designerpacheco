# QR para imprimir — ro.pachecost.com

Todos os ficheiros têm o mesmo QR do cartão. Abre `https://ro.pachecost.com/C`, e o Netlify reencaminha para a página
romena (`/?origem=cartao`). O destino muda em `marca/dados.json` → `destino_qr`, sem reimprimir nada.

**O QR só abre a página depois de o site estar publicado no Netlify com o domínio `ro.pachecost.com`**
(passos em `sites/pacheco-studios/LEIA-ME.md`). Antes disso, o telemóvel lê o QR mas dá erro.

## Que ficheiro usar

| Ficheiro | Para quê |
|---|---|
| `qr-teste-a4.pdf` | **Imprimir primeiro, em casa.** Cinco tamanhos (15, 21, 35, 50 e 80 mm), régua de 100 mm e lista de verificação |
| `qr-ro-pachecost.pdf` | Gráfica: QR vetorial, preto sobre branco, 50 × 50 mm com a margem branca incluída. Pode ser escalado |
| `qr-ro-pachecost.svg` | Designer, Canva, Illustrator: o mesmo, vetorial |
| `qr-ro-pachecost.png` | Word, Canva, redes: 1980 × 1980 px (8 cm a 600 ppp, 16 cm a 300 ppp) |
| `qr-autocolante.pdf` | Autocolante da marca em romeno, 55 × 85 mm com 3 mm de sangria («Vezi proiectele», «Nu promitem. Arătăm.») |
| `qr-autocolante.png` | O mesmo a 600 ppp, com sangria, para gráficas online que pedem imagem |
| `qr-autocolante-preview.png` | Só para ver como fica depois de cortado |

O cartão de visita tem o seu próprio PDF: `marca/cartao/cartao-impressao.pdf`.

## Regras de impressão

- **Tamanho mínimo: 15 mm.** O cartão usa 21 mm. Um QR lê-se até cerca de 10 vezes o seu tamanho.
- **Margem branca à volta:** 4 módulos (o PDF e o PNG já a trazem). Não encostar texto, linhas nem a borda do papel.
- **Escuro sobre claro, sempre.** Nunca inverter (claro sobre escuro), nunca pôr um logótipo no meio, nunca mudar a cor
  para laranja.
- Na gráfica: pedir o QR a **preto só (100 % K)**, papel ou vinil **mate**. O brilho reflete e o telemóvel não lê.
- Imprimir sempre a 100 %. Na folha de teste, a régua tem de medir 100 mm.

## Gerar de novo

```
python3 marca/qr/gerar.py
```

Lê `marca/dados.json` (domínio, caminho do QR, legenda e frase do cartão) e refaz tudo. Os testes correm sempre:
cada PDF é renderizado outra vez e cada QR tem de ser lido de perto, a meia distância e desfocado, incluindo o QR do
PDF final do cartão. Verifica também o tamanho de cada página, a margem branca, os 4 mm de margem ao corte do
autocolante, a letra (≥ 7,5 pt), o contraste (≥ 4,5:1), as letras romenas nas fontes e os 100 mm da régua.
