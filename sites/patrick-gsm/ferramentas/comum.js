var html=document.documentElement,reduz=matchMedia('(prefers-reduced-motion: reduce)').matches;
var $=function(id){return document.getElementById(id)};
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var L=function(){var l=html.dataset.lang;return l==='en'||l==='pt'?l:'ro'};
var t=function(ro,en,pt){var l=L();return l==='en'?en:l==='pt'?(pt||en):ro};
var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
function seteazaLimba(l){
  html.dataset.lang=l;html.lang=l==='pt'?'pt-PT':l;
  try{localStorage.setItem('__LSKEY__',l)}catch(e){}
  $$('[data-set-lang]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.setLang===l?'true':'false')});
  $$('[data-aria]').forEach(function(e){var a=e.dataset.aria.split('|');e.setAttribute('aria-label',l==='en'?a[1]:l==='pt'?a[2]:a[0])});
  $$('[data-alt]').forEach(function(e){var a=e.dataset.alt.split('|');e.setAttribute('alt',l==='en'?a[1]:l==='pt'?a[2]:a[0])});
  $$('[data-ph]').forEach(function(e){var a=e.dataset.ph.split('|');e.setAttribute('placeholder',l==='en'?a[1]:l==='pt'?a[2]:a[0])});
  var ti=document.querySelector('title[data-t]');if(ti){var a=ti.dataset.t.split('|');document.title=l==='en'?a[1]:l==='pt'?a[2]:a[0]}
  if(window.laLimba)window.laLimba(l);
}
$$('[data-set-lang]').forEach(function(b){b.addEventListener('click',function(){seteazaLimba(b.dataset.setLang)})});
function trimite(canal,txt,tel,wa){
  if(canal==='wa'){window.open('https://wa.me/'+wa+'?text='+encodeURIComponent(txt),'_blank','noopener')}
  else{location.href='sms:'+tel+'?&body='+encodeURIComponent(txt)}
}
function revela(){
  var els=$$('[data-rev]');
  if(reduz||!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('vz')});return}
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('vz');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
  els.forEach(function(e){io.observe(e)});
}
