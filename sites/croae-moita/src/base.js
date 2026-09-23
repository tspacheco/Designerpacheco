(function(){
  var nav=document.querySelector('.nav'),b=document.querySelector('.burger');
  if(b){b.addEventListener('click',function(){var o=nav.classList.toggle('aberta');b.setAttribute('aria-expanded',o?'true':'false');b.querySelector('span').textContent=o?'Fechar':'Menu';});
    document.querySelectorAll('.menu a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('aberta');b.setAttribute('aria-expanded','false');b.querySelector('span').textContent='Menu';});});}
  var sc=function(){nav.classList.toggle('scrolled',window.scrollY>12)};sc();window.addEventListener('scroll',sc,{passive:true});
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    document.querySelectorAll('.rv').forEach(function(el){io.observe(el);});}
  else{document.querySelectorAll('.rv').forEach(function(el){el.classList.add('on');});}
  var mq=document.querySelector('.marquee .faixa');if(mq){mq.innerHTML+=mq.innerHTML;}
})();
