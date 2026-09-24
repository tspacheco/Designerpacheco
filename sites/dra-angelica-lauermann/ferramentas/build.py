#!/usr/bin/env python3
"""Monta index.html (ficheiro único): fontes base64 de _fontes/fontes.css e fotos de media/ embutidas como data URI.
Fotos que ainda não existem em media/ ficam como caminho relativo (o <img> tem onerror e há fundo de reserva)."""
import base64, os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open('index.src.html', encoding='utf-8').read()
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
faltam = []
def emb(m):
    nome = m.group(1)
    if not os.path.exists('media/' + nome): faltam.append(nome); return m.group(0)
    return 'src="data:image/jpeg;base64,%s"' % base64.b64encode(open('media/' + nome, 'rb').read()).decode()
out = re.sub(r'src="media/([\w-]+\.jpg)"', emb, out)
assert '/*__FONTES__*/' not in out
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · por enviar: ' + ', '.join(faltam) if faltam else ''))
