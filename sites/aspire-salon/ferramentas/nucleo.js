/* nucleo comum das demos (língua, menu, revelação, mapa, pedido por SMS/WhatsApp) */
(function(){
  var html=document.documentElement,d=document;
  var PS=window.PS={};
  PS.reduz=matchMedia('(prefers-reduced-motion: reduce)').matches;
  PS.$=function(id){return d.getElementById(id)};
  PS.L=function(){var l=html.dataset.lang;return l==='en'||l==='pt'?l:'ro'};
  PS.t=function(ro,en,pt){var l=PS.L();return l==='en'?en:l==='pt'?(pt||en):ro};
  PS.tr=function(s){var a=String(s).split('|');return PS.t(a[0],a[1]||a[0],a[2])};
  PS.esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
  var fns=[];PS.onLang=function(f){fns.push(f)};
  function atrib(){
    d.querySelectorAll('[data-aria]').forEach(function(e){e.setAttribute('aria-label',PS.tr(e.dataset.aria))});
    d.querySelectorAll('[data-alt]').forEach(function(e){e.alt=PS.tr(e.dataset.alt)});
    d.querySelectorAll('[data-ph]').forEach(function(e){e.placeholder=PS.tr(e.dataset.ph)});
    var m=d.querySelector('meta[name="ps-titlu"]');if(m)d.title=PS.tr(m.content);
  }
  PS.seteaza=function(l){
    html.dataset.lang=l;html.lang=l==='pt'?'pt-PT':l;
    d.querySelectorAll('[data-set-lang]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.setLang===l?'true':'false')});
    try{localStorage.setItem('__LSKEY__',l)}catch(e){}
    atrib();fns.forEach(function(f){f()});
  };
  d.querySelectorAll('[data-set-lang]').forEach(function(b){b.addEventListener('click',function(){PS.seteaza(b.dataset.setLang)})});

  /* bara + bara de jos */
  var bara=PS.$('bara'),jos=PS.$('jos');
  function onScroll(){if(bara)bara.classList.toggle('scrolled',scrollY>8);if(jos)jos.classList.toggle('vizibil',scrollY>innerHeight*.45)}
  addEventListener('scroll',onScroll,{passive:true});onScroll();

  /* meniu mobil */
  var burger=d.querySelector('.burger'),meniu=PS.$('meniu');
  if(burger&&meniu){
    var inch=meniu.querySelector('.inchide');
    var desch=function(on){meniu.classList.toggle('deschis',on);burger.setAttribute('aria-expanded',on?'true':'false');d.body.style.overflow=on?'hidden':'';(on?inch:burger).focus()};
    burger.addEventListener('click',function(){desch(true)});
    inch.addEventListener('click',function(){desch(false)});
    meniu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){desch(false)})});
    d.addEventListener('keydown',function(e){if(e.key==='Escape'&&meniu.classList.contains('deschis'))desch(false)});
  }

  /* revelare */
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'}):null;
  d.querySelectorAll('.rv').forEach(function(x){if(io&&!PS.reduz)io.observe(x);else x.classList.add('vis')});

  /* harta la cerere */
  var ah=PS.$('arata-harta');
  if(ah)ah.addEventListener('click',function(){
    var h=PS.$('harta'),f=d.createElement('iframe');
    f.src=ah.dataset.src;f.title=PS.tr(ah.dataset.titlu);f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';
    h.innerHTML='';h.appendChild(f);h.classList.add('cu-harta');
  });

  /* zile: următoarele n zile, fără duminică */
  var ZI={ro:['duminică','luni','marți','miercuri','joi','vineri','sâmbătă'],en:['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],pt:['domingo','segunda','terça','quarta','quinta','sexta','sábado']};
  var LUNA={ro:['ian.','feb.','mar.','apr.','mai','iun.','iul.','aug.','sept.','oct.','nov.','dec.'],en:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],pt:['jan.','fev.','mar.','abr.','mai.','jun.','jul.','ago.','set.','out.','nov.','dez.']};
  PS.ziRo=function(iso){var x=new Date(iso+'T12:00:00');return ZI.ro[x.getDay()]+' '+x.getDate()+' '+LUNA.ro[x.getMonth()]};
  PS.zile=function(cont,nume,n){
    var sel=(cont.querySelector('input:checked')||{}).value,l=PS.L(),out='',x=new Date(),k=0;
    x.setHours(12,0,0,0);
    while(k<n){x.setDate(x.getDate()+1);if(x.getDay()===0)continue;k++;
      var iso=x.getFullYear()+'-'+('0'+(x.getMonth()+1)).slice(-2)+'-'+('0'+x.getDate()).slice(-2);
      out+='<label class="zi"><input type="radio" name="'+nume+'" value="'+iso+'"'+(iso===sel?' checked':'')+' required><span><small>'+ZI[l][x.getDay()].slice(0,l==='en'?3:3)+'</small><b>'+x.getDate()+'</b><small>'+LUNA[l][x.getMonth()]+'</small></span></label>';
    }
    cont.innerHTML=out;
  };

  /* pedido: valida e gera o link de SMS / WhatsApp */
  PS.formular=function(o){
    var f=PS.$(o.form);if(!f)return;
    var prev=o.previz?PS.$(o.previz):null;
    function erori(arata){
      var gresit=[];
      f.querySelectorAll('[data-oblig]').forEach(function(g){
        var ok=!!g.querySelector('input:checked')||(g.querySelector('input[type=text],textarea')&&g.querySelector('input[type=text],textarea').value.trim().length>1);
        var e=g.querySelector('.eroare');
        if(e)e.hidden=ok||!arata;
        g.classList.toggle('are-eroare',!ok&&arata);
        if(!ok)gresit.push(g);
      });
      return gresit;
    }
    function actual(){if(prev)prev.textContent=o.text();erori(false);if(o.schimbat)o.schimbat()}
    f.addEventListener('input',actual);f.addEventListener('change',actual);
    f.addEventListener('submit',function(e){e.preventDefault()});
    f.querySelectorAll('[data-trimite]').forEach(function(a){
      a.addEventListener('click',function(e){
        var g=erori(true);
        if(g.length){e.preventDefault();var p=g[0].querySelector('input,textarea');if(p)p.focus();var st=PS.$(o.stare);if(st)st.textContent=PS.t('Completează câmpurile marcate.','Please fill in the marked fields.','Preencha os campos assinalados.');return}
        var txt=encodeURIComponent(o.text());
        a.href=a.dataset.trimite==='wa'?'https://wa.me/'+o.wa+'?text='+txt:'sms:'+o.tel+'?&body='+txt;
        var st2=PS.$(o.stare);if(st2)st2.textContent=PS.t('Mesajul e gata: verifică-l și apasă Trimite.','Your message is ready: check it and press Send.','A mensagem está pronta: confirme e carregue em Enviar.');
      });
    });
    PS.onLang(actual);actual();
    return {actual:actual};
  };

  PS.porneste=function(){PS.seteaza(PS.L())};
})();
