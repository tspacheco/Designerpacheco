# Magic Key — pack de oferta (reunião 09/10/2026, 15h)

| Ficheiro | O quê |
|---|---|
| `afis-recenzii-a4.pdf` | Afiș RO A4 com QR para recenzie Google (fica no stand) |
| `afis-recenzii-a5x2.pdf` | O mesmo, 2× A5 numa A4 (cortar ao meio; balcão) |
| `oferta-ro.pdf` / `oferta-pt.pdf` | Oferta: 2.500 RON + 300 RON/lună, audit inclus gratuit, fără obligație |
| `audit-ro.pdf` / `auditoria-pt.pdf` | Auditoria partes 1 (vista de fora) e 2 (perguntas + números da reunião) |

QR → `https://search.google.com/local/writereview?placeid=ChIJdbn1UCv7ykAR8GfcUXEt81c`
(Place ID do link da ficha Google, `ponte/r3-magic-key-chei-auto-duplicare.txt`; QR lido de volta com OpenCV).

Gerar: `python3 gerar.py && node pdf.js` (fontes de `../_fontes/fontes.css`; precisa de `pip install qrcode`).
Parte 3 da auditoria (plano de 90 dias com contas) faz-se depois da reunião, com os números da parte 2.
