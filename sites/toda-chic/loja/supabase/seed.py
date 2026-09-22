#!/usr/bin/env python3
"""Gera seed.sql a partir de catalogo.json: as 72 peças e as cores/stock, para correr depois do schema.sql.
As fotos ficam como nomes relativos (media/produtos/…), servidos pelo próprio site."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cat = json.load(open('../../catalogo.json', encoding='utf-8'))
def nome(ref): return 'f%03d-c%d.jpg' % (ref['ficha'], ref['cel']) if isinstance(ref, dict) else 'f%03d.jpg' % ref
def q(v): return 'NULL' if v is None else "'" + str(v).replace("'", "''") + "'"
out = ['-- gerado por seed.py a partir de catalogo.json', 'begin;']
for i, c in enumerate(cat['categorias']):
    out.append("insert into categorias (id,nome,ordem,foto,provisorio) values (%s,%s,%d,%s,%s) on conflict (id) do nothing;" % (q(c['id']), q(c['nome']), i, q(c.get('foto')), 'true' if c.get('provisorio') else 'false'))
for i, e in enumerate(cat['estacoes']):
    out.append("insert into estacoes (id,nome,ordem,foto,titulo,frase) values (%s,%s,%d,%s,%s,%s) on conflict (id) do nothing;" % (q(e['id']), q(e['nome']), i, q(e.get('foto')), q(e.get('titulo')), q(e.get('frase'))))
for p in cat['pecas']:
    fotos = json.dumps([nome(f) for f in p.get('fotos', [])])
    out.append("insert into pecas (id,nome,cat,preco,preco_antigo,tam,tamanhos,descricao,estacao,nova,sub,fotos) values (%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s,%s,%s,%s::jsonb) on conflict (id) do nothing;" % (
        q(p['id']), q(p['nome']), q(p['cat']), p['preco'] if p.get('preco') is not None else 'NULL', p.get('precoAntigo', 'NULL') or 'NULL',
        q(p.get('tam') or 'Tamanho único'), q(json.dumps(p.get('tamanhos') or ['Único'], ensure_ascii=False)), q(p.get('desc', '')), q(p.get('estacao', 'meia')),
        'true' if p.get('nova') else 'false', q(p.get('sub')), q(fotos)))
    for i, c in enumerate(p['cores']):
        out.append("insert into cores (peca_id,posicao,nome,hex,foto,stock) values (%s,%d,%s,%s,%s,%d) on conflict do nothing;" % (
            q(p['id']), i, q(c['nome']), q(c.get('hex', '#CCCCCC')), q(nome(c['foto']) if c.get('foto') is not None else None), int(c.get('stock') or 0)))
out.append('commit;')
open('seed.sql', 'w', encoding='utf-8').write('\n'.join(out))
print('seed.sql:', len(cat['pecas']), 'peças')
