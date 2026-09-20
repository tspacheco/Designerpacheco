"""Converte texto em curvas SVG (path) a partir de um TTF. Logotipo vetorial, sem dependencia de fontes."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

_cache = {}
def _load(p):
    if p not in _cache:
        f = TTFont(p)
        _cache[p] = (f, f.getGlyphSet(), f['head'].unitsPerEm, f.getBestCmap(), f['hmtx'])
    return _cache[p]

def texto_path(ttf, texto, tamanho=100, tracking=0.0, x=0.0, y=0.0):
    """Devolve (path_d, largura_total). tracking em em. y = baseline."""
    font, gs, upem, cmap, hmtx = _load(ttf)
    escala = tamanho / upem
    partes, cursor = [], 0.0
    kern = tracking * tamanho
    for ch in texto:
        gname = cmap.get(ord(ch))
        if gname is None:
            cursor += tamanho * 0.35 + kern
            continue
        pen = SVGPathPen(gs)
        gs[gname].draw(pen)
        d = pen.getCommands()
        if d:
            # y invertido: as fontes crescem para cima, o SVG para baixo
            partes.append('<g transform="translate(%.3f %.3f) scale(%.6f %.6f)">%s</g>'
                          % (x + cursor, y, escala, -escala, d))
        cursor += hmtx[gname][0] * escala + kern
    largura = cursor - kern if texto else 0.0
    return "".join(partes), largura

def texto_path_puro(ttf, texto, tamanho=100, tracking=0.0, x=0.0, y=0.0):
    """Igual mas devolve um unico atributo d, com as coordenadas ja transformadas."""
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Transform
    font, gs, upem, cmap, hmtx = _load(ttf)
    escala = tamanho / upem
    out, cursor = [], 0.0
    kern = tracking * tamanho
    for ch in texto:
        gname = cmap.get(ord(ch))
        if gname is None:
            cursor += tamanho * 0.35 + kern
            continue
        pen = SVGPathPen(gs)
        tp = TransformPen(pen, Transform(escala, 0, 0, -escala, x + cursor, y))
        gs[gname].draw(tp)
        d = pen.getCommands()
        if d:
            out.append(d)
        cursor += hmtx[gname][0] * escala + kern
    return " ".join(out), (cursor - kern if texto else 0.0)
