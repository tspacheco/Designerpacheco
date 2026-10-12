  var html=document.documentElement,reduz=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $=function(i){return document.getElementById(i)};
  var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  function L(){var l=html.dataset.lang;return l==='en'||l==='pt'?l:'ro'}
  function t(ro,en,pt){var l=L();return l==='en'?en:l==='pt'?pt:ro}
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'}):null;
  $$('.rv').forEach(function(x){if(io)io.observe(x);else x.classList.add('vis')});
  function atrib(){
    $$('[data-aria]').forEach(function(e){e.setAttribute('aria-label',t.apply(null,e.dataset.aria.split('|')))});
    $$('[data-alt]').forEach(function(e){e.setAttribute('alt',t.apply(null,e.dataset.alt.split('|')))});
    $$('[data-ph]').forEach(function(e){e.setAttribute('placeholder',t.apply(null,e.dataset.ph.split('|')))});
  }
  var ganchos=[];
  function aoLimba(f){ganchos.push(f)}
  function seteaza(l){
    html.dataset.lang=l;html.lang=l==='pt'?'pt-PT':l;
    $$('[data-set-lang]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.setLang===l?'true':'false')});
    try{localStorage.setItem('__LSKEY__',l)}catch(e){}
    atrib();ganchos.forEach(function(f){f()});
  }
  $$('[data-set-lang]').forEach(function(b){b.addEventListener('click',function(){seteaza(b.dataset.setLang)})});
  var mapaB=$('arata-harta');
  if(mapaB)mapaB.addEventListener('click',function(){
    var h=$('harta'),f=document.createElement('iframe');
    f.src=mapaB.dataset.src;f.title=mapaB.dataset.titulo;f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';h.innerHTML='';h.appendChild(f);
  });
  var DIAS={ro:['dum','lun','mar','mie','joi','vin','sâm'],en:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],pt:['dom','seg','ter','qua','qui','sex','sáb']};
  var DIAS_RO=['duminică','luni','marți','miercuri','joi','vineri','sâmbătă'];
  function pad(n){return n<10?'0'+n:''+n}
  function zile(n){var o=[],d=new Date();d.setHours(12,0,0,0);for(var i=0;i<n;i++){var x=new Date(d.getTime());x.setDate(d.getDate()+i);o.push(x)}return o}
  function dataRo(x,i){return (i===0?'azi':i===1?'mâine':DIAS_RO[x.getDay()])+' '+pad(x.getDate())+'.'+pad(x.getMonth()+1)}
  function link(tel,msg){return {wa:'https://wa.me/'+tel.replace('+','')+'?text='+encodeURIComponent(msg),sms:'sms:'+tel+'?&body='+encodeURIComponent(msg)}}
