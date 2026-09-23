(function(){
  var nav=document.querySelector('.nav'),b=document.querySelector('.burger');
  if(b){b.addEventListener('click',function(){var o=nav.classList.toggle('aberta');b.setAttribute('aria-expanded',o?'true':'false');b.querySelector('span').textContent=o?'Fechar':'Menu';});
    document.querySelectorAll('.menu a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('aberta');b.setAttribute('aria-expanded','false');b.querySelector('span').textContent='Menu';});});}
  var sc=function(){nav.classList.toggle('scrolled',window.scrollY>12)};sc();window.addEventListener('scroll',sc,{passive:true});
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    document.querySelectorAll('.rv').forEach(function(el){io.observe(el);});}
  else{document.querySelectorAll('.rv').forEach(function(el){el.classList.add('on');});}
  var mq=document.querySelector('.marquee .faixa');if(mq){mq.innerHTML+=mq.innerHTML;}
  /* a trela: uma linha continua do herói até à chegada, desenhada com o scroll */
  var ini=document.querySelector('[data-trela-inicio]'),fim=document.querySelector('[data-trela-fim]');
  if(ini&&fim&&window.matchMedia('(min-width:1220px)').matches){
    var svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('class','trela');svg.setAttribute('aria-hidden','true');
    var path=document.createElementNS('http://www.w3.org/2000/svg','path');var mosq=document.createElementNS('http://www.w3.org/2000/svg','circle');mosq.setAttribute('class','mosq');mosq.setAttribute('r','9');
    svg.appendChild(path);svg.appendChild(mosq);document.body.appendChild(svg);
    var len=1,total=1,y0=0,y1=0;
    function medir(){
      var H=document.documentElement.scrollHeight,W=document.documentElement.clientWidth;
      svg.setAttribute('height',H);svg.setAttribute('viewBox','0 0 '+W+' '+H);
      var a=ini.getBoundingClientRect(),b=fim.getBoundingClientRect(),sy=window.scrollY;
      var x0=a.left+a.width*0.42,ya=a.bottom+sy-40; var x1=b.left+18,yb=b.top+sy+18;
      y0=ya;y1=yb;
      var cont=(W-Math.min(W,1160))/2+40; var gut=Math.round(cont*0.42),bulge2=Math.round(cont*0.78); // corre pela margem esquerda, nunca sobre o texto
      var d='M'+x0+' '+ya+' C '+x0+' '+(ya+180)+', '+gut+' '+(ya+120)+', '+gut+' '+(ya+320);
      var y=ya+320,k=0; while(y<yb-260){var s=Math.min(520,yb-260-y);var bul=(k%2?bulge2:gut+10);d+=' S '+bul+' '+(y+s*0.55)+', '+gut+' '+(y+s);y+=s;k++;}
      d+=' S '+(gut)+' '+(yb-80)+', '+x1+' '+yb;
      path.setAttribute('d',d);len=path.getTotalLength();total=len;
      path.style.setProperty('--len',len);mosq.setAttribute('cx',x0);mosq.setAttribute('cy',ya);
      desenhar();
    }
    function desenhar(){
      var sy=window.scrollY+window.innerHeight*0.72;var p=(sy-y0)/(y1-y0);p=Math.max(0,Math.min(1,p));
      path.style.setProperty('--off',total*(1-p));
    }
    var t;window.addEventListener('resize',function(){clearTimeout(t);t=setTimeout(medir,120)});
    window.addEventListener('scroll',desenhar,{passive:true});
    if(document.fonts&&document.fonts.ready){document.fonts.ready.then(medir)}else{medir()}
    window.addEventListener('load',function(){setTimeout(medir,300)});
    if('ResizeObserver' in window){var ro=new ResizeObserver(function(){clearTimeout(t);t=setTimeout(medir,80)});ro.observe(document.body);}
  }
})();
