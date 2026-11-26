(() => {
  'use strict';
  const ui=JSON.parse(document.querySelector('#ui-data').textContent), locale=document.documentElement.lang;
  const $=(s,root=document)=>root.querySelector(s), $$=(s,root=document)=>[...root.querySelectorAll(s)];
  const safeStore=(storage,key,value)=>{try{if(value===undefined)return window[storage].getItem(key);window[storage].setItem(key,value);return true;}catch(_){return null;}};
  const language=$('#language-switch');
  const updateLanguage=()=>{const target=new URL(language.getAttribute('href'),location.origin);const params=new URLSearchParams(location.search);if(target.searchParams.has("translation"))params.set("translation",target.searchParams.get("translation"));target.search=params.toString();target.hash=location.hash;language.href=target.pathname+target.search+target.hash;};
  updateLanguage();
  language.addEventListener('click',()=>{safeStore('localStorage','language',locale==='en'?'zh-CN':'en');safeStore('sessionStorage','intro-seen','1');});
  if(location.pathname==='/en/')safeStore('localStorage','language','en');
  $('#theme-toggle').addEventListener('click',()=>{const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=theme;safeStore('localStorage','theme',theme);});
  const replaceURL=url=>{history.replaceState(null,'',url);updateLanguage();};

  // Static links remain usable when script is disabled; enhancement records the route.
  const validReturn=raw=>{try{const u=new URL(raw,location.origin);return u.origin===location.origin && /^\/(en\/)?(?:knowledge|notes)\//.test(u.pathname)?u:null;}catch(_){return null;}};
  $$('[data-return-link]').forEach(a=>a.addEventListener('click',()=>{const source=new URL(location.href);const item=a.closest('[data-filter-item]');if(item?.id)source.hash=item.id;safeStore('sessionStorage','scroll:'+source.pathname+source.search,String(scrollY));const dest=new URL(a.href);dest.searchParams.set('from',source.pathname+source.search+source.hash);a.href=dest.pathname+dest.search+dest.hash;}));
  const from=validReturn(new URL(location.href).searchParams.get('from')||'');
  if(from)$$('[data-back]').forEach(a=>{let p=from.pathname.replace(/^\/en\//,'/');if(locale==='en')p='/en'+p;a.href=p+from.search+from.hash;if(a.hasAttribute('data-blog-back'))a.textContent='← '+ui.back;});
  if(!location.hash){const saved=safeStore('sessionStorage','scroll:'+location.pathname+location.search);if(saved)requestAnimationFrame(()=>scrollTo(0,Number(saved)));}
  const revealHash=()=>{let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch(_){return;}if(target){let parent=target.parentElement;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}};

  // Search uses the generated locale-specific content index, never fabricated posts.
  const dialog=$('#search-dialog'),input=$('#global-search'),list=$('#search-results'),status=$('#search-status');
  let index=null,loading=null,searchOpener=null;
  const addText=(tag,text,parent,className)=>{const el=document.createElement(tag);el.textContent=text;if(className)el.className=className;parent.append(el);return el;};
  async function search(){
    try {
      if(!index){loading??=fetch('/assets/search.'+locale+'.json').then(r=>{if(!r.ok)throw Error('index');return r.json();});index=await loading;}
      const words=input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      const found=index.filter(x=>words.every(w=>(x.title+' '+x.summary+' '+x.tags).toLowerCase().includes(w)));
      list.replaceChildren();status.textContent=found.length+' '+ui.results;
      found.slice(0,60).forEach(x=>{const li=addText('li','',list),a=addText('a','',li);a.href=x.url;if(x.contentLocale)a.lang=x.contentLocale;addText('strong',x.title,a);addText('p',x.summary,a);addText('small',x.kind+' · '+ui[x.status]+(x.contentLocale?' · '+x.contentLocale:''),a);});
      if(!found.length)status.textContent=ui.no_results;
    }catch(_){status.textContent=ui.search_error;loading=null;}
  }
  function openSearch(opener){searchOpener=opener||document.activeElement;dialog.showModal();input.focus();search();}
  $$('.search-open').forEach(b=>b.addEventListener('click',()=>openSearch(b)));
  input.addEventListener('input',search);$('[data-close]',dialog).addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',()=>searchOpener?.focus());
  dialog.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();dialog.close();}});
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
  document.addEventListener('keydown',e=>{if((e.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(e.target.tagName))||((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k')){e.preventDefault();if(!dialog.open)openSearch();}});

  // Both views are pre-rendered. URL controls, stage state, and popstate share one path.
  const explorer=$('[data-explorer]');
  if(explorer){
    const defaultView=explorer.dataset.explorer==='track'?'history':'topic';
    const controls=$$('input[name],select[name]',explorer),buttons=$$('[data-view]',explorer),panels=$$('[data-panel]',explorer);
    let view=defaultView,restoring=false;
    function filter(write=true){
      const params=new URL(location.href).searchParams;
      const terms=($('input[name=q]',explorer).value||'').trim().toLowerCase().split(/\s+/).filter(Boolean);
      let count=0;
      panels.forEach(panel=>{
        const active=panel.dataset.panel===view;panel.hidden=!active;
        $$('[data-filter-item]',panel).forEach(item=>{
          const text=(item.dataset.search||'').toLowerCase();
          const matches=terms.every(w=>text.includes(w))&&controls.filter(c=>c.name!=='q'&&c.value).every(c=>{const field=c.name==='tag'?'tags':c.name;return (item.dataset[field]||'').split(/\s+/).includes(c.value);});
          item.hidden=!matches;if(matches&&active)count++;
        });
        $$('details[data-stage]',panel).forEach(group=>{group.hidden=!$$('[data-filter-item]',group).some(x=>!x.hidden);if(controls.some(c=>c.value)&&!group.hidden)group.open=true;});
      });
      buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
      $('[data-results]',explorer).textContent=count+' '+ui.results;$('[data-empty]',explorer).hidden=count>0;
      if(write){params.set('view',view);controls.forEach(c=>{if(c.value)params.set(c.name,c.value);else params.delete(c.name);});const u=new URL(location.href);u.search=params;replaceURL(u);}
    }
    function restore(){
      restoring=true;const p=new URL(location.href).searchParams;view=buttons.some(b=>b.dataset.view===p.get('view'))?p.get('view'):defaultView;
      controls.forEach(c=>{c.value=p.get(c.name)||'';if(c.tagName==='SELECT'&&c.selectedIndex<0)c.value='';});
      const closed=(p.get('closed')||'').split(',');$$('details[data-stage]',explorer).forEach(d=>{if(p.has('closed'))d.open=!closed.includes(d.dataset.stage);});
      filter(false);requestAnimationFrame(()=>{restoring=false;revealHash();});
    }
    controls.forEach(c=>c.addEventListener(c.tagName==='INPUT'?'input':'change',()=>filter()));
    buttons.forEach(b=>b.addEventListener('click',()=>{view=b.dataset.view;const u=new URL(location.href);if(explorer.dataset.explorer==='track'&&/^#(?:learn-)?node-/.test(u.hash)){u.hash=view==='learning'?u.hash.replace(/^#(?:learn-)?node-/,'#learn-node-'):u.hash.replace(/^#(?:learn-)?node-/,'#node-');replaceURL(u);}filter();revealHash();}));
    $$('[data-reset]',explorer).forEach(b=>b.addEventListener('click',()=>{controls.forEach(c=>c.value='');$$('details[data-stage]',explorer).forEach(d=>d.open=true);const u=new URL(location.href);u.searchParams.delete('closed');u.hash='';replaceURL(u);filter();}));
    $$('details[data-stage]',explorer).forEach(d=>d.addEventListener('toggle',()=>{if(restoring||controls.some(c=>c.value))return;const u=new URL(location.href);u.searchParams.set('closed',$$('details[data-stage]',explorer).filter(x=>!x.open).map(x=>x.dataset.stage).join(','));replaceURL(u);}));
    $$('[data-year-jump]',explorer).forEach(a=>a.addEventListener('click',e=>{const panel=panels.find(p=>p.dataset.panel===view),target=$$('[data-filter-item]',panel).find(n=>!n.hidden&&n.dataset.year===a.dataset.yearJump);if(!target){e.preventDefault();return;}if(target){e.preventDefault();const d=target.closest('details');if(d)d.open=true;const u=new URL(location.href);u.hash=target.id;replaceURL(u);target.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});}}));
    window.addEventListener('popstate',restore);restore();
  }else revealHash();
  window.addEventListener('hashchange',revealHash);

  // Home modules reveal in reading order; below-the-fold modules wait for scroll.
  function createHomeEntrance(){
    if(!$('.hero'))return {prepare(){},start(){},stop(){},showAll(){}};
    const items=$$('.site-header, .hero-copy > *, .site-footer');
    let observer=null,started=false;
    const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
    const reveal=(item,delay=0)=>{item.style.setProperty('--reveal-delay',delay+'ms');item.classList.add('is-revealed');observer?.unobserve(item);};
    const showAll=()=>{observer?.disconnect();observer=null;items.forEach(item=>reveal(item));document.documentElement.classList.remove('home-motion');started=true;};
    const prepare=()=>{
      observer?.disconnect();observer=null;started=false;
      if(reduced()||location.hash){showAll();return;}
      items.forEach(item=>{item.setAttribute('data-home-reveal','');item.classList.remove('is-revealed');item.style.removeProperty('--reveal-delay');});
      document.documentElement.classList.add('home-motion');
    };
    const start=()=>{
      if(started)return;
      if(reduced()||location.hash||!('IntersectionObserver' in window)){showAll();return;}
      if(!document.documentElement.classList.contains('home-motion'))prepare();
      started=true;
      observer=new IntersectionObserver(entries=>{
        const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>items.indexOf(a.target)-items.indexOf(b.target));
        visible.forEach((entry,index)=>reveal(entry.target,Math.min(index*85,510)));
      },{threshold:0.08,rootMargin:'0px 0px -24px 0px'});
      items.forEach(item=>observer.observe(item));
    };
    document.addEventListener('focusin',event=>{const item=event.target.closest('[data-home-reveal]');if(item)reveal(item);});
    return {prepare,start,showAll,stop:showAll};
  }
  const homeEntrance=createHomeEntrance();

  // This terminal is a short visual narrative. No shell commands are executed.
  const intro=$('#intro'),script=$('#intro-script');let timer=null,introOpener=null,shatterLayer=null,shatterAnimations=[];
  const cleanShatter=()=>{shatterAnimations.forEach(animation=>animation.cancel());shatterAnimations=[];shatterLayer?.remove();shatterLayer=null;intro.classList.remove('is-shattering');};
  const finishIntro=()=>{clearTimeout(timer);timer=null;cleanShatter();document.documentElement.classList.remove('intro-open');if(intro.open)intro.close();homeEntrance.start();};
  intro.addEventListener('cancel',e=>{e.preventDefault();finishIntro();});
  intro.addEventListener('close',()=>{clearTimeout(timer);cleanShatter();document.documentElement.classList.remove('intro-open');homeEntrance.start();if(introOpener)introOpener.focus({preventScroll:true});else $('#main').focus({preventScroll:true});});
  $('#skip-intro').addEventListener('click',finishIntro);
  function shatterIntro(){
    if(!intro.open)return;
    if(matchMedia('(prefers-reduced-motion: reduce)').matches||!Element.prototype.animate){finishIntro();return;}
    clearTimeout(timer);intro.dataset.stage='shattering';
    const width=intro.clientWidth,height=intro.clientHeight,body=$('.intro-body',intro),rect=body.getBoundingClientRect();
    const columns=width<600?3:5,rows=3,points=[];
    // Shared, offset vertices produce contiguous irregular triangular pieces.
    for(let y=0;y<=rows;y++){
      points[y]=[];
      for(let x=0;x<=columns;x++)points[y][x]=[
        x*width/columns+(x>0&&x<columns?Math.sin(x*13+y*7)*width/columns*.23:0),
        y*height/rows+(y>0&&y<rows?Math.cos(x*9+y*11)*height/rows*.2:0)
      ];
    }
    shatterLayer=document.createElement('div');shatterLayer.className='terminal-shatter';shatterLayer.setAttribute('aria-hidden','true');shatterLayer.inert=true;
    const cracks=document.createElementNS('http://www.w3.org/2000/svg','svg');cracks.setAttribute('viewBox',`0 0 ${width} ${height}`);cracks.classList.add('terminal-cracks');
    let index=0;
    for(let y=0;y<rows;y++)for(let x=0;x<columns;x++){
      const a=points[y][x],b=points[y][x+1],c=points[y+1][x],d=points[y+1][x+1];
      const triangles=(x+y)%2?[[a,b,c],[b,d,c]]:[[a,b,d],[a,d,c]];
      for(const vertices of triangles){
        const left=Math.min(...vertices.map(p=>p[0])),top=Math.min(...vertices.map(p=>p[1]));
        const w=Math.max(...vertices.map(p=>p[0]))-left,h=Math.max(...vertices.map(p=>p[1]))-top;
        const shard=document.createElement('div');shard.className='terminal-shard';
        Object.assign(shard.style,{left:left+'px',top:top+'px',width:w+'px',height:h+'px',clipPath:'polygon('+vertices.map(p=>`${(p[0]-left)/w*100}% ${(p[1]-top)/h*100}%`).join(',')+')'});
        const snapshot=body.cloneNode(true);snapshot.removeAttribute('id');snapshot.querySelectorAll('[id]').forEach(el=>el.removeAttribute('id'));
        Object.assign(snapshot.style,{position:'absolute',left:(rect.left-left)+'px',top:(rect.top-top)+'px',width:rect.width+'px',height:rect.height+'px',minHeight:'0',margin:'0'});
        shard.append(snapshot);shatterLayer.append(shard);
        const outline=document.createElementNS('http://www.w3.org/2000/svg','polygon');outline.setAttribute('points',vertices.map(p=>p.join(',')).join(' '));cracks.append(outline);
        const drift=((left+w/2)-width/2)*.35+Math.sin(index*12)*60,rotation=Math.sin(index*7+2)*24;
        shatterAnimations.push(shard.animate([
          {transform:'translate3d(0,0,0) rotate(0deg)',opacity:1},
          {transform:`translate3d(${drift*.12}px,${height*.09}px,0) rotate(${rotation*.15}deg)`,opacity:1,offset:.28},
          {transform:`translate3d(${drift}px,${height+h+100}px,0) rotate(${rotation}deg)`,opacity:0}
        ],{duration:980+(index%4)*65,delay:140+(index%5)*35,easing:'cubic-bezier(.32,.02,.72,.45)',fill:'both'}));
        index++;
      }
    }
    shatterLayer.append(cracks);intro.append(shatterLayer);intro.classList.add('is-shattering');
    homeEntrance.start();
    // Bounded cleanup also covers background tabs and interrupted animations.
    timer=setTimeout(finishIntro,1500);
  }
  function playIntro(manual=false){
    if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    if(!safeStore('sessionStorage','intro-seen','1'))return;
    introOpener=manual?$('#replay'):null;
    clearTimeout(timer);cleanShatter();homeEntrance.prepare();script.replaceChildren();
    // Simulated SSH login and character-art welcome, then service startup.
    // These are visual commands only; no process or server is actually started.
    const cursor=document.createElement('span');cursor.className='terminal-cursor';
    const keyDelays=[55,75,45,65,85,50,70];let keyIndex=0;
    const append=(parent,text,cls='')=>{const span=document.createElement('span');span.textContent=text;if(cls)span.className=cls;parent.append(span);return span;};
    const later=(fn,delay)=>{timer=setTimeout(()=>{if(intro.open)fn();},delay);};
    const newline=()=>script.append(document.createTextNode('\n'));
    const output=(text,cls='')=>{append(script,text,cls);newline();};
    let remote=false;
    function prompt(path){
      const line=document.createElement('span');line.className='shell-line';
      append(line,remote?'river_ya@knowledge':'river-ya@local','shell-user');append(line,':');append(line,path,'shell-path');append(line,'$ ');
      script.append(line);return line;
    }
    function typeCommand(command,done,path='~/knowledge'){
      const line=prompt(path),input=append(line,'','shell-input');line.append(cursor);
      let position=0;
      const type=()=>{
        cursor.classList.add('is-typing');input.textContent+=command[position++];
        if(position<command.length)later(type,keyDelays[keyIndex++%keyDelays.length]);
        else {cursor.classList.remove('is-typing');later(()=>{cursor.remove();newline();done();},200);}
      };
      later(type,260);
    }
    function startServer(){
      intro.dataset.stage='server';
      typeCommand('npm run start',()=>{
        script.append(cursor);
        later(()=>{
          cursor.remove();output('Server starting...');script.append(cursor);
          later(()=>{
            cursor.remove();output('Server listening on http://localhost:5173','shell-directory');script.append(cursor);
            later(shatterIntro,950);
          },500);
        },300);
      });
    }
    document.documentElement.classList.add('intro-open');intro.showModal();$('#skip-intro').focus({preventScroll:true});
    intro.dataset.stage='ssh';
    typeCommand('ssh river_ya@192.0.2.24',()=>{
      intro.dataset.stage='connecting';
      output('Connecting to 192.0.2.24...', 'shell-directory');script.append(cursor);
      later(()=>{
        cursor.remove();remote=true;intro.dataset.stage='welcome';
        output('Connection established.', 'shell-user');
        const banner=append(script,'','shell-login-banner');
        append(banner,$('#nailong-art').content.textContent.trimEnd(),'shell-pixel-art');
        append(banner,ui.ssh_welcome,'shell-welcome');
        // Leave time to enjoy the login banner before typing the next command.
        later(()=>typeCommand('clear',()=>{
          script.replaceChildren();intro.dataset.stage='clearing';
          later(startServer,300);
        }),2800);
      },450);
    },'~');
  }
  $('#replay').addEventListener('click',()=>playIntro(true));
  if((location.pathname==='/'||location.pathname==='/en/')&&!location.hash&&!location.search&&!safeStore('sessionStorage','intro-seen'))playIntro();
  if(!intro.open)homeEntrance.start();
  matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',event=>{if(event.matches){finishIntro();homeEntrance.showAll();}});
  window.addEventListener('resize',()=>{if(shatterLayer)finishIntro();});
  window.addEventListener('pagehide',()=>{finishIntro();homeEntrance.stop();});
})();
