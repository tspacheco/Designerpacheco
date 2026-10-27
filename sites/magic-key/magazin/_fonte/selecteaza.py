"""Lê keyshop-parte*.txt (nome;marca;caminho_imagem por categoria, recolhidos do key-shop.ro a partir do PC do Tomás)
e escreve ../produse.json (o que o site mostra) e referinte.csv (ref. MK-… -> nome e caminho no fornecedor, só para o George).
Tira embalagens de revenda, licenças e peças de oficina; limpa os códigos internos do fornecedor; nunca copia preços."""
import os, re, json, csv
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FORA = re.compile(r'set 100|100 de bucati|100 bucati|1000 bucati|500 de bucati|200 de bucati|200 bucati|licent|Key Tool Max|xerox|'
                  r'Carcasa pentru telecomanda garaj|Capison de plastic|Kit adaptor|Placuta', re.I)
CAT = [  # ordem da página
    ('garaj', 'Porți, garaje, bariere', 'Gates, garages, barriers', 'Portões, garagens, barreiras'),
    ('auto', 'Telecomenzi auto', 'Car remotes', 'Comandos auto'),
    ('carcase', 'Carcase și lame', 'Key shells and blades', 'Carcaças e lâminas'),
    ('baterii', 'Baterii', 'Batteries', 'Pilhas'),
    ('taguri', 'Tag-uri și cartele', 'Fobs and cards', 'Tags e cartões'),
    ('huse', 'Huse pentru chei', 'Key covers', 'Capas de chave'),
    ('accesorii', 'Brelocuri', 'Keyrings', 'Porta-chaves'),
]
DIAC = [(r'\bTelecomanda\b', 'Telecomandă'), (r'\bpoarta\b', 'poartă'), (r'\btelecomanda\b', 'telecomandă'), (r'\bcartela\b', 'cartelă'), (r'\bcarabina\b', 'carabină'), (r'\bdesign nou\b', 'design nou'), (r'\bbariera\b', 'barieră'), (r'\bHusa\b', 'Husă'),
        (r'\bprotectie\b', 'protecție'), (r'\bCarcasa\b', 'Carcasă'), (r'\bfara\b', 'fără'), (r'\bneagra\b', 'neagră'),
        (r'\bneagru\b', 'negru'), (r'\bbucati\b', 'bucăți'), (r'\bbucata\b', 'bucată'), (r'\bCartela\b', 'Cartelă'),
        (r'\blocas\b', 'lăcaș'), (r'\burgenta\b', 'urgență'), (r'\boriginala\b', 'originală'), (r'\blama\b', 'lamă'),
        (r'\bsi\b', 'și'), (r'\bpana\b', 'până'), (r'\binainte\b', 'înainte'), (r'\bmaner\b', 'mâner'), (r'\bgri\b', 'gri'),
        (r'\bverde\b', 'verde'), (r'\bpiele\b', 'piele'), (r'\bculoare\b', 'culoare'), (r'\bnumar\b', 'număr'), (r'\bpisici\b', 'pisici'),
        (r'\bcaini\b', 'câini'), (r'\bfunctie\b', 'funcție'), (r'\balcalina\b', 'alcalină'), (r'\bpriza telecomandabila\b', 'priză telecomandabilă'),
        (r'\bschimb\b', 'schimb'), (r'\btip lacrima\b', 'tip lacrimă'), (r'\bsuruburi\b', 'șuruburi'), (r'\bversiune europeana\b', 'versiune europeană'),
        (r'\bclonabil\b', 'clonabil'), (r'\bPeuoget\b', 'Peugeot'), (r'\bmotocicleta\b', 'motocicletă'), (r'\bluminoasa\b', 'luminoasă'),
        (r'\bacces\b', 'acces'), (r'\bdiverse culori\b', 'diverse culori'), (r'\balba\b', 'albă'), (r'\balbastra\b', 'albastră'), (r'\binfrarosu\b', 'infraroșu'), (r'\brosu\b', 'roșu'), (r'\buniversala\b', 'universală'), (r'"lacrima"', '„lacrimă”'), (r'\bcarcasa\b', 'carcasa')]
COD = re.compile(r'^[A-Z][A-Z0-9]*(-[A-Z0-9]+)+$')  # códigos internos do fornecedor (PE-T-35B2, CR2430-1)
def curata(n):
    n = re.sub(r'\s+', ' ', n).strip().rstrip(',')
    t = n.split(' ')
    while len(t) > 3:
        u = t[-1]
        if COD.match(u):
            t.pop(); continue
        if u.isupper() and len(u) > 1 and u.lower() in ' '.join(t[:-1]).lower():
            t.pop(); continue
        break
    n = ' '.join(t).rstrip(',')
    n = re.sub(r'\s*\((?:[A-Z]+-[A-Z]-[A-Z0-9]+)\)', '', n)
    for a, b in DIAC: n = re.sub(a, b, n)
    return n
def spec(n):
    s = []
    m = re.search(r'(\d{3}(?:[.,]\d+)?)\s*MHz', n, re.I);  s += [m.group(1).replace('.', ',') + ' MHz'] if m else []
    m = re.search(r'(\d+)\s*(?:\(\d\+\d\)\s*)?(?:butoane|but\b)', n); s += [m.group(1) + ' {b}'] if m else []
    if re.search(r'rolling code', n, re.I): s.append('rolling code')
    elif re.search(r'fix code|cod fix', n, re.I): s.append('{f}')
    if re.search(r'keyless', n, re.I): s.append('keyless')
    return s
def tri(s):
    j = ' · '.join(s)
    return [j.replace('{b}', 'butoane').replace('{f}', 'cod fix'), j.replace('{b}', 'buttons').replace('{f}', 'fixed code'),
            j.replace('{b}', 'botões').replace('{f}', 'código fixo')]
vazut, prod = set(), []
for f in sorted(x for x in os.listdir('.') if x.startswith('keyshop-parte')):
    cat = None
    for l in open(f, encoding='utf-8'):
        l = l.rstrip('\n')
        if l.startswith('## '): cat = l[3:].strip(); continue
        if not l.strip(): continue
        nume, marca, img = [x.strip() for x in l.rsplit(';', 2)]
        if FORA.search(nume) or img in vazut: continue
        c = cat
        if cat in ('auto', 'carcase'):
            c = 'auto' if nume.startswith('Telecomanda') else 'huse' if nume.startswith('Husa') else 'carcase'
        vazut.add(img)
        ref = 'MK-' + os.path.splitext(os.path.basename(img))[0][-5:].upper()
        if not marca:
            m = re.search(r'\b(Nice|BFT|Came|FAAC|Sommer|Beninca|DoorHan|LiftMaster|Errebi|Xhorse|Electra|Canas|Securemme)\b', nume, re.I)
            marca = m.group(1) if m else ''
        prod.append({'ref': ref, 'cat': c, 'marca': marca, 'nume': curata(nume), 'spec': tri(spec(nume)) if spec(nume) else '',
                     'img': 'media/magazin/%s.webp' % ref.lower(), 'sursa': img, 'orig': nume})
ordem = {c[0]: i for i, c in enumerate(CAT)}
prod.sort(key=lambda p: ordem[p['cat']])
json.dump({'categorii': [dict(id=a, ro=b, en=c, pt=d) for a, b, c, d in CAT],
           'produse': [{k: v for k, v in p.items() if k not in ('sursa', 'orig')} for p in prod]},
          open('../produse.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open('referinte.csv', 'w', encoding='utf-8', newline='') as o:
    w = csv.writer(o); w.writerow(['ref', 'categoria', 'nume_fornecedor', 'imagem_fornecedor'])
    for p in prod: w.writerow([p['ref'], p['cat'], p['orig'], 'https://key-shop.ro' + p['sursa']])
with open('imagens.txt', 'w', encoding='utf-8') as o:  # para descarregar no PC: <ficheiro> <url>
    for p in prod: o.write('%s.jpg https://key-shop.ro%s\n' % (p['ref'].lower(), p['sursa']))
from collections import Counter
print(len(prod), dict(Counter(p['cat'] for p in prod)))
