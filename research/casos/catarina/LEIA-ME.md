# Caso 01 · Restaurante & Pizzaria Catarina (Altura)

Agente 10 (08/10/2026): o primeiro caso real da Pacheco Studios, e um pedido de indicação à dona.

| Ficheiro | O que é |
|---|---|
| `caso.html` + `img/` | Página do caso (antes/depois/resultado). Os números entram no objeto `CASO`, no fim do ficheiro; vazios mostram «a preencher». |
| `reel/saida/reel-catarina-9x16.mp4` | Reel 9:16, 31 s, com som. Abre com o resultado: «4,4★ no Google · 168 avaliações. Nenhum site. Agora tem.» |
| `reel/gerar.py` | Refaz o reel (usa o gerador do agente 4 e o site do ramo da Catarina, só lê). Com números, muda `GANCHO_L2`/`GANCHO_L3`. |

Dados usados (todos já publicados no site da Catarina, aprovado pela dona): 4,4★ e 168 avaliações Google, morada, telefone, horário, línguas, fotos da sala, esplanada e forno, e as alterações de 06/10/2026 feitas no mesmo dia.
O «antes» vem da pesquisa de julho (media/leia-me.txt do site): a casa só existia em Google, TripAdvisor, RestaurantGuru, cardapio.menu, Baixo Guadiana e Instagram, sem foto pública do exterior.

## Onde faltam números (não se inventam)

1. Data em que o site foi para o ar.
2. Reservas por telefone numa semana normal: antes do site e agora.
3. Visitas ao site num mês. O site não tem contador; ver «Próximo passo».
4. Clientes que disseram ter visto o site (por semana, aproximado).
5. Uma frase da dona, palavra por palavra, e o nome com que quer aparecer.
6. Endereço do site (domínio).

Enquanto faltarem, a página fica como rascunho (faixa «números por confirmar») e não vai para o site da Pacheco Studios.

## Mensagem para a dona (WhatsApp, grupo «Sites Catarina», com o reel em anexo)

> Olá, boa tarde! Aqui é o Tomás, da Pacheco Studios. Espero que esteja tudo bem por aí.
>
> Queria pedir-lhe três coisas rápidas:
>
> 1. **Autorização** para mostrar o site da Catarina como exemplo do nosso trabalho, no nosso site e no Instagram. Fiz este vídeo curto com ele (vai em anexo). O vídeo é vosso: podem publicá-lo à vontade.
>
> 2. **Três números**, para o exemplo ser verdadeiro:
>    - quantas reservas por telefone recebem numa semana normal agora, e quantas recebiam antes do site, na mesma altura do ano;
>    - se há clientes que dizem que vos encontraram pelo site (mais ou menos quantos por semana).
>    E, se puder, uma frase sua sobre o que mudou desde que tem o site.
>
> 3. **Dois nomes**: conhece dois donos de negócios aqui na zona que também precisem de um site? Basta o nome e o número. Eu falo com eles e digo que foi a Catarina que nos indicou.
>
> Sem pressa nenhuma. E se preferir que não mostremos o site, não há problema nenhum.
>
> Obrigado!

**Lembrete (só um, 4 dias depois, se não houver resposta):**

> Olá! Só para não se perder: viu o vídeo do site? Se puder responder às três perguntas quando tiver um minuto, agradeço muito. Obrigado!

**Se disser que sim:**

> Muito obrigado! Assim que tiver os números, mando-lhe a página antes de a publicar, para ver se está tudo certo. E ao Instagram, quando publicarmos, vai um convite de colaboração para @pizzaria_catarina: é só carregar em «Aceitar».

## Legenda do Instagram (só depois do sim; publicar como Colaboração com @pizzaria_catarina)

> 4,4★ no Google, 168 avaliações, e nenhum site. Agora tem. 🍕
>
> A Pizzaria Catarina, em Altura, só existia em sites de outros. Hoje tem casa própria na internet: reserva com um toque, ementa com preços, e tudo em português, inglês e espanhol.
>
> Tem um negócio? Merece um site assim.
>
> Mande-nos DM ou visite pachecost.com
> 📍 Portugal based · Acting worldwide
>
> #algarve #altura #pizzaria #webdesign #pequenosnegocios

Quando houver números, o reel e a legenda passam a abrir com eles (ex.: «+8 reservas por semana desde que tem site.»), e a página vai ao thread do site da Pacheco Studios (secção Casos).

## Próximo passo

O site da Catarina não conta visitas. Pôr o contador GoatCounter (sem cookies, como nas demos) no site dela, para haver um número de visitas daqui a 30 dias. É uma linha no index.html do ramo da Catarina e um zip novo para o Netlify.

## Execução contínua (cada cliente fechado)

- **Dia da entrega:** o site leva o contador de visitas.
- **Dia 30 do site no ar:** Claude copia `caso.html`, troca imagens e dados, gera o reel (`reel/gerar.py` com o ramo do cliente) e deixa a mensagem pronta (autorização + números + 2 nomes).
- **Tomás:** envia a mensagem, manda as respostas (capturas servem) e liga aos 2 indicados.
- **Claude:** preenche `CASO`, refaz o reel com o número no gancho, passa a página ao thread do site da Pacheco Studios e junta os indicados à lista de prospeção como leads quentes («indicado por …»).
- **Um lembrete só**, ao 4.º dia. Sem sim, nada se publica.
