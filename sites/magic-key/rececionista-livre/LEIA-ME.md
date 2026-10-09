# Magic Key — asistente de conversa livre (sem IA)

Página única (`index.html`) com um telemóvel e uma conversa de WhatsApp em romeno. A pessoa escreve o que quiser; o assistente responde por regras (palavras-chave, sem diacríticos, com tolerância a 1 erro de escrita). Funciona offline: fontes e fotos embutidas, zero pedidos à rede, sem IA.

## Como publicar
- app.netlify.com/drop → arrastar `rececionista-livre-netlify.zip` (ou a pasta). Tem `index.html` na raiz.
- Para editar: mudar `src.html` e correr `python3 build.py` (gera `index.html` e o zip; fontes de `../_fontes`, fotos de `../media`).

## O que reconhece
- Programa (geral, por dia: «program sambata», «deschis duminica?», «azi»), morada + cartão do mapa, telefone, recenzii (4,5 · 53).
- Preço: nunca dá números; diz que o dono confirma e abre a cerere de cheie.
- Cheie auto (pierdută, în plus, cip, briceag), telecomandă auto/reparação, baterie, telecomandă poartă/garaj/barieră, cartelă interfon/acces, chei de casă, mărci (com foto real quando é marca das lucrări), deslocação, duração, pagamento, «ești robot?», obrigado, adeus.
- Fluxo cheie: maşina (marca/modelo/ano, reconhece modelos como «golf», «logan»), o que aconteceu, se traz o carro, dia/hora (valida o horário), nome, telefone → cartão «Cerere cheie auto · transmisă».
- Programare: serviço, dia/hora, nome, telefone → cartão «Programare înregistrată».
- Não percebe → mensagem + 4 chips com as perguntas mais próximas + «Vorbesc cu proprietarul». 2.ª falha seguida ou esse chip → passa ao dono: pede nome e telefone → cartão «Transmis proprietarului».
- Botão ↻ no cabeçalho reinicia a conversa.

Dados: ficha Google (Selgros, Șos. Nicolina 57A; 0747 979 810; L–V 09–17, S 09–14, D fechado). Preços, deslocação, pagamento com cartão e feriados ficam «confirmă proprietarul».
