# Carmangeria Boierilor — intro de carregamento (vídeo)

Ecrã de entrada do site: a imagem do herói sem texto, a câmara avança devagar para dentro da moldura de madeira até a fotografia encher o ecrã, e o intro funde-se para o site.

## 1. O que foi gerado no Higgsfield (conta do Tomás)

| Passo | Modelo | O que faz | Onde está |
|---|---|---|---|
| 1. Limpeza | Nano Banana Pro (2K, 16:9) | Remove o título, o slogan e o ícone do menu; mantém a madeira, a moldura e a foto | Geração `81fc004d-b17f-4cfd-846e-5eae752883fe` |
| 2. Vídeo | Kling 3.0 pro, 5 s, sem som, 16:9 | Push-in lento e contínuo até à moldura, a partir da imagem limpa | Geração `74e50816-6ae0-40d6-af8a-ee41b587ced9` |

O CDN do Higgsfield está bloqueado nesta sessão: os ficheiros descarregam-se à mão em higgsfield.ai (Generations).

**Verificar antes de usar (o Claude não conseguiu ver os resultados):**
- Imagem limpa: nenhuma letra ou sombra de letra ficou; as tábuas continuam sem costuras; a moldura e a foto estão iguais ao original; os pontinhos vermelhos das tábuas ainda existem.
- Vídeo: a câmara avança sem tremer nem rodar; a moldura e a foto não se deformam; nada aparece (pessoas, objetos, texto); a foto acaba a encher o ecrã.
- Se algum falhar: repetir a geração (a limpeza custa 2 créditos, o vídeo 8,75). Guardar o melhor.

## 2. Preparar os ficheiros (ffmpeg)

Do vídeo descarregado (`kling.mp4`) para os ficheiros que o site usa, na pasta do intro:

```bash
# MP4 leve (H.264, 1080p, sem áudio), cortado aos 4,8 s
ffmpeg -i kling.mp4 -t 4.8 -vf "scale=1920:-2" -c:v libx264 -profile:v high -crf 22 -preset slow -pix_fmt yuv420p -movflags +faststart -an intro.mp4
# WebM (VP9) para browsers que o preferem — opcional, mais pequeno
ffmpeg -i kling.mp4 -t 4.8 -vf "scale=1920:-2" -c:v libvpx-vp9 -b:v 0 -crf 32 -an intro.webm
# Poster = 1.º fotograma (aparece antes de o vídeo arrancar; tem de ser igual ao início do vídeo)
ffmpeg -i intro.mp4 -frames:v 1 -q:v 2 intro-poster.jpg
```

Alvo: `intro.mp4` abaixo de 2,5 MB. Se ficar maior, subir o `-crf` para 24–26.

## 3. Pôr no site

1. Copiar `intro.mp4`, `intro.webm` e `intro-poster.jpg` para a raiz do site (ou ajustar os caminhos em `src`/`poster`).
2. Abrir `intro.html`, copiar o bloco entre `INÍCIO DO INTRO` e `FIM DO INTRO` e colá-lo no HTML do site **logo a seguir a `<body>`**, na página inicial.
   - WordPress: plugin de cabeçalho/rodapé (p. ex. "WPCode") → secção *Body*, só na página inicial; ou no `header.php` do tema filho.
   - Site estático: colar diretamente no `index.html`.
3. Testar em telemóvel (Safari iOS e Chrome Android) e em desktop: o vídeo arranca sozinho (está `muted` + `playsinline`), funde aos 4,6 s, o botão «Sari» aparece ao segundo 1.

## 4. Como o intro se comporta

- Mostra-se **uma vez por sessão** (`sessionStorage`); nas páginas seguintes e ao voltar atrás não repete.
- **Nunca prende o site:** se o vídeo não carregar em 2,5 s (rede lenta) ou o autoplay for bloqueado, o intro desaparece; tempo máximo total 6,5 s.
- **`prefers-reduced-motion`:** o intro não aparece.
- Botão «Sari» e tecla Esc saltam o intro. O fundo é a cor da madeira (`#2a1d14`), para não haver um flash branco.
- Para ajustar o ponto da fusão: `CORTE` no script (segundos). Para o vídeo acabar exatamente quando a foto enche o ecrã, cortar o `intro.mp4` nesse instante e pôr `CORTE` 0,2 s antes.

## 5. Ideia para depois (opcional)

Se o herói do site puder mostrar a fotografia da moldura a encher o ecrã nos primeiros segundos e depois "recuar" para a moldura pequena, a transição fica contínua: o vídeo acaba na foto grande e o site começa nela. Isso pede alterar o herói do site do cliente, não este intro.
