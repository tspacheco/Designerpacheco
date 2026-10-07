#!/usr/bin/env python3
"""Monta index.html (RO, botão EN) e pt.html (PT, para o Tomás rever) a partir de index.src.html.

No HTML de origem, cada texto traduzível escreve-se {{romeno|inglês|português}}:
- dentro de um atributo (aria-label, alt, title, placeholder, data-titulo, content…)
  -> o atributo fica com a língua da página e ganha data-ia="atributo:chave;…";
- sozinho dentro de um elemento -> o elemento ganha data-i="chave";
- no meio de outro texto -> fica embrulhado em <span data-i="chave">.
Todas as traduções vão para o dicionário JS /*__I18N__*/ = {chave:[ro,en,pt]}.
/*__FONTES__*/ -> _fontes/fontes.css (fontes em base64, latin + latin-ext).
As fotografias ficam em media/ (relativas, com onerror e fundo desenhado por baixo)."""
import html, json, os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = open('index.src.html', encoding='utf-8').read()
FONTES = open('_fontes/fontes.css', encoding='utf-8').read()
MARK = re.compile(r'\{\{(.*?)\}\}', re.S)


def partes(m):
    p = m.group(1).split('|')
    assert len(p) == 3, 'marcador sem 3 línguas: ' + m.group(0)[:120]
    return [x.strip() for x in p]


def monta(lingua):
    li = {'ro': 0, 'en': 1, 'pt': 2}[lingua]
    dic, n = {}, [0]

    def nova(p):
        k = 'k%d' % n[0]; n[0] += 1; dic[k] = p; return k

    # só se traduz fora de <script> e <style>
    blocos = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', SRC, flags=re.S)
    for bi, b in enumerate(blocos):
        if b.startswith('<script') or b.startswith('<style'):
            continue

        def tag(mt):
            t = mt.group(0)
            if '{{' not in t:
                return t
            refs = []

            def at(ma):
                p = partes(MARK.search(ma.group(2)))
                k = nova([html.unescape(x) for x in p]); refs.append('%s:%s' % (ma.group(1), k))
                return '%s="%s"' % (ma.group(1), MARK.sub(lambda _: p[li], ma.group(2)))
            t = re.sub(r'([\w-]+)="([^"]*\{\{.*?\}\}[^"]*)"', at, t)
            return t[:-1].rstrip('/') + ' data-ia="%s"%s>' % (';'.join(refs), '/' if t.endswith('/>') else '')
        b = re.sub(r'<[a-zA-Z][^<>]*>', tag, b)

        # elemento cujo conteúdo é só o marcador
        def inteiro(me):
            p = partes(MARK.search(me.group(4)))
            k = nova(p)
            return '%s data-i="%s">%s%s' % (me.group(1), k, me.group(3) + p[li] + me.group(5), me.group(6))
        b = re.sub(r'(<(\w+)\b[^<>]*?)>(\s*)(\{\{(?:(?!\{\{).)*?\}\})(\s*)(</\2>)', inteiro, b, flags=re.S)

        def solto(mm):
            p = partes(mm); k = nova(p)
            return '<span data-i="%s">%s</span>' % (k, p[li])
        b = MARK.sub(solto, b)
        blocos[bi] = b
    out = ''.join(blocos)
    out = out.replace('/*__FONTES__*/', FONTES)
    out = out.replace('/*__I18N__*/', json.dumps(dic, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
    out = out.replace('__LANG0__', lingua)
    if lingua == 'pt':
        out = out.replace('<html lang="ro"', '<html lang="pt-PT"', 1)
        out = re.sub(r'<title>(.*?)</title>', lambda m: '<title>%s</title>' % TITULO_PT, out, count=1)
        out = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + DESC_PT, out, count=1)
    assert '{{' not in out.split('<script>')[0], 'marcador por traduzir'
    return out


TITULO_PT = re.search(r'<!--TITULO_PT:(.*?)-->', SRC).group(1)
DESC_PT = re.search(r'<!--DESC_PT:(.*?)-->', SRC).group(1)
ro = monta('ro')
pt = monta('pt')
open('index.html', 'w', encoding='utf-8').write(ro)
open('pt.html', 'w', encoding='utf-8').write(pt)
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.(?:webp|mp4|webm))', ro) if not os.path.exists('media/' + m)})
print('index.html %.0f KB · pt.html %.0f KB' % (len(ro.encode()) / 1024, len(pt.encode()) / 1024)
      + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
