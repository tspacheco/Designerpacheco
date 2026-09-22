/* DEMONSTRAÇÃO — servidor da loja a correr dentro do browser (localStorage).
   Mesmas regras do loja/servidor-teste.js: reserva de stock, MB WAY simulado (6 s; telemóvel terminado em 0 falha),
   painel com palavra-passe 123. Só para experimentar: os dados ficam neste browser. */
(function(){
'use strict';
var CHAVE = 'tc.demo.db', SENHA = '123', RESERVA_MIN = 60;
var SEMENTE = __CATALOGO__;
window.LOJA_API = '/api';
function agora(){ return new Date().toISOString(); }
function ha(min){ return new Date(Date.now() - min * 60000).toISOString(); }
function token(){ var a = new Uint8Array(16); crypto.getRandomValues(a); return Array.prototype.map.call(a, function(b){ return ('0' + b.toString(16)).slice(-2); }).join(''); }
function grava(db){ try { localStorage.setItem(CHAVE, JSON.stringify(db)); } catch (e) { console.warn('demo: sem espaço no localStorage', e); } }
function cor(db, id, i){ var p = db.pecas.find(function(x){ return x.id === id; }); return p && p.cores[i]; }
function disponivel(c){ return Math.max(0, (c.stock || 0) - (c.reservado || 0)); }
function liberta(db, e){ e.linhas.forEach(function(l){ var c = cor(db, l.peca, l.cor); if (c) c.reservado = Math.max(0, c.reservado - l.qt); }); }
function marcaPaga(db, e){ if (e.estado !== 'pendente') return; e.linhas.forEach(function(l){ var c = cor(db, l.peca, l.cor); if (c) { c.stock = Math.max(0, c.stock - l.qt); c.reservado = Math.max(0, c.reservado - l.qt); } }); e.estado = 'paga'; e.paga = agora(); e.atualizada = agora(); }
function marcaFalhada(db, e, m){ if (e.estado !== 'pendente') return; liberta(db, e); e.estado = 'falhada'; e.motivo = m; e.atualizada = agora(); }

function semear(){
  var cat = JSON.parse(JSON.stringify(SEMENTE));
  cat.pecas.forEach(function(p){ p.ativo = true; p.cores.forEach(function(c){ if (typeof c.stock !== 'number') c.stock = 0; c.reservado = 0; }); });
  var db = { categorias: cat.categorias, estacoes: cat.estacoes, pecas: cat.pecas, encomendas: [], seq: 1000 };
  function linha(id, i, tam, qt){ var p = db.pecas.find(function(x){ return x.id === id; }); if (!p || !p.cores[i]) return null; var c = p.cores[i];
    return { peca: p.id, nome: p.nome, cor: i, corNome: c.nome, tam: tam, tamNome: p.tamanhos[tam] || 'Único', qt: qt, preco: p.preco, foto: c.foto }; }
  function enc(n, linhas, estado, minutos){
    linhas = linhas.filter(Boolean); if (!linhas.length) return;
    var e = { id: ++db.seq, token: token(), estado: 'pendente', linhas: linhas, cliente: { nome: 'Cliente de demonstração ' + n, telemovel: '91200000' + n, email: '', morada: 'Rua de Exemplo, ' + n, cp: '8000-000', localidade: 'Faro', nif: '' },
      total: Math.round(linhas.reduce(function(s, l){ return s + l.preco * l.qt; }, 0) * 100) / 100, portes: 0, criada: ha(minutos), atualizada: ha(minutos), pagamento: null };
    linhas.forEach(function(l){ cor(db, l.peca, l.cor).reservado += l.qt; });
    if (estado === 'paga' || estado === 'enviada') { marcaPaga(db, e); e.paga = ha(minutos - 1); }
    if (estado === 'enviada') { e.estado = 'enviada'; e.enviada = ha(minutos - 30); }
    e.atualizada = e.enviada || e.paga || e.criada;
    db.encomendas.push(e);
  }
  enc(1, [linha('calcas-pelo-dentro', 0, 0, 1), linha('leggings-termicas', 0, 1, 2)], 'enviada', 2 * 24 * 60);
  enc(2, [linha('leggings-termicas', 0, 0, 1)], 'paga', 70);
  enc(3, [linha('cuecas-renda', 0, 0, 2)], 'pendente', 4);
  grava(db); return db;
}
function carrega(){
  var db = null; try { var s = localStorage.getItem(CHAVE); if (s) db = JSON.parse(s); } catch (e) {}
  if (!db) db = semear();
  var limite = Date.now() - RESERVA_MIN * 60000, mudou = false;
  db.encomendas.forEach(function(e){
    if (e.estado !== 'pendente') return;
    if (e.pagamento && e.pagamento.simulado && Date.now() - new Date(e.pagamento.criado).getTime() > 6000) { resolve(db, e); mudou = true; }
    else if (new Date(e.criada).getTime() < limite) { liberta(db, e); e.estado = 'expirada'; e.motivo = 'Expirou sem pagamento'; e.atualizada = agora(); mudou = true; }
  });
  if (mudou) grava(db);
  return db;
}
function resolve(db, e){
  if (/0$/.test(e.cliente.telemovel)) { e.pagamento.estado = 'falhado'; marcaFalhada(db, e, 'MB WAY recusado (simulação: telemóvel termina em 0)'); }
  else { e.pagamento.estado = 'pago'; marcaPaga(db, e); }
}
function catalogoPublico(db){
  return { categorias: db.categorias, estacoes: db.estacoes,
    pecas: db.pecas.filter(function(p){ return p.ativo !== false; }).map(function(p){ return Object.assign({}, p, { cores: p.cores.map(function(c){ return { nome: c.nome, hex: c.hex, foto: c.foto, stock: disponivel(c) }; }) }); }) };
}
function criaEncomenda(db, corpo){
  var erros = [], cl = corpo.cliente || {};
  ['nome', 'telemovel', 'morada', 'cp', 'localidade'].forEach(function(k){ if (!cl[k] || String(cl[k]).trim().length < 2) erros.push('Falta ' + k); });
  if (!/^9\d{8}$/.test(String(cl.telemovel || '').replace(/\s/g, ''))) erros.push('O número MB WAY tem de ser um telemóvel português (9 dígitos, começa por 9)');
  if (!Array.isArray(corpo.linhas) || !corpo.linhas.length) erros.push('Saco vazio');
  if (erros.length) return { erro: erros.join(' · ') };
  var linhas = [], total = 0;
  for (var i = 0; i < corpo.linhas.length; i++) {
    var l = corpo.linhas[i], p = db.pecas.find(function(x){ return x.id === l.peca && x.ativo !== false; }), c = p && p.cores[l.cor];
    if (!p || !c) return { erro: 'Peça já não existe: ' + l.peca };
    if (p.preco == null) return { erro: p.nome + ' ainda não tem preço' };
    var qt = Math.max(1, Math.min(9, +l.qt || 1));
    if (disponivel(c) < qt) return { erro: 'Já não há stock suficiente de "' + p.nome + '" em ' + c.nome + ' (restam ' + disponivel(c) + ')' };
    linhas.push({ peca: p.id, nome: p.nome, cor: l.cor, corNome: c.nome, tam: l.tam, tamNome: (l.tam >= 0 && p.tamanhos[l.tam]) || 'Único', qt: qt, preco: p.preco, foto: c.foto });
    total += p.preco * qt;
  }
  linhas.forEach(function(l){ cor(db, l.peca, l.cor).reservado += l.qt; });
  var e = { id: ++db.seq, token: token(), estado: 'pendente', linhas: linhas, cliente: { nome: cl.nome, telemovel: String(cl.telemovel).replace(/\s/g, ''), email: cl.email || '', morada: cl.morada, cp: cl.cp, localidade: cl.localidade, nif: cl.nif || '' },
    total: Math.round(total * 100) / 100, portes: 0, criada: agora(), atualizada: agora(), pagamento: { simulado: true, metodo: 'mbw', estado: 'pendente', criado: agora() } };
  db.encomendas.push(e);
  setTimeout(function(){ var d = carrega(); var en = d.encomendas.find(function(x){ return x.token === e.token; }); if (en && en.estado === 'pendente') { resolve(d, en); grava(d); } }, 6000);
  return { encomenda: e };
}
function slug(s){ return (s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'peca'); }

function trata(rota, metodo, cab, b){
  var db = carrega(), m;
  if (metodo === 'GET' && rota === '/catalogo') return [200, catalogoPublico(db)];
  if (metodo === 'POST' && rota === '/encomendas') { var r = criaEncomenda(db, b); grava(db); return r.erro ? [400, { erro: r.erro }] : [201, { token: r.encomenda.token, id: r.encomenda.id, total: r.encomenda.total, estado: r.encomenda.estado }]; }
  if (metodo === 'GET' && (m = rota.match(/^\/encomendas\/([a-f0-9]{32})$/))) { var e = db.encomendas.find(function(x){ return x.token === m[1]; }); return e ? [200, { id: e.id, estado: e.estado, total: e.total, linhas: e.linhas, motivo: e.motivo || null }] : [404, { erro: 'Encomenda não encontrada' }]; }
  if (rota.indexOf('/painel/') === 0) {
    if (cab !== SENHA) return [401, { erro: 'Palavra-passe do painel errada' }];
    if (metodo === 'GET' && rota === '/painel/encomendas') return [200, db.encomendas.slice().reverse()];
    if (metodo === 'PATCH' && (m = rota.match(/^\/painel\/encomendas\/(\d+)$/))) {
      var en = db.encomendas.find(function(x){ return x.id === +m[1]; }); if (!en) return [404, { erro: 'Não existe' }];
      if (b.estado === 'enviada' && en.estado === 'paga') { en.estado = 'enviada'; en.enviada = agora(); }
      else if (b.estado === 'cancelada' && (en.estado === 'pendente' || en.estado === 'paga')) { if (en.estado === 'pendente') liberta(db, en); en.estado = 'cancelada'; }
      else return [400, { erro: 'Mudança de estado não permitida: ' + en.estado + ' → ' + b.estado }];
      en.atualizada = agora(); grava(db); return [200, en];
    }
    if (metodo === 'GET' && rota === '/painel/pecas') return [200, { categorias: db.categorias, estacoes: db.estacoes, pecas: db.pecas }];
    if (metodo === 'PATCH' && rota === '/painel/stock') { var c = cor(db, b.peca, +b.cor); if (!c) return [404, { erro: 'Peça/cor não existe' }]; c.stock = Math.max(0, Math.round(+b.stock || 0)); grava(db); return [200, { stock: c.stock, disponivel: disponivel(c) }]; }
    if (metodo === 'POST' && rota === '/painel/pecas') {
      if (!b.nome || b.preco == null || !Array.isArray(b.cores) || !b.cores.length) return [400, { erro: 'Nome, preço e pelo menos uma cor são obrigatórios' }];
      var id = slug(b.nome) + '-' + (db.seq + 1);
      var cores = b.cores.map(function(c, i){ var f = c.fotoBase64 ? (/^data:/.test(c.fotoBase64) ? c.fotoBase64 : 'data:image/jpeg;base64,' + c.fotoBase64) : null;
        return { nome: c.nome || 'Cor ' + (i + 1), hex: c.hex || '#CCCCCC', foto: f, stock: Math.max(0, Math.round(+c.stock || 0)), reservado: 0 }; });
      var peca = { id: id, nome: b.nome, cat: b.cat || 'blusas', preco: +b.preco, precoAntigo: b.precoAntigo ? +b.precoAntigo : undefined, promo: !!b.precoAntigo, tam: b.tam || 'Tamanho único', tamanhos: b.tamanhos && b.tamanhos.length ? b.tamanhos : ['Único'], cores: cores, desc: b.desc || '', estacao: b.estacao || 'meia', nova: true, ativo: true };
      db.pecas.unshift(peca); db.seq++; grava(db); return [201, peca];
    }
    if (metodo === 'PATCH' && (m = rota.match(/^\/painel\/pecas\/([a-z0-9-]+)$/))) {
      var pe = db.pecas.find(function(x){ return x.id === m[1]; }); if (!pe) return [404, { erro: 'Não existe' }];
      ['nome', 'preco', 'precoAntigo', 'desc', 'tam', 'cat', 'estacao', 'ativo', 'nova'].forEach(function(k){ if (k in b) pe[k] = b[k]; });
      pe.promo = pe.precoAntigo != null && pe.precoAntigo > pe.preco; grava(db); return [200, pe];
    }
  }
  return [404, { erro: 'Rota desconhecida' }];
}
var fetchReal = window.fetch.bind(window);
window.fetch = function(url, op){
  var u = typeof url === 'string' ? url : (url && url.url) || '';
  if (u.indexOf('/api/') !== 0) return fetchReal(url, op);
  op = op || {};
  var cab = op.headers ? (op.headers['X-Painel'] || op.headers['x-painel'] || (op.headers.get && op.headers.get('X-Painel'))) : null;
  return new Promise(function(ok){ setTimeout(function(){
    var r; try { r = trata(u.slice(4), (op.method || 'GET').toUpperCase(), cab, op.body ? JSON.parse(op.body) : {}); } catch (e) { r = [500, { erro: e.message }]; }
    ok(new Response(JSON.stringify(r[1]), { status: r[0], headers: { 'Content-Type': 'application/json; charset=utf-8' } }));
  }, 80); });
};
window.__demoRepor = function(){ try { localStorage.removeItem(CHAVE); } catch (e) {} location.reload(); };
})();
