(function(){
'use strict';
var D=document,H=D.documentElement,W=window;
var RM=W.matchMedia&&W.matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,c){return (c||D).querySelector(s)}
function $$(s,c){return Array.prototype.slice.call((c||D).querySelectorAll(s))}
var TEL='40742500111';
var LS_KEY='sofiapets.lang';

/* ================= TEXTOS ================= */
var T={ro:{
  'title.acasa':'Sofia Pets · Coafor canin și felin în Iași',
  'title.servicii':'Servicii · Sofia Pets, coafor canin Iași',
  'title.programare':'Programare pe WhatsApp · Sofia Pets',
  'title.salonul':'Salonul · Sofia Pets, Alexandru cel Bun',
  'title.galerie':'Galerie · Sofia Pets',
  'title.vizita':'Vizită și program · Sofia Pets, Bd. Alexandru cel Bun 37',
  'banda':'baie|tuns|toaletare completă|câini mici, medii și mari|pisici|fundițe și papioane|Alexandru cel Bun 37',
  'st0':'Înainte: <b>zburlit</b>','st1':'În lucru: <b>mașina de tuns</b>','st2':'După: <b>gata de poză</b>',
  'a.burger2':'Închide meniul',
  'g.1':'Golden, la baie','g.2':'Yorkie, după tuns','g.3':'Pisică „leu”, cu ochelari','g.4':'Bichon, pe pernă','g.5':'Fundal de Crăciun','g.6':'Rochiță roz și fundă','g.7':'Labrador, în brațe','g.8':'Cravată cu buline','g.9':'Blană lungă, la baie','g.10':'Panoul de pe bulevard',
  'm.salut':'Bună ziua! Aș dori o programare la Sofia Pets.','m.animal':'Animal','m.caine':'câine','m.pisica':'pisică',
  'm.talie.mic':'talie mică','m.talie.mediu':'talie medie','m.talie.mare':'talie mare','m.talie.nustiu':'talie: nu știu sigur',
  'm.blana':'Blana','m.b.scurta':'scurtă','m.b.lunga':'lungă','m.b.noduri':'lungă, cu noduri',
  'm.nume':'Numele lui','m.serv':'Serviciu','m.s.baie':'baie','m.s.tuns':'tuns','m.s.complet':'toaletare completă','m.s.sfat':'aș vrea un sfat',
  'm.cand':'Când','m.oricand':'cât mai curând','m.i.dim':'dimineața','m.i.pranz':'la prânz','m.i.dupa':'după-amiaza',
  'm.final':'Mulțumesc!','m.gen':'Bună ziua! Aș dori o programare la Sofia Pets.','loc':'ro-RO'
},
en:{
  'title.acasa':'Sofia Pets · Dog & cat grooming in Iași',
  'title.servicii':'Services · Sofia Pets, dog grooming Iași',
  'title.programare':'Book on WhatsApp · Sofia Pets',
  'title.salonul':'The salon · Sofia Pets, Alexandru cel Bun',
  'title.galerie':'Gallery · Sofia Pets',
  'title.vizita':'Visit & hours · Sofia Pets, Bd. Alexandru cel Bun 37',
  'banda':'bath|haircut|full grooming|small, medium and large dogs|cats|bows and bow ties|Alexandru cel Bun 37',
  'st0':'Before: <b>scruffy</b>','st1':'Working: <b>the clipper</b>','st2':'After: <b>photo-ready</b>',
  'a.burger2':'Close menu',
  'g.1':'Golden, bath time','g.2':'Yorkie, after the cut','g.3':'"Lion cut" cat, with glasses','g.4':'Bichon, on a cushion','g.5':'Christmas backdrop','g.6':'Pink dress and bow','g.7':'Labrador, in good hands','g.8':'Polka-dot tie','g.9':'Long coat, bath time','g.10':'Our sign on the boulevard',
  'm.salut':'Hello! I would like to book an appointment at Sofia Pets.','m.animal':'Pet','m.caine':'dog','m.pisica':'cat',
  'm.talie.mic':'small size','m.talie.mediu':'medium size','m.talie.mare':'large size','m.talie.nustiu':'size: not sure',
  'm.blana':'Coat','m.b.scurta':'short','m.b.lunga':'long','m.b.noduri':'long, with mats',
  'm.nume':'Name','m.serv':'Service','m.s.baie':'bath','m.s.tuns':'haircut','m.s.complet':'full grooming','m.s.sfat':'I would like some advice',
  'm.cand':'When','m.oricand':'as soon as possible','m.i.dim':'morning','m.i.pranz':'around noon','m.i.dupa':'afternoon',
  'm.final':'Thank you!','m.gen':'Hello! I would like to book an appointment at Sofia Pets.','loc':'en-GB',
  'sari':'Skip to content','prez':'<b>PACHECO STUDIOS PRESENTATION</b> · demo website for Sofia Pets','marca.sub':'dog & cat grooming',
  'nav.acasa':'Home','nav.servicii':'Services','nav.programare':'Book','nav.salonul':'The salon','nav.galerie':'Gallery','nav.vizita':'Visit',
  'a.marca':'Sofia Pets — home','a.nav':'Main menu','a.limba':'Language','a.burger':'Open menu','a.prev':'Preview','a.lb':'Enlarged photo','a.prev2':'Previous photo','a.next':'Next photo','a.close':'Close',
  'h.ochi':'Dog & cat grooming · Iași','h.l1':'Comes in scruffy.','h.l2':'Leaves looking sharp.','h.sub':'Baths, haircuts and full grooming for dogs and cats, at 37 Alexandru cel Bun Boulevard.','h.nota':'4.9 on Google · 129 reviews','h.scena':'A fluffy little dog that gets groomed as you scroll','h.indiciu':'Scroll — we groom him on the way','h.cursor':'Or drag with your finger to groom him',
  'cta.prog':'Book him in','conf':'to be confirmed','conf.pret':'price to be confirmed','pret':'Price',
  'b.ochi':'The blue tub','b.t':'Bath time, with someone <em>right beside him</em>.','b.sub':'Shampoo, rinse, drying and plenty of patience. Big dogs welcome too — a Golden or a Labrador fits in the tub and comes out smiling.',
  'alt.golden':'A wet Golden Retriever standing in the blue tub, held by the groomer','alt.labrador':'A Labrador resting its head on the groomer\'s shoulder','alt.maro':'A long-haired brown dog, wet, in the blue tub','alt.yorkie':'A freshly groomed Yorkshire Terrier lying on a blanket','alt.pisica':'A calico cat with a lion cut, glasses and a green bow tie','alt.craciun':'Fluffy dog against a Christmas backdrop with lights and presents','alt.rochita':'White dog in a pink dress with a bow, against a floral backdrop','alt.cravata':'Black-and-white cat wearing a red polka-dot tie','alt.bichon':'White Bichon, freshly groomed, on a fluffy cushion','alt.panou':'The purple Sofia Pets sign on the boulevard, with a corgi drawing',
  'et.golden':'Golden, bath time','et.labrador':'Labrador, in good hands','et.maro':'Long coat, soaking wet','et.cada':'The tub','et.masa':'The grooming table','et.panou':'Our sign on the boulevard',
  'd.ochi':'Who we welcome','d.t':'Dogs. <em>And cats.</em>','d.caini':'Dogs','d.caini.p':'From Yorkies to Goldens. Tell us the size and the coat, and we\'ll tell you how long it takes and what it costs.','d.mic':'small','d.mediu':'medium','d.mare':'large','d.pisici':'Cats','d.pisici.p':'Baths and haircuts for cats, including the "lion cut": short body, fluffy paws and tail.','d.leu':'lion cut','d.baie':'bath',
  'p.ochi':'At the end','p.t':'And a photo <em>to keep on your phone</em>.','p.sub':'Themed backdrops — Christmas, springtime — and accessories for the going-home photo.','p.funda':'bows','p.papion':'bow ties','p.cravata':'ties','p.ochelari':'even glasses',
  'n.t':'129 reviews on Google.','n.p':'That\'s the score owners give once they take their dog (or cat) home. We read it as a promise for the next appointment.',
  'pa.ochi':'How to find us','pa.t':'Look for the purple sign <em>with the corgi</em>.','pa.sub':'At 37 Alexandru cel Bun Boulevard, by the pavement: a purple sign with a giant corgi being groomed by four people on ladders. That\'s us.','pa.ore':'Tuesday: 08:00–19:00 · other days:','pa.btn':'See the map and hours',
  'c.ochi':'Booking','c.t':'Tell us <em>who\'s coming</em>.','c.sub':'Dog or cat, size, coat, what you\'d like done. The WhatsApp message writes itself.',
  's.ochi':'Services','s.t':'Complete grooming <em>for dogs and cats</em>.','s.sub':'The price depends on size, coat and how matted it is. You get it on WhatsApp before you come — no surprises at the till.',
  's1.t':'Bath','s1.p':'Shampoo, a good rinse and drying. For a coat that smells like the park after rain.','s2.t':'Haircut','s2.p':'To breed standard or the way you like it: short for summer, fluffy for winter, eyes clear.','s3.t':'Full grooming','s3.p':'Bath and haircut in one visit. Drop him off scruffy, pick him up neat and fresh.','s4.t':'Cats','s4.p':'Baths and haircuts for cats, including the "lion cut" — short body, fluffy paws and tail.','s5.t':'Photo accessories','s5.p':'A bow, bow tie or necktie and a themed backdrop for the going-home photo.','s6.t':'Not sure what he needs?','s6.p':'Send us a photo of him on WhatsApp. We\'ll tell you what would suit him and how long it would take.','s6.btn':'Send a photo',
  't.ochi':'Size matters','t.t':'Small, medium or large?','t.sub':'The examples are just a guide — if you\'re not sure, pick "not sure" when booking.','t.mic':'Small','t.mic.p':'For example: Yorkie, Bichon, Maltese, Shih Tzu, Pomeranian.','t.mediu':'Medium','t.mediu.p':'For example: Cocker, Beagle, Schnauzer, a very fluffy Bichon.','t.mare':'Large','t.mare.p':'For example: Golden Retriever, Labrador, Shepherd, Husky.',
  'sf.ochi':'Before you come','sf.t':'Four things that help.','sf1.b':'Walk him first.','sf1.s':'A dog who has done his business stays calmer in the tub and on the table.','sf2.b':'Tell us about mats.','sf2.s':'A matted coat takes longer. If you tell us beforehand, we\'ll give you an honest time slot.','sf3.b':'Tell us if he\'s nervous.','sf3.s':'Or if he has a wound, an allergy or a recent operation. It helps us handle him properly.','sf4.b':'Bring the lead and collar.','sf4.s':'For the walk home — freshly groomed, he\'ll want to show off round the block.',
  'pr.ochi':'Booking on WhatsApp','pr.t':'Tell us <em>who\'s coming</em>.','pr.sub':'Tick a few things and the message writes itself. We\'ll confirm on WhatsApp with the exact time and price.',
  'f.animal':'Who\'s coming?','f.caine':'Dog','f.pisica':'Cat','f.talie':'What size?','f.mic':'Small','f.mic.s':'Yorkie, Bichon','f.mediu':'Medium','f.mediu.s':'Cocker, Beagle','f.mare':'Large','f.mare.s':'Golden, Labrador','f.nustiu':'Not sure','f.blana':'What\'s the coat like now?','f.scurta':'Short','f.lunga':'Long','f.noduri':'Long, with mats','f.serv':'What should we do?','f.baie':'Bath','f.tuns':'Haircut','f.complet':'Full grooming','f.sfat':'I\'d like advice','f.er.serv':'Choose what we should do — or "I\'d like advice".','f.cand':'When suits you?','f.zi':'Preferred day','f.interval':'Time of day','f.dim':'Morning','f.pranz':'Around noon','f.dupa':'Afternoon','f.nume':'Your names','f.pet':'Pet\'s name','f.pet.ph':'Max','f.rasa':'Breed (optional)','f.rasa.ph':'Bichon','f.tu':'Your name (optional)',
  'fi.t':'Your message','fi.btn':'Send on WhatsApp','fi.mic':'WhatsApp opens with the message ready. Nothing is sent until you tap "Send".',
  'sa.ochi':'The salon','sa.t':'A neighbourhood salon <em>with a blue tub</em>.','sa.sub':'On Alexandru cel Bun, between the blocks and the shops on the boulevard. Small dogs, big dogs, cats — all go through the same hands.','sa2.ochi':'In short','sa2.t':'Good to know.','sa2.1':'Dogs of every size, and cats.','sa2.2':'Bookings on 0742 500 111, by phone or WhatsApp.','sa2.3':'4.9 on Google from 129 reviews.','sa2.4':'On Facebook, Instagram and TikTok: "Sofia Pets-Coafor Canin".','sa2.5':'The team and years of experience:','sa2.6':'Card payment:',
  'g.ochi':'Gallery','g.t':'Our clients, <em>after</em>.','g.sub':'And a few photos from work in progress. Tap a photo to see it large.',
  'v.ochi':'Visit','v.t':'37 Alexandru cel Bun Blvd, <em>by the purple sign</em>.','v.sub':'Call or message us first — we work by appointment, so nobody waits around holding a lead.','v.adr':'Address','v.dir':'Open in Google Maps →','v.prog':'Bookings','v.prog.s':'Phone or WhatsApp.','v.ore':'Opening hours','v.retele':'On social media','v.retele.s':'Facebook, Instagram and TikTok: search for "Sofia Pets-Coafor Canin".','v.parcare':'Parking',
  'zi.1':'Monday','zi.2':'Tuesday','zi.3':'Wednesday','zi.4':'Thursday','zi.5':'Friday','zi.6':'Saturday','zi.0':'Sunday',
  'ft.desc':'Dog and cat grooming in Iași. Baths, haircuts and full grooming for dogs and cats.','ft.contact':'Contact','ft.pag':'Pages','ft.sal':'ANPC · Alternative dispute resolution (ADR)','ft.odr':'Online dispute resolution (ODR)','ft.firma':'Company name and tax ID:','ft.credit':'Website by Pacheco Studios','fix.suna':'Call'
},
pt:{
  'title.acasa':'Sofia Pets · Tosquias de cães e gatos em Iași',
  'title.servicii':'Serviços · Sofia Pets, tosquias em Iași',
  'title.programare':'Marcação por WhatsApp · Sofia Pets',
  'title.salonul':'O salão · Sofia Pets, Alexandru cel Bun',
  'title.galerie':'Galeria · Sofia Pets',
  'title.vizita':'Visitar e horário · Sofia Pets, Bd. Alexandru cel Bun 37',
  'banda':'banho|tosquia|tratamento completo|cães pequenos, médios e grandes|gatos|laços e laçarotes|Alexandru cel Bun 37',
  'st0':'Antes: <b>desgrenhado</b>','st1':'A trabalhar: <b>a máquina</b>','st2':'Depois: <b>pronto para a foto</b>',
  'a.burger2':'Fechar o menu',
  'g.1':'Golden, no banho','g.2':'Yorkie, depois da tosquia','g.3':'Gata «leão», de óculos','g.4':'Bichon, na almofada','g.5':'Cenário de Natal','g.6':'Vestido cor-de-rosa e laço','g.7':'Labrador, ao colo','g.8':'Gravata às bolinhas','g.9':'Pelo comprido, no banho','g.10':'O painel na avenida',
  'm.salut':'Olá! Gostava de marcar no Sofia Pets.','m.animal':'Animal','m.caine':'cão','m.pisica':'gato',
  'm.talie.mic':'porte pequeno','m.talie.mediu':'porte médio','m.talie.mare':'porte grande','m.talie.nustiu':'porte: não sei bem',
  'm.blana':'Pelo','m.b.scurta':'curto','m.b.lunga':'comprido','m.b.noduri':'comprido, com nós',
  'm.nume':'Nome','m.serv':'Serviço','m.s.baie':'banho','m.s.tuns':'tosquia','m.s.complet':'tratamento completo','m.s.sfat':'queria um conselho',
  'm.cand':'Quando','m.oricand':'o mais cedo possível','m.i.dim':'de manhã','m.i.pranz':'à hora de almoço','m.i.dupa':'à tarde',
  'm.final':'Obrigado!','m.gen':'Olá! Gostava de marcar no Sofia Pets.','loc':'pt-PT',
  'sari':'Saltar para o conteúdo','prez':'<b>APRESENTAÇÃO PACHECO STUDIOS</b> · site de demonstração para o Sofia Pets','marca.sub':'tosquias de cães e gatos',
  'nav.acasa':'Início','nav.servicii':'Serviços','nav.programare':'Marcação','nav.salonul':'O salão','nav.galerie':'Galeria','nav.vizita':'Visitar',
  'a.marca':'Sofia Pets — início','a.nav':'Menu principal','a.limba':'Língua','a.burger':'Abrir o menu','a.prev':'Pré-visualização','a.lb':'Foto ampliada','a.prev2':'Foto anterior','a.next':'Foto seguinte','a.close':'Fechar',
  'h.ochi':'Tosquias de cães e gatos · Iași','h.l1':'Entra desgrenhado.','h.l2':'Sai um brinco.','h.sub':'Banho, tosquia e tratamento completo para cães e gatos, na Avenida Alexandru cel Bun 37.','h.nota':'4,9 no Google · 129 avaliações','h.scena':'Um cãozinho fofo que vai sendo tosquiado à medida que se desce a página','h.indiciu':'Desça — tosquiamo-lo pelo caminho','h.cursor':'Ou arraste com o dedo para o tosquiar',
  'cta.prog':'Marcar','conf':'a confirmar','conf.pret':'preço a confirmar','pret':'Preço',
  'b.ochi':'A banheira azul','b.t':'O banho, com alguém <em>ao lado dele</em>.','b.sub':'Champô, enxaguar, secar e muita paciência. Os cães grandes também entram — um Golden ou um Labrador cabem na banheira e saem a sorrir.',
  'alt.golden':'Um Golden Retriever molhado, de pé na banheira azul, seguro pelo tosquiador','alt.labrador':'Um Labrador encosta a cabeça ao ombro do tosquiador','alt.maro':'Um cão castanho de pelo comprido, molhado, na banheira azul','alt.yorkie':'Um Yorkshire Terrier acabado de tosquiar, deitado numa manta','alt.pisica':'Uma gata tricolor com corte «leão», óculos e laçarote verde','alt.craciun':'Cão fofo num cenário de Natal com luzes e presentes','alt.rochita':'Cão branco com vestido cor-de-rosa e laço, num cenário de flores','alt.cravata':'Gato preto e branco com gravata vermelha às bolinhas','alt.bichon':'Bichon branco, acabado de tosquiar, numa almofada fofa','alt.panou':'O painel roxo do Sofia Pets na avenida, com um corgi desenhado',
  'et.golden':'Golden, no banho','et.labrador':'Labrador, ao colo','et.maro':'Pelo comprido, encharcado','et.cada':'A banheira','et.masa':'A mesa de tosquia','et.panou':'O painel na avenida',
  'd.ochi':'Quem recebemos','d.t':'Cães. <em>E gatos.</em>','d.caini':'Cães','d.caini.p':'Do Yorkie ao Golden. Diga-nos o porte e como está o pelo, e dizemos-lhe quanto tempo demora e quanto custa.','d.mic':'porte pequeno','d.mediu':'porte médio','d.mare':'porte grande','d.pisici':'Gatos','d.pisici.p':'Banho e tosquia para gatos, incluindo o corte «leão»: corpo curto, patas e cauda fofas.','d.leu':'corte leão','d.baie':'banho',
  'p.ochi':'No fim','p.t':'E uma foto <em>para guardar no telemóvel</em>.','p.sub':'Cenários temáticos — de Natal, de primavera — e acessórios para a foto da saída.','p.funda':'laços','p.papion':'laçarotes','p.cravata':'gravatas','p.ochelari':'até óculos',
  'n.t':'129 avaliações no Google.','n.p':'É a nota que os donos dão depois de levarem o cão (ou o gato) para casa. Lemo-la como uma promessa para a próxima marcação.',
  'pa.ochi':'Como nos encontrar','pa.t':'Procure o painel roxo <em>com o corgi</em>.','pa.sub':'Na Avenida Alexandru cel Bun 37, junto ao passeio: um painel roxo com um corgi gigante a ser tosquiado por quatro pessoas em escadotes. É aí.','pa.ore':'Terça: 08:00–19:00 · restantes dias:','pa.btn':'Ver o mapa e o horário',
  'c.ochi':'Marcação','c.t':'Diga-nos <em>quem vem</em>.','c.sub':'Cão ou gato, porte, pelo, o que quer que lhe façamos. A mensagem de WhatsApp escreve-se sozinha.',
  's.ochi':'Serviços','s.t':'Tratamento completo <em>para cães e gatos</em>.','s.sub':'O preço depende do porte, do pelo e de quantos nós tem. Fica a sabê-lo por WhatsApp antes de vir — sem surpresas ao pagar.',
  's1.t':'Banho','s1.p':'Champô, bom enxaguamento e secagem. Para o pelo que cheira a parque depois da chuva.','s2.t':'Tosquia','s2.p':'Segundo o padrão da raça ou como preferir: curto no verão, fofo no inverno, olhos à vista.','s3.t':'Tratamento completo','s3.p':'Banho e tosquia na mesma visita. Deixa-o desgrenhado, leva-o arranjado e perfumado.','s4.t':'Gatos','s4.p':'Banho e tosquia para gatos, incluindo o corte «leão» — corpo curto, patas e cauda fofas.','s5.t':'Acessórios para a foto','s5.p':'Laço, laçarote ou gravata e um cenário temático para a foto da saída.','s6.t':'Não sabe do que precisa?','s6.p':'Mande-nos uma foto dele por WhatsApp. Dizemos-lhe o que lhe ficava bem e quanto tempo demorava.','s6.btn':'Enviar uma foto',
  't.ochi':'O porte conta','t.t':'Pequeno, médio ou grande?','t.sub':'Os exemplos são indicativos — se não souber, escolha «não sei» na marcação.','t.mic':'Porte pequeno','t.mic.p':'Por exemplo: Yorkie, Bichon, Maltês, Shih Tzu, Pomerânia.','t.mediu':'Porte médio','t.mediu.p':'Por exemplo: Cocker, Beagle, Schnauzer, um Bichon com muito pelo.','t.mare':'Porte grande','t.mare.p':'Por exemplo: Golden Retriever, Labrador, Pastor, Husky.',
  'sf.ochi':'Antes de vir','sf.t':'Quatro coisas que ajudam.','sf1.b':'Passeie-o antes.','sf1.s':'Um cão que já fez as necessidades fica mais calmo na banheira e na mesa.','sf2.b':'Avise se tem nós.','sf2.s':'Pelo com nós leva mais tempo. Se nos disser antes, damos-lhe uma hora certa.','sf3.b':'Avise se é medroso.','sf3.s':'Ou se tem uma ferida, uma alergia, uma operação recente. Ajuda-nos a tratá-lo como deve ser.','sf4.b':'Traga a trela e a coleira.','sf4.s':'Para o regresso — acabado de tosquiar, vai querer exibir-se no bairro.',
  'pr.ochi':'Marcação por WhatsApp','pr.t':'Diga-nos <em>quem vem</em>.','pr.sub':'Escolhe umas quantas coisas e a mensagem escreve-se sozinha. Confirmamos por WhatsApp, com a hora certa e o preço.',
  'f.animal':'Quem vem?','f.caine':'Cão','f.pisica':'Gato','f.talie':'Que porte tem?','f.mic':'Pequeno','f.mic.s':'Yorkie, Bichon','f.mediu':'Médio','f.mediu.s':'Cocker, Beagle','f.mare':'Grande','f.mare.s':'Golden, Labrador','f.nustiu':'Não sei','f.blana':'Como está o pelo?','f.scurta':'Curto','f.lunga':'Comprido','f.noduri':'Comprido, com nós','f.serv':'O que lhe fazemos?','f.baie':'Banho','f.tuns':'Tosquia','f.complet':'Tratamento completo','f.sfat':'Quero um conselho','f.er.serv':'Escolha o que lhe fazemos — ou «Quero um conselho».','f.cand':'Quando lhe dá jeito?','f.zi':'Dia preferido','f.interval':'Período','f.dim':'Manhã','f.pranz':'Hora de almoço','f.dupa':'Tarde','f.nume':'Como se chamam?','f.pet':'Nome dele / dela','f.pet.ph':'Max','f.rasa':'Raça (opcional)','f.rasa.ph':'Bichon','f.tu':'O seu nome (opcional)',
  'fi.t':'A sua mensagem','fi.btn':'Enviar por WhatsApp','fi.mic':'O WhatsApp abre com a mensagem pronta. Nada é enviado até carregar em «Enviar».',
  'sa.ochi':'O salão','sa.t':'Um salão de bairro, <em>com banheira azul</em>.','sa.sub':'Na Alexandru cel Bun, entre os prédios e as lojas da avenida. Cães pequenos, cães grandes, gatos — passam todos pelas mesmas mãos.','sa2.ochi':'Em resumo','sa2.t':'O que precisa de saber.','sa2.1':'Cães de todos os portes, e gatos.','sa2.2':'Marcações pelo 0742 500 111, por telefone ou WhatsApp.','sa2.3':'4,9 no Google em 129 avaliações.','sa2.4':'No Facebook, Instagram e TikTok: «Sofia Pets-Coafor Canin».','sa2.5':'A equipa e os anos de experiência:','sa2.6':'Pagamento com cartão:',
  'g.ochi':'Galeria','g.t':'Os nossos clientes, <em>depois</em>.','g.sub':'E algumas fotos do trabalho. Toque numa foto para a ver em grande.',
  'v.ochi':'Visitar','v.t':'Bd. Alexandru cel Bun 37, <em>junto ao painel roxo</em>.','v.sub':'Ligue ou escreva antes — trabalhamos por marcação, para ninguém ficar à espera de trela na mão.','v.adr':'Morada','v.dir':'Abrir no Google Maps →','v.prog':'Marcações','v.prog.s':'Telefone ou WhatsApp.','v.ore':'Horário','v.retele':'Nas redes','v.retele.s':'Facebook, Instagram e TikTok: procure «Sofia Pets-Coafor Canin».','v.parcare':'Estacionamento',
  'zi.1':'Segunda','zi.2':'Terça','zi.3':'Quarta','zi.4':'Quinta','zi.5':'Sexta','zi.6':'Sábado','zi.0':'Domingo',
  'ft.desc':'Tosquias de cães e gatos em Iași. Banho, tosquia e tratamento completo para cães e gatos.','ft.contact':'Contacto','ft.pag':'Páginas','ft.sal':'ANPC · Resolução alternativa de litígios (RAL)','ft.odr':'Resolução de litígios em linha (RLL / ODR)','ft.firma':'Denominação e NIF da empresa:','ft.credit':'Site feito pela Pacheco Studios','fix.suna':'Ligar'
}};
var lang=H.dataset.lang||'ro';
function t(k){return (T[lang]&&T[lang][k]!=null)?T[lang][k]:(T.ro[k]!=null?T.ro[k]:k)}

/* captura o romeno que já está no HTML */
$$('[data-t]').forEach(function(e){var k=e.getAttribute('data-t');if(T.ro[k]==null)T.ro[k]=e.innerHTML.trim()});
$$('[data-ta]').forEach(function(e){e.getAttribute('data-ta').split(';').forEach(function(p){var a=p.split(':');if(T.ro[a[1]]==null)T.ro[a[1]]=e.getAttribute(a[0])||''})});

function applyLang(l){
  lang=T[l]?l:'ro';H.dataset.lang=lang;H.lang=lang==='pt'?'pt-PT':lang;
  $$('[data-t]').forEach(function(e){var v=t(e.getAttribute('data-t'));if(e.innerHTML!==v)e.innerHTML=v});
  $$('[data-ta]').forEach(function(e){e.getAttribute('data-ta').split(';').forEach(function(p){var a=p.split(':');e.setAttribute(a[0],t(a[1]))})});
  $$('.lang button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===lang?'true':'false')});
  splitH1();fillBanda();
  var wa='https://wa.me/'+TEL+'?text='+encodeURIComponent(t('m.gen'));
  $$('.wa-link').forEach(function(a){a.href=wa});
  if(cur)D.title=t('title.'+cur);
  if(pet0)setStare(pet0.p);
  updMsg();
  var bg=$('.burger');bg.setAttribute('aria-label',bg.getAttribute('aria-expanded')==='true'?t('a.burger2'):t('a.burger'));
}
$$('.lang button').forEach(function(b){b.addEventListener('click',function(){applyLang(b.dataset.l);try{localStorage.setItem(LS_KEY,lang)}catch(e){}})});

function splitH1(){
  var h=$('#h1'),i=0,full=[];
  $$('[data-split]',h).forEach(function(s){
    var txt=s.textContent;full.push(txt);
    s.innerHTML=txt.split(' ').map(function(w){return '<span style="display:inline-block;white-space:nowrap">'+w.split('').map(function(c){return '<span class="c" style="--i:'+(i++)+'">'+c+'</span>'}).join('')+'</span>'}).join(' ');
    s.setAttribute('aria-hidden','true');
  });
  h.setAttribute('aria-label',full.join(' '));
}
function fillBanda(){
  var b=$('#banda');if(!b)return;var it=t('banda').split('|');var h='';
  for(var r=0;r<4;r++)it.forEach(function(x){h+='<span>'+x+'</span>'});
  b.innerHTML=h;
}

/* ================= O CÃO (SVG) ================= */
var NS='http://www.w3.org/2000/svg';
function el(tg,a,p){var e=D.createElementNS(NS,tg);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
function rnd(seed){var s=seed%2147483647;if(s<=0)s+=2147483646;return function(){s=s*16807%2147483647;return (s-1)/2147483646}}
var COL={
  crem:{f:'#F7E9D7',s:'#EAD3B7',o:'#D9BC98',fir:['#F7E9D7','#FFF4E6','#EFDDC4','#F3E3CC']},
  caise:{f:'#F2C48D',s:'#E2A869',o:'#C98C4C',fir:['#F2C48D','#F8D6AA','#E8B477','#F5CC9B']},
  aur:{f:'#E7C891',s:'#D3AE6E',o:'#B99252',fir:['#E7C891','#F0D7A8','#DDBB7C','#EBD09E']}
};
function inside(pr,x,y){
  if(pr.t==='e'){var a=(x-pr.cx)/pr.rx,b=(y-pr.cy)/pr.ry;return a*a+b*b<1}
  return x>pr.x&&x<pr.x+pr.w&&y>pr.y&&y<pr.y+pr.h;
}
function buildPet(svg,o){
  o=o||{};var kind=o.kind||'caine',fur=o.fur||'lunga',size=o.size||1,col=COL[o.col||'crem'],R=rnd(o.seed||7);
  while(svg.firstChild)svg.removeChild(svg.firstChild);
  var FL=266;
  var root=el('g',{'class':'caine-tot'},svg);
  el('ellipse',{cx:210,cy:FL+6,rx:150*size,ry:10*size,fill:'rgba(42,20,49,.28)'},root);
  var g=el('g',{transform:'translate(210 '+FL+') scale('+size+') translate(-210 -'+FL+')'},root);
  var prims,P;
  if(kind==='pisica'){
    prims=[{t:'e',cx:192,cy:192,rx:80,ry:38,p:'corp'},{t:'e',cx:262,cy:160,rx:24,ry:30,p:'gat'},{t:'e',cx:292,cy:128,rx:37,ry:32,p:'cap'},
      {t:'r',x:132,y:196,w:18,h:70,p:'picior'},{t:'r',x:152,y:200,w:20,h:66,p:'picior'},{t:'r',x:232,y:196,w:18,h:70,p:'picior'},{t:'r',x:252,y:200,w:20,h:66,p:'picior'},
      {t:'e',cx:96,cy:100,rx:13,ry:13,p:'coada'}];
    el('path',{d:'M116 182C70 170 64 120 96 100',fill:'none',stroke:col.s,'stroke-width':16,'stroke-linecap':'round'},g);
    [[132,196,18,70,1],[232,196,18,70,1]].forEach(function(r){el('rect',{x:r[0],y:r[1],width:r[2],height:r[3],rx:9,fill:col.s},g)});
    el('ellipse',{cx:192,cy:192,rx:80,ry:38,fill:col.f},g);
    el('ellipse',{cx:168,cy:180,rx:30,ry:19,fill:'#E8A04F',opacity:.9},g);
    el('ellipse',{cx:222,cy:192,rx:22,ry:15,fill:'#3A2B2E',opacity:.85},g);
    [[152,200,20,66],[252,200,20,66]].forEach(function(r){el('rect',{x:r[0],y:r[1],width:r[2],height:r[3],rx:10,fill:col.f},g)});
    el('ellipse',{cx:262,cy:160,rx:24,ry:30,fill:col.f},g);
    el('path',{d:'M266 110 272 74 294 100Z',fill:col.f},g);el('path',{d:'M294 98 318 76 322 114Z',fill:col.f},g);
    el('path',{d:'M271 102 274 84 286 99Z',fill:'#E7A2B0'},g);el('path',{d:'M300 98 315 84 316 106Z',fill:'#E7A2B0'},g);
    el('ellipse',{cx:292,cy:128,rx:37,ry:32,fill:col.f},g);
    el('path',{d:'M268 112c6-10 16-14 22-12-2 8-10 14-22 12z',fill:'#E8A04F'},g);
    P={eyes:el('g',{},g)};
    [[280,124],[304,124]].forEach(function(e){el('ellipse',{cx:e[0],cy:e[1],rx:6,ry:5,fill:'#7FB24A'},P.eyes);el('ellipse',{cx:e[0],cy:e[1],rx:1.6,ry:4.4,fill:'#2A1431'},P.eyes)});
  }else{
    prims=[{t:'e',cx:190,cy:170,rx:84,ry:46,p:'corp'},{t:'e',cx:262,cy:142,rx:30,ry:38,p:'gat'},{t:'e',cx:298,cy:106,rx:42,ry:40,p:'cap'},{t:'e',cx:338,cy:124,rx:24,ry:18,p:'bot'},
      {t:'r',x:126,y:180,w:24,h:86,p:'picior'},{t:'r',x:150,y:186,w:26,h:80,p:'picior'},{t:'r',x:232,y:180,w:24,h:86,p:'picior'},{t:'r',x:256,y:186,w:26,h:80,p:'picior'},
      {t:'e',cx:98,cy:110,rx:15,ry:15,p:'coada'},{t:'e',cx:274,cy:124,rx:15,ry:30,p:'ureche'}];
    el('path',{d:'M116 150C96 142 92 128 98 112',fill:'none',stroke:col.s,'stroke-width':12,'stroke-linecap':'round'},g);
    el('circle',{cx:98,cy:110,r:15,fill:col.s},g);
    [[126,180,24,86],[232,180,24,86]].forEach(function(r){el('rect',{x:r[0],y:r[1],width:r[2],height:r[3],rx:12,fill:col.s},g)});
    el('ellipse',{cx:190,cy:170,rx:84,ry:46,fill:col.f},g);
    [[150,186,26,80],[256,186,26,80]].forEach(function(r){el('rect',{x:r[0],y:r[1],width:r[2],height:r[3],rx:13,fill:col.f},g)});
    el('ellipse',{cx:262,cy:142,rx:30,ry:38,fill:col.f},g);
    el('ellipse',{cx:298,cy:106,rx:42,ry:40,fill:col.f},g);
    el('ellipse',{cx:338,cy:124,rx:24,ry:18,fill:col.f},g);
    P={eyes:el('g',{},g)};
    el('circle',{cx:318,cy:98,r:5.5,fill:'#2A1431'},P.eyes);el('circle',{cx:320,cy:96,r:1.8,fill:'#fff'},P.eyes);
    el('ellipse',{cx:274,cy:124,rx:15,ry:30,fill:col.s,transform:'rotate(14 274 124)'},g);
  }
  var puffs=el('g',{},g),strands=el('g',{},g),top=el('g',{},g);
  if(kind==='pisica'){
    el('path',{d:'M292 134l-5 -4h10z',fill:'#E07B8E'},top);
    el('path',{d:'M292 136q-4 6 -9 4M292 136q4 6 9 4',fill:'none',stroke:'#2A1431','stroke-width':1.8,'stroke-linecap':'round'},top);
    el('path',{d:'M270 134h-26M270 139l-24 4M314 134h26M314 139l24 4',stroke:'#2A1431','stroke-width':1.3,opacity:.7},top);
  }else{
    el('ellipse',{cx:357,cy:116,rx:8.5,ry:7,fill:'#2A1431'},top);
    el('path',{d:'M342 132q-8 10 -18 4',fill:'none',stroke:'#2A1431','stroke-width':2.4,'stroke-linecap':'round'},top);
    el('ellipse',{cx:333,cy:139,rx:5,ry:6,fill:'#E07B8E'},top);
  }
  var items=[];
  function thr(x){return .08+Math.max(0,Math.min(1,(x-80)/292))*.78}
  var keep=kind==='pisica'?{cap:1,coada:1}:{};
  var base=fur==='scurta'?0:(kind==='pisica'?13:23);
  function strand(x,y,nx,ny,L,part){
    var gx=nx,gy=ny+.6;var m=Math.sqrt(gx*gx+gy*gy);gx/=m;gy/=m;
    var sx=x-nx*3,sy=y-ny*3,ex=sx+gx*L,ey=sy+gy*L,w=(R()-.5)*L*.5;
    var c=col.fir[(R()*col.fir.length)|0];
    var pth=el('path',{d:'M'+sx.toFixed(1)+' '+sy.toFixed(1)+'Q'+(sx+gx*L*.5-gy*w).toFixed(1)+' '+(sy+gy*L*.5+gx*w).toFixed(1)+' '+ex.toFixed(1)+' '+ey.toFixed(1),stroke:c,'stroke-width':(5+R()*3.5).toFixed(1),fill:'none','stroke-linecap':'round','class':'fir'},strands);
    var dy=FL-Math.max(sy,ey)+4+R()*6;
    pth.style.setProperty('--dx',((R()-.5)*36).toFixed(0)+'px');pth.style.setProperty('--dy',dy.toFixed(0)+'px');pth.style.setProperty('--r',((R()-.5)*150).toFixed(0)+'deg');
    items.push({e:pth,t:keep[part]?9:thr(x)+(R()-.5)*.05,cut:false});
    if(fur==='noduri'&&R()<.12){var k=el('circle',{cx:(sx+gx*L*.6).toFixed(1),cy:(sy+gy*L*.6).toFixed(1),r:(4+R()*3).toFixed(1),fill:col.o,'class':'fir'},strands);k.style.setProperty('--dx','0px');k.style.setProperty('--dy',(FL-sy).toFixed(0)+'px');k.style.setProperty('--r','40deg');items.push({e:k,t:keep[part]?9:thr(x),cut:false})}
  }
  if(base){
    prims.forEach(function(pr,ix){
      var pts=[];
      if(pr.t==='e'){var per=2*Math.PI*Math.sqrt((pr.rx*pr.rx+pr.ry*pr.ry)/2),n=Math.round(per/5.5);
        for(var i=0;i<n;i++){var a=i/n*2*Math.PI+R()*.1,x=pr.cx+pr.rx*Math.cos(a),y=pr.cy+pr.ry*Math.sin(a),nx=Math.cos(a)/pr.rx,ny=Math.sin(a)/pr.ry,m=Math.sqrt(nx*nx+ny*ny);pts.push([x,y,nx/m,ny/m])}}
      else{for(var yy=pr.y+8;yy<pr.y+pr.h-4;yy+=5.5){pts.push([pr.x,yy,-1,0]);pts.push([pr.x+pr.w,yy,1,0])}for(var xx=pr.x+4;xx<pr.x+pr.w;xx+=7)pts.push([xx,pr.y+pr.h-2,0,1])}
      pts.forEach(function(q,j){
        var x=q[0],y=q[1],ok=true;
        prims.forEach(function(o2,k2){if(k2!==ix&&o2.p!=='ureche'&&inside(o2,x+q[2]*2,y+q[3]*2))ok=false});
        if(!ok)return;
        if(y>FL-2)return;
        var L=base*(.6+R()*.8)*(pr.p==='picior'?.8:1)*(pr.p==='bot'?.7:1);
        if(pr.p==='ureche'&&q[3]<.2)return;
        if(fur!=='scurta'&&j%2===0&&pr.p!=='picior'&&pr.p!=='bot'){
          var r=(kind==='pisica'?7:11)+R()*7,pc=el('circle',{cx:(x+q[2]*r*.45).toFixed(1),cy:(y+q[3]*r*.45).toFixed(1),r:r.toFixed(1),fill:col.fir[j%col.fir.length],'class':'puf'},puffs);
          items.push({e:pc,t:keep[pr.p]?9:thr(x)+(R()-.5)*.05,cut:false});
        }
        strand(x,y,q[2],q[3],L,pr.p);
      });
    });
    if(kind!=='pisica'){for(var f=0;f<11;f++){var fx=300+f*3.4+R()*3,fy=70+R()*8;strand(fx,fy,.35,.8,28+R()*10,'cap')}}
  }
  // laço / laçarote
  var bow=el('g',{'class':'funda'},g);
  if(kind==='pisica'){el('path',{d:'M262 136 246 126v20zM262 136l16-10v20z',fill:'#1F7A4D'},bow);el('rect',{x:257,y:131,width:10,height:10,rx:3,fill:'#145234'},bow)}
  else{el('path',{d:'M296 62 270 46 272 80zM296 62l26-16-2 34z',fill:'#F4A259',stroke:'#2A1431','stroke-width':2.5,'stroke-linejoin':'round'},bow);el('circle',{cx:296,cy:63,r:7,fill:'#E07B3C',stroke:'#2A1431','stroke-width':2.5},bow)}
  var sp=el('g',{},g);
  [[350,60,1],[248,70,.8],[370,150,.7]].forEach(function(s){el('path',{d:'M0 -12 3 -3 12 0 3 3 0 12 -3 3 -12 0 -3 -3z',fill:'#FFE7B0',transform:'translate('+s[0]+' '+s[1]+') scale('+s[2]+')','class':'scanteie'},sp)});
  // máquina
  var mc=el('g',{'class':'masina',opacity:0},g),mv=el('g',{'class':'masina-vib'},mc);
  el('path',{d:'M-30 4C-60 10-70 40-50 60',fill:'none',stroke:'#2A1431','stroke-width':3,'stroke-linecap':'round'},mv);
  el('rect',{x:-34,y:-11,width:52,height:22,rx:11,fill:'#2A1431'},mv);
  el('rect',{x:-26,y:-6,width:20,height:12,rx:6,fill:'#F4A259'},mv);
  el('rect',{x:16,y:-12,width:12,height:24,rx:3,fill:'#C9D1D9'},mv);
  for(var tt=-10;tt<=10;tt+=4)el('rect',{x:27,y:tt-1,width:5,height:2,fill:'#8A949E'},mv);
  function topAt(x){var m=FL;prims.forEach(function(pr){if(pr.t==='e'&&Math.abs(x-pr.cx)<pr.rx){var y=pr.cy-pr.ry*Math.sqrt(1-Math.pow((x-pr.cx)/pr.rx,2));if(y<m)m=y}});return m}
  var api={p:-1,svg:svg,items:items,setP:function(p){
    api.p=p;
    for(var i=0;i<items.length;i++){var it=items[i],c=p>=it.t;if(c!==it.cut){it.cut=c;it.e.classList.toggle('taiat',c)}}
    var q=Math.max(0,Math.min(1,(p-.08)/.78)),x=80+q*292,vis=p>.05&&p<.88;
    mc.setAttribute('opacity',vis?1:0);
    if(vis)mc.setAttribute('transform','translate('+x.toFixed(1)+' '+(topAt(x)-16).toFixed(1)+') rotate(-28)');
    svg.classList.toggle('gata',p>=.9);
  }};
  api.animate=function(to,ms){
    var from=Math.max(0,api.p),t0=null;ms=ms||1500;
    if(RM){api.setP(to);return}
    function f(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/ms);api.setP(from+(to-from)*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)api._r=requestAnimationFrame(f)}
    cancelAnimationFrame(api._r);api._r=requestAnimationFrame(f);
  };
  api.setP(0);
  return api;
}

/* ================= HERÓI: tosquia ao scroll ================= */
var pet0=null,tuns=$('#tuns'),slider=$('#pieptene'),stareEt=$('#stare-et'),lastSt=-1;
function setStare(p){var s=p<.06?0:(p<.9?1:2);if(s!==lastSt||true){stareEt.innerHTML=t('st'+s)}lastSt=s}
function heroP(p){if(!pet0)return;pet0.setP(p);var s=p<.06?0:(p<.9?1:2);if(s!==lastSt){lastSt=s;stareEt.innerHTML=t('st'+s)}}
pet0=buildPet($('#scena-erou'),{kind:'caine',fur:'lunga',col:'crem',seed:11});
setStare(0);
var scrolly=!RM;
function hh(){return $('#bara').offsetHeight}
function heroRange(){var r=tuns.getBoundingClientRect();var len=tuns.offsetHeight-(W.innerHeight-hh());return {top:r.top+W.pageYOffset-hh(),len:Math.max(1,len)}}
function onScroll(){
  $('#bara').classList.toggle('scrolled',W.pageYOffset>8);
  if(cur!=='acasa'||!scrolly)return;
  var g=heroRange(),p=(W.pageYOffset-g.top)/(g.len*.86);p=Math.max(0,Math.min(1,p));
  heroP(p);slider.value=Math.round(p*100);
}
W.addEventListener('scroll',onScroll,{passive:true});
W.addEventListener('resize',onScroll);
slider.addEventListener('input',function(){
  var v=slider.value/100;
  if(scrolly){var g=heroRange();W.scrollTo(0,g.top+v*g.len*.86)}else heroP(v);
});
if(RM){heroP(1);slider.value=100}

/* ================= ROUTER ================= */
var PAGES=['acasa','servicii','programare','salonul','galerie','vizita'],cur=null,first=true;
function route(){
  var h=(location.hash||'').replace(/^#\/?/,'').split(/[?#]/)[0];
  var pg=PAGES.indexOf(h)>-1?h:'acasa';
  $$('.pg').forEach(function(s){s.hidden=s.dataset.pg!==pg});
  $$('.nav a,.meniu a[data-pg]').forEach(function(a){if(a.dataset.pg===pg)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
  cur=pg;D.title=t('title.'+pg);
  closeMenu();
  if(!first){W.scrollTo(0,0);var f=$('.pg[data-pg="'+pg+'"] [tabindex="-1"]');if(f)f.focus({preventScroll:true})}
  first=false;
  if(pg==='vizita'){var fr=$('#harta');if(fr&&!fr.src)fr.src=fr.dataset.src}
  if(pg==='acasa')onScroll();
  var fx=$('.cta-fix .wa-link');if(fx)fx.href='https://wa.me/'+TEL+'?text='+encodeURIComponent(t('m.gen'));
  if(pg==='programare')updMsg();
  marcaAzi();
}
W.addEventListener('hashchange',route);

/* burger */
var burger=$('.burger'),meniu=$('#meniu');
function closeMenu(){meniu.classList.remove('deschis');burger.setAttribute('aria-expanded','false');burger.setAttribute('aria-label',t('a.burger'));D.body.style.overflow=''}
burger.addEventListener('click',function(){var o=burger.getAttribute('aria-expanded')!=='true';meniu.classList.toggle('deschis',o);burger.setAttribute('aria-expanded',o?'true':'false');burger.setAttribute('aria-label',o?t('a.burger2'):t('a.burger'));D.body.style.overflow=o?'hidden':''});
D.addEventListener('keydown',function(e){if(e.key==='Escape'&&meniu.classList.contains('deschis')){closeMenu();burger.focus()}});

function marcaAzi(){var d=new Date().getDay();$$('#ore div').forEach(function(r){r.classList.toggle('azi',+r.dataset.z===d)})}

/* ================= PROGRAMARE ================= */
var form=$('#form-prog'),pet1=null,lastKey='';
function val(n){var e=form.querySelector('input[name="'+n+'"]:checked');return e?e.value:''}
function fmtDate(v){try{var p=v.split('-');var d=new Date(+p[0],+p[1]-1,+p[2]);return d.toLocaleDateString(t('loc'),{weekday:'long',day:'numeric',month:'long'})}catch(e){return v}}
function updMsg(){
  if(!form)return;
  var a=val('animal'),ta=val('talie'),b=val('blana'),s=val('serv'),iv=val('interval'),zi=$('#f-zi').value,pet=$('#f-pet').value.trim(),rasa=$('#f-rasa').value.trim(),tu=$('#f-tu').value.trim();
  $('#pas-talie').hidden=a==='pisica';
  var n=1;$$('.pas',form).forEach(function(fs){if(!fs.hidden){fs.querySelector('legend i').textContent=n++}});
  var L=[t('m.salut'),''];
  L.push('• '+t('m.animal')+': '+(a==='pisica'?t('m.pisica'):t('m.caine')+(ta?', '+t('m.talie.'+ta):''))+(rasa?' ('+rasa+')':''));
  if(pet)L.push('• '+t('m.nume')+': '+pet);
  if(b)L.push('• '+t('m.blana')+': '+t('m.b.'+b));
  L.push('• '+t('m.serv')+': '+(s?t('m.s.'+s):'…'));
  L.push('• '+t('m.cand')+': '+(zi?fmtDate(zi):t('m.oricand'))+(iv?', '+t('m.i.'+iv):''));
  L.push('');L.push(t('m.final')+(tu?'\n'+tu:''));
  var m=L.join('\n');$('#mesaj').textContent=m;
  var href='https://wa.me/'+TEL+'?text='+encodeURIComponent(m);$('#trimite').href=href;
  var fx=$('.cta-fix .wa-link');if(fx&&cur==='programare')fx.href=href;
  var key=a+ta+b;
  if(key!==lastKey){lastKey=key;
    var sz=a==='pisica'?.82:({mic:.62,mediu:.8,mare:1,nustiu:.8}[ta]||.8);
    pet1=buildPet($('#scena-fisa'),{kind:a||'caine',fur:b||'lunga',size:sz,col:a==='pisica'?'crem':({mic:'crem',mediu:'caise',mare:'aur'}[ta]||'caise'),seed:3});
    pet1.svg.classList.remove('gata');
    if(s==='tuns'||s==='complet')pet1.setP(1);
  }
}
if(form){
  form.addEventListener('change',function(e){
    if(e.target.name==='serv'){$('#er-serv').classList.remove('vis');var s=val('serv');if(pet1){if(s==='tuns'||s==='complet')pet1.animate(1,1500);else pet1.animate(0,500)}}
    updMsg();
  });
  form.addEventListener('input',updMsg);
  form.addEventListener('submit',function(e){e.preventDefault()});
  var today=new Date();$('#f-zi').min=today.getFullYear()+'-'+String(today.getMonth()+1).padStart(2,'0')+'-'+String(today.getDate()).padStart(2,'0');
  if('IntersectionObserver' in W){new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&pet1){var s=val('serv');if(s==='tuns'||s==='complet'){pet1.setP(0);pet1.animate(1,1600)}}})},{threshold:.6}).observe($('.fisa-scena'))}
  $$('#trimite,.cta-fix .wa-link').forEach(function(bt){bt.addEventListener('click',function(e){if(cur!=='programare')return;if(!val('serv')){e.preventDefault();$('#er-serv').classList.add('vis');var r=form.querySelector('input[name="serv"]');r.focus();r.closest('.pas').scrollIntoView({behavior:RM?'auto':'smooth',block:'center'})}})});
}

/* ================= GALERIA ================= */
var GAL=[['baie-golden','alt.golden',1],['yorkie-dupa-tuns','alt.yorkie',2],['pisica-ochelari','alt.pisica',3],['bichon-pe-perna','alt.bichon',4],['sedinta-foto-craciun','alt.craciun',5],['catel-rochita-roz','alt.rochita',6],['labrador-in-lucru','alt.labrador',7],['pisica-cravata','alt.cravata',8],['baie-catel-maro','alt.maro',9],['panou-bulevard','alt.panou',10]];
var FB=['#E9EEF7','#E9D8CC','#E6E9F2','#2F5E66','#5B3A2E','#7FA77A','#F2F2F2','#EDEDED','#F4F0EC','#C9D3DD'];
var gal=$('#gal');
if(gal){
  gal.innerHTML=GAL.map(function(g,i){return '<button type="button" data-i="'+i+'"><figure style="margin:0"><div class="ph" style="aspect-ratio:3/4"><svg viewBox="0 0 300 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="300" height="400" fill="'+FB[i]+'"/><g fill="#9B3787" opacity=".35"><ellipse cx="150" cy="215" rx="30" ry="25"/><circle cx="112" cy="180" r="14"/><circle cx="135" cy="155" r="14"/><circle cx="165" cy="155" r="14"/><circle cx="188" cy="180" r="14"/></g></svg><img src="media/'+g[0]+'.webp" alt="" data-ta="alt:'+g[1]+'" loading="lazy" onerror="this.remove()"></div><figcaption data-t="g.'+g[2]+'"></figcaption></figure></button>'}).join('');
  var lb=$('#lb'),li=0;
  function show(i){li=(i+GAL.length)%GAL.length;var g=GAL[li];$('#lb-img').src='media/'+g[0]+'.webp';$('#lb-img').alt=t(g[1]);$('#lb-cap').textContent=t('g.'+g[2])}
  gal.addEventListener('click',function(e){var b=e.target.closest('button[data-i]');if(!b)return;show(+b.dataset.i);if(lb.showModal)lb.showModal();else lb.setAttribute('open','')});
  $('#lb-prev').addEventListener('click',function(){show(li-1)});
  $('#lb-next').addEventListener('click',function(){show(li+1)});
  $('#lb-x').addEventListener('click',function(){lb.close()});
  lb.addEventListener('click',function(e){if(e.target===lb)lb.close()});
  lb.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')show(li-1);if(e.key==='ArrowRight')show(li+1)});
}

/* ================= REVELAÇÃO ================= */
if('IntersectionObserver' in W&&!RM){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  $$('.rv').forEach(function(e){io.observe(e)});
}else $$('.rv').forEach(function(e){e.classList.add('in')});

/* ================= ARRANQUE ================= */
if(!RM)H.classList.add('intrare');
setTimeout(function(){H.classList.remove('intrare')},3200);
route();
applyLang(lang);
onScroll();
})();
