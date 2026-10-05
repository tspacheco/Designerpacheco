#!/usr/bin/env python3
"""Monta index.html a partir de index.src.html:
- /*__FONTES__*/   -> _fontes/fontes.css (Tilt Warp, Onest e Share Tech Mono em base64, latin + latin-ext)
- __CONTA_KMH__ / __CONTA_RPM__ -> mostradores do tablier desenhados em SVG (marcas e números)
As fotografias ficam em media/*.webp (relativas, com onerror e desenho SVG por baixo)."""
import os, re, math
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def mostrador(maximo, passo, sub, rotulo, unidade, vermelho_de=None):
    # arco de 240 graus (de -210 a +30, 0 = 3h), centro 100,100
    a0, a1, out = 150, 390, []
    n = int(maximo / sub)
    for i in range(n + 1):
        v = i * sub
        ang = math.radians(a0 + (a1 - a0) * v / maximo)
        grande = abs(v / passo - round(v / passo)) < 1e-6
        r1, r2 = 86, (72 if grande else 79)
        cor = '#E5322D' if (vermelho_de is not None and v >= vermelho_de) else '#C9CED6'
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            100 + r1 * math.cos(ang), 100 + r1 * math.sin(ang), 100 + r2 * math.cos(ang), 100 + r2 * math.sin(ang), cor, '2.4' if grande else '1.2'))
        if grande:
            rt = 61
            out.append('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="central" class="g-num" fill="%s">%s</text>' % (
                100 + rt * math.cos(ang), 100 + rt * math.sin(ang), cor, int(v if maximo > 20 else v)))
    out.append('<text x="100" y="128" text-anchor="middle" class="g-uni">%s</text>' % unidade)
    out.append('<text x="100" y="146" text-anchor="middle" class="g-rot">%s</text>' % rotulo)
    return ''.join(out)

src = open('index.src.html', encoding='utf-8').read()
out = (src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
          .replace('__CONTA_KMH__', mostrador(240, 40, 10, 'SOS CAR', 'km/h'))
          .replace('__CONTA_RPM__', mostrador(7, 1, 0.5, 'OLHÃO', 'x1000 rpm', vermelho_de=6)))
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
