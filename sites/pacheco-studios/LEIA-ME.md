# pachecostudios.pt — página do QR do cartão

Uma página só, na identidade do Instagram e do cartão: o slogan, trabalhos reais (capturas do Grupo Naval e do
Hanam, mais os parceiros que já aparecem no Instagram), o que fazemos com preços, como funciona, o campo para abrir
o endereço escrito no cartão e o contacto. Sem telefone em `marca/dados.json`, os botões mandam email; com telefone,
passam a abrir o WhatsApp com uma mensagem já escrita.

## Publicar (Netlify — obrigatório por causa dos redirecionamentos)

1. Confirmar que o domínio `pachecostudios.pt` está livre e comprá-lo. Não respondia no DNS a 25/09; o `.com` já é
   de outra pessoa.
2. `python3 gerar.py` (nesta pasta). Gera o site, corre os testes e faz `pacheco-studios-netlify.zip`.
3. Netlify → arrastar o zip → *Domain management* → ligar `pachecostudios.pt` (o HTTPS é automático).
4. Testar no telemóvel: `pachecostudios.pt/c` abre a página; `pachecostudios.pt/nada` abre a página
   "Este endereço não existe (ainda)".
5. Só depois disto: `dominio_confirmado: true` em `marca/dados.json` e gerar o PDF final do cartão.

Hostinger não serve para este site: o `_redirects` (QR e endereços curtos) é próprio do Netlify.

## O que o gerador verifica

HTML válido, um só `h1`, `lang="pt-PT"`, Livro de Reclamações, zero campos por preencher. Em 360, 390 e 1280 px:
sem scroll horizontal, alvos de toque ≥ 44 px, letra ≥ 12 px e contraste de cada texto (mínimo 4,9:1). Testa também
o formulário (vazio mostra o erro; "Mercado da Vila" leva a /mercado-da-vila) e a barra fixa do telemóvel.

## Ficheiros

- `index.src.html`: desenho e textos (editar aqui)
- `gerar.py`: monta `index.html`, `404.html`, `_redirects`, `netlify.toml`, `media/og.png` e o zip
- `verificar.cjs`: testes no Chromium
- `media/`: capturas dos sites (WebP) e a imagem de partilha (og.png). Para mudar os trabalhos, trocar as capturas
  e o bloco "Trabalhos" do `index.src.html`
