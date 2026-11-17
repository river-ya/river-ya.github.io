(() => {
  'use strict';
  const root=document.querySelector('[data-blog]');if(!root)return;
  const input=root.querySelector('#blog-query'),form=root.querySelector('.blog-search-form');if(!input)return;
  const posts=[...root.querySelectorAll('[data-blog-post]')];
  const count=root.querySelector('#blog-result-count'),empty=root.querySelector('#blog-no-results'),tagLine=root.querySelector('#blog-filter');
  const ui=JSON.parse(document.querySelector('#ui-data').textContent);
  let tag='';
  function filter(write=false){
    const words=input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);let matches=0;
    posts.forEach(post=>{
      const tags=JSON.parse(post.dataset.tags),haystack=[post.dataset.title,post.dataset.summary,...tags].join(' ').toLocaleLowerCase();
      post.hidden=!(words.every(word=>haystack.includes(word))&&(!tag||tags.includes(tag)));
      if(!post.hidden)matches++;
    });
    count.hidden=posts.length===0;count.textContent=matches+' '+ui.blog_count;
    empty.hidden=!(matches===0&&(posts.length>0||input.value.trim()||tag));
    tagLine.hidden=!tag;tagLine.querySelector('strong').textContent=tag;
    if(write){const url=new URL(location.href);input.value.trim()?url.searchParams.set('q',input.value.trim()):url.searchParams.delete('q');tag?url.searchParams.set('tag',tag):url.searchParams.delete('tag');history.replaceState(null,'',url);}
    const link=document.querySelector('#language-switch'),other=new URL(link.href);other.search=location.search;other.hash=location.hash;link.href=other.pathname+other.search+other.hash;
  }
  function restore(){const params=new URLSearchParams(location.search);input.value=params.get('q')||'';tag=params.get('tag')||'';filter();}
  input.addEventListener('input',()=>filter(true));
  form.addEventListener('submit',event=>{event.preventDefault();filter(true);});
  root.querySelectorAll('[data-blog-reset]').forEach(button=>button.addEventListener('click',()=>{input.value='';tag='';filter(true);input.focus();}));
  window.addEventListener('popstate',restore);restore();
})();
