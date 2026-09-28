# Casa Bolta Rece — novo site (proposta Pacheco Studios, 27/09/2026)

Restaurante histórico em Iași (Str. Rece nr. 10, desde 1786). O cliente tem um site WordPress (casaboltarece.ro); esta é a proposta de substituição: página inicial nova de raiz e as outras páginas no mesmo sistema.

## Estrutura

| Ficheiro | O que é |
|---|---|
| `index.html`, `istoric.html`, `meniu.html`, `galerie.html`, `contact.html`, `carmangeria.html` | páginas finais, cada uma em ficheiro único (CSS, JS e fontes embutidos) — **geradas, não editar à mão** |
| `src/pages/*.html` | conteúdo de cada página; `src/site.css`, `src/site.js`, `src/nav.html`, `src/footer.html` partilhados; `src/intro.html` (vídeo de entrada, só index); `src/bolta.js` (boltă 3D, só index) |
| `ferramentas/build.py` | monta as páginas finais: `python3 ferramentas/build.py` |
| `ferramentas/fontes.py` → `_fontes/fontes.css` | fontes Google (Bona Nova, Albert Sans, EB Garamond itálico) em base64, latin + latin-ext (ș ț ă) |
| `ferramentas/three.min.js` | Three.js r152 (UMD), embutido só no index |
| `media/` | 48 fotografias do site atual a 1800 px, logótipos, selo ANPC |

## Assinatura visual

**"Sub boltă"**: a pivniță de cărămidă em 3D (Three.js) pela qual a câmara avança conforme o scroll, com felinare a tremeluzir e a luz ao fundo do túnel; as fotografias entram em arcos (cards com inclinação 3D que segue o cursor); **"O seară la Bolta Rece"** — uma faixa horizontal comandada pelo scroll vertical, em três capítulos (I masa: o prato · II vinul: as garrafas · III versul: a placă de lemn), com paragem em cada capítulo, fusão suave entre fotografias, parallax leve e barra de progresso; a lista do menu desenha as linhas pontilhadas ao aparecer; as poesias da carte de oaspeți revelam-se verso a verso. Sem WebGL a boltă cai para fotografia. O `<html>` nasce com `class="no-js"` e um script no head troca para `js` (e junta `rm` com movimento reduzido): sem JavaScript ou com movimento reduzido, a faixa e a boltă ficam empilhadas na vertical, com tudo visível. Fontes: Bona Nova (títulos), Albert Sans (corpo), EB Garamond itálico (citações e versos).

## Intro em vídeo (só na primeira entrada)

`src/intro.html` mostra `media/intro.mp4` (+ `media/intro.webm`) em ecrã inteiro **uma vez por sessão**, só no index, e funde para o herói — que é a mesma fotografia em que o vídeo acaba. Sem o ficheiro, o intro não aparece (guarda de 2,5 s). Os ficheiros vêm do Higgsfield (ver `sites/carmangeria-boierilor/intro/LEIA-ME.md` para os comandos ffmpeg). Não usar em transições entre páginas.

## Dados reais (do site atual) e o que está "de confirmat"

Reais: nome, morada, telefones (+40 752 589 881 · +40 232 212 255), e-mail, horário (Luni–Duminică 08:00–22:00), Facebook/Instagram, textos do istoric e da página inicial, nomes dos pratos, poesias, a ligação ao magazin Carmangeria Boierilor (Dacia).
De confirmat: denumire firmă/CUI/Reg. Com. (rodapé), preços (não há nenhum no site), PDF do menu, alergénios, link de encomenda online da Carmangeria, morada/horário do magazin.

## Publicar

- **Netlify:** arrastar a pasta `sites/bolta-rece/` (ou um zip com `*.html`, `media/`, `netlify.toml`). O formulário de reserva funciona lá (Netlify Forms, `data-netlify`); noutro alojamento, ligar o `action` a um serviço de formulários ou deixar só o telefone.
- **Hostinger:** o mesmo, sem `netlify.toml`, em `public_html`.
- Na venda: retirar o `.banner` de `src/nav.html`, preencher os dados da firma no `src/footer.html`, voltar a correr o build.

## Vídeo "Antes vs Depois"

Gravar a página inicial: intro em vídeo → herói → scroll pela boltă 3D → cards → menu → faixa horizontal "O seară la Bolta Rece" (deixar o scroll parar em cada capítulo) → história → poesias → reservas. Para o intro aparecer em cada take, abrir numa janela anónima nova (o intro só se mostra uma vez por sessão).
