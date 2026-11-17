/* Progressive enhancement: the complete chronology stays readable without JS. */
(() => {
  'use strict';
  const root=document.querySelector('[data-explorer="track"]');
  const milestones=document.querySelector('.milestones');
  const motion=matchMedia('(prefers-reduced-motion: reduce)');
  const animations=new Set();let observer=null,frame=0;
  const nodes=[...document.querySelectorAll('.timeline-node, .milestones a')];
  function reveal(entry){
    const el=entry.target;
    if(!entry.isIntersecting)return;
    observer?.unobserve(el);
    if(el===milestones){el.classList.add('timeline-in-view');return;}
    if(motion.matches||!el.animate)return;
    const animation=el.animate([{opacity:.25,transform:'translateY(20px)'},{opacity:1,transform:'translateY(0)'}],{duration:620,easing:'cubic-bezier(.2,.7,.2,1)'});
    animations.add(animation);animation.finished.then(()=>animations.delete(animation),()=>animations.delete(animation));
  }
  function observe(){
    observer?.disconnect();
    if(motion.matches||!('IntersectionObserver' in window)){milestones?.classList.add('timeline-in-view');return;}
    observer=new IntersectionObserver(entries=>entries.forEach(reveal),{threshold:.08});
    nodes.forEach(node=>observer.observe(node));if(milestones)observer.observe(milestones);
  }
  if(root){
    const panels=[...root.querySelectorAll('[data-panel]')];
    const years=[...root.querySelectorAll('[data-year-jump]')];
    panels.forEach(panel=>{const line=document.createElement('span');line.className='timeline-progress';line.setAttribute('aria-hidden','true');panel.append(line);});
    let current=null,hovered=null;
    function highlight(node){
      if(current!==node){current?.classList.remove('is-current');current=node;current?.classList.add('is-current');}
      years.forEach(link=>{if(node&&link.dataset.yearJump===node.dataset.year)link.setAttribute('aria-current','date');else link.removeAttribute('aria-current');});
    }
    function update(){
      frame=0;
      const panel=panels.find(item=>!item.hidden);if(!panel)return;
      const items=[...panel.querySelectorAll('.timeline-node')].filter(item=>!item.hidden);
      const available=new Set(items.map(item=>item.dataset.year));
      years.forEach(link=>{const enabled=available.has(link.dataset.yearJump);link.setAttribute('aria-disabled',String(!enabled));link.tabIndex=enabled?0:-1;});
      const bounds=panel.getBoundingClientRect(),start=64,total=Math.max(0,bounds.height-start);
      const readAt=innerHeight*.43,progress=Math.max(0,Math.min(total,readAt-bounds.top-start));
      panel.style.setProperty('--timeline-progress',progress+'px');
      const visible=items.filter(item=>item.getClientRects().length);
      const near=visible.reduce((best,item)=>{
        const distance=Math.abs(item.getBoundingClientRect().top+40-readAt);
        return !best||distance<best.distance?{item,distance}:best;
      },null);
      const focused=document.activeElement.closest?.('.timeline-node');
      highlight(focused&&panel.contains(focused)&&focused.getClientRects().length?focused:hovered&&panel.contains(hovered)&&hovered.getClientRects().length?hovered:near?.item);
    }
    const schedule=()=>{if(!frame)frame=requestAnimationFrame(update);};
    root.addEventListener('input',schedule);root.addEventListener('change',schedule);root.addEventListener('click',schedule);root.addEventListener('toggle',schedule,true);
    root.addEventListener('pointerover',event=>{const node=event.target.closest('.timeline-node');if(node){hovered=node;highlight(node);}});
    root.addEventListener('pointerout',event=>{if(!event.relatedTarget?.closest?.('.timeline-node'))hovered=null;schedule();});
    root.addEventListener('focusin',event=>{const node=event.target.closest('.timeline-node');if(node)highlight(node);});
    root.addEventListener('focusout',schedule);
    window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);window.addEventListener('popstate',schedule);window.addEventListener('hashchange',schedule);
    schedule();
  }
  motion.addEventListener('change',()=>{animations.forEach(animation=>animation.cancel());animations.clear();observe();});
  window.addEventListener('pagehide',()=>{cancelAnimationFrame(frame);frame=0;observer?.disconnect();animations.forEach(animation=>animation.cancel());animations.clear();});
  window.addEventListener('pageshow',event=>{if(event.persisted){observe();window.dispatchEvent(new Event('scroll'));}});
  observe();
})();
