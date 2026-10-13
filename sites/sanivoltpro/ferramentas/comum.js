/* base partilhada: limbă, reveal, scroll, trimitere, lightbox, hartă */
(function(){
'use strict';
var html=document.documentElement,PS=window.PS={hooks:[],sc:[]};
PS.reduz=matchMedia('(prefers-reduced-motion: reduce)').matches;
PS.L=function(){var l=html.dataset.lang;return l==='en'||l==='pt'?l:'ro'};
PS.t=function(ro,en,pt){var l=PS.L();return l==='en'?en:l==='pt'?(pt||en):ro};
PS.tr=function(s){var a=s.split('|');return PS.t(a[0],a[1],a[2])};
PS.$=function(id){return document.getElementById(id)};
PS.esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
PS.clamp=function(x,a,b){return x<a?a:x>b?b:x};
PS.bi=function(a){return '<span lang="ro">'+a[0]+'</span><span lang="en">'+a[1]+'</span><span lang="pt">'+a[2]+'</span>'};
PS.atrib=function(){
  document.querySelectorAll('[data-aria]').forEach(function(e){e.setAttribute('aria-label',PS.tr(e.dataset.aria))});
  document.querySelectorAll('[data-ph]').forEach(function(e){e.setAttribute('placeholder',PS.tr(e.dataset.ph))});
  document.querySelectorAll('img[data-alt]').forEach(function(e){e.setAttribute('alt',PS.tr(e.dataset.alt))});
  if(PS.titles)document.title=PS.t(PS.titles[0],PS.titles[1],PS.titles[2]);
};
PS.seteaza=function(l){
  html.dataset.lang=l;html.lang=l==='pt'?'pt-PT':l;
  document.querySelectorAll('[data-set-lang]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.setLang===l?'true':'false')});
  try{localStorage.setItem('__LSKEY__',l)}catch(e){}
  PS.atrib();PS.hooks.forEach(function(f){f(l)});
};
/* chips: items=[[valoare RO, ro, en, pt], ...] */
PS.chips=function(el,name,tip,items){
  el.innerHTML=items.map(function(it,i){
    return '<label class="chip"><input type="'+tip+'" name="'+name+'" value="'+PS.esc(it[0])+'"'+(tip==='radio'&&i===0&&el.dataset.def!=='none'?' checked':'')+'><span>'+PS.bi([it[1],it[2],it[3]])+'</span></label>';
  }).join('');
};
/* reveal */
var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'}):null;
PS.observa=function(root){(root||document).querySelectorAll('.rv:not(.vis)').forEach(function(x){if(io)io.observe(x);else x.classList.add('vis')})};
/* scroll (rAF) */
var tick=false;
PS.run=function(){tick=false;PS.sc.forEach(function(f){f()})};
addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(PS.run)}},{passive:true});
addEventListener('resize',function(){if(!tick){tick=true;requestAnimationFrame(PS.run)}});
/* trimitere: wa = https://wa.me, sms = sms: */
PS.send=function(canal,tel,wa,msg){
  if(canal==='wa'){var u='https://wa.me/'+wa+'?text='+encodeURIComponent(msg);var w=window.open(u,'_blank','noopener');if(!w)location.href=u}
  else location.href='sms:'+tel+'?&body='+encodeURIComponent(msg);
};
/* lightbox */
PS.lightbox=function(sel){
  var items=[].slice.call(document.querySelectorAll(sel)),i=0,ant=null;
  if(!items.length)return;
  var lb=document.createElement('div');lb.className='lb';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');
  lb.innerHTML='<button type="button" class="lb-x" data-k="x">×</button><button type="button" class="lb-p" data-k="p">‹</button><figure><img alt=""><figcaption></figcaption></figure><button type="button" class="lb-n" data-k="n">›</button>';
  document.body.appendChild(lb);
  var im=lb.querySelector('img'),cap=lb.querySelector('figcaption'),bs=lb.querySelectorAll('button');
  function lab(){bs[0].setAttribute('aria-label',PS.t('Închide','Close','Fechar'));bs[1].setAttribute('aria-label',PS.t('Anterioară','Previous','Anterior'));bs[2].setAttribute('aria-label',PS.t('Următoarea','Next','Seguinte'));lb.setAttribute('aria-label',PS.t('Fotografie mărită','Enlarged photo','Fotografia ampliada'))}
  function arata(n){i=(n+items.length)%items.length;var it=items[i],fc=it.querySelector('figcaption'),a=it.querySelector('img');im.src=it.dataset.lb;im.alt=a?a.alt:'';cap.innerHTML=fc?fc.innerHTML:'';lab()}
  function deschide(n){ant=document.activeElement;arata(n);lb.classList.add('on');document.body.style.overflow='hidden';bs[0].focus()}
  function inchide(){lb.classList.remove('on');document.body.style.overflow='';if(ant)ant.focus()}
  items.forEach(function(it,n){it.addEventListener('click',function(){deschide(n)})});
  lb.addEventListener('click',function(e){var k=e.target.dataset&&e.target.dataset.k;if(k==='x'||e.target===lb)inchide();if(k==='p')arata(i-1);if(k==='n')arata(i+1)});
  document.addEventListener('keydown',function(e){
    if(!lb.classList.contains('on'))return;
    if(e.key==='Escape')inchide();
    if(e.key==='ArrowLeft')arata(i-1);
    if(e.key==='ArrowRight')arata(i+1);
    if(e.key==='Tab'){var l=[bs[0],bs[1],bs[2]],ix=l.indexOf(document.activeElement);e.preventDefault();l[(ix+(e.shiftKey?-1:1)+3)%3].focus()}
  });
  var x0=null;lb.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
  lb.addEventListener('touchend',function(e){if(x0===null)return;var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>50)arata(i+(d<0?1:-1));x0=null});
};
/* hartă la cerere */
PS.harta=function(btn,box,lat,lng,titlu){
  btn.addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.src='https://www.google.com/maps?q='+lat+','+lng+'&z=17&output=embed';
    f.title=titlu;f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';box.innerHTML='';box.appendChild(f);btn.hidden=true;
  });
};
/* progresso 0..1 de um elemento a atravessar o ecrã */
PS.prog=function(el){var r=el.getBoundingClientRect(),h=innerHeight;return PS.clamp((h-r.top)/(h+r.height),0,1)};
/* arranque comum */
PS.init=function(){
  document.querySelectorAll('[data-set-lang]').forEach(function(b){b.addEventListener('click',function(){PS.seteaza(b.dataset.setLang)})});
  var bara=PS.$('bara'),jos=PS.$('jos');
  PS.sc.push(function(){if(bara)bara.classList.toggle('scrolled',scrollY>8);if(jos)jos.classList.toggle('vizibil',scrollY>innerHeight*.5)});
  PS.seteaza(PS.L());PS.observa();PS.run();
};
})();
