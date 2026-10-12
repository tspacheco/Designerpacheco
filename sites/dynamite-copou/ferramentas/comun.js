/* comun: limbă, meniu, revelare, marcare (RO/EN/PT), hartă la cerere */
(function(){
  var html=document.documentElement, CFG=window.CFG, $=function(i){return document.getElementById(i)};
  var reduz=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var L=function(){var l=html.dataset.lang;return l==='en'||l==='pt'?l:'ro'};
  var t=function(r,e,p){var l=L();return l==='en'?e:l==='pt'?p:r};
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
  var tri=function(o){return '<span lang="ro">'+esc(o.ro)+'</span><span lang="en">'+esc(o.en)+'</span><span lang="pt">'+esc(o.pt)+'</span>'};
  window.PS={L:L,t:t,esc:esc,tri:tri,reduz:reduz,$:$};
  var locale={ro:'ro-RO',en:'en-GB',pt:'pt-PT'};

  /* ---------- limba ---------- */
  function atrib(){
    document.querySelectorAll('[data-alt]').forEach(function(e){var p=e.dataset.alt.split('|');e.alt=p[{ro:0,en:1,pt:2}[L()]]||p[0]});
    document.querySelectorAll('[data-aria]').forEach(function(e){var p=e.dataset.aria.split('|');e.setAttribute('aria-label',p[{ro:0,en:1,pt:2}[L()]]||p[0])});
    document.querySelectorAll('[data-nml3]').forEach(function(e){var p=e.dataset.nml3.split('|');e.setAttribute('data-nml',p[{ro:0,en:1,pt:2}[L()]]||p[0])});
  }
  function seteaza(l){
    html.dataset.lang=l;html.lang=l==='pt'?'pt-PT':l;
    document.querySelectorAll('[data-set-lang]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.setLang===l?'true':'false')});
    try{localStorage.setItem('__LSKEY__',l)}catch(e){}
    atrib();zile();rezumat();
    if(window.PS.onLang)window.PS.onLang(l);
  }
  document.querySelectorAll('[data-set-lang]').forEach(function(b){b.addEventListener('click',function(){seteaza(b.dataset.setLang)})});

  /* ---------- meniu mobil ---------- */
  var burger=document.querySelector('.burger'),meniu=$('meniu'),inchide=meniu.querySelector('.inchide');
  function deschide(d){meniu.classList.toggle('deschis',d);burger.setAttribute('aria-expanded',d?'true':'false');document.body.style.overflow=d?'hidden':'';(d?inchide:burger).focus()}
  burger.addEventListener('click',function(){deschide(true)});
  inchide.addEventListener('click',function(){deschide(false)});
  meniu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){deschide(false)})});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&meniu.classList.contains('deschis'))deschide(false)});

  /* ---------- revelare + bară ---------- */
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'}):null;
  document.querySelectorAll('.rv').forEach(function(x){if(io&&!reduz)io.observe(x);else x.classList.add('vis')});
  var bara=$('bara'),jos=$('jos');
  function onScroll(){bara.classList.toggle('scrolled',scrollY>8);if(jos)jos.classList.toggle('vizibil',scrollY>innerHeight*.5);if(window.PS.onScroll)window.PS.onScroll()}
  addEventListener('scroll',onScroll,{passive:true});addEventListener('resize',onScroll);

  /* ---------- marcare ---------- */
  var st={serv:null,zi:null,ora:null};
  var form=$('marcare');
  function chip(name,val,html_,extra){return '<label class="chip"><input type="radio" name="'+name+'" value="'+esc(val)+'"'+(extra||'')+'><span>'+html_+'</span></label>'}
  function servicii(){
    $('b-serv').innerHTML=CFG.servicii.map(function(s,i){return chip('serv',s.id,'<b>'+tri(s)+'</b>'+(s.nota?'<small>'+tri(s.nota)+'</small>':''))}).join('');
  }
  function zile(){
    var box=$('b-zi');if(!box)return;
    var ro1=new Intl.DateTimeFormat('ro-RO',{weekday:'long'}),ro2=new Intl.DateTimeFormat('ro-RO',{day:'numeric',month:'long'}),keep=st.zi,d=new Date(),out=[],n=0,fmt=new Intl.DateTimeFormat(locale[L()],{weekday:'short'}),fm=new Intl.DateTimeFormat(locale[L()],{day:'numeric',month:'short'});
    d.setHours(12,0,0,0);
    while(out.length<CFG.nzile&&n<40){
      d=new Date(d.getTime()+864e5);n++;
      if(CFG.inchis.indexOf(d.getDay())>-1)continue;
      var iso=d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
      var w=fmt.format(d).replace('.','');
      out.push(chip('zi',iso,'<small>'+esc(w)+'</small><b>'+esc(fm.format(d).replace('.',''))+'</b>',keep===iso?' checked':'')+'');
      out[out.length-1]=out[out.length-1].replace('<input','<input data-w="'+d.getDay()+'" data-lb="'+esc(w+' '+fm.format(d).replace('.',''))+'" data-et="'+esc(ro1.format(d)+', '+ro2.format(d))+'"');
    }
    box.innerHTML=out.join('');
  }
  function ore(){var box=$('b-ora');if(!box||!CFG.ore)return;box.innerHTML=CFG.ore.map(function(o){return chip('ora',o,'<b>'+o+'</b>')}).join('')}
  function sel(n){var e=form.querySelector('input[name='+n+']:checked');return e}
  function msg(){
    var s=sel('serv'),z=sel('zi'),o=sel('ora'),nm=$('b-nume').value.trim(),nt=$('b-nota').value.trim();
    var sv=s?CFG.servicii.filter(function(x){return x.id===s.value})[0].ro:'';
    var m='Bună ziua! Aș dori o programare la '+CFG.nume+': '+sv+(z?', '+z.dataset.et:'')+(CFG.ore&&o?', ora '+o.value:'')+'.';
    if(nt)m+=' '+nt;
    if(nm)m+=' Nume: '+nm+'.';
    m+=' Vă rog să-mi confirmați.';
    return m;
  }
  function lipsa(){var l=[];if(!sel('serv'))l.push('serv');if(!sel('zi'))l.push('zi');if(CFG.ore&&!sel('ora'))l.push('ora');return l}
  function rezumat(){
    var s=sel('serv'),z=sel('zi'),o=sel('ora'),r=$('b-rez');if(!r)return;
    var sv=s?CFG.servicii.filter(function(x){return x.id===s.value})[0]:null;
    var parts=[];
    if(sv)parts.push('<b>'+tri(sv)+'</b>');
    if(z)parts.push(esc(z.dataset.lb));
    if(CFG.ore&&o)parts.push(esc(o.value));
    r.innerHTML=parts.length?parts.join(' · '):t('Alege serviciul, ziua'+(CFG.ore?' și ora':''),'Pick a service, a day'+(CFG.ore?' and a time':''),'Escolha o serviço, o dia'+(CFG.ore?' e a hora':''));
    r.classList.toggle('plin',!lipsa().length);
    var m=encodeURIComponent(msg());
    $('b-wa').href='https://wa.me/'+CFG.tel+'?text='+m;
    $('b-sms').href='sms:+'+CFG.tel+'?&body='+m;
    var ok=!lipsa().length;
    ['b-wa','b-sms'].forEach(function(i){$(i).setAttribute('aria-disabled',ok?'false':'true')});
    if(window.PS.onForm)window.PS.onForm(ok,s,z,o);
  }
  function eroare(){
    var l=lipsa(),e=$('b-err');
    if(!l.length){e.hidden=true;return false}
    var nm={serv:t('serviciul','the service','o serviço'),zi:t('ziua','the day','o dia'),ora:t('ora','the time','a hora')};
    e.hidden=false;e.textContent=t('Mai alege ','Still to pick: ','Falta escolher: ')+l.map(function(x){return nm[x]}).join(', ')+'.';
    var g=$('b-'+({serv:'serv',zi:'zi',ora:'ora'}[l[0]]));var f=g.querySelector('input');if(f)f.focus();
    return true;
  }
  if(form){
    servicii();zile();ore();
    form.addEventListener('change',function(e){if(e.target.name){st[e.target.name]=e.target.value}$('b-err').hidden=true;rezumat();if(window.PS.onPick)window.PS.onPick(e.target)});
    form.addEventListener('input',rezumat);
    form.addEventListener('submit',function(e){e.preventDefault()});
    ['b-wa','b-sms'].forEach(function(i){$(i).addEventListener('click',function(e){if(eroare()){e.preventDefault()}})});
    var pre=document.querySelectorAll('[data-pre]');
    pre.forEach(function(a){a.addEventListener('click',function(){var r=form.querySelector('input[name=serv][value='+a.dataset.pre+']');if(r){r.checked=true;st.serv=r.value;rezumat();if(window.PS.onPick)window.PS.onPick(r)}})});
  }

  /* ---------- harta la cerere ---------- */
  var bh=$('arata-harta');
  if(bh)bh.addEventListener('click',function(){
    var h=$('harta'),f=document.createElement('iframe');
    f.src='https://www.google.com/maps?q='+CFG.geo+'&z=17&output=embed';
    f.title=t('Hartă: '+CFG.nume,'Map: '+CFG.nume,'Mapa: '+CFG.nume);f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';
    h.innerHTML='';h.appendChild(f);
  });

  window.PS.init=function(){seteaza(L());onScroll()};
})();
