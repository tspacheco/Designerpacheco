#!/usr/bin/env python3
"""Monta index.html a partir de index.src.html:
- /*__FONTES__*/ -> _fontes/fontes.css (Petrona, Karla e Caveat em base64, latin + latin-ext)
- <!--__CARTA__--> -> carta gerada a partir das listas abaixo (transcritas das fotos da carta)
As fotografias ficam em media/*.webp (relativas, com onerror e fundo desenhado por baixo)."""
import os, re, html
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carta ilustrada (numerada, preços atualizados à mão na própria carta) -> preços firmes
ILUSTRADA = [
  ('esp', 'Espetadas e pedra', 'Chegam penduradas no suporte de madeira, a pingar para o prato.', [
    (44, 'Espetada de frango', '14,00'),
    (45, 'Espetada de camarão', '16,00'),
    (46, 'Espetada de porco preto', '14,00'),
    (47, 'Espetada de tamboril e camarão', '16,00'),
    (48, 'Espetada de novilho', '15,00'),
    (49, 'Naco na pedra', '19,50'),
  ]),
  ('brasa', 'Peixe e bacalhau', 'Na brasa ou no tacho, com o molho de cada um.', [
    (32, 'Bacalhau na brasa', '15,00'),
    (33, 'Sargo na brasa', '13,00'),
    (34, 'Bacalhau com natas', '12,00'),
    (35, 'Bacalhau à Brás', '13,00'),
    (36, 'Robalo em molho de limão', '15,00'),
    (37, 'Linguado em molho de laranja', '25,00'),
  ]),
]
# Carta afixada à porta -> preços com selo "a confirmar"
AFIXADA = [
  ('couvert', 'Couvert', [
    ('Pão (por pessoa)', '0,80'), ('Azeitonas', '0,80'), ('Manteiga', '0,40'),
    ('Paté de sardinha', '0,60'), ('Queijo', '0,60'), ('Sopa', '2,00')]),
  ('entradas', 'Entradas', [
    ('Amêijoas', '14,50'), ('Conquilhas', '13,00'), ('Camarão frito', '11,00'), ('Camarão grelhado', '20,00'),
    ('Presunto ibérico', '11,00'), ('Lulas fritas', '12,00'), ('Choco frito', '12,00'), ('Cavalas alimadas', '8,00'),
    ('Queijo de cabra', '3,00'), ('Queijo amanteigado', '2,50'), ('Chouriço assado', '11,00')]),
  ('saladas', 'Saladas e acompanhamentos', [
    ('Salada de frango', '8,00'), ('Salada de atum', '9,00'), ('Salada grega', '9,00'), ('Salada da casa', '10,00'),
    ('Salada de tomate', '3,00'), ('Salada montanheira', '3,00'), ('Salada mista', '3,00'), ('Pimentos assados', '4,50'),
    ('Legumes assados', '4,00'), ('Feijão preto', '3,00'), ('Batata frita', '3,00'), ('Arroz', '2,00')]),
  ('massas', 'Massas e frango', [
    ('Esparguete à bolonhesa', '9,00 · 12,00'), ('Lasanha à bolonhesa', '11,00'), ('Lasanha vegetariana', '11,00'),
    ('Frango no espeto com camarão', None), ('Frango panado', '8,00 · 11,00')]),
  ('grelha', 'Grelha (preços na carta da casa)', [
    ('Peixe grelhado do dia', None), ('Bife à pimenta', None), ('Bife da casa', None), ('Lombo de novilho', None),
    ('Ribeye', None), ('Picanha', None), ('Costeletas de borrego', None), ('Peito de pato', None),
    ('Porco e porco ibérico', None)]),
]
ADD = '<button type="button" class="poe" data-poe="%s" aria-label="Juntar %s à reserva" data-pousa><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></button>'

def carta():
    h = []
    for cid, tit, sub, itens in ILUSTRADA:
        h.append('<section class="ca-bloco ilus rv" id="c-%s" aria-labelledby="t-%s"><header><h3 id="t-%s">%s</h3><p>%s</p></header><ol class="etiqueta">' % (cid, cid, cid, tit, sub))
        for n, nome, p in itens:
            e = html.escape(nome)
            h.append('<li><span class="num">%d</span><span class="nm">%s</span><span class="pz">%s&nbsp;€</span>%s</li>' % (n, e, p, ADD % (e, e)))
        h.append('</ol></section>')
    h.append('<div class="ca-afix rv"><h3>Da carta afixada à porta <span class="selo">preços a confirmar</span></h3><p>O resto da carta, como está no quadro da entrada. Os preços podem ter mudado: confirme à mesa.</p></div>')
    for cid, tit, itens in AFIXADA:
        h.append('<section class="ca-bloco rv" id="c-%s" aria-labelledby="t-%s"><header><h3 id="t-%s">%s</h3></header><ul class="lista">' % (cid, cid, cid, tit))
        for nome, p in itens:
            e = html.escape(nome)
            pz = ('<span class="pz">%s&nbsp;€</span>' % p) if p else '<span class="pz sem">à mesa</span>'
            h.append('<li><span class="nm">%s</span><span class="pt" aria-hidden="true"></span>%s%s</li>' % (e, pz, ADD % (e, e)))
        h.append('</ul></section>')
    return '\n'.join(h)

src = open('index.src.html', encoding='utf-8').read()
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read()).replace('<!--__CARTA__-->', carta())
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
