#!/usr/bin/env python3
"""Proposta comercial Frișcot (Prioridade 1) — HTML A4 → PDF (RO para o cliente, PT para o Tomás). Uso: python3 gerar.py (precisa de Playwright/Chromium)."""
import base64, pathlib, subprocess, json
AQUI = pathlib.Path(__file__).parent
FS = pathlib.Path('/tmp/claude-0/-home-user-Designerpacheco/53c8a074-377d-58ee-b801-b59b59b7af13/scratchpad/fs')

def fonte(fam, pkg, peso):
    out = ''
    for sub, rng in (('latin', 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215'), ('latin-ext', 'U+0100-024F,U+0259,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF')):
        f = next((FS / pkg).glob(f'package/files/{fam}-{sub}-{peso}-normal.woff2'))
        out += f"@font-face{{font-family:'{fam.title()}';font-weight:{peso};src:url(data:font/woff2;base64,{base64.b64encode(f.read_bytes()).decode()}) format('woff2');unicode-range:{rng}}}\n"
    return out
FONTES = ''.join(fonte('fraunces', 'fontsource-fraunces-5.3.0', p) for p in (400, 600, 700)) + ''.join(fonte('inter', 'fontsource-inter-5.3.0', p) for p in (400, 600, 700))

T = {
 'ro': dict(
  lang='ro', doc='Propunere comercială', titulo='Un singur site pentru cele cinci cofetării Frișcot',
  para='Pentru', para_v='Frișcot · Str. Codrescu 6, Iași', data='Data', data_v='28 septembrie 2026 · valabilă 30 de zile', de='De la', de_v='Tomás Pacheco · Pacheco Studios · tspacheco26@gmail.com',
  s1='Ce am observat', s1_nota='verificat pe 27 septembrie 2026',
  obs=['<b>Site-ul de comenzi friscot-comanda.ro nu mai există.</b> Cine încearcă azi să comande un tort online primește o eroare — inclusiv din linkurile vechi de pe Instagram și Google.',
       'Cele cinci cofetării apar pe Google ca <b>profiluri separate</b>. Cel din Codrescu apare doar ca „Cofetărie": Brasseria, pinsa și băcănia gourmet nu apar la căutare.',
       'Profilul din Codrescu are <b>4,2★ din 709 recenzii</b> — sub nivelul spațiului și al produselor.',
       '<b>Frișcot Brasserie</b>, deschisă pe 20 mai 2025, merită să fie găsită de cine caută un loc de brunch sau de seară în Copou.'],
  s2='Ce propunem — Prioritatea 1', s2_sub='Ce se poate face în două săptămâni, fără efort operațional din partea echipei.',
  blocos=[('A','Site nou pentru cele cinci cofetării',['Cele cinci locații pe o hartă-tort interactivă, cu adresă, program și „Cum ajung" pentru fiecare','Secțiune Frișcot Brasserie: pinsa, băcănie gourmet, rezervări pe WhatsApp','Campania „Tortul de ziua ta" și comenzi pe WhatsApp în trei pași','Legături către Instagram, TikTok și Facebook','Conform legii: datele firmei, ANPC-SAL, cookie-uri, politici RGPD — în limba română','Gândit pentru telefon, rapid, fără abonament la o platformă de tip Wix']),
          ('B','Adresa veche de comenzi, redirecționată',['Recuperăm domeniul friscot-comanda.ro (dacă este disponibil) și îl trimitem spre pagina de comenzi','Linkurile vechi nu mai duc la o eroare; domeniul inclus în primul an']),
          ('C','Cele cinci profiluri Google',['Categorii corecte (Brasseria și ca bistro / cafenea), program, fotografii, meniu','Cod QR pentru recenzii, gata de tipar, pentru fiecare locație','Model de răspuns la recenzii pentru echipă'])],
  s3='Investiție',
  linhas=[('Site nou pentru cele cinci cofetării','2 990 lei'),('Redirecționare friscot-comanda.ro','inclus'),('Cinci profiluri Google + coduri QR','1 490 lei')],
  total_sep='Total separat', total_sep_v='4 480 lei', pacote='Pachet Prioritatea 1', pacote_v='3 990 lei',
  manut='Mentenanță (opțional): <b>349 lei / lună</b> — găzduire, domeniu, certificat SSL, copii de siguranță, modificări în maximum 7 zile, suport direct.',
  iva='Prețurile nu includ TVA. Factura se emite din Portugalia (UE); pentru beneficiarii cu cod de TVA valid se aplică taxarea inversă.',
  pag='Plata: 50% la acceptare, 50% la publicare, prin transfer bancar.',
  s4='Calendar', s4_sub='zile lucrătoare de la primirea materialelor',
  cal=[('Zilele 1–3','Fotografii în cele cinci locații, programul, datele firmei'),('Zilele 4–8','Versiunea finală a site-ului, pentru aprobare'),('Zilele 9–10','Publicare și redirecționarea adresei vechi'),('În paralel','Profilurile Google (verificarea de către Google poate dura câteva zile)')],
  s5='De ce avem nevoie de la voi',
  prec=['Logo (vector, dacă există) și fotografii — sau acordul de a fotografia în locații','Programul fiecărei locații','Denumirea firmei, CUI și Nr. Reg. Com.','Acces la domeniul friscot.ro și la contul în care era friscot-comanda.ro','Rol de „Manager" în profilurile Google Business'],
  s6='Pasul următor (ofertă separată)', prox='<b>Prioritatea 2 — magazin online de torturi</b>, cu ridicare din locația aleasă, construit pe baza noului site. Catalogul vechi (torturi, prăjituri, patiserie, sezoniere) poate fi reluat.',
  aceite='Acceptare', ass1='Pentru Frișcot', ass2='Pacheco Studios — Tomás Pacheco', dat='Data', rodape='Pacheco Studios · web design și marketing digital · tspacheco26@gmail.com'),
 'pt': dict(
  lang='pt-PT', doc='Proposta comercial — tradução para o Tomás', titulo='Um só site para as cinco pastelarias Frișcot',
  para='Para', para_v='Frișcot · Str. Codrescu 6, Iași', data='Data', data_v='28 de setembro de 2026 · válida 30 dias', de='De', de_v='Tomás Pacheco · Pacheco Studios · tspacheco26@gmail.com',
  s1='O que observámos', s1_nota='verificado a 27 de setembro de 2026',
  obs=['<b>O site de encomendas friscot-comanda.ro já não existe.</b> Quem tenta hoje encomendar um bolo online recebe um erro — também a partir dos links antigos no Instagram e no Google.',
       'As cinco pastelarias aparecem no Google como <b>perfis separados</b>. O de Codrescu aparece só como "Confeitaria": a Brasserie, a pinsa e a mercearia gourmet não aparecem nas pesquisas.',
       'O perfil de Codrescu tem <b>4,2★ em 709 avaliações</b> — abaixo do nível do espaço e dos produtos.',
       'A <b>Frișcot Brasserie</b>, aberta a 20 de maio de 2025, merece ser encontrada por quem procura um sítio para brunch ou para a noite em Copou.'],
  s2='O que propomos — Prioridade 1', s2_sub='O que se faz em duas semanas, sem esforço operacional da equipa.',
  blocos=[('A','Site novo para as cinco pastelarias',['As cinco lojas num mapa-bolo interativo, com morada, horário e "Como chegar" para cada uma','Secção Frișcot Brasserie: pinsa, mercearia gourmet, reservas por WhatsApp','Campanha "O bolo do teu aniversário" e encomendas por WhatsApp em três passos','Ligações para Instagram, TikTok e Facebook','Conforme a lei: dados da empresa, ANPC-SAL, cookies, políticas RGPD — em romeno','Pensado para telemóvel, rápido, sem mensalidade de uma plataforma tipo Wix']),
          ('B','O endereço antigo de encomendas, redirecionado',['Recuperamos o domínio friscot-comanda.ro (se estiver disponível) e apontamo-lo para a página de encomendas','Os links antigos deixam de dar erro; domínio incluído no primeiro ano']),
          ('C','Os cinco perfis Google',['Categorias certas (a Brasserie também como bistro / café), horário, fotos, menu','Código QR para avaliações, pronto a imprimir, para cada loja','Modelo de resposta às avaliações para a equipa'])],
  s3='Investimento',
  linhas=[('Site novo para as cinco pastelarias','2 990 lei'),('Redirecionamento de friscot-comanda.ro','incluído'),('Cinco perfis Google + códigos QR','1 490 lei')],
  total_sep='Total em separado', total_sep_v='4 480 lei', pacote='Pacote Prioridade 1', pacote_v='3 990 lei',
  manut='Manutenção (opcional): <b>349 lei / mês</b> — alojamento, domínio, certificado SSL, cópias de segurança, alterações em 7 dias no máximo, suporte direto.',
  iva='Preços sem IVA. A fatura é emitida em Portugal (UE); para clientes com número de IVA válido aplica-se a autoliquidação. <i>(Confirmar com o contabilista antes de enviar.)</i>',
  pag='Pagamento: 50% na aceitação, 50% na publicação, por transferência bancária.',
  s4='Calendário', s4_sub='dias úteis a contar da receção dos materiais',
  cal=[('Dias 1–3','Fotos nas cinco lojas, horários, dados da empresa'),('Dias 4–8','Versão final do site, para aprovação'),('Dias 9–10','Publicação e redirecionamento do endereço antigo'),('Em paralelo','Perfis Google (a verificação pela Google pode demorar alguns dias)')],
  s5='O que precisamos da vossa parte',
  prec=['Logótipo (vetorial, se existir) e fotos — ou autorização para fotografar nas lojas','Horário de cada loja','Nome da empresa, CUI e N.º Reg. Com.','Acesso ao domínio friscot.ro e à conta onde estava o friscot-comanda.ro','Função de "Gestor" nos perfis Google Business'],
  s6='Próximo passo (proposta separada)', prox='<b>Prioridade 2 — loja online de bolos</b>, com levantamento na loja escolhida, construída sobre o site novo. O catálogo antigo (bolos, bolinhos, pastelaria, sazonais) pode ser retomado.',
  aceite='Aceitação', ass1='Pela Frișcot', ass2='Pacheco Studios — Tomás Pacheco', dat='Data', rodape='Pacheco Studios · web design e marketing digital · tspacheco26@gmail.com'),
}

CSS = FONTES + '''
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font:10.2pt/1.5 Inter,sans-serif;color:#1b2333;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pag{width:210mm;height:297mm;padding:18mm 18mm 16mm;position:relative;page-break-after:always;overflow:hidden}
.pag:last-child{page-break-after:auto}
.topo{background:#142238;color:#fff;margin:-18mm -18mm 8mm;padding:12mm 18mm 9mm;position:relative}
.topo:after{content:"";position:absolute;left:18mm;bottom:0;width:36mm;height:3px;background:#C59A3E}
.marca{font:600 9pt Inter;letter-spacing:.2em;text-transform:uppercase;color:#C59A3E}
.doc{font:600 8.5pt Inter;letter-spacing:.14em;text-transform:uppercase;opacity:.75;margin-top:6mm}
h1{font:700 25pt/1.1 Fraunces,serif;margin:2mm 0 0;max-width:150mm}
.meta{display:grid;grid-template-columns:auto 1fr;gap:1.2mm 6mm;margin-bottom:5mm;font-size:9.4pt}
.meta dt{font-weight:700;color:#8a6a2a;text-transform:uppercase;letter-spacing:.08em;font-size:7.8pt;padding-top:.6mm}.meta dd{margin:0}
h2{font:700 14pt Fraunces,serif;color:#142238;margin:5.5mm 0 2.5mm;display:flex;align-items:baseline;gap:3mm}
h2 small{font:400 8.5pt Inter;color:#6b7385}
ul{margin:0;padding-left:5mm}li{margin:0 0 1.1mm}
.obs li::marker{color:#C59A3E}
.bloco{display:grid;grid-template-columns:10mm 1fr;gap:0 4mm;margin:0 0 4mm;break-inside:avoid}
.bloco .l{width:10mm;height:10mm;border-radius:50%;background:#142238;color:#C59A3E;font:700 11pt Fraunces;display:grid;place-items:center}
.bloco h3{font:700 11pt Inter;margin:1.5mm 0 1.5mm;color:#142238}
.sub{color:#6b7385;margin:-1mm 0 4mm}
table{width:100%;border-collapse:collapse;font-size:10pt}
td{padding:2.2mm 0;border-bottom:1px solid #e3e6ec}td:last-child{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;font-weight:600}
tr.sep td{color:#6b7385;font-weight:400}tr.sep td:last-child{text-decoration:line-through;font-weight:400}
tr.pac td{border:0;padding-top:4mm;font:700 13pt Fraunces;color:#142238}tr.pac td:last-child{font:700 17pt Fraunces;color:#142238}
.caixa{background:#f7f3ea;border-left:3px solid #C59A3E;padding:3.5mm 4.5mm;margin-top:4mm;font-size:9.4pt}
.caixa p{margin:0 0 1.5mm}.caixa p:last-child{margin:0}
.cal{display:grid;grid-template-columns:24mm 1fr;gap:2mm 5mm;font-size:9.6pt}.cal b{color:#142238}
.prox{background:#142238;color:#fff;border-radius:3mm;padding:5mm 6mm;margin-top:3mm;font-size:9.8pt}.prox b{color:#C59A3E}
.ass{display:grid;grid-template-columns:1fr 1fr;gap:12mm;margin-top:9mm;font-size:9pt;color:#6b7385}
.ass div{border-top:1px solid #1b2333;padding-top:2mm}
.rod{position:absolute;left:18mm;right:18mm;bottom:9mm;font-size:7.8pt;color:#8a90a0;display:flex;justify-content:space-between;border-top:1px solid #e3e6ec;padding-top:2.5mm}
'''

def html(t):
    obs = ''.join(f'<li>{o}</li>' for o in t['obs'])
    blocos = ''.join(f'<div class="bloco"><div class="l">{l}</div><div><h3>{h}</h3><ul>{"".join(f"<li>{i}</li>" for i in its)}</ul></div></div>' for l, h, its in t['blocos'])
    linhas = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in t['linhas'])
    cal = ''.join(f'<b>{a}</b><span>{b}</span>' for a, b in t['cal'])
    prec = ''.join(f'<li>{p}</li>' for p in t['prec'])
    rod = lambda n: f'<div class="rod"><span>{t["rodape"]}</span><span>{n}/2</span></div>'
    return f'''<!DOCTYPE html><html lang="{t['lang']}"><head><meta charset="utf-8"><title>{t['doc']} — Frișcot</title><style>{CSS}</style></head><body>
<section class="pag">
 <header class="topo"><div class="marca">Pacheco Studios</div><div class="doc">{t['doc']}</div><h1>{t['titulo']}</h1></header>
 <dl class="meta"><dt>{t['para']}</dt><dd>{t['para_v']}</dd><dt>{t['data']}</dt><dd>{t['data_v']}</dd><dt>{t['de']}</dt><dd>{t['de_v']}</dd></dl>
 <h2>{t['s1']} <small>{t['s1_nota']}</small></h2><ul class="obs">{obs}</ul>
 <h2>{t['s2']}</h2><p class="sub">{t['s2_sub']}</p>{blocos}
 {rod(1)}
</section>
<section class="pag">
 <h2 style="margin-top:0">{t['s3']}</h2>
 <table>{linhas}<tr class="sep"><td>{t['total_sep']}</td><td>{t['total_sep_v']}</td></tr><tr class="pac"><td>{t['pacote']}</td><td>{t['pacote_v']}</td></tr></table>
 <div class="caixa"><p>{t['manut']}</p><p>{t['iva']}</p><p>{t['pag']}</p></div>
 <h2>{t['s4']} <small>{t['s4_sub']}</small></h2><div class="cal">{cal}</div>
 <h2>{t['s5']}</h2><ul>{prec}</ul>
 <h2>{t['s6']}</h2><div class="prox">{t['prox']}</div>
 <h2>{t['aceite']}</h2><div class="ass"><div>{t['ass1']}<br><br>{t['dat']}:</div><div>{t['ass2']}<br><br>{t['dat']}:</div></div>
 {rod(2)}
</section></body></html>'''

for k, t in T.items():
    (AQUI / f'proposta-{k}.html').write_text(html(t), encoding='utf-8')
js = '''const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox']});const p=await b.newPage();
for(const k of ['ro','pt']){await p.goto('file://%s/proposta-'+k+'.html');await p.waitForTimeout(400);await p.pdf({path:'%s/proposta-friscot-'+k+'.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
await p.setViewportSize({width:794,height:1123});await p.screenshot({path:'%s/previa-'+k+'.png',fullPage:true});}await b.close();})();''' % (AQUI, AQUI, AQUI)
pathlib.Path('/tmp/claude-0/-home-user-Designerpacheco/53c8a074-377d-58ee-b801-b59b59b7af13/scratchpad/pdf.js').write_text(js)
subprocess.run(['node', 'pdf.js'], cwd='/tmp/claude-0/-home-user-Designerpacheco/53c8a074-377d-58ee-b801-b59b59b7af13/scratchpad', check=True)
print('ok')
