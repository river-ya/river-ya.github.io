(() => {
 'use strict';
 const ui=JSON.parse(document.querySelector('#ui-data').textContent),locale=document.documentElement.lang,prefix=locale==='en'?'/en':'';
 const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 const L=x=>x?.[locale]||x?.['zh-CN']||'',U=x=>prefix+x;
 const colors={diffusion:'var(--accent)',transformer:'var(--violet)',vae:'var(--blue)',gan:'var(--amber)'},dashes={diffusion:'',transformer:'7 6',vae:'2 5',gan:'12 4 2 4'};
 const title=id=>data?.families.find(f=>f.id===id)?.title?.[locale]||(id==='vae'||id==='gan'?id.toUpperCase():id[0].toUpperCase()+id.slice(1));
 const svgNS='http://www.w3.org/2000/svg';let data,nodes,zoom=1,focus='dit';
 const families=()=>$$('input[name=family]:checked').map(x=>x.value);
 const el=(tag,text,parent,cls)=>{const x=document.createElement(tag);x.textContent=text;if(cls)x.className=cls;parent.append(x);return x;};
 const svg=(tag,attrs,parent)=>{const x=document.createElementNS(svgNS,tag);Object.entries(attrs).forEach(([k,v])=>x.setAttribute(k,String(v)));parent.append(x);return x;};
 const nodeURL=id=>U('/knowledge/nodes/'+id+'/');
 const dateOf=n=>n.dates[n.timelineDateIndex||0].value;
 function dateFloat(n){const [year,month='01',day='01']=dateOf(n).split('-');const start=Date.UTC(+year,0,1),end=Date.UTC(+year+1,0,1);return +year+(Date.UTC(+year,+month-1,+day)-start)/(end-start);}
 function syncURL(){const u=new URL(location.href);u.searchParams.set('families',families().join(','));u.searchParams.set('start',$('#from-year').value);u.searchParams.set('end',$('#to-year').value);u.searchParams.set('node',focus);if($('#only-confluence').checked)u.searchParams.set('only','1');else u.searchParams.delete('only');if(zoom!==1)u.searchParams.set('zoom',String(zoom));else u.searchParams.delete('zoom');history.replaceState(null,'',u);const a=$('#language-switch'),other=new URL(a.href);other.search=u.search;other.hash=u.hash;a.href=other.pathname+other.search+other.hash;}
 function detail(id){
   const n=nodes[id];if(!n)return;focus=id;const box=$('#graph-detail');box.replaceChildren();
   el('p',ui.graph_focus+' / '+dateOf(n),box,'eyebrow');el('h2',L(n.title),box);el('p',L(n.summary),box);
   el('h3',ui.from_routes,box);const tags=el('div','',box,'tags');n.familyIds.forEach(f=>{const a=el('a',title(f),tags);a.href=U('/knowledge/ai/families/'+f+'/');});
   const edges=data.relations.filter(r=>r.toNodeId===id||r.fromNodeId===id);
   if(edges.length){el('h3',ui.contributions,box);edges.forEach(r=>{const row=el('div','',box,'contribution');el('span',ui[r.kind],row,'badge');const a=el('a',L(nodes[r.fromNodeId].title)+' → '+L(nodes[r.toNodeId].title),row);a.href=nodeURL(r.fromNodeId===id?r.toNodeId:r.fromNodeId);el('p',L(r.contribution),row);r.sourceUrls.forEach(url=>{const source=el('a',ui.sources+' ↗',row,'small');source.href=url;});});}
   if(id==='dit'){el('h3',ui.changes,box);el('p',ui.dit_changes,box);}
   const a=el('a',ui.view_node+' →',box,'button primary');a.href=nodeURL(id);
 }
 function render(write=true){
   if(!data)return;
   let start=Number($('#from-year').value),end=Number($('#to-year').value);start=Math.max(1986,Math.min(2024,Number.isFinite(start)?start:2019));end=Math.max(start,Math.min(2024,Number.isFinite(end)?end:2024));$('#from-year').value=start;$('#to-year').value=end;
   const fs=families(),only=$('#only-confluence').checked,conIds=new Set(data.confluences.map(c=>c.nodeId));
   const visible=data.nodes.filter(n=>n.dates.length&&n.dateVerification==='verified'&&n.familyIds.some(f=>fs.includes(f))&&dateFloat(n)>=start&&dateFloat(n)<end+1&&(!only||conIds.has(n.id))).sort((a,b)=>dateFloat(a)-dateFloat(b));
   const width=Math.max(630,fs.length*215+80),row=160*zoom,height=(end-start+1)*row+90,canvas=$('#graph-canvas');canvas.replaceChildren();canvas.style.width=width+'px';canvas.style.height=height+'px';
   const drawing=svg('svg',{width,height,'aria-hidden':'true',class:'graph-svg'},canvas);
   const xpos=f=>80+(fs.indexOf(f)+.5)*(width-100)/Math.max(1,fs.length),ypos=n=>65+(dateFloat(n)-start)*row;
   for(let y=start;y<=end;y++){const yy=65+(y-start)*row;svg('line',{x1:55,y1:yy,x2:width-15,y2:yy,stroke:'var(--line)','stroke-width':1},drawing);const text=svg('text',{x:10,y:yy+4,fill:'var(--muted)','font-size':10,'font-family':'monospace'},drawing);text.textContent=y;}
   fs.forEach(f=>{const x=xpos(f);svg('line',{x1:x,y1:45,x2:x,y2:height-10,stroke:colors[f],'stroke-width':2,'stroke-dasharray':dashes[f],opacity:.6},drawing);const label=el('span',title(f),canvas,'graph-family-label');label.style.left=x+'px';label.style.setProperty('--node-color',colors[f]);});
   // Position dots by actual dates; label offsets do not redefine chronological position.
   const points={};visible.forEach(n=>{const lanes=n.familyIds.filter(f=>fs.includes(f));points[n.id]={x:lanes.reduce((sum,f)=>sum+xpos(f),0)/lanes.length,y:ypos(n),lane:lanes[0]};});
   const active=data.relations.filter(r=>(r.toNodeId===focus||r.fromNodeId===focus)&&points[r.fromNodeId]&&points[r.toNodeId]);
   active.forEach(r=>{const a=points[r.fromNodeId],b=points[r.toNodeId];if(r.kind==='uses-component'||r.kind==='inspired-by')return;const bend=(a.y+b.y)/2;svg('path',{d:`M${a.x},${a.y} C${a.x},${bend} ${b.x},${bend} ${b.x},${b.y}`,fill:'none',stroke:colors[a.lane],'stroke-width':2,'stroke-dasharray':r.kind==='combines'?'':'4 4'},drawing);});
   const lastLabel={};
   visible.forEach(n=>{const p=points[n.id],color=colors[p.lane],y=Math.max(p.y,(lastLabel[p.lane]||0)+44);lastLabel[p.lane]=y;
     svg('circle',{cx:p.x,cy:p.y,r:4,fill:'var(--bg)',stroke:color,'stroke-width':2},drawing);
     if(y!==p.y)svg('path',{d:`M${p.x},${p.y}h12V${y}h-12`,fill:'none',stroke:'var(--faint)','stroke-width':1},drawing);
     const b=el('button',L(n.title),canvas,'graph-node'+(conIds.has(n.id)?' is-confluence':'')+(focus===n.id?' selected':''));b.style.left=p.x+'px';b.style.top=y+'px';b.style.setProperty('--node-color',color);b.dataset.node=n.id;b.title=L(n.summary);b.addEventListener('focus',()=>{$('#graph-status').textContent=L(n.summary);});b.addEventListener('mouseenter',()=>{$('#graph-status').textContent=L(n.summary);});b.setAttribute('aria-label',L(n.title)+' · '+dateOf(n)+' · '+L(n.summary));b.setAttribute('aria-pressed',String(focus===n.id));el('small',dateOf(n),b);b.addEventListener('click',()=>select(n.id,true));
   });
   const list=$('#graph-list');list.replaceChildren();visible.forEach(n=>{const item=el('article','',list);el('time',dateOf(n),item);const b=el('button',L(n.title)+' ↗',item);b.dataset.listNode=n.id;b.setAttribute('aria-expanded',String(focus===n.id));const tags=el('div','',item,'tags');n.familyIds.forEach(f=>el('span',title(f),tags));b.addEventListener('click',()=>select(n.id,false));if(focus===n.id){const desc=el('div','',item,'mini-sources');el('p',L(n.summary),desc);const inputs=data.relations.filter(r=>r.toNodeId===n.id&&r.kind==='combines');if(inputs.length){const mini=el('div','',desc,'mini-confluence'),lines=svg('svg',{viewBox:'0 0 300 130','aria-hidden':'true'},mini);inputs.forEach((r,i)=>{const x=(i+.5)*300/inputs.length;svg('path',{d:`M${x},35V60L150,90`,fill:'none',stroke:colors[nodes[r.fromNodeId].familyIds.find(f=>colors[f])]||'var(--accent)','stroke-width':1.5},lines);const link=el('a',L(nodes[r.fromNodeId].title),mini);link.href=nodeURL(r.fromNodeId);link.style.left=(x/3)+'%';});el('span',L(n.title),mini,'mini-target');}data.relations.filter(r=>r.toNodeId===n.id).forEach(r=>{const a=el('a',L(nodes[r.fromNodeId].title)+' → '+L(n.title),desc);a.href=nodeURL(r.fromNodeId);el('p',ui[r.kind]+' · '+L(r.contribution),desc);});const a=el('a',ui.view_node+' →',desc);a.href=nodeURL(n.id);}});
   if(!visible.some(n=>n.id===focus)){$('#graph-detail').hidden=true;}else{$('#graph-detail').hidden=false;detail(focus);}
   $('#graph-status').textContent=visible.length?visible.length+' '+ui.results:ui.no_results;$('#zoom-label').textContent=Math.round(zoom*100)+'%';
   if(write)syncURL();
 }
 function select(id,graph){focus=id;render();const b=graph?document.querySelector(`[data-node="${id}"]`):document.querySelector(`[data-list-node="${id}"]`);b?.focus({preventScroll:true});}
 function restore(){const p=new URL(location.href).searchParams;const fs=p.has('families')?p.get('families').split(',').filter(f=>data.families.some(t=>t.id===f)).slice(0,4):['diffusion','transformer'];$$('input[name=family]').forEach(c=>c.checked=fs.includes(c.value));$('#from-year').value=p.get('start')||2019;$('#to-year').value=p.get('end')||2024;$('#only-confluence').checked=p.get('only')==='1';focus=nodes[p.get('node')]?p.get('node'):'dit';zoom=Math.max(.6,Math.min(2,Number(p.get('zoom'))||1));render(false);}
 $$('input[name=family],#from-year,#to-year,#only-confluence').forEach(c=>c.addEventListener('change',()=>{if(families().length>4){c.checked=false;$('#graph-status').textContent=ui.families_select;return;}render();}));
 $('#reset-graph').addEventListener('click',()=>{history.replaceState(null,'',location.pathname);restore();syncURL();});
 $('#zoom-in').addEventListener('click',()=>{zoom=Math.min(2,+(zoom+.2).toFixed(1));render();});$('#zoom-out').addEventListener('click',()=>{zoom=Math.max(.6,+(zoom-.2).toFixed(1));render();});
 $('#pan-left').addEventListener('click',()=>$('#graph-scroll').scrollBy({left:-200}));$('#pan-right').addEventListener('click',()=>$('#graph-scroll').scrollBy({left:200}));
 $('#graph-mode').addEventListener('click',()=>{const full=$('#graph-app').classList.toggle('show-full-graph');$('#graph-mode').textContent=full?ui.list_graph:ui.full_graph;});
 $('#share-graph').addEventListener('click',async()=>{syncURL();try{await navigator.clipboard.writeText(location.href);$('#graph-status').textContent=ui.copied;}catch(_){$('#graph-status').textContent=ui.copy_failed;}});
 window.addEventListener('popstate',restore);
 fetch('/assets/graph.json').then(r=>{if(!r.ok)throw Error('graph');return r.json();}).then(json=>{data=json;data.families.forEach(f=>{colors[f.id]=f.graphStyle?.color||'var(--accent)';dashes[f.id]=f.graphStyle?.dash||'';});nodes=Object.fromEntries(data.nodes.map(n=>[n.id,n]));restore();}).catch(()=>{$('#graph-status').textContent=ui.search_error;});
})();
