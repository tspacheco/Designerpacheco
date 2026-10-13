/* núcleo comum: idioma RO/EN/PT, menu, revelação, progresso de scroll, formulário -> WhatsApp / SMS, mapa a pedido */
(function(){
  var html=document.documentElement,$=function(i){return document.getElementById(i)};
  var PS=window.PS={reduz:matchMedia('(prefers-reduced-motion: reduce)').matches,sc:[],lg:[],p:0};
  function L(){return html.dataset.lang||'ro'}
  PS.L=L;
  PS.t=function(a,b,c){var l=L();return l==='en'?b:l==='pt'?c:a};
  PS.onScroll=function(f){PS.sc.push(f)};
  PS.onLang=function(f){PS.lg.push(f)};
  var idx={ro:0,en:1,pt:2};
  function aplicaLang(l){
    html.dataset.lang=l;html.lang=l==='pt'?'pt-PT':l;
    document.querySelectorAll('[data-set-lang]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.setLang===l?'true':'false')});
    document.querySelectorAll('[data-aria]').forEach(function(e){e.setAttribute('aria-label',e.dataset.aria.split('|')[idx[l]])});
    document.querySelectorAll('[data-alt]').forEach(function(e){e.alt=e.dataset.alt.split('|')[idx[l]]});
    document.querySelectorAll('[data-t]').forEach(function(e){e.textContent=e.dataset.t.split('|')[idx[l]]});
    document.querySelectorAll('[data-ph]').forEach(function(e){e.placeholder=e.dataset.ph.split('|')[idx[l]]});
    var tt=document.querySelector('meta[name="ps-titles"]');if(tt)document.title=tt.content.split('|')[idx[l]];
    try{localStorage.setItem('__LSKEY__',l)}catch(e){}
    PS.lg.forEach(function(f){f(l)});if(PS.prev)PS.prev();
  }
  document.querySelectorAll('[data-set-lang]').forEach(function(b){b.addEventListener('click',function(){aplicaLang(b.dataset.setLang)})});

  /* menu */
  var bg=document.querySelector('.burger'),mn=$('meniu');
  function menu(d){mn.classList.toggle('deschis',d);bg.setAttribute('aria-expanded',d?'true':'false');document.body.style.overflow=d?'hidden':'';if(d){var a=mn.querySelector('a,button');a&&a.focus()}else bg.focus()}
  if(bg&&mn){bg.addEventListener('click',function(){menu(!mn.classList.contains('deschis'))});mn.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){mn.classList.remove('deschis');bg.setAttribute('aria-expanded','false');document.body.style.overflow=''})});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&mn.classList.contains('deschis'))menu(false)})}

  /* revelação */
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'}):null;
  PS.observa=function(root){(root||document).querySelectorAll('.rv:not(.vis),.clip:not(.vis)').forEach(function(x){if(io)io.observe(x);else x.classList.add('vis')})};

  /* progresso de scroll */
  var tick=false;
  function sc(){tick=false;var h=html.scrollHeight-innerHeight;PS.p=h>0?Math.min(1,Math.max(0,scrollY/h)):0;html.style.setProperty('--p',PS.p.toFixed(4));
    var n=document.querySelector('.nav');if(n)n.classList.toggle('scrolled',scrollY>8);PS.sc.forEach(function(f){f(PS.p)})}
  addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(sc)}},{passive:true});
  addEventListener('resize',function(){if(!tick){tick=true;requestAnimationFrame(sc)}});
  PS.refresh=sc;

  /* formulário: mensagem em romeno, enviada por WhatsApp ou SMS */
  var f=$('cerere');
  if(f){
    PS.vals=function(n){var out=[];Array.prototype.forEach.call(f.querySelectorAll('[name="'+n+'"]'),function(e){if(e.type==='checkbox'||e.type==='radio'){if(e.checked)out.push(e.value)}else if(e.value.trim())out.push(e.value.trim())});return out};
    PS.val=function(n){return PS.vals(n).join(', ')};
    var pv=$('prev'),st=$('stare'),tel=f.dataset.tel;
    PS.prev=function(){if(pv&&PS.msg)pv.value=PS.msg()};
    f.addEventListener('input',PS.prev);f.addEventListener('change',PS.prev);
    function stare(m,bad){st.textContent=m;st.classList.toggle('bad',!!bad)}
    function verifica(){
      var falta=null;f.querySelectorAll('.camp').forEach(function(c){c.classList.remove('bad')});
      (PS.req||[]).forEach(function(r){if(falta)return;if(!PS.vals(r.n).length){falta=r}});
      if(falta){var el=f.querySelector('[name="'+falta.n+'"]');var c=el.closest('.camp');if(c)c.classList.add('bad');stare(PS.t.apply(null,falta.m),true);el.focus();return false}
      return true}
    f.querySelectorAll('[data-send]').forEach(function(b){b.addEventListener('click',function(){
      if(!verifica())return;var m=encodeURIComponent(PS.msg());
      if(b.dataset.send==='wa'){stare(PS.t('Se deschide WhatsApp cu mesajul gata scris. Apasă „Trimite” acolo.','WhatsApp opens with the message ready. Press “Send” there.','O abrir o WhatsApp com a mensagem pronta. Carrega em “Enviar” lá.'));window.open('https://wa.me/'+tel+'?text='+m,'_blank','noopener')}
      else{stare(PS.t('Se deschide aplicația de SMS cu mesajul gata scris.','Your SMS app opens with the message ready.','A abrir a app de SMS com a mensagem pronta.'));location.href='sms:+'+tel+'?&body='+m}
    })});
    var cp=f.querySelector('[data-copy]');
    if(cp)cp.addEventListener('click',function(){var ok=function(){stare(PS.t('Mesaj copiat.','Message copied.','Mensagem copiada.'))};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(PS.msg()).then(ok,function(){pv.select();stare(PS.t('Selectat: copiază manual.','Selected: copy it manually.','Selecionado: copia manualmente.'))})}else{pv.select();try{document.execCommand('copy');ok()}catch(e){}}});
    f.addEventListener('submit',function(e){e.preventDefault()});
  }

  /* hartă la cerere */
  var hb=$('arata-harta');
  if(hb)hb.addEventListener('click',function(){var h=$('harta'),i=document.createElement('iframe');i.src=hb.dataset.src;i.title=hb.dataset.title.split('|')[idx[L()]];i.loading='lazy';i.referrerPolicy='no-referrer-when-downgrade';h.innerHTML='';h.appendChild(i)});

  var l0=html.dataset.lang||'ro';aplicaLang(l0);sc();PS.observa();
  html.classList.add('pronto');
})();
