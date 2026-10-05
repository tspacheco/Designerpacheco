#!/usr/bin/env python3
"""Monta index.html a partir de index.src.html:
- /*__FONTES__*/   -> _fontes/fontes.css (Hepta Slab, Figtree e Reenie Beanie em base64, latin + latin-ext)
- <!--__CARTA__--> -> carta bilingue gerada da lista abaixo (transcrita do PDF "Menu 2023" da casa)
As fotografias ficam em media/*.webp (relativas, com onerror e fundo desenhado por baixo)."""
import os, re, html
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (id, PT, EN, [(pt, en, preço, id-curto)])  — preços da carta de 2023 (selo "a confirmar" no site)
CARTA = [
  ('couvert', 'Couvert', 'Couvert', [
    ('Pão, manteiga e azeitonas', 'Bread, butter & olives', '2,50'),
    ('Queijo curado', 'Cured cheese', '3,50'),
    ('Paté do dia', 'Homemade pâté of the day', '3,50')]),
  ('entradas', 'Entradas', 'Starters', [
    ('Gambas ao alhinho', 'Garlic prawns', '9,50'),
    ('Chamuças de legumes', 'Vegetable samosas', '7,50'),
    ('Carpaccio de bife com estragão, azeite e parmesão', 'Beef carpaccio with tarragon, olive oil and parmesan', '13,00')]),
  ('peixe', 'Peixe', 'Fish', [
    ('Atum braseado com sementes de sésamo e salada com balsâmico de limão', 'Seared tuna with sesame seeds, salad with lemon balsamic', '15,50'),
    ('Caril de camarão com arroz basmati', 'Prawn curry with basmati rice', '18,00'),
    ('Filete de robalo em cama de espinafres salteados com alho e azeite, e batatinhas', 'Sea bass fillet on spinach sautéed with garlic and olive oil, with baby potatoes', '16,50')]),
  ('carne', 'Carne', 'Meat', [
    ('Lombo na pedra com batata frita caseira e salada', 'Fillet steak on a hot stone, homemade fries and salad', '21,00'),
    ('Bife do lombo com molho de cogumelos ou pimenta, batata frita caseira e salada', 'Fillet steak with mushroom or pepper sauce, homemade fries and salad', '22,75'),
    ('Pernil de borrego no forno com molho de alecrim, batata gratinada e salada', 'Slow-roasted lamb shank with rosemary sauce, potato gratin and salad', '17,50'),
    ('Bochechas de porco estufadas em vinho tinto com puré de batata', 'Pork cheeks braised in red wine with mashed potato', '16,00'),
    ('Costeletas de borrego grelhadas com molho de menta, batata frita caseira e salada', 'Grilled lamb chops with mint sauce, homemade fries and salad', '18,50')]),
  ('vegetariano', 'Vegetariano', 'Vegetarian', [
    ('Linguini com bolonhesa de legumes', 'Linguini with vegetable bolognese', '12,75')]),
  ('acompanhamentos', 'Acompanhamentos (extra)', 'Side dishes (extra)', [
    ('Salada mista', 'Mixed salad', '4,00'), ('Legumes', 'Vegetables', '4,50'), ('Arroz', 'Rice', '3,00'),
    ('Batata frita', 'French fries', '3,50'), ('Batata-doce frita', 'Sweet potato fries', '4,00')]),
  ('sobremesas', 'Sobremesas', 'Desserts', [
    ('Sobremesas do dia', 'Desserts of the day', '3,75'), ('Bola de gelado', 'Scoop of ice cream', '2,50'), ('Fruta do dia', 'Fruit of the day', '3,00')]),
]

def curto(pt):
    # nome curto para a conta (até à primeira vírgula / " com " longo)
    c = re.split(r',| com batata| com molho| em cama| com sementes| e salada| com puré| estufadas| no forno', pt)[0]
    return c.strip()

CURTOS = {'Pão':('Pão, manteiga e azeitonas','Bread, butter & olives'),'Carpaccio de bife com estragão':('Carpaccio de bife','Beef carpaccio'),
  'Caril de camarão com arroz basmati':('Caril de camarão','Prawn curry'),'Filete de robalo':('Filete de robalo','Sea bass fillet'),
  'Bochechas de porco':('Bochechas de porco','Pork cheeks'),'Costeletas de borrego grelhadas':('Costeletas de borrego','Lamb chops'),
  'Linguini com bolonhesa de legumes':('Linguini de legumes','Vegetable linguini'),'Paté do dia':('Paté do dia','Pâté of the day')}
def carta():
    h = []
    for cid, pt, en, itens in CARTA:
        h.append('<section class="ca-sec rv" id="c-%s" aria-labelledby="t-%s"><h3 id="t-%s" data-en="%s">%s</h3><ul>' % (cid, cid, cid, html.escape(en), html.escape(pt)))
        for ipt, ien, p in itens:
            c = curto(ipt); ce = curto(ien) if len(ien) < 40 else ien.split(',')[0].split(' with ')[0]
            c, ce = CURTOS.get(c, (c, ce))
            h.append(
              '<li><button type="button" class="it" data-conta data-nome="%s" data-nome-en="%s" data-preco="%s" aria-pressed="false">'
              '<span class="it-nm"><span class="pt-nm">%s</span><span class="en-nm">%s</span></span>'
              '<span class="it-pz">%s&nbsp;€</span><span class="it-mais" aria-hidden="true"></span></button></li>'
              % (html.escape(c), html.escape(ce), p, html.escape(ipt), html.escape(ien), p))
        h.append('</ul></section>')
    return '\n'.join(h)

P = 'M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z'
def estrela(f, i):
    if f >= 1: return '<svg viewBox="0 0 24 24"><path d="%s" fill="#C8473B"/></svg>' % P
    return ('<svg viewBox="0 0 24 24"><defs><linearGradient id="e%d"><stop offset="%d%%" stop-color="#C8473B"/>'
            '<stop offset="%d%%" stop-color="#D6E5EE"/></linearGradient></defs><path d="%s" fill="url(#e%d)"/></svg>') % (i, f*100, f*100, P, i)
n = [0]
def est(_):
    n[0] += 1
    return ''.join(estrela(1 if k < 4 else .6, n[0]) for k in range(5))
src = re.sub('__ESTRELAS__', est, open('index.src.html', encoding='utf-8').read())
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read()).replace('<!--__CARTA__-->', carta())
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
