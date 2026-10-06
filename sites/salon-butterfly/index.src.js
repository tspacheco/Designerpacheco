(function(){
'use strict';
var D=document,H=D.documentElement,W=window;
var RM=W.matchMedia&&W.matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,c){return (c||D).querySelector(s)}
function $$(s,c){return Array.prototype.slice.call((c||D).querySelectorAll(s))}
var TEL='40748578709',LS_KEY='butterfly.lang';
var LUCRARI=/*__LUCRARI__*/[];

/* ================= DADOS ================= */
var CUL=[['nud','#E8B9A4'],['pudra','#E9A6B4'],['bombon','#E8588C'],['coral','#F2665A'],['rosu','#C8102E'],['cireasa','#A3123F'],['bordo','#6B0F2A'],['pruna','#4B1D3F'],['lila','#B79AD6'],['lavanda','#7E68C2'],['morpho','#2448C8'],['bleu','#8EC5E8'],['salvie','#9DB89A'],['smarald','#0F6B4F'],['negru','#1B171E'],['laptos','#F4EFEA'],['auriu','#C9A75A']];
function ci(id){for(var i=0;i<CUL.length;i++)if(CUL[i][0]===id)return i;return 5}
var SERV=['semi','gel','intretinere','clasica','pedichiura','nailart'];
var FORME=['oval','migdala','patrat','balerina','stiletto'];
var LUNG=['scurt','mediu','lung'];
var FIN=['lucios','mat','cromat','cateye'];
var DECOR=['fara','french','ombre','sclipici','accent','fluturas','linii'];
var IV=['dim','pranz','dupa'];
var IDEI=[
  {id:1,forma:'migdala',lung:'mediu',cul:'cireasa',fin:'lucios',decor:'fara',bg:'#2A1430'},
  {id:2,forma:'migdala',lung:'mediu',cul:'pudra',fin:'lucios',decor:'french',bg:'#3A1E42'},
  {id:3,forma:'oval',lung:'scurt',cul:'lila',fin:'lucios',decor:'fluturas',bg:'#2A1430'},
  {id:4,forma:'balerina',lung:'lung',cul:'negru',fin:'mat',decor:'linii',bg:'#4A2A52'},
  {id:5,forma:'patrat',lung:'mediu',cul:'bombon',fin:'lucios',decor:'ombre',bg:'#3A1E42'},
  {id:6,forma:'stiletto',lung:'lung',cul:'morpho',fin:'cromat',decor:'fara',bg:'#2A1430'},
  {id:7,forma:'oval',lung:'scurt',cul:'nud',fin:'lucios',decor:'accent',bg:'#4A2A52'},
  {id:8,forma:'migdala',lung:'lung',cul:'bordo',fin:'cateye',decor:'fara',bg:'#3A1E42'}
];
var S={serv:'',forma:'migdala',lung:'mediu',cul:5,fin:'lucios',decor:'fara',iv:''};

/* ================= TEXTOS ================= */
var T={ro:{
  'title.acasa':'Salon Butterfly · Manichiură în Moara de Foc, Iași','title.servicii':'Servicii · Salon Butterfly, manichiură Iași','title.creeaza':'Creează-ți unghiile · Salon Butterfly','title.salonul':'Salonul · Salon Butterfly, Șos. Moara de Foc 33','title.idei':'Idei de unghii · Salon Butterfly','title.vizita':'Vizită și program · Salon Butterfly, Iași',
  'banda':'ustensile de unică folosință|mediu sterilizat|oameni prietenoși|Șos. Moara de Foc 33|luni – vineri, 09:30–20:00|4,9 pe Google',
  'a.burger2':'Închide meniul','nr':'Nr.',
  'cul.nud':'Nud piersică','cul.pudra':'Roz pudră','cul.bombon':'Roz bombon','cul.coral':'Coral','cul.rosu':'Roșu clasic','cul.cireasa':'Cireașă','cul.bordo':'Bordo','cul.pruna':'Prună','cul.lila':'Lila','cul.lavanda':'Lavandă','cul.morpho':'Albastru morpho','cul.bleu':'Bleu','cul.salvie':'Verde salvie','cul.smarald':'Smarald','cul.negru':'Negru','cul.laptos':'Alb lăptos','cul.auriu':'Auriu',
  'sv.semi':'Semipermanentă','sv.gel':'Gel','sv.intretinere':'Întreținere','sv.clasica':'Manichiură clasică','sv.pedichiura':'Pedichiură','sv.nailart':'Nail art','sv.nustiu':'Nu știu încă',
  'sv.semi.p':'Culoare care ține și strălucește, pe unghia ta naturală.','sv.gel.p':'Pentru unghii mai rezistente sau mai lungi decât ale tale.','sv.intretinere.p':'Completare și reîmprospătare, când crește unghia.','sv.clasica.p':'Cuticule, pilire, formă — și o culoare, dacă vrei.','sv.pedichiura.p':'Picioare îngrijite, iarna ca și vara.','sv.nailart.p':'French, ombré, sclipici, linii fine — sau ce ai tu în minte.',
  'pret':'Preț și durată',
  'fo.oval':'Oval','fo.migdala':'Migdală','fo.patrat':'Pătrat','fo.balerina':'Balerină','fo.stiletto':'Stiletto',
  'fo.oval.p':'Rotunjită, discretă. Merge la orice lungime.','fo.migdala.p':'Subțiată spre vârf, alungește degetele.','fo.patrat.p':'Vârf drept, colțuri ușor rotunjite. Rezistentă.','fo.balerina.p':'Ca un pantof de balet: subțiată, cu vârful tăiat drept.','fo.stiletto.p':'Ascuțită, dramatică. Cere unghii lungi.',
  'lu.scurt':'Scurtă','lu.mediu':'Medie','lu.lung':'Lungă','lu.m.scurt':'lungime scurtă','lu.m.mediu':'lungime medie','lu.m.lung':'lungime mare',
  'fi.lucios':'Lucios','fi.mat':'Mat','fi.cromat':'Cromat','fi.cateye':'Cat-eye',
  'de.fara':'Fără','de.french':'French','de.ombre':'Ombré','de.sclipici':'Sclipici','de.accent':'Unghie accent','de.fluturas':'Fluturaș','de.linii':'Linii aurii',
  'de.m.accent':'unghie accent cu sclipici auriu','de.m.fluturas':'un fluturaș pe inelar',
  'iv.dim':'Dimineața','iv.pranz':'La prânz','iv.dupa':'După-amiaza','iv.m.dim':'dimineața (09:30–12:00)','iv.m.pranz':'la prânz (12:00–15:00)','iv.m.dupa':'după-amiaza (15:00–20:00)',
  'id.1':'Cireașă clasică','id.2':'French pe migdală','id.3':'Lila cu fluturaș','id.4':'Negru mat, linii aurii','id.5':'Ombré roz','id.6':'Morpho cromat','id.7':'Nud cu unghie accent','id.8':'Bordo cat-eye','id.incearca':'Încearcă în atelier',
  'f.adr':'Șoseaua Moara de Foc 33, 707410 Iași','f.tel':'Programări: 0748 578 709, telefon sau WhatsApp','f.ore':'Luni – vineri, 09:30–20:00; sâmbătă și duminică închis','f.nota':'4,9 pe Google, din 24 de recenzii','f.echipa':'Echipa și anii de experiență:','f.card':'Plata cu cardul:','f.fb':'Pagina de Facebook:',
  'acum.da':'Deschis acum · până la 20:00','acum.nu.azi':'Închis acum · deschidem azi la 09:30','acum.nu.maine':'Închis acum · deschidem mâine la 09:30','acum.nu.luni':'Închis acum · deschidem luni la 09:30',
  'm.salut':'Bună! Aș vrea o programare la Salon Butterfly.','m.serv':'Serviciu','m.forma':'Formă','m.cul':'Culoare','m.fin':'Finisaj','m.decor':'Decor','m.cand':'Când','m.oricand':'cât mai curând','m.final':'Mulțumesc!',
  'm.gen':'Bună! Aș vrea o programare la Salon Butterfly.','m.idee':'Bună! Am o idee pentru unghii, vă trimit o poză:','loc':'ro-RO','et.sep':' · '
},
en:{
  'title.acasa':'Salon Butterfly · Nail salon in Moara de Foc, Iași','title.servicii':'Services · Salon Butterfly, nails in Iași','title.creeaza':'Design your nails · Salon Butterfly','title.salonul':'The salon · Salon Butterfly, Șos. Moara de Foc 33','title.idei':'Nail ideas · Salon Butterfly','title.vizita':'Visit & hours · Salon Butterfly, Iași',
  'banda':'single-use tools|sterilised workspace|friendly people|Șos. Moara de Foc 33|Monday – Friday, 09:30–20:00|4.9 on Google',
  'a.burger2':'Close menu','nr':'No.',
  'cul.nud':'Peach nude','cul.pudra':'Powder pink','cul.bombon':'Candy pink','cul.coral':'Coral','cul.rosu':'Classic red','cul.cireasa':'Cherry','cul.bordo':'Burgundy','cul.pruna':'Plum','cul.lila':'Lilac','cul.lavanda':'Lavender','cul.morpho':'Morpho blue','cul.bleu':'Sky blue','cul.salvie':'Sage','cul.smarald':'Emerald','cul.negru':'Black','cul.laptos':'Milky white','cul.auriu':'Gold',
  'sv.semi':'Gel polish','sv.gel':'Gel nails','sv.intretinere':'Infill','sv.clasica':'Classic manicure','sv.pedichiura':'Pedicure','sv.nailart':'Nail art','sv.nustiu':'Not sure yet',
  'sv.semi.p':'Colour that lasts and shines, on your natural nail.','sv.gel.p':'For nails that are stronger or longer than your own.','sv.intretinere.p':'Infill and refresh as the nail grows out.','sv.clasica.p':'Cuticles, filing, shape — and a colour if you like.','sv.pedichiura.p':'Well-kept feet, winter and summer.','sv.nailart.p':'French, ombré, glitter, fine lines — or whatever you have in mind.',
  'pret':'Price & duration',
  'fo.oval':'Oval','fo.migdala':'Almond','fo.patrat':'Square','fo.balerina':'Ballerina','fo.stiletto':'Stiletto',
  'fo.oval.p':'Rounded and understated. Works at any length.','fo.migdala.p':'Tapered towards the tip; makes fingers look longer.','fo.patrat.p':'Straight tip, softened corners. Sturdy.','fo.balerina.p':'Like a ballet shoe: tapered, with a flat tip.','fo.stiletto.p':'Pointed and dramatic. Needs long nails.',
  'lu.scurt':'Short','lu.mediu':'Medium','lu.lung':'Long','lu.m.scurt':'short length','lu.m.mediu':'medium length','lu.m.lung':'long length',
  'fi.lucios':'Glossy','fi.mat':'Matte','fi.cromat':'Chrome','fi.cateye':'Cat-eye',
  'de.fara':'None','de.french':'French','de.ombre':'Ombré','de.sclipici':'Glitter','de.accent':'Accent nail','de.fluturas':'Little butterfly','de.linii':'Gold lines',
  'de.m.accent':'accent nail with gold glitter','de.m.fluturas':'a little butterfly on the ring finger',
  'iv.dim':'Morning','iv.pranz':'Midday','iv.dupa':'Afternoon','iv.m.dim':'morning (09:30–12:00)','iv.m.pranz':'midday (12:00–15:00)','iv.m.dupa':'afternoon (15:00–20:00)',
  'id.1':'Classic cherry','id.2':'Almond French','id.3':'Lilac with a butterfly','id.4':'Matte black, gold lines','id.5':'Pink ombré','id.6':'Morpho chrome','id.7':'Nude with an accent nail','id.8':'Burgundy cat-eye','id.incearca':'Try it in the studio',
  'f.adr':'Șoseaua Moara de Foc 33, 707410 Iași','f.tel':'Bookings: 0748 578 709, phone or WhatsApp','f.ore':'Monday – Friday, 09:30–20:00; closed Saturday and Sunday','f.nota':'4.9 on Google, from 24 reviews','f.echipa':'The team and years of experience:','f.card':'Card payment:','f.fb':'Facebook page:',
  'acum.da':'Open now · until 20:00','acum.nu.azi':'Closed now · we open today at 09:30','acum.nu.maine':'Closed now · we open tomorrow at 09:30','acum.nu.luni':'Closed now · we open Monday at 09:30',
  'm.salut':'Hi! I would like to book an appointment at Salon Butterfly.','m.serv':'Service','m.forma':'Shape','m.cul':'Colour','m.fin':'Finish','m.decor':'Decoration','m.cand':'When','m.oricand':'as soon as possible','m.final':'Thank you!',
  'm.gen':'Hi! I would like to book an appointment at Salon Butterfly.','m.idee':'Hi! I have a nail idea, here is a photo:','loc':'en-GB','et.sep':' · ',
  'sari':'Skip to content','prez':'<b>PACHECO STUDIOS PRESENTATION</b> · demo website for Salon Butterfly','marca.sub':'nails · Iași',
  'nav.acasa':'Home','nav.servicii':'Services','nav.creeaza':'Design','nav.salonul':'The salon','nav.idei':'Ideas','nav.vizita':'Visit','nav.prog':'Book now',
  'a.marca':'Salon Butterfly — home','a.nav':'Main menu','a.limba':'Language','a.burger':'Open menu','a.culori':'Colours','a.mana':'Preview on a hand',
  'h.ochi':'Nail salon · Moara de Foc, Iași','h.sr':' — nail salon in Iași','h.motto':'Pick the colour. <em>We\'ll give it wings.</em>','h.fl':'A butterfly whose wings are made of polished nails','h.alege':'Tap a bottle','h.nota':'on Google · 24 reviews','cta.creeaza':'Design your nails','conf':'to be confirmed',
  'cu.ochi':'What clients notice','cu.t':'Clean, <em>above all</em>.','cu.sub':'The reviews keep coming back to the same thing: a clean salon, with single-use tools and a sterilised workspace. And people you enjoy spending an hour with.',
  'cu1.t':'Single-use','cu1.p':'The tools are single-use — yours, and only yours.','cu2.t':'Sterilised workspace','cu2.p':'A sterilised, clean workspace, from the table to the tools.','cu3.t':'Friendly people','cu3.p':'Quality work and a relaxed atmosphere while the polish dries.',
  'no.ochi':'On Google','no.t':'24 reviews. 22 of them five stars.','no.5':'5 stars','no.4':'4 stars','no.3':'1–3 stars',
  'at.ochi':'Your studio','at.t':'Design your nails <em>before you come</em>.','at1.b':'The shape','at1.p':'Oval, almond, square, ballerina or stiletto — plus the length.','at2.b':'Colour and finish','at2.p':'From the palette: glossy, matte, chrome or cat-eye.','at3.b':'The decoration','at3.p':'French, ombré, glitter, gold lines — or a little butterfly.','at.sub':'Your design arrives ready-written on WhatsApp; the salon replies with the time and price.',
  'un.ochi':'Where and when','un.t':'Șoseaua Moara de Foc <em>33</em>.','un.ore1':'Monday – Friday: 09:30–20:00','un.ore2':'Saturday and Sunday: closed','un.btn':'Map and hours',
  'alt.salon':'Salon Butterfly','alt.interior':'Inside Salon Butterfly',
  'id.ochi':'Already have an idea?','id.t':'Send us <em>your inspiration photo</em>.','id.sub':'A Pinterest screenshot, an Instagram photo, a friend\'s nails. Send it on WhatsApp and we\'ll talk it through.','id.btn':'Send the photo on WhatsApp','id.btn2':'See ideas',
  's.ochi':'Services','s.t':'What you <em>can ask for</em>.','s.sub':'You get the price and duration on WhatsApp, depending on what you choose. Full list of services:',
  'fo.ochi':'A small glossary','fo.t':'Five nail shapes.','fo.sub':'So you know what to ask for. The right shape depends on your natural nail length and how much you use your hands.',
  'ig.ochi':'At every appointment','ig.t':'Hygiene isn\'t optional.','ig.1':'single-use tools','ig.2':'sterilised workspace','ig.3':'a clean space',
  'cr.ochi':'Your studio','cr.t':'Design <em>your nails</em>.','cr.sub':'Pick the shape, colour and decoration, see it on a hand, and the booking message writes itself.',
  'c.serv':'What would you like?','c.er':'Choose what you\'d like — or "Not sure yet".','c.forma':'Shape','c.lung':'Length','c.cul':'Colour','c.cul.conf':'shades are a guide — to be confirmed in the salon','c.fin':'Finish','c.decor':'Decoration','c.cand':'When?','c.zi':'Preferred day','c.weekend':'The salon is closed on Saturday and Sunday — pick a day from Monday to Friday.','c.iv':'Time of day','c.nume':'Your name','c.nume.ph':'Ana',
  'fi.t':'Your message','fi.btn':'Send on WhatsApp','fi.mic':'WhatsApp opens with the message ready. Nothing is sent until you tap "Send".',
  'sa.ochi':'The salon','sa.t':'A small salon, <em>very clean</em>.','sa.sub':'At Șoseaua Moara de Foc 33, near Strada Păcurari. Manicures Monday to Friday, by appointment.','sa2.ochi':'In short','sa2.t':'Good to know.',
  're.ochi':'From the reviews, in short','re.t':'What clients say.','re.1':'one of the cleanest salons','re.2':'single-use tools','re.3':'sterilised workspace','re.4':'quality work','re.5':'friendly people','re.6':'a pleasant atmosphere','re.n':'4.9 out of 5 · 24 reviews on Google',
  'i.ochi':'Ideas','i.t':'Eight ideas <em>to start from</em>.','i.sub':'Pick one and we\'ll open it in the studio, where you can change anything: shape, colour, decoration.','lu.ochi':'From the salon','lu.t':'Recent work.',
  'v.ochi':'Visit','v.t':'Șos. Moara de Foc 33, <em>Iași</em>.','v.sub':'We work by appointment. Message us on WhatsApp or call — we\'ll tell you straight away which times are free.','v.adr':'Address','v.dir':'Open in Google Maps →','v.prog':'Bookings','v.prog.s':'Phone or WhatsApp.','v.ore':'Opening hours','v.fb':'The salon\'s page — link','v.parcare':'Parking','inchis':'closed',
  'zi.1':'Monday','zi.2':'Tuesday','zi.3':'Wednesday','zi.4':'Thursday','zi.5':'Friday','zi.6':'Saturday','zi.0':'Sunday',
  'ft.desc':'Nail salon in Iași. Monday–Friday, 09:30–20:00.','ft.contact':'Contact','ft.pag':'Pages','ft.sal':'ANPC · Alternative dispute resolution (ADR)','ft.odr':'Online dispute resolution (ODR)','ft.firma':'Company name and tax ID:','ft.credit':'Website by Pacheco Studios','fix.suna':'Call'
},
pt:{
  'title.acasa':'Salon Butterfly · Manicure em Moara de Foc, Iași','title.servicii':'Serviços · Salon Butterfly, unhas em Iași','title.creeaza':'Crie as suas unhas · Salon Butterfly','title.salonul':'O salão · Salon Butterfly, Șos. Moara de Foc 33','title.idei':'Ideias de unhas · Salon Butterfly','title.vizita':'Visitar e horário · Salon Butterfly, Iași',
  'banda':'utensílios descartáveis|ambiente esterilizado|gente simpática|Șos. Moara de Foc 33|segunda a sexta, 09:30–20:00|4,9 no Google',
  'a.burger2':'Fechar o menu','nr':'N.º',
  'cul.nud':'Nude pêssego','cul.pudra':'Rosa empoado','cul.bombon':'Rosa chiclete','cul.coral':'Coral','cul.rosu':'Vermelho clássico','cul.cireasa':'Cereja','cul.bordo':'Bordeaux','cul.pruna':'Ameixa','cul.lila':'Lilás','cul.lavanda':'Lavanda','cul.morpho':'Azul morpho','cul.bleu':'Azul-céu','cul.salvie':'Verde-sálvia','cul.smarald':'Esmeralda','cul.negru':'Preto','cul.laptos':'Branco leitoso','cul.auriu':'Dourado',
  'sv.semi':'Verniz gel (semipermanente)','sv.gel':'Unhas de gel','sv.intretinere':'Manutenção','sv.clasica':'Manicure clássica','sv.pedichiura':'Pedicure','sv.nailart':'Nail art','sv.nustiu':'Ainda não sei',
  'sv.semi.p':'Cor que dura e brilha, na sua unha natural.','sv.gel.p':'Para unhas mais resistentes ou mais compridas do que as suas.','sv.intretinere.p':'Preenchimento e retoque, quando a unha cresce.','sv.clasica.p':'Cutículas, limar, forma — e uma cor, se quiser.','sv.pedichiura.p':'Pés cuidados, no inverno como no verão.','sv.nailart.p':'Francesa, ombré, brilhantes, linhas finas — ou o que tiver em mente.',
  'pret':'Preço e duração',
  'fo.oval':'Oval','fo.migdala':'Amêndoa','fo.patrat':'Quadrada','fo.balerina':'Bailarina','fo.stiletto':'Stiletto',
  'fo.oval.p':'Arredondada, discreta. Fica bem em qualquer comprimento.','fo.migdala.p':'Afina para a ponta, alonga os dedos.','fo.patrat.p':'Ponta reta, cantos ligeiramente arredondados. Resistente.','fo.balerina.p':'Como uma sapatilha de ballet: afinada, com a ponta cortada a direito.','fo.stiletto.p':'Pontiaguda, dramática. Pede unhas compridas.',
  'lu.scurt':'Curta','lu.mediu':'Média','lu.lung':'Comprida','lu.m.scurt':'comprimento curto','lu.m.mediu':'comprimento médio','lu.m.lung':'comprimento longo',
  'fi.lucios':'Brilhante','fi.mat':'Mate','fi.cromat':'Cromado','fi.cateye':'Olho de gato',
  'de.fara':'Nenhuma','de.french':'Francesa','de.ombre':'Ombré','de.sclipici':'Brilhantes','de.accent':'Unha de destaque','de.fluturas':'Borboletinha','de.linii':'Linhas douradas',
  'de.m.accent':'unha de destaque com brilhantes dourados','de.m.fluturas':'uma borboletinha no anelar',
  'iv.dim':'Manhã','iv.pranz':'Hora de almoço','iv.dupa':'Tarde','iv.m.dim':'de manhã (09:30–12:00)','iv.m.pranz':'à hora de almoço (12:00–15:00)','iv.m.dupa':'à tarde (15:00–20:00)',
  'id.1':'Cereja clássica','id.2':'Francesa em amêndoa','id.3':'Lilás com borboleta','id.4':'Preto mate, linhas douradas','id.5':'Ombré rosa','id.6':'Morpho cromado','id.7':'Nude com unha de destaque','id.8':'Bordeaux olho de gato','id.incearca':'Experimentar no atelier',
  'f.adr':'Șoseaua Moara de Foc 33, 707410 Iași','f.tel':'Marcações: 0748 578 709, telefone ou WhatsApp','f.ore':'Segunda a sexta, 09:30–20:00; sábado e domingo fechado','f.nota':'4,9 no Google, em 24 avaliações','f.echipa':'A equipa e os anos de experiência:','f.card':'Pagamento com cartão:','f.fb':'Página de Facebook:',
  'acum.da':'Aberto agora · até às 20:00','acum.nu.azi':'Fechado agora · abrimos hoje às 09:30','acum.nu.maine':'Fechado agora · abrimos amanhã às 09:30','acum.nu.luni':'Fechado agora · abrimos segunda às 09:30',
  'm.salut':'Olá! Gostava de marcar no Salon Butterfly.','m.serv':'Serviço','m.forma':'Forma','m.cul':'Cor','m.fin':'Acabamento','m.decor':'Decoração','m.cand':'Quando','m.oricand':'o mais cedo possível','m.final':'Obrigada!',
  'm.gen':'Olá! Gostava de marcar no Salon Butterfly.','m.idee':'Olá! Tenho uma ideia para as unhas, envio uma foto:','loc':'pt-PT','et.sep':' · ',
  'sari':'Saltar para o conteúdo','prez':'<b>APRESENTAÇÃO PACHECO STUDIOS</b> · site de demonstração para o Salon Butterfly','marca.sub':'manicure · Iași',
  'nav.acasa':'Início','nav.servicii':'Serviços','nav.creeaza':'Criar','nav.salonul':'O salão','nav.idei':'Ideias','nav.vizita':'Visitar','nav.prog':'Marcar',
  'a.marca':'Salon Butterfly — início','a.nav':'Menu principal','a.limba':'Língua','a.burger':'Abrir o menu','a.culori':'Cores','a.mana':'Pré-visualização numa mão',
  'h.ochi':'Salão de manicure · Moara de Foc, Iași','h.sr':' — manicure em Iași','h.motto':'Escolha a cor. <em>Nós damos-lhe asas.</em>','h.fl':'Uma borboleta com as asas feitas de unhas pintadas','h.alege':'Toque num frasco','h.nota':'no Google · 24 avaliações','cta.creeaza':'Crie as suas unhas','conf':'a confirmar',
  'cu.ochi':'O que as clientes notam','cu.t':'A limpeza, <em>antes de tudo</em>.','cu.sub':'Nas avaliações repete-se o mesmo: um salão limpo, com utensílios descartáveis e ambiente esterilizado. E pessoas com quem se está bem.',
  'cu1.t':'Descartáveis','cu1.p':'Os utensílios são de uso único — seus, só para si.','cu2.t':'Ambiente esterilizado','cu2.p':'Um espaço de trabalho esterilizado e limpo, da mesa aos instrumentos.','cu3.t':'Gente simpática','cu3.p':'Serviço de qualidade e um ambiente onde se está bem enquanto o verniz seca.',
  'no.ochi':'No Google','no.t':'24 avaliações. 22 de cinco estrelas.','no.5':'5 estrelas','no.4':'4 estrelas','no.3':'1–3 estrelas',
  'at.ochi':'O seu atelier','at.t':'Crie as suas unhas <em>antes de vir</em>.','at1.b':'A forma','at1.p':'Oval, amêndoa, quadrada, bailarina ou stiletto — e o comprimento.','at2.b':'Cor e acabamento','at2.p':'Da paleta: brilhante, mate, cromado ou olho de gato.','at3.b':'A decoração','at3.p':'Francesa, ombré, brilhantes, linhas douradas — ou uma borboletinha.','at.sub':'Recebe o design já escrito no WhatsApp; o salão responde com a hora e o preço.',
  'un.ochi':'Onde e quando','un.t':'Șoseaua Moara de Foc <em>33</em>.','un.ore1':'Segunda a sexta: 09:30–20:00','un.ore2':'Sábado e domingo: fechado','un.btn':'Mapa e horário',
  'alt.salon':'Salon Butterfly','alt.interior':'Interior do Salon Butterfly',
  'id.ochi':'Já tem uma ideia?','id.t':'Mande-nos <em>a foto de inspiração</em>.','id.sub':'Uma captura do Pinterest, uma foto do Instagram, as unhas de uma amiga. Envie por WhatsApp e falamos sobre ela.','id.btn':'Enviar a foto por WhatsApp','id.btn2':'Ver ideias',
  's.ochi':'Serviços','s.t':'O que <em>pode pedir</em>.','s.sub':'O preço e a duração ficam a saber-se por WhatsApp, conforme o que escolher. Lista completa de serviços:',
  'fo.ochi':'Pequeno dicionário','fo.t':'Cinco formas de unha.','fo.sub':'Para saber o que pedir. A forma certa depende do comprimento da sua unha e de quanto trabalha com as mãos.',
  'ig.ochi':'Em cada marcação','ig.t':'A higiene não é opcional.','ig.1':'utensílios descartáveis','ig.2':'ambiente esterilizado','ig.3':'espaço limpo',
  'cr.ochi':'O seu atelier','cr.t':'Crie as suas <em>unhas</em>.','cr.sub':'Escolhe a forma, a cor e a decoração, vê o resultado numa mão, e a mensagem de marcação escreve-se sozinha.',
  'c.serv':'O que deseja?','c.er':'Escolha o que deseja — ou «Ainda não sei».','c.forma':'Forma','c.lung':'Comprimento','c.cul':'Cor','c.cul.conf':'tons indicativos — a confirmar no salão','c.fin':'Acabamento','c.decor':'Decoração','c.cand':'Quando?','c.zi':'Dia preferido','c.weekend':'Ao sábado e ao domingo o salão está fechado — escolha um dia de segunda a sexta.','c.iv':'Período','c.nume':'O seu nome','c.nume.ph':'Ana',
  'fi.t':'A sua mensagem','fi.btn':'Enviar por WhatsApp','fi.mic':'O WhatsApp abre com a mensagem pronta. Nada é enviado até carregar em «Enviar».',
  'sa.ochi':'O salão','sa.t':'Um salão pequeno, <em>muito limpo</em>.','sa.sub':'Na Șoseaua Moara de Foc 33, perto da Strada Păcurari. Manicure de segunda a sexta, por marcação.','sa2.ochi':'Em resumo','sa2.t':'O que precisa de saber.',
  're.ochi':'Das avaliações, em resumo','re.t':'O que dizem as clientes.','re.1':'um dos salões mais limpos','re.2':'utensílios descartáveis','re.3':'ambiente esterilizado','re.4':'serviço de qualidade','re.5':'gente simpática','re.6':'ambiente agradável','re.n':'4,9 em 5 · 24 avaliações no Google',
  'i.ochi':'Ideias','i.t':'Oito ideias <em>para começar</em>.','i.sub':'Escolha uma e abrimo-la no atelier, onde pode mudar tudo: outra forma, outra cor, outra decoração.','lu.ochi':'Do salão','lu.t':'Trabalhos recentes.',
  'v.ochi':'Visitar','v.t':'Șos. Moara de Foc 33, <em>Iași</em>.','v.sub':'Trabalhamos por marcação. Escreva-nos por WhatsApp ou ligue — dizemos logo que horas estão livres.','v.adr':'Morada','v.dir':'Abrir no Google Maps →','v.prog':'Marcações','v.prog.s':'Telefone ou WhatsApp.','v.ore':'Horário','v.fb':'Página do salão — link','v.parcare':'Estacionamento','inchis':'fechado',
  'zi.1':'Segunda','zi.2':'Terça','zi.3':'Quarta','zi.4':'Quinta','zi.5':'Sexta','zi.6':'Sábado','zi.0':'Domingo',
  'ft.desc':'Salão de manicure em Iași. Segunda a sexta, 09:30–20:00.','ft.contact':'Contacto','ft.pag':'Páginas','ft.sal':'ANPC · Resolução alternativa de litígios (RAL)','ft.odr':'Resolução de litígios em linha (RLL / ODR)','ft.firma':'Denominação e NIF da empresa:','ft.credit':'Site feito pela Pacheco Studios','fix.suna':'Ligar'
}};
var lang=H.dataset.lang||'ro';
function t(k){return (T[lang]&&T[lang][k]!=null)?T[lang][k]:(T.ro[k]!=null?T.ro[k]:k)}
function capture(){
  $$('[data-t]').forEach(function(e){var k=e.getAttribute('data-t');if(T.ro[k]==null)T.ro[k]=e.innerHTML.trim()});
  $$('[data-ta]').forEach(function(e){e.getAttribute('data-ta').split(';').forEach(function(p){var a=p.split(':');if(T.ro[a[1]]==null)T.ro[a[1]]=e.getAttribute(a[0])||''})});
}

/* ================= SVG: UNHAS ================= */
var NS='http://www.w3.org/2000/svg',UID=0;
function el(tg,a,p){var e=D.createElementNS(NS,tg);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
function f1(n){return Math.round(n*10)/10}
function mix(hex,to,a){var c=[1,3,5].map(function(i){return parseInt(hex.substr(i,2),16)}),d=[1,3,5].map(function(i){return parseInt(to.substr(i,2),16)});return '#'+c.map(function(v,i){var r=Math.round(v+(d[i]-v)*a);return ('0'+r.toString(16)).slice(-2)}).join('')}
function lum(hex){var c=[1,3,5].map(function(i){return parseInt(hex.substr(i,2),16)/255});return .2126*c[0]+.7152*c[1]+.0722*c[2]}
function nailD(f,w,L){
  var h=w/2,cu=w*.3,e=' L'+f1(h)+' 0 Q0 '+f1(cu)+' '+f1(-h)+' 0Z',b='M'+f1(-h)+' 0',P=function(x,y){return f1(x)+' '+f1(y)};
  if(f==='patrat'){var r=w*.16;return b+' L'+P(-h,-L+r)+' Q'+P(-h,-L)+' '+P(-h+r,-L)+' L'+P(h-r,-L)+' Q'+P(h,-L)+' '+P(h,-L+r)+e}
  if(f==='oval')return b+' L'+P(-h,-L*.58)+' C'+P(-h,-L*1.07)+' '+P(h,-L*1.07)+' '+P(h,-L*.58)+e;
  if(f==='balerina')return b+' L'+P(-h,-L*.55)+' L'+P(-w*.25,-L)+' Q'+P(0,-L*1.01)+' '+P(w*.25,-L)+' L'+P(h,-L*.55)+e;
  if(f==='stiletto')return b+' L'+P(-h,-L*.42)+' C'+P(-h,-L*.72)+' '+P(-w*.05,-L*.9)+' '+P(0,-L)+' C'+P(w*.05,-L*.9)+' '+P(h,-L*.72)+' '+P(h,-L*.42)+e;
  return b+' L'+P(-h,-L*.5)+' C'+P(-h,-L*.84)+' '+P(-w*.15,-L)+' '+P(0,-L)+' C'+P(w*.15,-L)+' '+P(h,-L*.84)+' '+P(h,-L*.5)+e;
}
function defsOf(svg){return svg.querySelector('defs')||el('defs',{},svg)}
function miniFluture(p,x,y,s){var g=el('g',{transform:'translate('+f1(x)+' '+f1(y)+') scale('+s+')'},p);el('path',{d:'M-1 0C-6-14-17-16-18-10s6 11 17 10zM1 0c5-14 16-16 17-10S12 1 1 0z',fill:'#FFF6EA'},g);el('path',{d:'M-1 1c-9 1-13 9-10 11s8-2 10-11zM1 1c9 1 13 9 10 11S3 10 1 1z',fill:'#E3C98A'},g);el('rect',{x:-1,y:-8,width:2,height:18,rx:1,fill:'#2A1430'},g)}
/* uma unha completa: base, decoração, acabamento */
function drawNail(svg,parent,x,y,rot,w,L,ext,st,o){
  o=o||{};var defs=defsOf(svg),id='u'+(UID++),d=nailD(st.forma,w,L);
  var col=CUL[st.cul][1],g=el('g',{transform:'translate('+f1(x)+' '+f1(y)+') rotate('+f1(rot)+')'},parent);
  var cp=el('clipPath',{id:id},defs);el('path',{d:d},cp);
  var accent=st.decor==='accent'&&o.accent;
  var baseCol=accent?'#C9A75A':(st.fin==='cateye'?mix(col,'#000000',.45):col);
  var base=el('path',{d:d,'class':'unghie-baza',stroke:'rgba(23,10,27,.25)','stroke-width':.8},g);base.style.fill=baseCol;
  var c=el('g',{'clip-path':'url(#'+id+')'},g);
  var tipY=-L,free=-L+ext;
  if(st.fin==='cateye'){var gid=id+'c',gr=el('linearGradient',{id:gid,x1:0,y1:1,x2:1,y2:0},defs);el('stop',{offset:.3,'stop-color':mix(col,'#FFFFFF',.55),'stop-opacity':0},gr);el('stop',{offset:.5,'stop-color':mix(col,'#FFFFFF',.55),'stop-opacity':.95},gr);el('stop',{offset:.7,'stop-color':mix(col,'#FFFFFF',.55),'stop-opacity':0},gr);el('rect',{x:-w,y:-L-4,width:w*2,height:L+8,fill:'url(#'+gid+')'},c)}
  if(st.fin==='cromat'){var gid2=id+'k',g2=el('linearGradient',{id:gid2,x1:0,y1:0,x2:1,y2:0},defs);[[0,.65],[.3,0],[.55,.45],[.8,0],[1,.5]].forEach(function(s){el('stop',{offset:s[0],'stop-color':'#FFFFFF','stop-opacity':s[1]},g2)});el('rect',{x:-w/2,y:-L-4,width:w,height:L+8,fill:'url(#'+gid2+')'},c)}
  if(st.decor==='ombre'&&!accent){var gid3=id+'o',g3=el('linearGradient',{id:gid3,x1:0,y1:1,x2:0,y2:0},defs);el('stop',{offset:0,'stop-color':'#F3DCD3','stop-opacity':1},g3);el('stop',{offset:.8,'stop-color':'#F3DCD3','stop-opacity':0},g3);el('rect',{x:-w,y:-L-4,width:w*2,height:L+12,fill:'url(#'+gid3+')'},c)}
  if(st.decor==='french'&&!accent){var sy=free+Math.max(ext*.15,w*.12),dd=Math.max(ext*.45,w*.25);el('path',{d:'M'+f1(-w)+' '+f1(-L-6)+' H'+f1(w)+' V'+f1(sy+dd*.4)+' Q0 '+f1(sy-dd)+' '+f1(-w)+' '+f1(sy+dd*.4)+'Z',fill:'#FBF6F0'},c)}
  var glitter=st.decor==='sclipici'||accent;
  if(glitter){var n=accent?46:16;for(var i=0;i<n;i++){var gx=(Math.sin(i*12.9898+UID)*43758.5453)%1,gy=(Math.sin(i*78.233+UID)*12345.678)%1;gx=Math.abs(gx);gy=Math.abs(gy);el('circle',{cx:f1((gx-.5)*w),cy:f1(-gy*L),r:f1(w*(.025+((i*7)%5)*.012)),fill:i%3?'#F2DC9C':'#FFFFFF',opacity:.95},c)}}
  if(st.decor==='linii'&&!accent){el('path',{d:'M'+f1(-w*.45)+' '+f1(-L*.12)+' C'+f1(w*.55)+' '+f1(-L*.32)+' '+f1(-w*.55)+' '+f1(-L*.6)+' '+f1(w*.3)+' '+f1(-L*.9),fill:'none',stroke:'#E3C98A','stroke-width':f1(Math.max(1,w*.06)),'stroke-linecap':'round'},c);el('circle',{cx:f1(w*.3),cy:f1(-L*.9),r:f1(w*.07),fill:'#E3C98A'},c)}
  if(st.decor==='fluturas'&&o.accent)miniFluture(c,0,-L*.5,w/44);
  if(st.fin==='mat'){el('rect',{x:-w,y:-L-4,width:w*2,height:L+8,fill:'#FFFFFF',opacity:.06},c)}
  else{el('path',{d:'M'+f1(-w*.22)+' '+f1(-L*.12)+' Q'+f1(-w*.3)+' '+f1(-L*.5)+' '+f1(-w*.1)+' '+f1(-L*.8),fill:'none',stroke:'#FFFFFF','stroke-opacity':lum(baseCol)>.7?.75:.45,'stroke-width':f1(w*.11),'stroke-linecap':'round'},c)}
  return {g:g,base:base};
}

/* ================= A MÃO ================= */
var DEG=[{x:94,top:152,w:40,r:-9},{x:142,top:98,w:46,r:-3},{x:194,top:80,w:48,r:1},{x:246,top:104,w:46,r:6},{x:300,top:206,w:48,r:40}];
function drawHand(svg,st){
  while(svg.firstChild)svg.removeChild(svg.firstChild);
  var g=el('g',{},svg),skin='#E9C3A9',sh='#D8A98C';
  el('path',{d:'M58 380C60 300 70 270 96 250H286C306 262 318 300 316 380Z',fill:skin},g);
  DEG.forEach(function(f,i){
    var bx=f.x,by=i===4?330:300,fg=el('g',{transform:'rotate('+f.r+' '+bx+' '+by+')'},g);
    var x=bx-f.w/2,h=(i===4?352:390)-f.top;
    el('rect',{x:x,y:f.top,width:f.w,height:h,rx:f.w/2,fill:skin},fg);
    el('path',{d:'M'+(x+8)+' '+(f.top+f.w*2)+' q'+(f.w/2-8)+' 5 '+(f.w-16)+' 0',fill:'none',stroke:sh,'stroke-width':2,'stroke-linecap':'round',opacity:.7},fg);
    var nw=f.w*.74,ext=nw*({scurt:.1,mediu:.55,lung:1.05}[st.lung]||.55),L=nw*1.02+ext;
    drawNail(svg,fg,bx,f.top+nw*1.02+3,0,nw,L,ext,st,{accent:i===1});
  });
  el('path',{d:'M250 300c16 10 30 10 44 2',fill:'none',stroke:sh,'stroke-width':2,'stroke-linecap':'round',opacity:.6},g);
}

/* ================= A BORBOLETA ================= */
var flNails=[];
function drawFluture(svg,st){
  while(svg.firstChild)svg.removeChild(svg.firstChild);flNails=[];
  var defs=defsOf(svg),gl=el('radialGradient',{id:'flg',cx:'50%',cy:'50%',r:'50%'},defs);el('stop',{offset:0,'stop-color':'#E3C98A','stop-opacity':.22},gl);el('stop',{offset:1,'stop-color':'#E3C98A','stop-opacity':0},gl);
  el('circle',{cx:200,cy:170,r:170,fill:'url(#flg)'},svg);
  var aS=el('g',{'class':'aripa aripa-s'},svg),aD=el('g',{'class':'aripa aripa-d'},svg);
  var SUS=[[36,138,27],[52,158,28],[68,140,27],[84,108,25]],JOS=[[108,96,24],[128,102,24],[148,86,22]];
  var MEM=['M208 156C226 90 262 24 304 22C346 22 364 50 358 80C352 112 346 140 322 158C290 172 240 168 208 162Z','M208 176C250 170 304 180 316 214C326 246 302 278 270 276C240 274 220 240 208 190Z'];
  var k=0;
  [[aS,-1],[aD,1]].forEach(function(A){
    var par=A[0],side=A[1],m=el('g',{transform:side<0?'translate(400 0) scale(-1 1)':''},par);
    MEM.forEach(function(d,j){var mb=el('path',{d:d,stroke:'#E3C98A','stroke-width':1.6,'class':'unghie-baza'},m);flNails.push({b:mb,mem:1,lvl:j,i:0,k:j})});
    el('circle',{cx:334,cy:58,r:9,fill:'none',stroke:'#E3C98A','stroke-width':1.4},m);el('circle',{cx:334,cy:58,r:3,fill:'#E3C98A'},m);
    function wing(set,py,dist){set.forEach(function(n,i){
      var r=n[0],rad=r*Math.PI/180,x=208+Math.sin(rad)*dist,y=py-Math.cos(rad)*dist;
      var wrap=el('g',{'class':'unghie-fl'},m);wrap.style.setProperty('--i',k);
      var u=drawNail(svg,wrap,x,y,r,n[2],n[1],n[1]*.4,{forma:st.forma,cul:st.cul,fin:'lucios',decor:'fara'});
      u.base.setAttribute('stroke','#E3C98A');u.base.setAttribute('stroke-width',1.1);
      flNails.push({b:u.base,lvl:set===JOS?1:0,i:i,k:k+2});k++;
    })}
    wing(JOS,182,8);wing(SUS,156,8);
  });
  var b=el('g',{},svg);
  el('path',{d:'M196 112c-8-26-26-36-36-28M204 112c8-26 26-36 36-28',fill:'none',stroke:'#E3C98A','stroke-width':2,'stroke-linecap':'round','class':'desen',style:'--len:60'},b);
  el('circle',{cx:160,cy:84,r:3.5,fill:'#E3C98A'},b);el('circle',{cx:240,cy:84,r:3.5,fill:'#E3C98A'},b);
  el('ellipse',{cx:200,cy:174,rx:7.5,ry:52,fill:'#170A1B',stroke:'#E3C98A','stroke-width':1.5},b);
  el('circle',{cx:200,cy:116,r:9,fill:'#170A1B',stroke:'#E3C98A','stroke-width':1.5},b);
  for(var s=0;s<5;s++)el('path',{d:'M194 '+(148+s*12)+'q6 4 12 0',fill:'none',stroke:'#E3C98A','stroke-width':1,opacity:.6},b);
  if(!RM)svg.classList.add('zboara');
  recolor(st.cul,false);
}
function nailCol(c,n){var h=CUL[c][1];if(n.mem)return mix(h,'#170A1B',n.lvl?.62:.5);return n.lvl?mix(h,'#170A1B',.18+n.i*.06):mix(h,'#FFFFFF',(n.i%2)*.12)}
function recolor(c,anim){flNails.forEach(function(n){n.b.style.transitionDelay=anim&&!RM?(n.k*45)+'ms':'0ms';n.b.style.fill=nailCol(c,n)})}

/* ================= ESTADO / UI ================= */
function colName(i){return t('nr')+' '+('0'+(i+1)).slice(-2)+' · '+t('cul.'+CUL[i][0])}
function bottle(hex){return '<svg viewBox="0 0 30 50" aria-hidden="true"><rect x="10" y="1" width="10" height="17" rx="2" fill="#170A1B" stroke="#E3C98A" stroke-width=".8"/><rect x="7" y="16" width="16" height="4" rx="1" fill="#E3C98A"/><path d="M5 22h20a3 3 0 0 1 3 3v19a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V25a3 3 0 0 1 3-3z" fill="'+hex+'" stroke="rgba(255,255,255,.35)"/><path d="M7 27v14" stroke="#fff" stroke-opacity=".45" stroke-width="2.4" stroke-linecap="round"/></svg>'}
var HERO_CUL=['nud','pudra','bombon','rosu','cireasa','bordo','lila','morpho','smarald','negru'];
function buildSticle(){
  var b=$('#sticle');b.innerHTML=HERO_CUL.map(function(id){var i=ci(id);return '<button type="button" class="sticla" data-c="'+i+'" aria-pressed="false">'+bottle(CUL[i][1])+'<span class="sr" data-cn="'+i+'"></span></button>'}).join('');
  b.addEventListener('click',function(e){var x=e.target.closest('.sticla');if(!x)return;setCul(+x.dataset.c,true)});
}
function setCul(i,anim){
  S.cul=i;recolor(i,anim);
  $$('.sticla').forEach(function(x){x.setAttribute('aria-pressed',+x.dataset.c===i?'true':'false')});
  $('#cul-nume').textContent=colName(i);
  var r=$('#c-cul input[value="'+i+'"]');if(r)r.checked=true;
  renderAll();
}
function chips(box,name,list,pref,sel,extra){
  $(box).innerHTML=list.map(function(v){return '<label class="cip"><input type="radio" name="'+name+'" value="'+v+'"'+(sel===v?' checked':'')+'><span>'+(extra?extra(v):'')+'<span data-t="'+pref+v+'">'+t(pref+v)+'</span></span></label>'}).join('');
}
function shapeIcon(f){return '<svg viewBox="0 0 18 30" aria-hidden="true"><path d="'+nailD(f,14,26).replace(/^M/,'M')+'" transform="translate(9 28)" fill="#A3123F"/></svg>'}
function buildForm(){
  chips('#c-serv','serv',SERV.concat(['nustiu']),'sv.',S.serv);
  chips('#c-forma','forma',FORME,'fo.',S.forma,shapeIcon);
  chips('#c-lung','lung',LUNG,'lu.',S.lung);
  chips('#c-fin','fin',FIN,'fi.',S.fin);
  chips('#c-decor','decor',DECOR,'de.',S.decor);
  chips('#c-iv','iv',IV,'iv.',S.iv);
  $('#c-cul').innerHTML=CUL.map(function(c,i){return '<label class="cul"><input type="radio" name="cul" value="'+i+'"'+(S.cul===i?' checked':'')+' aria-label="'+t('cul.'+c[0])+'" data-cul="'+i+'"><span><i style="background:'+c[1]+'"></i><span data-t="cul.'+c[0]+'">'+t('cul.'+c[0])+'</span></span></label>'}).join('');
}
function syncForm(){
  ['serv','forma','lung','fin','decor','iv'].forEach(function(n){$$('#cfg input[name="'+n+'"]').forEach(function(r){r.checked=r.value===S[n]})});
  $$('#cfg input[name="cul"]').forEach(function(r){r.checked=+r.value===S.cul});
}
var lastShape='';
function renderAll(){
  drawHand($('#mana'),S);
  drawHand($('#mana-teaser'),S);
  drawHand($('#mana-mini'),S);
  if(lastShape!==S.forma){lastShape=S.forma;drawFluture($('#fluture'),S)}
  etichete();
  updMsg();
}
function etichete(){var e=t('fo.'+S.forma)+' · '+t('lu.'+S.lung)+' · '+t('cul.'+CUL[S.cul][0])+' · '+t('fi.'+S.fin)+(S.decor!=='fara'?' · '+t('de.'+S.decor):'');$('#eticheta').textContent=e;$('#eticheta-mini').textContent=e}
function fmtDate(v){try{var p=v.split('-');return new Date(+p[0],+p[1]-1,+p[2]).toLocaleDateString(t('loc'),{weekday:'long',day:'numeric',month:'long'})}catch(e){return v}}
function weekend(v){if(!v)return false;var p=v.split('-'),d=new Date(+p[0],+p[1]-1,+p[2]).getDay();return d===0||d===6}
function updMsg(){
  var zi=$('#c-zi').value,nume=$('#c-nume').value.trim();
  $('#av-weekend').classList.toggle('vis',weekend(zi));
  var dec=S.decor==='accent'||S.decor==='fluturas'?t('de.m.'+S.decor):t('de.'+S.decor).toLowerCase();
  var L=[t('m.salut'),'','• '+t('m.serv')+': '+(S.serv?t('sv.'+S.serv).toLowerCase():'…'),
    '• '+t('m.forma')+': '+t('fo.'+S.forma).toLowerCase()+', '+t('lu.m.'+S.lung),
    '• '+t('m.cul')+': '+colName(S.cul),
    '• '+t('m.fin')+': '+t('fi.'+S.fin).toLowerCase(),
    '• '+t('m.decor')+': '+dec,
    '• '+t('m.cand')+': '+(zi?fmtDate(zi):t('m.oricand'))+(S.iv?', '+t('iv.m.'+S.iv):''),
    '',t('m.final')+(nume?'\n'+nume:'')];
  var m=L.join('\n');$('#mesaj').textContent=m;
  var href='https://wa.me/'+TEL+'?text='+encodeURIComponent(m);$('#trimite').href=href;
  var fx=$('.cta-fix .wa-link');if(fx&&cur==='creeaza')fx.href=href;
}
function bindForm(){
  var f=$('#cfg');
  f.addEventListener('change',function(e){
    var n=e.target.name;if(!n)return;
    if(n==='cul'){setCul(+e.target.value,true);return}
    S[n]=e.target.value;if(n==='serv')$('#er-serv').classList.remove('vis');
    renderAll();
  });
  f.addEventListener('input',function(e){if(e.target.id==='c-nume'||e.target.id==='c-zi')updMsg()});
  f.addEventListener('submit',function(e){e.preventDefault()});
  var d=new Date();$('#c-zi').min=d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2);
  $$('#trimite,.cta-fix .wa-link').forEach(function(b){b.addEventListener('click',function(e){
    if(cur!=='creeaza')return;
    if(!S.serv){e.preventDefault();$('#er-serv').classList.add('vis');var r=$('#cfg input[name="serv"]');r.focus();r.closest('.pas').scrollIntoView({behavior:RM?'auto':'smooth',block:'center'})}
  })});
}

/* ================= PÁGINAS GERADAS ================= */
function buildServ(){
  $('#serv-lista').innerHTML=SERV.map(function(s,i){
    var st={forma:['oval','migdala','patrat','oval','oval','balerina'][i],cul:ci(['cireasa','pudra','nud','laptos','coral','lila'][i]),fin:'lucios',decor:['fara','fara','french','fara','fara','fluturas'][i]};
    return '<article class="s-card rv"><svg viewBox="0 0 64 40" aria-hidden="true" data-mini="'+i+'"></svg><h3 data-t="sv.'+s+'">'+t('sv.'+s)+'</h3><p data-t="sv.'+s+'.p">'+t('sv.'+s+'.p')+'</p><p class="pret"><span data-t="pret">'+t('pret')+'</span><span class="conf" data-t="conf">'+t('conf')+'</span></p></article>';
  }).join('');
  $$('#serv-lista svg[data-mini]').forEach(function(sv){var i=+sv.dataset.mini;var st={forma:['oval','migdala','patrat','oval','oval','balerina'][i],cul:ci(['cireasa','pudra','nud','laptos','coral','lila'][i]),fin:'lucios',decor:['fara','fara','french','fara','fara','fluturas'][i]};for(var j=0;j<3;j++)drawNail(sv,sv,14+j*18,38,(j-1)*8,13,30,10,st,{accent:j===1})});
  $('#forme').innerHTML=FORME.map(function(f){return '<div class="forma rv"><svg viewBox="0 0 50 84" aria-hidden="true" data-forma="'+f+'"></svg><h3 data-t="fo.'+f+'">'+t('fo.'+f)+'</h3><p data-t="fo.'+f+'.p">'+t('fo.'+f+'.p')+'</p></div>'}).join('');
  $$('#forme svg').forEach(function(sv){drawNail(sv,sv,25,80,0,34,74,30,{forma:sv.dataset.forma,cul:5,fin:'lucios',decor:'fara'})});
}
function buildIdei(){
  $('#idei').innerHTML=IDEI.map(function(d){return '<article class="idee rv"><div class="idee-viz" style="background:'+d.bg+'"><svg viewBox="0 0 250 200" aria-hidden="true" data-idee="'+d.id+'"></svg></div><div class="idee-in"><h3 data-t="id.'+d.id+'">'+t('id.'+d.id)+'</h3><p class="spec" data-spec="'+d.id+'"></p><button type="button" class="btn btn-cir btn-mic" data-incearca="'+d.id+'"><span data-t="id.incearca">'+t('id.incearca')+'</span></button></div></article>'}).join('');
  IDEI.forEach(function(d){var sv=$('svg[data-idee="'+d.id+'"]'),st={forma:d.forma,cul:ci(d.cul),fin:d.fin,decor:d.decor},ws=[30,36,38,36,30],ys=[150,130,122,130,150];
    var ext={scurt:.15,mediu:.55,lung:1}[d.lung];
    for(var j=0;j<5;j++){var w=ws[j]*.9;drawNail(sv,sv,45+j*40,ys[j]+20,(j-2)*7,w,w*1.05+w*ext,w*ext,st,{accent:j===3})}
  });
  $('#idei').addEventListener('click',function(e){var b=e.target.closest('[data-incearca]');if(!b)return;var d=IDEI.filter(function(x){return x.id===+b.dataset.incearca})[0];
    S.forma=d.forma;S.lung=d.lung;S.fin=d.fin;S.decor=d.decor;syncForm();location.hash='#/creeaza';setCul(ci(d.cul),false)});
  var lu=$('#lucrari'),sec=$('#lucrari-sec');sec.hidden=true;
  lu.innerHTML=LUCRARI.map(function(f){return '<figure class="ph" style="margin:0"><img src="media/'+f+'" alt="" loading="lazy"></figure>'}).join('');
  sec.hidden=!LUCRARI.length;
  $$('img',lu).forEach(function(im){im.addEventListener('error',function(){im.parentElement.remove()})});
}
function specs(){IDEI.forEach(function(d){var p=$('[data-spec="'+d.id+'"]');if(p)p.textContent=[t('fo.'+d.forma),t('lu.'+d.lung),t('cul.'+d.cul),t('fi.'+d.fin)].join(' · ')})}
var FAPTE=[['f.adr','pin'],['f.tel','tel'],['f.ore','ceas'],['f.nota','stea'],['f.fb','info',1],['f.echipa','info',1],['f.card','info',1]];
function buildFapte(){$('#fapte').innerHTML=FAPTE.map(function(f){return '<li><svg viewBox="0 0 16 24" aria-hidden="true"><path d="M2 11C2 4 4 1 8 1s6 3 6 10v12H2z" fill="'+(f[2]?'#C9A75A':'#A3123F')+'"/></svg><span><span data-t="'+f[0]+'">'+t(f[0])+'</span>'+(f[2]?' <span class="conf" data-t="conf">'+t('conf')+'</span>':'')+'</span></li>'}).join('')}
function buildStele(){var b=$('#stele-u');b.innerHTML='';for(var i=0;i<5;i++){var sv=el('svg',{viewBox:'0 0 20 32'},b);drawNail(sv,sv,10,31,0,16,30,8,{forma:'migdala',cul:5,fin:'lucios',decor:'fara'})}}

/* ================= ABERTO AGORA ================= */
function acum(){
  var z,h,m;try{var p=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Bucharest',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date()),o={};p.forEach(function(x){o[x.type]=x.value});z=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(o.weekday);h=+o.hour%24;m=+o.minute}catch(e){var d=new Date();z=d.getDay();h=d.getHours();m=d.getMinutes()}
  var min=h*60+m,lucru=z>=1&&z<=5,deschis=lucru&&min>=570&&min<1200,k;
  if(deschis)k='acum.da';else if(lucru&&min<570)k='acum.nu.azi';else if(z>=1&&z<=4)k='acum.nu.maine';else k='acum.nu.luni';
  $$('.deschis-acum').forEach(function(e){e.classList.toggle('da',deschis);e.querySelector('span').textContent=t(k)});
  $$('#ore div').forEach(function(r){r.classList.toggle('azi',+r.dataset.z===z)});
}

/* ================= LÍNGUA ================= */
function fillBanda(){var b=$('#banda'),it=t('banda').split('|'),h='';for(var r=0;r<4;r++)it.forEach(function(x){h+='<span>'+x+'</span>'});b.innerHTML=h}
function applyLang(l){
  lang=T[l]?l:'ro';H.dataset.lang=lang;H.lang=lang==='pt'?'pt-PT':lang;
  $$('[data-t]').forEach(function(e){var v=t(e.getAttribute('data-t'));if(e.innerHTML!==v)e.innerHTML=v});
  $$('[data-ta]').forEach(function(e){e.getAttribute('data-ta').split(';').forEach(function(p){var a=p.split(':');e.setAttribute(a[0],t(a[1]))})});
  $$('[data-cul]').forEach(function(e){e.setAttribute('aria-label',t('cul.'+CUL[+e.dataset.cul][0]))});
  $$('[data-cn]').forEach(function(e){e.textContent=colName(+e.dataset.cn)});
  $$('.lang button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===lang?'true':'false')});
  fillBanda();specs();acum();
  $('#cul-nume').textContent=colName(S.cul);
  var wa='https://wa.me/'+TEL+'?text='+encodeURIComponent(t('m.gen'));$$('.wa-link').forEach(function(a){a.href=wa});
  $$('.wa-idee').forEach(function(a){a.href='https://wa.me/'+TEL+'?text='+encodeURIComponent(t('m.idee'))});
  if(cur)D.title=t('title.'+cur);
  var bg=$('.burger');bg.setAttribute('aria-label',bg.getAttribute('aria-expanded')==='true'?t('a.burger2'):t('a.burger'));
  etichete();
  updMsg();
}
$$('.lang button').forEach(function(b){b.addEventListener('click',function(){applyLang(b.dataset.l);try{localStorage.setItem(LS_KEY,lang)}catch(e){}})});

/* ================= ROUTER ================= */
var PAGES=['acasa','servicii','creeaza','salonul','idei','vizita'],cur=null,first=true;
var burger=$('.burger'),meniu=$('#meniu');
function closeMenu(){meniu.classList.remove('deschis');burger.setAttribute('aria-expanded','false');burger.setAttribute('aria-label',t('a.burger'));D.body.style.overflow=''}
burger.addEventListener('click',function(){var o=burger.getAttribute('aria-expanded')!=='true';meniu.classList.toggle('deschis',o);burger.setAttribute('aria-expanded',o?'true':'false');burger.setAttribute('aria-label',o?t('a.burger2'):t('a.burger'));D.body.style.overflow=o?'hidden':''});
D.addEventListener('keydown',function(e){if(e.key==='Escape'&&meniu.classList.contains('deschis')){closeMenu();burger.focus()}});
function route(){
  var h=(location.hash||'').replace(/^#\/?/,'').split(/[?#]/)[0],pg=PAGES.indexOf(h)>-1?h:'acasa';
  $$('.pg').forEach(function(s){s.hidden=s.dataset.pg!==pg});
  $$('.nav a,.meniu a[data-pg]').forEach(function(a){if(a.dataset.pg===pg)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
  cur=pg;D.title=t('title.'+pg);closeMenu();
  if(!first){W.scrollTo(0,0);var f=$('.pg[data-pg="'+pg+'"] [tabindex="-1"]');if(f)f.focus({preventScroll:true})}
  first=false;
  if(pg==='vizita'){var fr=$('#harta');if(fr&&!fr.src)fr.src=fr.dataset.src}
  var fx=$('.cta-fix .wa-link');if(fx)fx.href='https://wa.me/'+TEL+'?text='+encodeURIComponent(t('m.gen'));
  if(pg==='creeaza')updMsg();
}
W.addEventListener('hashchange',route);
W.addEventListener('scroll',function(){$('#bara').classList.toggle('scrolled',W.pageYOffset>8)},{passive:true});

/* ================= ARRANQUE ================= */
if(!RM)H.classList.add('intrare');
capture();
buildSticle();buildForm();buildServ();buildIdei();buildFapte();buildStele();bindForm();
route();
setCul(S.cul,false);
applyLang(lang);
setInterval(acum,60000);
setTimeout(function(){H.classList.remove('intrare')},3600);
if('IntersectionObserver' in W&&!RM){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  $$('.rv').forEach(function(e){io.observe(e)});
}else $$('.rv').forEach(function(e){e.classList.add('in')});
})();
