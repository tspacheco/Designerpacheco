#!/usr/bin/env python3
"""Reduz as faces grandes de _fontes/fontes.css (corre depois de fontes.py):
o latin-ext do Google traz ~1400 glifos (vietnamita, etc.); aqui fica só o Latin Extended-A
(ă â î ș ț e vizinhos) e o eixo wght é limitado ao intervalo que o site usa."""
import re, base64, io, os
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.varLib import instancer
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KEEP = set(range(0x20, 0x7F)) | set(range(0xA0, 0x180)) | {0x218, 0x219, 0x21A, 0x21B, 0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E, 0x2022, 0x2026, 0x2039, 0x203A, 0x20AC, 0x2122}
css = open('_fontes/fontes.css').read()
def faz(m):
    b = m.group(0)
    d = base64.b64decode(re.search(r'base64,([^)]+)\)', b).group(1))
    if len(d) < 60000: return b
    f = TTFont(io.BytesIO(d), lazy=False)
    w = re.search(r'font-weight: (\d+)(?: (\d+))?;', b)
    lo, hi = int(w.group(1)), int(w.group(2) or w.group(1))
    if 'fvar' in f:
        f = instancer.instantiateVariableFont(f, {'wght': (lo, hi) if lo != hi else lo})
        tmp = io.BytesIO(); f.save(tmp); tmp.seek(0); f = TTFont(tmp, lazy=False)
    cm = set(f.getBestCmap())
    o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['*']
    s = subset.Subsetter(o); s.populate(unicodes=sorted(cm & KEEP)); s.subset(f)
    out = io.BytesIO(); f.flavor = 'woff2'; f.save(out); nd = out.getvalue()
    print('%s %s: %d KB -> %d KB' % (re.search(r"font-family: '([^']+)'", b).group(1), w.group(0), len(d) // 1024, len(nd) // 1024))
    return b.replace(re.search(r'base64,([^)]+)\)', b).group(1), base64.b64encode(nd).decode())
css = re.sub(r'@font-face \{.*?\}', faz, css, flags=re.S)
open('_fontes/fontes.css', 'w').write(css)
print(round(os.path.getsize('_fontes/fontes.css') / 1024), 'KB')
