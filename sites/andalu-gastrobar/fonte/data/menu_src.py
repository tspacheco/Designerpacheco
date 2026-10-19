# -*- coding: utf-8 -*-
"""Carta real do Andalu Gastrobar (fonte: API Poloniq do site oficial, recolhida 2026-10-19, 169 produtos).
Gera data/menu.json: `python3 data/menu_src.py` a partir de fonte/.
Preços em lei, tal como no menu digital. EN = tradução nossa, nomes espanhóis mantidos.
Tags: veg vegetarian · glu gluten · lac lactate · cru crustacee · mol moluște · pes pește · ou ouă · nuc nuci/oleaginoase · sul sulfiți."""
import json, pathlib

S = []  # (id, kicker_ro, kicker_en, title_ro, title_en, lead_ro, lead_en, [dishes])
def sec(*a): S.append(a)
def d(ro, en, w, price, dro, den, tags='', fav=False):
    return dict(name={'ro': ro, 'en': en}, w=w, price=f'{price} lei', desc={'ro': dro, 'en': den}, tags=tags.split(), fav=fav)

# ----------------------------------------------------------------------------- TACOS & NACHOS
sec('tacos', 'De început', 'To start', 'Tacos & nachos', 'Tacos & nachos',
    'Nachos gratinați cu guacamole făcut din avocado proaspăt, tacos cu creveți sau cu mușchi de vită.',
    'Nachos baked with cheese and guacamole from fresh avocado, tacos with prawns or beef.', [
 d('Tacos con gambas · 4 buc.', 'Tacos con gambas · 4 pcs', '400 g', 66, 'Lipii din grâu, creveți trași la tigaie, pico de gallo cu avocado, salsa rosa și salată.', 'Wheat tortillas, pan-fried prawns, avocado pico de gallo, salsa rosa and salad.', 'cru glu lac', True),
 d('Nachos cu brânză și guacamole', 'Nachos with cheese and guacamole', '380 g', 44, 'Nachos, cheddar, mozzarella, jalapeños, guacamole, rodie.', 'Nachos, cheddar, mozzarella, jalapeños, guacamole, pomegranate.', 'veg lac'),
 d('Nachos cu fasole roșie, legume și guacamole', 'Nachos with red beans, vegetables and guacamole', '450 g', 51, 'Nachos gratinați la cuptor cu cheddar și mozzarella, legume și fasole roșie, guacamole și jalapeños.', 'Nachos baked with cheddar and mozzarella, vegetables and red beans, guacamole and jalapeños.', 'veg lac'),
 d('Nachos cu carne și guacamole', 'Nachos with meat and guacamole', '450 g', 53, 'Nachos gratinați cu cheddar și mozzarella, carne de vită și porc în sos de roșii, guacamole și jalapeños.', 'Nachos baked with cheddar and mozzarella, beef and pork in tomato sauce, guacamole and jalapeños.', 'lac'),
 d('Tacos gorditos cu mușchi de vită · 4 buc.', 'Tacos gorditos with beef · 4 pcs', '350 g', 66, 'Fâșii de mușchi de vită la grătar, cremă de fasole roșie cu susan, chorizo crocant, sirop de arțar, ridiche; picanți la alegere.', 'Grilled beef strips, red-bean and sesame cream, crispy chorizo, maple syrup, radish; spicy on request.', 'glu nuc'),
])

# ----------------------------------------------------------------------------- TAPAS
sec('tapas', 'De împărțit', 'To share', 'Tapas', 'Tapas',
    'Farfurii mici, puse în mijlocul mesei. Trei-patru pentru doi oameni sunt o masă.',
    'Small plates for the middle of the table. Three or four between two people make a meal.', [
 d('Patatas bravas', 'Patatas bravas', '200 g', 17, 'Cuburi de cartofi proaspeți, prăjiți, cu sos picant brava.', 'Cubes of fresh fried potato with spicy brava sauce.', 'veg', True),
 d('Patatas alioli', 'Patatas alioli', '200 g', 17, 'Cartofi prăjiți cu alioli: maioneză fină, usturoi, pătrunjel și puțină portocală.', 'Fried potatoes with alioli: fine mayonnaise, garlic, parsley and a touch of orange.', 'veg lac ou'),
 d('Patatas dos salsas', 'Patatas dos salsas', '250 g', 24, 'Cartofi prăjiți cu ambele sosuri: alioli și brava.', 'Fried potatoes with both sauces: alioli and brava.', 'veg lac ou'),
 d('Pimientos de Padrón', 'Pimientos de Padrón', '100 g', 33, 'Ardei verzi mici din Galicia, prăjiți, cu sare Maldon. Unii iuți, cei mai mulți nu.', 'Small green peppers from Galicia, fried, with Maldon salt. Some are hot, most are not.', 'veg'),
 d('Gambas al ajillo · 1 persoană', 'Gambas al ajillo · for one', '200 g', 39, 'Creveți în ulei de măsline extravirgin, usturoi și ardei iute. Pâinea e pentru sos.', 'Prawns in extra-virgin olive oil, garlic and chilli. The bread is for the sauce.', 'cru glu', True),
 d('Gambas al ajillo · 2 persoane', 'Gambas al ajillo · for two', '400 g', 75, 'Aceeași rețetă, porție de împărțit.', 'Same recipe, sharing portion.', 'cru glu'),
 d('Gambón · creveți roșii sălbatici', 'Gambón · wild red prawns', '240 g', 66, 'Marcați pe grătar și terminați la tigaie cu ulei de măsline, usturoi, cognac, pătrunjel și sare Maldon.', 'Seared on the grill and finished in the pan with olive oil, garlic, cognac, parsley and Maldon salt.', 'cru'),
 d('Chipirones fritos', 'Chipirones fritos', '200 g', 39, 'Baby calamari prăjiți după tehnica „rebozado andaluz”, cu alioli de portocale.', 'Baby squid fried the Andalusian way, with orange alioli.', 'mol glu lac', True),
 d('Pulpo a la gallega', 'Pulpo a la gallega', '400 g', 78, 'Tentacul de caracatiță fiert ca în Galicia, cu pimentón de la Vera, ulei de măsline și rondele de cartofi.', 'Octopus tentacle cooked the Galician way, with pimentón de la Vera, olive oil and potato rounds.', 'mol', True),
 d('Pulpo a la brasa', 'Pulpo a la brasa', '400 g', 80, 'Caracatiță pe jar cu salsa verde și cremă de cartofi cu pimentón.', 'Charcoal-grilled octopus with salsa verde and smoked-paprika potato cream.', 'mol lac'),
 d('Pulpo al ajillo', 'Pulpo al ajillo', '', 69, 'Caracatiță în ulei de măsline, usturoi, coniac, chili și boia afumată.', 'Octopus in olive oil, garlic, brandy, chilli and smoked paprika.', 'mol'),
 d('Scoici Saint-Jacques pe grătar · 4 buc.', 'Grilled scallops · 4 pcs', '', 42, 'Vieiras cu unt, salsa verde, un strop de vin alb și sare Maldon.', 'Scallops with butter, salsa verde, a splash of white wine and Maldon salt.', 'mol lac'),
 d('Stridii Gillardeau nr. 2 · 1 buc.', 'Gillardeau oyster no. 2 · 1 pc', '', 25, 'Cu salsa mignonette.', 'With mignonette sauce.', 'mol'),
 d('Jamón ibérico', 'Jamón ibérico', '150 g', 60, 'Cebo de campo, 50 % rasă iberică, tăiat la cuțit. Cu pâine prăjită, roșii rase, ulei și usturoi.', 'Cebo de campo, 50 % Iberian breed, hand-carved. With toasted bread, grated tomato, oil and garlic.', 'glu', True),
 d('Brânzeturi maturate spaniole', 'Aged Spanish cheeses', '120 g', 53, 'Două brânzeturi de oaie din Castilla-La Mancha și Valladolid, dulceață de ceapă, miez de nucă, oregano.', 'Two sheep cheeses from Castilla-La Mancha and Valladolid, onion jam, walnuts, oregano.', 'veg lac nuc'),
 d('Tartar de vită', 'Beef tartare', '150 g', 69, 'Mușchi de vită, capere, anșoa, ceapă roșie, gălbenuș, muștar, salsa Valentina. Pâine de casă prăjită.', 'Beef fillet, capers, anchovy, red onion, egg yolk, mustard, Valentina sauce. Toasted homemade bread.', 'pes ou glu'),
 d('Tartar de ton roșu cu avocado', 'Red tuna tartare with avocado', '150 g', 66, 'Ton proaspăt, avocado, ceapă roșie, soia, ulei de susan, perle de soia.', 'Fresh tuna, avocado, red onion, soy, sesame oil, soy pearls.', 'pes nuc'),
 d('Gilda con atún', 'Gilda con atún', '60 g', 21, 'Frigăruie cu ton roșu marinat, piparras (ardei verzi în oțet), cepșoară murată, măsline.', 'Skewer of marinated red tuna, piparras (pickled green peppers), pickled onion, olives.', 'pes'),
 d('Boquerones en vinagre', 'Boquerones en vinagre', '', 33, 'Anșoa marinate în oțet, usturoi și pătrunjel, cu sos de roșii proaspete și pâine prăjită.', 'Anchovies marinated in vinegar, garlic and parsley, with fresh tomato sauce and toasted bread.', 'pes glu'),
 d('Pate de anșoa', 'Anchovy pâté', '150 g', 33, 'Pate fin cu anșoa, ton și cremă de brânză.', 'Smooth pâté of anchovy, tuna and cream cheese.', 'pes lac'),
 d('Ensalada del mar', 'Ensalada del mar', '250 g', 39, 'Somon afumat, ton, crab, puțină ceapă și sos fin de maioneză, cu pâinea noastră de casă.', 'Smoked salmon, tuna, crab, a little onion and a light mayonnaise, with our homemade bread.', 'pes cru glu ou lac nuc'),
 d('Tapa de solomillo con foie', 'Tapa de solomillo con foie', '120 g', 28, 'Mușchi de vită, foie gras, dulceață de pere cu muguri de pin, pe pâine brioșă.', 'Beef fillet, foie gras, pear jam with pine nuts, on brioche.', 'glu nuc'),
 d('Momițe de vițel pe jar', 'Charcoal-grilled veal sweetbreads', '170 g', 39, 'Terminate la tigaie cu salsa verde și usturoi, stropite cu lămâie coaptă pe jar.', 'Finished in the pan with salsa verde and garlic, with charred lemon.', ''),
 d('Torreznos', 'Torreznos', '150 g', 39, 'Piept de porc crocant, ardei Padrón, sos dulce-acrișor.', 'Crispy pork belly, Padrón peppers, sweet and sour sauce.', 'nuc'),
 d('Empanadas · 2 buc.', 'Empanadas · 2 pcs', '160 g', 33, 'Plăcințele cu carne de vită, ou fiert și măsline, în aluat făcut de noi. Cu salsa criolla.', 'Pastries of beef, boiled egg and olives in our own dough. With salsa criolla.', 'glu ou'),
 d('Crochete cu caracatiță și chorizo · 5 buc.', 'Octopus and chorizo croquettes · 5 pcs', '250 g', 35, 'Cremoase în interior, crocante la exterior, cu alioli.', 'Creamy inside, crisp outside, with alioli.', 'glu mol lac ou'),
 d('Crochete cu hribi, parmezan și trufe · 5 buc.', 'Porcini, parmesan and truffle croquettes · 5 pcs', '250 g', 28, 'Cu hribi, ghebe și parmezan.', 'With porcini, honey mushrooms and parmesan.', 'veg glu ou lac nuc'),
])

# ----------------------------------------------------------------------------- SALATE
sec('salate', 'Proaspăt', 'Fresh', 'Salate', 'Salads', 'Cu ardei kapia copți de noi, rucola, spanac și ulei de măsline extravirgin.', 'With peppers we roast ourselves, rocket, spinach and extra-virgin olive oil.', [
 d('Salată cu brânză de capră și jamón crocant', 'Goat cheese and crispy jamón salad', '350 g', 57, 'Medalion gratinat de brânză de capră, jamón crocant, ardei copți, nuci, stafide, dulceață de ceapă, balsamic cu trufe.', 'Grilled goat cheese, crispy jamón, roasted peppers, walnuts, raisins, onion jam, truffle balsamic.', 'lac nuc'),
 d('Ensalada fresca cu creveți', 'Ensalada fresca with prawns', '', 60, 'Creveți la tigaie, ardei copți, avocado, cherry, rucola, spanac, ceapă roșie, susan.', 'Pan-fried prawns, roasted peppers, avocado, cherry tomatoes, rocket, spinach, red onion, sesame.', 'cru nuc'),
 d('Ensalada fresca', 'Ensalada fresca', '', 42, 'Rucola, spanac, ardei copți, cherry, ceapă roșie, avocado, susan.', 'Rocket, spinach, roasted peppers, cherry tomatoes, red onion, avocado, sesame.', 'veg nuc'),
])

# ----------------------------------------------------------------------------- FELURI PRINCIPALE
sec('principale', 'Carne și pește', 'Meat and fish', 'Feluri principale', 'Mains', 'Pe jar sau gătite lent. Porții pentru o persoană.', 'Charcoal-grilled or slow-cooked. Single portions.', [
 d('Secreto ibérico cu cartofi aurii', 'Secreto ibérico with golden potatoes', '400 g', 57, 'Mușchi de porc intercostal, fâșii pe jar, cartofi proaspeți și salsa chimichurri.', 'Iberian pork secreto, strips over charcoal, fresh potatoes and chimichurri.', '', True),
 d('Secreto ibérico cu salată', 'Secreto ibérico with salad', '450 g', 66, 'Același secreto, cu salată de rucola, spanac și ardei copți, salsa verde și chimichurri.', 'The same secreto, with rocket, spinach and roasted pepper salad, salsa verde and chimichurri.', ''),
 d('Mușchi de vită pe jar cu cremă de cartofi și trufe', 'Charcoal-grilled beef fillet with truffle potato cream', '350 g', 114, 'Trufe răzuite, ulei cu trufe, sos chimichurri.', 'Shaved truffle, truffle oil, chimichurri.', 'lac'),
 d('Rabo de toro', 'Rabo de toro', '450 g', 80, 'Coadă de vită gătită lent în vin roșu, cu legume, dafin și rozmarin. Piure de cartofi cu unt.', 'Oxtail slow-cooked in red wine with vegetables, bay and rosemary. Buttered potato purée.', 'glu sul lac', True),
 d('Obrăjori de porc cu cremă de cartofi, morcovi și trufe', 'Pork cheeks with potato, carrot and truffle cream', '400 g', 69, 'Gătiți lent în vin roșu, legume, cherry și busuioc. Nuci coapte.', 'Slow-cooked in red wine, vegetables, cherry tomatoes and basil. Toasted walnuts.', 'glu nuc lac'),
 d('Coaste de porc, cremă de cartofi cu chives', 'Pork ribs, chive potato cream', '300 g', 60, 'Muștar Dijon, sirop de arțar, usturoi, unt, piparras.', 'Dijon mustard, maple syrup, garlic, butter, piparras.', 'lac'),
 d('Pepito de ternera', 'Pepito de ternera', '350 g', 57, 'Pâine de casă prăjită, felii de mușchi de vită pe grătar, ardei copți, rucola, chimichurri ușor picant.', 'Toasted homemade bread, slices of grilled beef, roasted peppers, rocket, mildly spicy chimichurri.', 'glu', True),
 d('Huevos rotos con jamón ibérico y trufas', 'Huevos rotos con jamón ibérico y trufas', '400 g', 60, 'Cartofi aurii, jamón ibérico, două ouă ochi, trufe răzuite, sare Maldon.', 'Golden potatoes, jamón ibérico, two fried eggs, shaved truffle, Maldon salt.', 'ou'),
 d('Atún a la brasa con ensalada tropical', 'Atún a la brasa con ensalada tropical', '400 g', 98, 'Steak de ton roșu pe jar, salată de avocado și mango, infuzie de busuioc, crumble cu lămâie și usturoi.', 'Charcoal-grilled red tuna steak, avocado and mango salad, basil infusion, lemon and garlic crumble.', 'pes nuc'),
 d('Dorada pe jar cu legume coapte', 'Charcoal-grilled sea bream with roasted vegetables', '450 g', 60, 'Dorada întreagă, desfăcută, cu salsa verde și sare neagră. Broccoli, conopidă, ardei.', 'Whole butterflied sea bream with salsa verde and black salt. Broccoli, cauliflower, peppers.', 'pes'),
 d('Ardei piquillo umpluți cu creveți și cod', 'Piquillo peppers stuffed with prawns and cod', '400 g', 71, 'Cu praz și bechamel, gratinați în sos de ardei copți.', 'With leek and béchamel, baked in roasted-pepper sauce.', 'cru pes glu lac'),
 d('Flamenco burger cu blue cheese', 'Flamenco burger with blue cheese', '480 g', 51, 'Vită, jamón serrano crocant, blue cheese, rucola, dulceață de ceapă. Cartofi aurii, alioli și bravas.', 'Beef, crispy jamón serrano, blue cheese, rocket, onion jam. Golden potatoes, alioli and bravas.', 'glu lac ou nuc'),
 d('Flamenco burger', 'Flamenco burger', '480 g', 46, 'Vită, jamón serrano crocant, cheddar, rucola, dulceață de ceapă. Cartofi aurii, alioli și bravas.', 'Beef, crispy jamón serrano, cheddar, rocket, onion jam. Golden potatoes, alioli and bravas.', 'glu lac ou nuc'),
 d('Ibérico burger', 'Ibérico burger', '480 g', 46, 'Pulled pork, sos de muștar și castraveți murați, dulceață de ceapă, cheddar, roșie, rucola. Cartofi aurii și alioli.', 'Pulled pork, mustard and pickle sauce, onion jam, cheddar, tomato, rocket. Golden potatoes and alioli.', 'glu lac ou nuc'),
])

# ----------------------------------------------------------------------------- PAELLA
sec('paella', 'Orez din Valencia', 'Rice from Valencia', 'Paella și orez', 'Paella and rice', 'Paella pentru două persoane, cu „sofrito” gătit de noi din legume proaspete, pimentón și șofran. Se face la comandă; între timp, tapas.', 'Paella for two, with our own sofrito of fresh vegetables, pimentón and saffron. Cooked to order; tapas in the meantime.', [
 d('Paella cu fructe de mare, creveți roșii sălbatici și pește · 2 pers.', 'Seafood paella with wild red prawns and fish · for two', '800 g', 134, 'Creveți roșii sălbatici, creveți, baby calamari, dorada, supă de pește făcută de noi.', 'Wild red prawns, prawns, baby squid, sea bream, our own fish stock.', 'cru pes mol', True),
 d('Paella neagră cu creveți și calamari · 2 pers.', 'Black paella with prawns and squid · for two', '800 g', 114, 'Orez gătit cu cerneală de sepie în fumé de pește.', 'Rice cooked with cuttlefish ink in fish stock.', 'cru pes mol'),
 d('Paella cu pui, iepure și chorizo · 2 pers.', 'Chicken, rabbit and chorizo paella · for two', '800 g', 96, 'Rețeta „de la țară”: pui, iepure, chorizo, fumé de pui făcut în casă.', 'The country recipe: chicken, rabbit, chorizo, homemade chicken stock.', '', True),
 d('Paella cu secreto ibérico, chorizo și ardei copți · 2 pers.', 'Secreto ibérico, chorizo and roasted pepper paella · for two', '800 g', 106, 'Secreto ibérico, un mușchi de porc de sub coaste, cu chorizo și ardei copți.', 'Secreto ibérico, a special cut from under the ribs, with chorizo and roasted peppers.', ''),
 d('Paella cu mușchi de vită, hribi și trufe · 2 pers.', 'Beef, porcini and truffle paella · for two', '800 g', 156, 'Felii de mușchi de vită pe jar, hribi, trufe rase.', 'Slices of charcoal-grilled beef fillet, porcini, shaved truffle.', ''),
 d('Paella cu legume și hribi · 2 pers.', 'Vegetable and porcini paella · for two', '800 g', 96, 'Legume coapte, hribi, ardei kapia copți, fumé din legume făcut în casă.', 'Roasted vegetables, porcini, roasted peppers, homemade vegetable stock.', 'veg'),
 d('Orez cremos cu creveți și caracatiță', 'Creamy rice with prawns and octopus', '400 g', 69, 'Orez arborio, sofrito, unt, boia afumată, șofran, supă de pește. Pentru o persoană.', 'Arborio rice, sofrito, butter, smoked paprika, saffron, fish stock. For one.', 'cru mol pes lac'),
])

# ----------------------------------------------------------------------------- DESERT
sec('desert', 'Sobremesa', 'Sobremesa', 'Desert', 'Dessert', 'Partea de masă care nu se grăbește.', 'The part of the meal nobody hurries.', [
 d('Crema catalana', 'Crema catalana', '150 g', 30, 'Lapte, ouă, vanilie, coajă de portocală și de lămâie, zahăr ars deasupra.', 'Milk, eggs, vanilla, orange and lemon zest, burnt sugar on top.', 'veg ou lac', True),
 d('Tartă de brânză San Sebastián', 'San Sebastián cheesecake', '130 g', 33, 'După rețeta clasică din orașul San Sebastián.', 'The classic recipe from San Sebastián.', 'veg ou lac glu', True),
 d('Tartă Valentina cu ciocolată belgiană', 'Valentina Belgian chocolate tart', '130 g', 33, 'Blat de biscuiți, mousse și ganache de ciocolată belgiană, fructe roșii proaspete.', 'Biscuit base, Belgian chocolate mousse and ganache, fresh red berries.', 'veg glu lac'),
 d('Cremă de arroz con leche', 'Arroz con leche', '150 g', 30, 'Orez fiert în frișcă și lapte, cu sos dulce-acrișor de vișine și coacăze.', 'Rice cooked in cream and milk, with a sweet-sour sour-cherry and currant sauce.', 'veg lac'),
 d('Piña asada', 'Piña asada', '250 g', 30, 'Ananas caramelizat pe grătar cu înghețată de vanilie (sau ciocolată belgiană, caramel sărat, mango, cocos).', 'Grilled caramelised pineapple with vanilla ice cream (or Belgian chocolate, salted caramel, mango, coconut).', 'veg lac'),
 d('Înghețată · 2 cupe', 'Ice cream · 2 scoops', '140 g', 26, 'Vanilie, ciocolată, fistic, mango, fructul pasiunii sau zmeură.', 'Vanilla, chocolate, pistachio, mango, passion fruit or raspberry.', 'veg lac nuc'),
])

# ----------------------------------------------------------------------------- SANGRÍA
sec('sangria', 'Bar', 'Bar', 'Sangría', 'Sangría', 'La pahar sau la carafă de un litru. „Sangría es alegría, olé!”', 'By the glass or by the one-litre jug. "Sangría es alegría, olé!"', [
 d('Sangria clasică cu vin roșu', 'Classic red-wine sangria', '400 ml · 1 l', '30 · 60', 'Vin roșu, suc de lămâie, portocale și lămâi. Andalucía într-un pahar.', 'Red wine, lemon juice, oranges and lemons. Andalusia in a glass.', 'veg sul', True),
 d('White sangria', 'White sangria', '380 ml · 1 l', '30 · 60', 'Vin alb sec, portocale, lămâi, zmeură, piersici, Sprite. Foarte aromată și efervescentă.', 'Dry white wine, oranges, lemons, raspberries, peaches, Sprite. Fragrant and fizzy.', 'veg sul'),
 d('Sangria cu cava', 'Cava sangria', '380 ml · 1 l', '35 · 69', 'Cava brut, portocale, lămâi, zmeură, afine, Sprite și „ingredientul nostru magic: el amor”.', 'Brut cava, oranges, lemons, raspberries, blueberries, Sprite and "our magic ingredient: el amor".', 'veg sul', True),
 d('Sangria alegría', 'Sangria alegría', '380 ml · 1 l', '33 · 66', 'Gin de căpșuni, vin roșu, suc de lămâie și portocale, căpșuni.', 'Strawberry gin, red wine, lemon and orange juice, strawberries.', 'veg sul'),
 d('Sangria cu cava fără alcool', 'Alcohol-free cava sangria', '380 ml · 1 l', '33 · 67', 'Aceeași rețetă, cu cava fără alcool.', 'Same recipe, with alcohol-free cava.', 'veg'),
])

# ----------------------------------------------------------------------------- VINURI
sec('vinuri', 'La sticlă', 'By the bottle', 'Vinuri', 'Wines', 'Spania în primul rând: Rioja, Ribera del Duero, Rías Baixas, Jumilla, cava. Plus un argentinian și două românești.', 'Spain first: Rioja, Ribera del Duero, Rías Baixas, Jumilla, cava. Plus one Argentinian and two Romanians.', [
 d('Cava Hola Barcelona brut', 'Hola Barcelona brut cava', '750 ml', 130, 'Cava alb brut, metoda tradițională.', 'White brut cava, traditional method.', 'veg sul'),
 d('Cava Hola Barcelona fără alcool', 'Hola Barcelona alcohol-free cava', '750 ml', 130, '', '', 'veg sul'),
 d('Cava Masia brut organic', 'Masia organic brut cava', '750 ml', 140, 'Cava brut, metoda tradițională, struguri ecologici.', 'Brut cava, traditional method, organic grapes.', 'veg sul'),
 d('Cava Parxet Cuvée 21 brut organic 2024', 'Parxet Cuvée 21 organic brut cava 2024', '750 ml', 150, 'Macabeo, xarel·lo și parellada. Măr verde, pară, citrice, salcâm.', 'Macabeo, xarel·lo and parellada. Green apple, pear, citrus, acacia.', 'veg sul'),
 d('Cava Anna de Codorníu Blanc de Blancs brut', 'Anna de Codorníu Blanc de Blancs brut cava', '750 ml', 156, 'Peste 15 luni în sticlă: pâine prăjită, brioche, citrice, bule fine.', 'Over 15 months in bottle: toast, brioche, citrus, fine bubbles.', 'veg sul'),
 d('Albariño El Pez Volador · alb sec', 'Albariño El Pez Volador · dry white', '750 ml', 140, 'D.O. Rías Baixas. Piersică, caisă, citrice, fenicul; mineral și proaspăt.', 'D.O. Rías Baixas. Peach, apricot, citrus, fennel; mineral and fresh.', 'veg sul'),
 d('Gran Bazán Etiqueta Ámbar · alb sec', 'Gran Bazán Etiqueta Ámbar · dry white', '750 ml', 161, 'Albariño de pe viță de 35 de ani, Rías Baixas. Floral, citric, cu note saline.', 'Albariño from 35-year-old vines, Rías Baixas. Floral, citrus, saline notes.', 'veg sul'),
 d('Habla de Ti · alb', 'Habla de Ti · white', '750 ml', 138, '100 % Sauvignon Blanc, ecologic, Bodegas Habla. Mango, sparanghel, fructe tropicale.', '100 % Sauvignon Blanc, organic, Bodegas Habla. Mango, asparagus, tropical fruit.', 'veg sul'),
 d('Volver Verdejo & Sauvignon Blanc · alb', 'Volver Verdejo & Sauvignon Blanc · white', '700 ml', 120, 'Fructe tropicale, citrice, flori; aciditate vibrantă.', 'Tropical fruit, citrus, flowers; vibrant acidity.', 'veg sul'),
 d('Azumbre Verdejo 2024 · alb', 'Azumbre Verdejo 2024 · white', '700 ml', 125, 'Caise, piersici, mango, notă de fenicul.', 'Apricot, peach, mango, a note of fennel.', 'veg sul'),
 d('Pincel Blanc de Noir · alb', 'Pincel Blanc de Noir · white', '700 ml', 130, 'Monastrell presat ușor, fermentat la rece. Delicat și fructat.', 'Gently pressed Monastrell, cold-fermented. Delicate and fruity.', 'veg sul'),
 d('Tarima Monastrell · rosé', 'Tarima Monastrell · rosé', '750 ml', 125, 'Căpșuni, zmeură, flori; proaspăt și răcoritor.', 'Strawberry, raspberry, flowers; fresh and refreshing.', 'veg sul'),
 d('Luzón · rosé', 'Luzón · rosé', '750 ml', 125, 'D.O.P. Jumilla, 100 % Monastrell. Cireșe, vișine, final dulce-răcoritor.', 'D.O.P. Jumilla, 100 % Monastrell. Cherries, sour cherries, a sweet refreshing finish.', 'veg sul'),
 d('Rioja Viña Pomal Crianza 2022 · roșu sec', 'Rioja Viña Pomal Crianza 2022 · dry red', '750 ml', 135, '100 % Tempranillo, 12 luni în stejar american. Rioja clasică, catifelată.', '100 % Tempranillo, 12 months in American oak. Classic, velvety Rioja.', 'veg sul'),
 d('Rioja Finca la Montesa 2021 · roșu', 'Rioja Finca la Montesa 2021 · red', '750 ml', 147, 'Ecologic, cules manual. Cireșe, zmeură, violete, coajă de portocală.', 'Organic, hand-picked. Cherry, raspberry, violet, orange peel.', 'veg sul'),
 d('Rioja Viña Pomal 120 Ediție limitată 2019 · roșu', 'Rioja Viña Pomal 120 Limited Edition 2019 · red', '750 ml', 375, 'Cupaj tempranillo, garnacha, maturana tinta, graciano. Fructe negre, violete, fundal mineral.', 'Tempranillo, garnacha, maturana tinta and graciano blend. Black fruit, violets, mineral backdrop.', 'veg sul'),
 d('Protos Ribera del Duero 2023 · roșu sec', 'Protos Ribera del Duero 2023 · dry red', '750 ml', 143, '100 % Tempranillo. Fructat, catifelat, taninuri moi.', '100 % Tempranillo. Fruity, velvety, soft tannins.', 'veg sul'),
 d('Emilio Moro Ribera del Duero 2019 · roșu sec', 'Emilio Moro Ribera del Duero 2019 · dry red', '750 ml', 190, 'Viță veche, 12 luni în stejar. Coacăze coapte, vanilie, final lung.', 'Old vines, 12 months in oak. Ripe blackcurrant, vanilla, long finish.', 'veg sul'),
 d('Malleolus 2022 Ribera del Duero · roșu sec', 'Malleolus 2022 Ribera del Duero · dry red', '700 ml', 422, '100 % Tempranillo, 18 luni în stejar din Allier. Zmeură, piper alb, cafea, ciocolată neagră.', '100 % Tempranillo, 18 months in Allier oak. Raspberry, white pepper, coffee, dark chocolate.', 'veg sul'),
 d('Áster Finca El Otero 2018 Ribera del Duero · roșu sec', 'Áster Finca El Otero 2018 Ribera del Duero · dry red', '700 ml', 510, 'La Rioja Alta, 100 % Tempranillo, 16 luni în stejar franțuzesc. Vinul de elită al casei.', 'La Rioja Alta, 100 % Tempranillo, 16 months in French oak. The house\'s top bottle.', 'veg sul'),
 d('Habla del Silencio 2021 · roșu sec', 'Habla del Silencio 2021 · dry red', '750 ml', 145, 'Syrah, Cabernet Sauvignon, Tempranillo; 8 luni în baric. Cireșe, mure, mentă, rozmarin.', 'Syrah, Cabernet Sauvignon, Tempranillo; 8 months in barrique. Cherry, blackberry, mint, rosemary.', 'veg sul'),
 d('Pétalos 2022 Bierzo · roșu sec', 'Pétalos 2022 Bierzo · dry red', '750 ml', 174, 'Mencía de pe viță veche. Petale de flori roșii, violete, hibiscus.', 'Old-vine Mencía. Red flower petals, violets, hibiscus.', 'veg sul'),
 d('El Enemigo Bonarda 2022, Mendoza · roșu sec', 'El Enemigo Bonarda 2022, Mendoza · dry red', '700 ml', 224, 'Argentina, Alejandro Vigil. Mure, prune, cacao, condimente; catifelat.', 'Argentina, Alejandro Vigil. Blackberry, plum, cocoa, spice; velvety.', 'veg sul'),
 d('1000 Chipuri cupaj 2025, Dealu Mare · alb sec', '1000 Chipuri blend 2025, Dealu Mare · dry white', '750 ml', 125, 'Citrice, fructe galbene, mere verzi, flori albe.', 'Citrus, yellow fruit, green apple, white flowers.', 'veg sul'),
 d('1000 Chipuri Cabernet Sauvignon & Cabernet Franc · roșu sec', '1000 Chipuri Cabernet Sauvignon & Cabernet Franc · dry red', '750 ml', 145, '', '', 'veg sul'),
])

# ----------------------------------------------------------------------------- COCKTAILURI
sec('cocktailuri', 'Bar', 'Bar', 'Cocktailuri', 'Cocktails', 'Gin tonic cu Flor de Sevilla, mojito „Danielito” și versiuni „treze”, fără alcool, pentru cine conduce.', 'Gin and tonic with Flor de Sevilla, the "Danielito" mojito and "sober" alcohol-free versions for the driver.', [
 d('Gin & Tonic Tanqueray Flor de Sevilla', 'Gin & Tonic Tanqueray Flor de Sevilla', '310 ml', 33, 'Ginul cu portocale de Sevilla, 250 ml Fever-Tree, felii de portocală.', 'The Seville-orange gin, 250 ml Fever-Tree, orange slices.', 'veg', True),
 d('Gin & Tonic Malfy Rosa, Fentimans', 'Gin & Tonic Malfy Rosa, Fentimans', '310 ml', 33, 'Gin italian cu grepfrut roz sicilian, felii de grepfrut.', 'Italian gin with Sicilian pink grapefruit, grapefruit slices.', 'veg'),
 d('Gin & Tonic Malfy Originale, Fentimans', 'Gin & Tonic Malfy Originale, Fentimans', '310 ml', 30, 'Dry gin de pe Coasta Amalfi: ienupăr, coriandru, anason.', 'Dry gin from the Amalfi coast: juniper, coriander, anise.', 'veg'),
 d('Gin & Tonic Tanqueray 0.0 · fără alcool', 'Gin & Tonic Tanqueray 0.0 · alcohol-free', '310 ml', 30, '60 ml Tanqueray 0.0, lime, 250 ml Fever-Tree.', '60 ml Tanqueray 0.0, lime, 250 ml Fever-Tree.', 'veg'),
 d('Mojito Danielito', 'Mojito Danielito', '290 ml', 30, 'Rom alb, Sprite, lime, mentă proaspătă, zahăr brun, gheață pisată.', 'White rum, Sprite, lime, fresh mint, brown sugar, crushed ice.', 'veg', True),
 d('Mojito cu zmeură și afine', 'Raspberry and blueberry mojito', '290 ml', 34, 'Rom alb, sirop de zmeură făcut în casă, lime, mentă, afine proaspete.', 'White rum, homemade raspberry syrup, lime, mint, fresh blueberries.', 'veg'),
 d('Mojito treaz · fără alcool', 'Sober mojito · alcohol-free', '290 ml', 28, 'Mentă proaspătă, lime, Sprite, gheață.', 'Fresh mint, lime, Sprite, ice.', 'veg'),
 d('Mojito treaz cu zmeură și afine · fără alcool', 'Sober raspberry and blueberry mojito · alcohol-free', '290 ml', 29, 'Sirop de zmeură de casă, lime, mentă, afine, Sprite.', 'Homemade raspberry syrup, lime, mint, blueberries, Sprite.', 'veg'),
 d('Hugo', 'Hugo', '250 ml', 33, 'Sirop de soc, mentă, lime, cava și apă minerală.', 'Elderflower syrup, mint, lime, cava and sparkling water.', 'veg sul'),
 d('Hugo treaz · fără alcool', 'Sober Hugo · alcohol-free', '250 ml', 30, 'Sirop de soc, mentă, Sprite, lime.', 'Elderflower syrup, mint, Sprite, lime.', 'veg'),
 d('Campari Spritz', 'Campari Spritz', '300 ml', 33, 'Campari, cava, apă minerală, felie de portocală.', 'Campari, cava, sparkling water, orange slice.', 'veg sul'),
 d('Petroni Aperitivo Spritz', 'Petroni Aperitivo Spritz', '300 ml', 33, 'Aperitivo spaniol Petroni, cava, apă minerală, portocală.', 'Spanish Petroni aperitivo, cava, sparkling water, orange.', 'veg sul'),
 d('Ramazzotti Spritz · fără alcool', 'Ramazzotti Spritz · alcohol-free', '300 ml', 30, 'Aperitivo Ramazzotti fără alcool, cava fără alcool, apă minerală, portocală.', 'Alcohol-free Ramazzotti aperitivo, alcohol-free cava, sparkling water, orange.', 'veg'),
 d('Vermut Petroni roșu sau alb', 'Petroni vermouth, red or white', '100 ml', 30, 'Vermut spaniol, gheață, lămâie sau portocală.', 'Spanish vermouth, ice, lemon or orange.', 'veg sul'),
 d('Negroni', 'Negroni', '300 ml', 35, 'Gin Malfy, vermut roșu 1757 di Torino, Campari, cub de gheață XXL.', 'Malfy gin, 1757 di Torino red vermouth, Campari, XXL ice cube.', 'veg'),
 d('Espresso Martini', 'Espresso Martini', '300 ml', 33, 'Espresso, Kahlúa, vodka, boabe de cafea.', 'Espresso, Kahlúa, vodka, coffee beans.', 'veg'),
 d('Paloma', 'Paloma', '150 ml', 30, 'Tequila Olmeca Altos Plata, fresh de lămâie, grapefruit soda.', 'Olmeca Altos Plata tequila, fresh lemon, grapefruit soda.', 'veg'),
 d('Magic Margarita cu zmeură', 'Magic raspberry Margarita', '150 ml', 30, 'Tequila, triplu sec, suc de lămâie proaspăt, piure de zmeură de casă.', 'Tequila, triple sec, fresh lemon juice, homemade raspberry purée.', 'veg'),
 d('El Presidente', 'El Presidente', '', 33, 'Tequila, triplu sec, suc de lămâie, sirop de zahăr, lime și tajín pe marginea paharului.', 'Tequila, triple sec, lemon juice, sugar syrup, lime and tajín on the rim.', 'veg'),
 d('Cosmopolitan', 'Cosmopolitan', '160 ml', 30, 'Vodka, triplu sec, suc de portocale, lime.', 'Vodka, triple sec, orange juice, lime.', 'veg'),
 d('Cuba Libre Havana Especial', 'Cuba Libre Havana Especial', '290 ml', 31, 'Rom Havana Club Especial, Pepsi, lămâie.', 'Havana Club Especial rum, Pepsi, lemon.', 'veg'),
 d('Long Island', 'Long Island', '200 ml', 33, 'Tequila, rom alb, vodka, gin, triplu sec, Pepsi, lime.', 'Tequila, white rum, vodka, gin, triple sec, Pepsi, lime.', 'veg'),
])

# ----------------------------------------------------------------------------- LIMONADĂ
sec('limonada', 'Fără alcool', 'Alcohol-free', 'Limonadă', 'Lemonade', 'Lămâi proaspăt stoarse și apă purificată prin osmoză inversă. La pahar sau la carafă.', 'Freshly squeezed lemons and reverse-osmosis water. By the glass or by the jug.', [
 d('Limonadă cu mentă și miere', 'Mint and honey lemonade', '400 ml · 1 l', '20 · 41', '', '', 'veg'),
 d('Limonadă cu zmeură, afine și mentă', 'Raspberry, blueberry and mint lemonade', '400 ml · 1 l', '24 · 48', 'Cu piure de zmeură făcut în casă și miere de albine.', 'With homemade raspberry purée and honey.', 'veg'),
 d('Limonadă cu mango și ananas', 'Mango and pineapple lemonade', '400 ml · 1 l', '24 · 48', 'Piure de mango, bucăți de ananas, mentă.', 'Mango purée, pineapple pieces, mint.', 'veg'),
])

# ----------------------------------------------------------------------------- CAFEA ȘI CEAI
sec('cafea', 'Sobremesa', 'Sobremesa', 'Cafea și ceai', 'Coffee and tea', 'Espresso, cortado, café bombón cu lapte condensat, ca în Spania.', 'Espresso, cortado, café bombón with condensed milk, the Spanish way.', [
 d('Espresso', 'Espresso', '30 ml', 10, '', '', 'veg'),
 d('Espresso dublu', 'Double espresso', '60 ml', 13, '', '', 'veg'),
 d('Café cortado', 'Café cortado', '50 ml', 12, 'Espresso lung, cremă de lapte.', 'Long espresso, milk foam.', 'veg lac'),
 d('Café bombón', 'Café bombón', '60 ml', 15, 'Espresso și lapte condensat.', 'Espresso and condensed milk.', 'veg lac'),
 d('Cappuccino', 'Cappuccino', '200 ml', 16, '', '', 'veg lac'),
 d('Café latte', 'Café latte', '200 ml', 17, '', '', 'veg lac'),
 d('Iced latte', 'Iced latte', '200 ml', 18, '', '', 'veg lac'),
 d('Café al Baileys', 'Café al Baileys', '80 ml', 18, 'Espresso, cremă de whisky, cremă de lapte opțional.', 'Espresso, Irish cream, milk foam optional.', 'veg lac'),
 d('Ciocolată caldă clasică neagră', 'Classic dark hot chocolate', '200 ml', 17, 'Cremoasă; se poate prepara și cu apă.', 'Creamy; can be made with water.', 'veg lac'),
 d('Ceai verde Green Diamond', 'Green Diamond green tea', '250 ml', 17, 'Cu ananas, mango, petale de portocal și trandafir.', 'With pineapple, mango, orange blossom and rose petals.', 'veg'),
 d('Infuzie de mentă Nana Mint', 'Nana Mint infusion', '250 ml', 17, 'Mentă creață, caldă sau rece.', 'Spearmint, hot or cold.', 'veg'),
 d('Infuzie de fructe roșii Forest Berry', 'Forest Berry infusion', '250 ml', 17, 'Măceșe, mere, hibiscus, zmeură, coacăze, soc.', 'Rosehip, apple, hibiscus, raspberry, currant, elderberry.', 'veg'),
 d('Infuzie Mango Cocktail', 'Mango Cocktail infusion', '300 ml', 17, 'Măceșe, hibiscus, mango, mere, ananas, portocală, gălbenele.', 'Rosehip, hibiscus, mango, apple, pineapple, orange, marigold.', 'veg'),
 d('Infuzie de mușețel bio', 'Organic chamomile infusion', '300 ml', 18, '', '', 'veg'),
 d('Rooibos African Chai', 'Rooibos African Chai', '300 ml', 17, 'Fără cafeină: scorțișoară, cardamom, ghimbir, anason, cuișoare.', 'Caffeine-free: cinnamon, cardamom, ginger, anise, cloves.', 'veg'),
])

# ----------------------------------------------------------------------------- RĂCORITOARE
sec('racoritoare', 'Fără alcool', 'Alcohol-free', 'Răcoritoare', 'Soft drinks', '', '', [
 d('Apă plată Bucovina', 'Bucovina still water', '330 ml · 750 ml', '13 · 19', '', '', 'veg'),
 d('Apă carbogazoasă Bucovina', 'Bucovina sparkling water', '330 ml · 750 ml', '13 · 19', '', '', 'veg'),
 d('Suc de mere Fresco Jugo', 'Fresco Jugo apple juice', '330 ml', 16, 'Natural, fără zahăr adăugat.', 'Natural, no added sugar.', 'veg'),
 d('Suc de mere și rodii Fresco Jugo', 'Fresco Jugo apple and pomegranate juice', '330 ml', 16, 'Natural, fără zahăr adăugat.', 'Natural, no added sugar.', 'veg'),
 d('Coca-Cola', 'Coca-Cola', '250 ml', 13, '', '', 'veg'),
 d('Coca-Cola Zero', 'Coca-Cola Zero', '250 ml', 13, '', '', 'veg'),
 d('Schweppes', 'Schweppes', '250 ml', 13, '', '', 'veg'),
])

# ----------------------------------------------------------------------------- BERE
sec('bere', 'La sticlă și draught', 'Bottled and draught', 'Bere', 'Beer', 'Madrí Excepcional, lagerul spaniol, la draught și la sticlă.', 'Madrí Excepcional, the Spanish lager, on draught and in the bottle.', [
 d('Madrí Excepcional draught', 'Madrí Excepcional draught', '400 ml', 18, 'Lager spaniolă, 4,6 %, proaspătă și echilibrată.', 'Spanish lager, 4.6 %, fresh and balanced.', 'veg glu', True),
 d('Madrí Excepcional', 'Madrí Excepcional', '330 ml', 18, '', '', 'veg glu'),
 d('Corona', 'Corona', '330 ml', 22, '', '', 'veg glu'),
 d('Stella Artois', 'Stella Artois', '330 ml', 19, '', '', 'veg glu'),
 d('Stella Artois fără alcool', 'Stella Artois alcohol-free', '330 ml', 17, '', '', 'veg glu'),
 d('Hoegaarden', 'Hoegaarden', '330 ml', 24, '', '', 'veg glu'),
 d('Leffe Blond', 'Leffe Blond', '330 ml', 24, '', '', 'veg glu'),
 d('Leffe Brown', 'Leffe Brown', '330 ml', 25, '', '', 'veg glu'),
 d('Franziskaner Weissbier', 'Franziskaner Weissbier', '500 ml', 26, '', '', 'veg glu'),
 d('Beck\'s', 'Beck\'s', '330 ml', 17, '', '', 'veg glu'),
 d('Staropramen', 'Staropramen', '330 ml', 16, '', '', 'veg glu'),
 d('Fresh 0.0 lemon & orange', 'Fresh 0.0 lemon & orange', '330 ml', 15, 'Bere aromatizată, fără alcool.', 'Flavoured beer, alcohol-free.', 'veg glu'),
 d('Fresh 0.0 raspberry & lemon', 'Fresh 0.0 raspberry & lemon', '330 ml', 15, 'Bere aromatizată, fără alcool.', 'Flavoured beer, alcohol-free.', 'veg glu'),
])

# ----------------------------------------------------------------------------- SPIRTOASE
sec('spirtoase', 'Bar', 'Bar', 'Băuturi alcoolice', 'Spirits', '', '', [
 d('Brandy Torres 10 Reserva Imperial', 'Torres 10 Reserva Imperial brandy', '50 ml', 30, 'Distilat din xarel·lo, macabeo și parellada, învechit în stejar prin sistemul solera.', 'Distilled from xarel·lo, macabeo and parellada, oak-aged in the solera system.', 'veg'),
 d('Glenfiddich Single Malt 15 YO', 'Glenfiddich Single Malt 15 YO', '50 ml', 38, '', '', 'veg'),
 d('Jameson Irish Whiskey', 'Jameson Irish Whiskey', '50 ml', 24, '', '', 'veg'),
 d('Rom Bumbu Original', 'Bumbu Original rum', '50 ml', 28, '', '', 'veg'),
 d('Vodka Voronskaya Bio', 'Voronskaya Bio vodka', '50 ml', 24, '', '', 'veg'),
 d('Fernet-Branca', 'Fernet-Branca', '50 ml', 21, '', '', 'veg'),
])

out = {'_nota': 'Carta real, din meniul digital Poloniq al restaurantului (andalu.poloniq.ro/meniu), recolhida 2026-10-19. 169 produse, 14 secțiuni. Prețuri în lei, octombrie 2026. EN = tradução Pacheco Studios. Alergeni după textul meniului + evidentes; não é a lista legal completa.',
       'sections': [dict(id=i, kicker={'ro': kr, 'en': ke}, title={'ro': tr, 'en': te}, lead={'ro': lr, 'en': le}, dishes=ds) for i, kr, ke, tr, te, lr, le, ds in S]}
p = pathlib.Path(__file__).with_name('menu.json')
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(sum(len(s['dishes']) for s in out['sections']), 'produse em', len(out['sections']), 'secções →', p)
