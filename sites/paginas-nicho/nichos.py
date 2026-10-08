"""Nichos, cidades e textos das páginas por nicho e cidade (lido por gerar.py).

Cada demo entra num nicho por esta ordem: FIXOS (slug → nicho) → palavras do título → @type do JSON-LD.
Uma página só nasce quando o nicho tem demos suficientes (MINIMO) e texto escrito na língua da cidade.
Textos sem números inventados: só o número de demos, que é contado.
"""

MINIMO = 3          # demos (da cidade + de fora) para uma página existir
MINIMO_LOCAIS = 1   # demos da própria cidade

# donos que pediram para sair das páginas (o slug curto da demo); a demo continua no ar
EXCLUIR = set()

FIXOS = {
    "ceasornicarie-nicolina": "chei",
    "tapiterie": "domiciliu",
    "arca-pet": "animale",
    "frame-art": "magazine",
}

# (início de palavra no título, em minúsculas e sem acentos) → nicho. A primeira que bate ganha.
PALAVRAS = [
    ("barber", "frizerii"), ("frizer", "frizerii"), ("barbearia", "frizerii"),
    ("chei", "chei"), ("lacatus", "chei"),
    ("toaletaj", "animale"), ("veterinar", "animale"), ("pets", "animale"), ("pet spa", "animale"), ("pet shop", "animale"), ("canin", "animale"),
    ("masaj", "masaj"), ("massage", "masaj"), ("massagem", "masaj"),
    ("tatuaj", "tatuaje"), ("tattoo", "tatuaje"),
    ("croitor", "reparatii"), ("retus", "reparatii"), ("incaltaminte", "reparatii"), ("cizmar", "reparatii"),
    ("reparatii", "reparatii"), ("costureira", "reparatii"), ("sapateiro", "reparatii"),
    ("tapiterie", "domiciliu"), ("instalator", "domiciliu"), ("electrician", "domiciliu"),
    ("curatatorie", "domiciliu"), ("spalatorie si", "domiciliu"), ("lavandaria", "domiciliu"),
    ("spalatorie auto", "auto"), ("detailing", "auto"), ("service auto", "auto"), ("vulcaniz", "auto"),
    ("oficina", "auto"), ("mecanica", "auto"),
    ("stomatolog", "clinici"), ("dentist", "clinici"), ("clinica", "clinici"),
    ("fitness", "fitness"), ("ginasio", "fitness"), ("sala de sport", "fitness"),
]

TIPOS = {
    "BarberShop": "frizerii",
    "HairSalon": "saloane", "BeautySalon": "saloane", "NailSalon": "saloane", "DaySpa": "saloane",
    "AutoRepair": "auto", "TireShop": "auto", "AutoWash": "auto", "AutoBodyShop": "auto", "AutoDealer": "auto",
    "Restaurant": "restaurante", "FastFoodRestaurant": "restaurante", "BarOrPub": "restaurante",
    "CafeOrCoffeeShop": "cafenele", "Bakery": "cafenele", "IceCreamShop": "cafenele",
    "VeterinaryCare": "animale", "PetStore": "animale",
    "TattooParlor": "tatuaje",
    "HealthAndBeautyBusiness": "masaj",
    "ShoeRepair": "reparatii",
    "Locksmith": "chei",
    "Florist": "magazine", "JewelryStore": "magazine", "BikeStore": "magazine", "LiquorStore": "magazine",
    "ButcherShop": "magazine", "Store": "magazine", "ClothingStore": "magazine", "HomeGoodsStore": "magazine",
    "Plumber": "domiciliu", "Electrician": "domiciliu", "DryCleaningOrLaundry": "domiciliu",
    "HousePainter": "domiciliu", "HVACBusiness": "domiciliu",
    "Dentist": "clinici", "MedicalClinic": "clinici", "Physician": "clinici", "Optician": "clinici",
    "ExerciseGym": "fitness", "SportsActivityLocation": "fitness",
}

# Ordem das páginas nos índices
ORDEM = ["restaurante", "cafenele", "frizerii", "saloane", "auto", "magazine", "animale",
         "tatuaje", "masaj", "reparatii", "chei", "domiciliu", "clinici", "fitness"]

CIDADES = {
    "iasi": {
        "lingua": "ro", "nome": "Iași", "em": "în Iași", "de": "din Iași",
        "host": "https://ro.pachecost.com", "base": "/site-uri/",
        "diag": "https://ro.pachecost.com/?utm_source=nisa&utm_medium=site&utm_content=diag-nisa-{pagina}#diagnostico",
        "whatsapp": "40723098556",
        "pixel": False,
    },
    "algarve": {
        "lingua": "pt", "nome": "Algarve", "em": "no Algarve", "de": "do Algarve",
        "host": "https://pachecost.com", "base": "/sites/",
        "diag": "https://pachecost.com/?utm_source=nicho&utm_medium=site&utm_content=diag-nicho-{pagina}#diagnostico",
        "whatsapp": "351967117357",
        "pixel": True,
    },
}

# ─── textos da página (comuns por língua) ───
UI = {
    "ro": {
        "html": "ro", "og": "ro_RO",
        "toate": "Toate domeniile", "cta": "Cunoaște-ne", "cta_scurt": "Cunoaște-ne",
        "vezi": "Vezi site-urile", "deschide": "Vezi site-ul",
        "numar": ["site făcut deja pentru {plural} {de}", "site-uri făcute deja pentru {plural} {de}"],
        "strada_t": "Deja online, pe strada ta.",
        "strada_p": "Prezentări făcute de Pacheco Studios pentru afaceri reale {de}, pornind de la ce aveau deja public. Deschide-le pe telefon: așa le vor vedea clienții.",
        "afara": "Făcut în {oras}",
        "ce_t": "Ce face site-ul pentru {sing}",
        "pasi_t": "Cum începem",
        "pasi": [
            ("Diagnosticul", "Câteva întrebări despre afacerea ta, în două minute. Ajung la noi pe WhatsApp."),
            ("Discuția de 20 de minute", "Ne vedem în Iași sau vorbim la telefon. Ne spui ce vrei să obții."),
            ("Propunerea scrisă", "Primești ce facem, cum arată și cât costă. Decizi tu, fără grabă."),
        ],
        "faq_t": "Întrebări",
        "faq": [
            ("Trebuie să am poze profesionale?", "Nu. Pornim de la ce ai deja public, pe Google, Instagram sau Facebook, și le înlocuim când ai poze noi."),
            ("Merge bine pe telefon?", "Da. Îl gândim întâi pentru telefon și abia apoi pentru calculator."),
            ("Pot vedea cum ar arăta pentru afacerea mea?", "Da. Începe cu diagnosticul și îți arătăm o prezentare făcută pentru afacerea ta."),
        ],
        "alte_t": "Alte domenii {em}",
        "final_t": "Afacerea ta e următoarea de pe stradă?",
        "final_p": "Răspunde la câteva întrebări și vorbim 20 de minute. Fără obligații.",
        "whatsapp": "Scrie-ne pe WhatsApp",
        "wa_msg": "Bună! Am văzut site-urile pentru {plural} {de} și vreau unul pentru afacerea mea.",
        "acasa": "Pacheco Studios", "site_uri": "Site-uri",
        "privacidade": ("Confidențialitate", "https://ro.pachecost.com/confidentialitate.html"),
        "cookies": ("Cookie-uri", "https://ro.pachecost.com/cookie-uri.html"),
        "reclamacoes": "Cartea de reclamații (PT)",
        "rodape": "Site-uri și sisteme AI pentru afaceri locale.",
        "indice_h1": "Site-uri pentru afaceri {de}, pe domenii",
        "indice_p": "Alege domeniul tău și vezi site-urile pe care le-am făcut deja pentru afaceri ca a ta.",
        "indice_title": "Site-uri pentru afaceri {de} · exemple pe domenii · Pacheco Studios",
        "indice_desc": "{n} site-uri făcute pentru afaceri {de}, pe domenii: {lista}. Vezi exemple reale și cere-l pe al tău.",
        "card_n": ["{n} site", "{n} site-uri"],
        "title": "Site pentru {plural} {em} · {n} exemple reale · Pacheco Studios",
        "skip": "Sari la conținut",
    },
    "pt": {
        "html": "pt-PT", "og": "pt_PT",
        "toate": "Todas as áreas", "cta": "Conhece-nos", "cta_scurt": "Conhece-nos",
        "vezi": "Ver os sites", "deschide": "Ver o site",
        "numar": ["site já feito para {plural}", "sites já feitos para {plural}"],
        "strada_t": "Já online, na tua rua.",
        "strada_p": "Apresentações feitas pela Pacheco Studios para negócios reais, a partir do que já tinham público. Abre-as no telemóvel: é assim que os clientes as veem.",
        "afara": "Feito em {oras}",
        "ce_t": "O que o site faz por {sing}",
        "pasi_t": "Como começamos",
        "pasi": [
            ("O diagnóstico", "Umas perguntas sobre o teu negócio, em dois minutos. Chegam-nos pelo WhatsApp."),
            ("A conversa de 20 minutos", "Por videochamada ou telefone. Dizes-nos o que queres conseguir."),
            ("A proposta escrita", "Recebes o que fazemos, como fica e quanto custa. Decides tu, sem pressa."),
        ],
        "faq_t": "Perguntas",
        "faq": [
            ("Preciso de fotografias profissionais?", "Não. Partimos do que já tens público, no Google, Instagram ou Facebook, e trocamos quando tiveres fotos novas."),
            ("Fica bem no telemóvel?", "Sim. Pensamos primeiro no telemóvel e só depois no computador."),
            ("Posso ver como ficaria para o meu negócio?", "Sim. Começa pelo diagnóstico e mostramos-te uma apresentação feita para o teu negócio."),
        ],
        "alte_t": "Outras áreas {em}",
        "final_t": "O teu negócio é o próximo da rua?",
        "final_p": "Responde a umas perguntas e falamos 20 minutos. Sem compromisso.",
        "whatsapp": "Fala connosco no WhatsApp",
        "wa_msg": "Olá! Vi os sites para {plural} {em} e quero um para o meu negócio.",
        "acasa": "Pacheco Studios", "site_uri": "Sites",
        "privacidade": ("Privacidade", "https://pachecost.com/privacidade.html"),
        "cookies": ("Cookies", "https://pachecost.com/cookies.html"),
        "reclamacoes": "Livro de Reclamações",
        "rodape": "Sites e sistemas de IA para negócios locais.",
        "indice_h1": "Sites para negócios {de}, por área",
        "indice_p": "Escolhe a tua área e vê os sites que já fizemos para negócios como o teu.",
        "indice_title": "Sites para negócios {de} · exemplos por área · Pacheco Studios",
        "indice_desc": "{n} sites feitos para negócios locais, por área: {lista}. Vê exemplos reais e pede o teu.",
        "card_n": ["{n} site", "{n} sites"],
        "title": "Sites para {plural} {em} · {n} exemplos reais · Pacheco Studios",
        "skip": "Saltar para o conteúdo",
    },
}

# ─── textos por nicho ───
# slug: parte do endereço (+ "-<cidade>"); plural: no H1 («Site pentru {plural} în Iași»);
# sing: «Ce face site-ul pentru {sing}»; curto: nome nos índices; lead; ce: 4 (etiqueta, frase); faq: 1 própria.
NICHOS = {
    "frizerii": {
        "ro": {
            "slug": "frizerii", "plural": "frizerii", "sing": "o frizerie", "curto": "Frizerii",
            "lead": "Clienții noi caută „frizerie” pe Google Maps și aleg după ce văd în primele secunde: tunsori, prețuri, unde se programează. Un site pune totul într-un singur link.",
            "ce": [("Programări", "Butonul de programare duce unde programezi deja: MERO, Booksy, WhatsApp sau telefon."),
                   ("Prețuri", "Serviciile și prețurile, scrise clar, ca nimeni să nu mai întrebe în mesaje."),
                   ("Galerie", "Tunsorile tale în față: fade-uri, bărbi, înainte și după."),
                   ("Echipa", "Fiecare frizer cu numele și stilul lui, ca clientul să știe la cine vine.")],
            "faq": ("Pot păstra programările pe MERO sau Booksy?", "Da. Site-ul nu înlocuiește aplicația: butonul de programare duce acolo."),
        },
        "pt": {
            "slug": "barbearias", "plural": "barbearias", "sing": "uma barbearia", "curto": "Barbearias",
            "lead": "Quem procura «barbearia» no Google Maps escolhe pelo que vê nos primeiros segundos: cortes, preços e onde marcar. Um site junta tudo num só link.",
            "ce": [("Marcações", "O botão de marcar leva onde já marcas: Booksy, Fresha, WhatsApp ou telefone."),
                   ("Preços", "Os serviços e os preços, escritos com clareza, para ninguém perguntar por mensagem."),
                   ("Galeria", "Os teus cortes à frente: fades, barbas, antes e depois."),
                   ("A equipa", "Cada barbeiro com o nome e o estilo, para o cliente saber com quem vai.")],
            "faq": ("Posso manter as marcações no Booksy?", "Sim. O site não substitui a aplicação: o botão de marcar leva lá."),
        },
    },
    "saloane": {
        "ro": {
            "slug": "saloane-infrumusetare", "plural": "saloane de înfrumusețare", "sing": "un salon", "curto": "Saloane de înfrumusețare",
            "lead": "Unghii, gene, sprâncene, păr: clientele aleg salonul după poze și după cât de ușor se programează. Un site arată lucrările și duce la programare dintr-o atingere.",
            "ce": [("Portofoliu", "Lucrările tale pe categorii: manichiură, gene, sprâncene, păr."),
                   ("Servicii și prețuri", "Ce faci, cât durează și cât costă, într-o listă ușor de citit pe telefon."),
                   ("Programare", "Un buton spre MERO, WhatsApp sau telefon, vizibil pe fiecare ecran."),
                   ("Cum ajungi", "Adresa, harta și programul, fără să le cauți prin postări.")],
            "faq": ("Am deja Instagram. De ce și site?", "Instagram arată lucrările. Site-ul apare pe Google și răspunde la ce întreabă orice clientă nouă: prețuri, program, adresă, programare."),
        },
        "pt": {
            "slug": "saloes-de-beleza", "plural": "salões de beleza", "sing": "um salão", "curto": "Salões de beleza",
            "lead": "Unhas, pestanas, sobrancelhas, cabelo: as clientes escolhem o salão pelas fotos e pela facilidade de marcar. Um site mostra os trabalhos e leva à marcação num toque.",
            "ce": [("Portefólio", "Os teus trabalhos por categoria: unhas, pestanas, sobrancelhas, cabelo."),
                   ("Serviços e preços", "O que fazes, quanto demora e quanto custa, numa lista fácil de ler no telemóvel."),
                   ("Marcação", "Um botão para a aplicação, o WhatsApp ou o telefone, à vista em cada ecrã."),
                   ("Como chegar", "Morada, mapa e horário, sem procurar entre publicações.")],
            "faq": ("Já tenho Instagram. Para quê um site?", "O Instagram mostra os trabalhos. O site aparece no Google e responde ao que qualquer cliente nova pergunta: preços, horário, morada, marcação."),
        },
    },
    "auto": {
        "ro": {
            "slug": "service-auto", "plural": "service-uri auto și spălătorii", "sing": "un service auto", "curto": "Service-uri auto și spălătorii",
            "lead": "Când se aprinde un martor în bord, șoferul caută „service auto” lângă el și sună primul care pare de încredere. Un site spune ce faceți, unde sunteți și cum vă sună.",
            "ce": [("Servicii", "Revizii, diagnoză, frâne, roți, spălare, detailing: lista exactă a ce faceți."),
                   ("Sună acum", "Pe telefon, primul lucru de pe site e butonul de apel."),
                   ("Hartă și program", "Adresa, harta și orele, ca nimeni să nu vină la ușa închisă."),
                   ("Mărci și pachete", "Mărcile cu care lucrați sau pachetele de spălare, cu prețuri dacă vreți.")],
            "faq": ("Clienții mei sună, nu scriu. Mai ajută un site?", "Da. Pe telefon, site-ul începe cu butonul de apel: doar îi convinge să te sune pe tine."),
        },
        "pt": {
            "slug": "oficinas", "plural": "oficinas e lavagens auto", "sing": "uma oficina", "curto": "Oficinas e lavagens auto",
            "lead": "Quando acende uma luz no painel, o condutor procura «oficina» perto de si e liga à primeira que parece de confiança. Um site diz o que fazem, onde estão e como vos ligar.",
            "ce": [("Serviços", "Revisões, diagnóstico, travões, pneus, lavagem: a lista exata do que fazem."),
                   ("Ligar já", "No telemóvel, a primeira coisa do site é o botão de chamada."),
                   ("Mapa e horário", "Morada, mapa e horas, para ninguém chegar com a porta fechada."),
                   ("Marcas e pacotes", "As marcas com que trabalham ou os pacotes de lavagem, com preços se quiserem.")],
            "faq": ("Os meus clientes ligam, não escrevem. Um site ajuda?", "Sim. No telemóvel o site abre com o botão de chamada: só os convence a ligar-te a ti."),
        },
    },
    "restaurante": {
        "ro": {
            "slug": "restaurante", "plural": "restaurante", "sing": "un restaurant", "curto": "Restaurante",
            "lead": "Înainte să rezerve, oamenii vor să vadă meniul, sala și cât costă. Un site le arată pe toate și duce la rezervare sau la comandă.",
            "ce": [("Meniu", "Meniul complet pe telefon, cu poze și prețuri, ușor de schimbat."),
                   ("Rezervări", "Un buton de rezervare la telefon sau pe WhatsApp, mereu la vedere."),
                   ("Livrare", "Linkurile spre Glovo, Tazz sau Bolt Food, dacă sunteți acolo."),
                   ("Sala și terasa", "Pozele locului, ca oamenii să știe unde vin.")],
            "faq": ("Meniul se schimbă des. Cine îl actualizează?", "Ne trimiți meniul nou pe WhatsApp și îl schimbăm noi."),
        },
        "pt": {
            "slug": "restaurantes", "plural": "restaurantes", "sing": "um restaurante", "curto": "Restaurantes",
            "lead": "Antes de reservar, as pessoas querem ver a ementa, a sala e quanto custa. No Algarve, muitas leem em inglês. Um site mostra tudo nas duas línguas e leva à reserva.",
            "ce": [("Ementa", "A ementa completa no telemóvel, com fotos e preços, fácil de mudar."),
                   ("Reservas", "Um botão para reservar por telefone ou WhatsApp, sempre à vista."),
                   ("Pratos do dia", "O prato do dia em destaque, trocado quando muda."),
                   ("Português e inglês", "O mesmo site nas duas línguas, para quem está de passagem.")],
            "faq": ("A ementa muda muitas vezes. Quem a atualiza?", "Mandas-nos a ementa nova pelo WhatsApp e mudamos nós."),
        },
    },
    "cafenele": {
        "ro": {
            "slug": "cafenele-cofetarii", "plural": "cafenele și cofetării", "sing": "o cafenea sau cofetărie", "curto": "Cafenele și cofetării",
            "lead": "Torturi la comandă, prăjituri, pâine, înghețată, cafea: produsele se vând din poze. Un site le arată cum trebuie și primește comenzile.",
            "ce": [("Vitrina", "Produsele cu poze, pe categorii, cum le-ar vedea cineva la tejghea."),
                   ("Comenzi", "Pentru torturi și evenimente: un formular scurt care ajunge la tine pe WhatsApp."),
                   ("Program", "Orele, adresa și harta, la un clic."),
                   ("Evenimente", "Candy bar, botezuri, aniversări: ce oferiți și cum se comandă.")],
            "faq": ("Pot primi comenzi de torturi prin site?", "Da. Un formular scurt (data, câte persoane, ce model) care îți ajunge pe WhatsApp."),
        },
        "pt": {
            "slug": "pastelarias-e-cafes", "plural": "pastelarias e cafés", "sing": "uma pastelaria ou café", "curto": "Pastelarias e cafés",
            "lead": "Bolos por encomenda, pastelaria, brunch, café: os produtos vendem-se pelas fotos. Um site mostra-os como merecem e recebe as encomendas.",
            "ce": [("Montra", "Os produtos com fotos, por categoria, como se estivessem no balcão."),
                   ("Encomendas", "Para bolos e festas: um formulário curto que te chega pelo WhatsApp."),
                   ("Horário", "Horas, morada e mapa, a um toque."),
                   ("Para eventos", "Batizados, aniversários, empresas: o que fazem e como se encomenda.")],
            "faq": ("Posso receber encomendas de bolos pelo site?", "Sim. Um formulário curto (data, quantas pessoas, que modelo) que te chega pelo WhatsApp."),
        },
    },
    "animale": {
        "ro": {
            "slug": "animale", "plural": "cabinete veterinare, pet shop-uri și toaletaj", "sing": "o afacere cu animale", "curto": "Veterinari, pet shop, toaletaj",
            "lead": "Stăpânii caută un loc în care să aibă încredere. Un site arată cine are grijă de animal, ce servicii aveți și cum se face programarea.",
            "ce": [("Servicii", "Consultații, toaletaj, hrană, accesorii: ce găsește stăpânul la voi."),
                   ("Programare", "Un buton spre telefon sau WhatsApp, cu ce informații să trimită."),
                   ("Echipa", "Oamenii care au grijă de animale, cu nume și poze."),
                   ("Program și urgențe", "Orele clare și numărul la care se sună când e grav.")],
            "faq": ("Pot pune și produsele din magazin?", "Da. O vitrină cu produsele principale și comandă pe WhatsApp sau telefon."),
        },
    },
    "tatuaje": {
        "ro": {
            "slug": "tatuaje", "plural": "studiouri de tatuaje", "sing": "un studio de tatuaje", "curto": "Studiouri de tatuaje",
            "lead": "Un tatuaj se alege după portofoliu. Un site pune lucrările fiecărui artist în față și duce la o programare pentru consultație.",
            "ce": [("Portofoliu pe artiști", "Fiecare artist cu stilul și lucrările lui."),
                   ("Consultație", "Clientul trimite ideea și locul tatuajului pe WhatsApp, dintr-un buton."),
                   ("Îngrijire", "Instrucțiunile de după tatuaj, mereu la îndemână."),
                   ("Piercing", "Ce faceți, cu ce bijuterii și cum se programează.")],
            "faq": ("Am portofoliul pe Instagram. Ajunge?", "Instagram e bun pentru cine te urmărește deja. Site-ul te aduce pe Google, în fața celor care caută un studio acum."),
        },
    },
    "masaj": {
        "ro": {
            "slug": "masaj", "plural": "centre de masaj", "sing": "un centru de masaj", "curto": "Masaj",
            "lead": "Clienții vor să știe ce tip de masaj primesc, cât durează și cât costă, înainte să sune. Un site răspunde la toate și duce la programare.",
            "ce": [("Tipuri de masaj", "Terapeutic, de relaxare, la domiciliu: ce face fiecare, pe înțeles."),
                   ("Durate și prețuri", "30, 60 sau 90 de minute, cu prețul lângă fiecare."),
                   ("Programare", "Un buton spre telefon sau WhatsApp, pe fiecare ecran."),
                   ("Vouchere", "O pagină pentru vouchere cadou, comandate pe WhatsApp.")],
            "faq": ("Lucrez la domiciliu, fără salon. Am nevoie de site?", "Da, mai ales. Site-ul arată zonele în care vii, serviciile și cum te programează."),
        },
    },
    "reparatii": {
        "ro": {
            "slug": "croitorii-reparatii", "plural": "croitorii și ateliere de reparații", "sing": "un atelier", "curto": "Croitorii și reparații",
            "lead": "Croitorie, retușuri, cizmărie, televizoare: oamenii caută „lângă mine” și vor să știe dacă faceți ce le trebuie. Un site spune clar ce reparați și cum ajung la voi.",
            "ce": [("Ce reparăm", "Lista exactă a lucrărilor, ca omul să știe că a ajuns unde trebuie."),
                   ("Trimite o poză", "Clientul trimite poza pe WhatsApp și primește un răspuns înainte să vină."),
                   ("Termene", "Cât durează de obicei fiecare lucrare, scris de voi."),
                   ("Adresa", "Harta, programul și unde se intră.")],
            "faq": ("Am un atelier mic. Merită un site?", "Da. Oamenii caută „croitorie” sau „cizmărie” lângă ei; site-ul te pune pe hartă cu tot ce trebuie să știe."),
        },
    },
    "chei": {
        "ro": {
            "slug": "chei", "plural": "copiere chei și chei auto", "sing": "un atelier de chei", "curto": "Chei și chei auto",
            "lead": "Cine a pierdut cheia mașinii caută urgent și sună primul care pare că se pricepe. Un site arată ce chei faceți, pentru ce mărci și cum vă găsesc.",
            "ce": [("Ce copiem", "Chei, cartele de interfon, telecomenzi: tot ce faceți, cu poze."),
                   ("Chei auto", "Mărcile și tipurile de chei cu cip cu care lucrați."),
                   ("Sună acum", "Butonul de apel, primul pe ecranul telefonului."),
                   ("Hartă", "Unde sunteți exact, chiar și într-un magazin sau într-o piață.")],
            "faq": ("Lucrez într-un chioșc. Mă găsește lumea pe site?", "Da. Site-ul spune exact unde e chioșcul, cu hartă și poză de la intrare."),
        },
    },
    "magazine": {
        "ro": {
            "slug": "magazine", "plural": "magazine locale", "sing": "un magazin", "curto": "Magazine locale",
            "lead": "Flori, bijuterii, vinuri, biciclete, carne: oamenii vor să vadă ce găsesc la tine înainte să vină. Un site e vitrina care stă deschisă și noaptea.",
            "ce": [("Vitrina", "Produsele principale, cu poze, pe categorii."),
                   ("Comenzi", "Comandă pe WhatsApp sau la telefon, dintr-un buton."),
                   ("Program și adresă", "Orele și harta, la un clic."),
                   ("Livrare", "Dacă livrați, unde și cum.")],
            "faq": ("Trebuie să fie magazin online cu plată?", "Nu. Mulți încep cu vitrina și comanda pe WhatsApp; plata online se poate pune mai târziu."),
        },
        "pt": {
            "slug": "lojas", "plural": "lojas locais", "sing": "uma loja", "curto": "Lojas locais",
            "lead": "Flores, joias, vinhos, bicicletas: as pessoas querem ver o que encontram antes de irem. Um site é a montra que fica aberta também à noite.",
            "ce": [("Montra", "Os produtos principais, com fotos, por categoria."),
                   ("Encomendas", "Encomenda por WhatsApp ou telefone, num botão."),
                   ("Horário e morada", "As horas e o mapa, a um toque."),
                   ("Entregas", "Se entregam, onde e como.")],
            "faq": ("Tem de ser uma loja online com pagamento?", "Não. Muitos começam pela montra e pela encomenda no WhatsApp; o pagamento online pode vir depois."),
        },
    },
    "domiciliu": {
        "ro": {
            "slug": "servicii-la-domiciliu", "plural": "servicii la domiciliu", "sing": "un serviciu la domiciliu", "curto": "Servicii la domiciliu",
            "lead": "Când curge o țeavă sau trebuie curățată o canapea, omul caută pe telefon și sună primul de încredere. Un site arată ce faceți, în ce zone și cum vă sună.",
            "ce": [("Servicii", "Ce faceți, explicat simplu: instalații, curățenie, tapițerie, spălătorie."),
                   ("Zone", "Cartierele și localitățile în care veniți."),
                   ("Sună acum", "Butonul de apel, primul pe ecran."),
                   ("Lucrări", "Poze înainte și după, ca omul să vadă că vă pricepeți.")],
            "faq": ("Lucrez singur, fără firmă mare. Arată serios un site?", "Da. Un site curat, cu lucrările tale și numele tău, arată mai serios decât un anunț."),
        },
    },
    "clinici": {
        "ro": {
            "slug": "cabinete-medicale", "plural": "cabinete medicale și stomatologice", "sing": "un cabinet", "curto": "Cabinete medicale",
            "lead": "Pacienții aleg medicul după încredere: cine e, ce face și cât de ușor se programează. Un site răspunde la toate înainte de primul telefon.",
            "ce": [("Medicii", "Fiecare medic cu numele, specializarea și poza."),
                   ("Tratamente", "Ce faceți, explicat pe înțelesul pacientului."),
                   ("Programare", "Un buton spre telefon, WhatsApp sau platforma pe care o folosiți."),
                   ("Cum ajungi", "Adresa, harta, parcarea și programul.")],
            "faq": ("Pot pune prețurile tratamentelor?", "Da, sau prețuri „de la”, dacă depind de consultație."),
        },
    },
    "fitness": {
        "ro": {
            "slug": "sali-fitness", "plural": "săli de fitness", "sing": "o sală", "curto": "Săli de fitness",
            "lead": "Cine vrea să înceapă caută o sală aproape și se uită la abonamente, program și antrenori. Un site arată tot și duce la prima vizită.",
            "ce": [("Abonamente", "Prețurile clare, pe tipuri de abonament."),
                   ("Clase și program", "Ce clase aveți și la ce oră."),
                   ("Antrenori", "Cine antrenează și ce face fiecare."),
                   ("Prima vizită", "Un buton pentru o primă vizită, pe WhatsApp sau telefon.")],
            "faq": ("Orarul claselor se schimbă. Cine îl actualizează?", "Ne trimiți orarul nou și îl schimbăm noi."),
        },
    },
}
