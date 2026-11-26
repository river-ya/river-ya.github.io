(() => {
  'use strict';
  const page = document.documentElement;
  const system = matchMedia('(prefers-color-scheme: dark)');
  const toggle = document.querySelector('#theme-toggle');
  let preference = page.dataset.theme;
  function showTheme() {
    page.dataset.theme = preference || (system.matches ? 'dark' : 'light');
    toggle.setAttribute('aria-pressed', String(page.dataset.theme === 'dark'));
  }
  showTheme();
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    preference = page.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('blog-theme', preference); } catch {}
    showTheme();
  });
  system.addEventListener('change', showTheme);

  const language = document.querySelector('#language-switch');
  const translation = new URL(language.href);
  function syncLanguage() {
    const target = new URL(translation);
    const params = new URLSearchParams(location.search);
    params.delete('translation');
    for (const [key, value] of translation.searchParams) params.set(key, value);
    target.search = params;
    target.hash = location.hash;
    language.href = target.href;
  }
  syncLanguage();
  window.addEventListener('hashchange', syncLanguage);

  const back = document.querySelector('[data-blog-back]');
  const from = new URLSearchParams(location.search).get('from');
  if (back && from) {
    try {
      const route = new URL(from, location.origin);
      if (route.origin === location.origin && /^\/(en\/)?(?:knowledge\/|notes\/|blog\/category\/)/.test(route.pathname)) {
        const path = route.pathname.replace(/^\/en\//, '/');
        back.href = (page.lang === 'en' ? '/en' : '') + path + route.search + route.hash;
        back.textContent = '← ' + back.dataset.routeLabel;
      }
    } catch {}
  }

  const section = document.querySelector('#posts');
  if (!section) return;
  const input = section.querySelector('#blog-query');
  const cards = [...section.querySelectorAll('[data-blog-post]')].map(node => {
    const tags = JSON.parse(node.dataset.tags);
    const summary = node.dataset.summary ?? '';
    const text = [node.querySelector('h2').textContent, summary, ...tags].join(' ').toLocaleLowerCase();
    return { node, tags, text };
  });
  const count = section.querySelector('#blog-result-count');
  const filter = section.querySelector('#blog-filter');
  function render() {
    const params = new URLSearchParams(location.search);
    const query = params.get('q') || '';
    const tag = params.get('tag') || '';
    if (input && input.value !== query) input.value = query;
    const words = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let matches = 0;
    for (const card of cards) {
      card.node.hidden = !words.every(word => card.text.includes(word)) || Boolean(tag && !card.tags.includes(tag));
      if (!card.node.hidden) matches++;
    }
    const filtering = Boolean(words.length || tag);
    count.hidden = !filtering;
    count.textContent = matches + ' ' + section.dataset.countLabel;
    filter.hidden = !tag;
    filter.querySelector('strong').textContent = tag;
    section.querySelector('#blog-no-results').hidden = !filtering || matches > 0;
    const empty = section.querySelector('.blog-empty, #search-empty');
    if (empty) empty.hidden = filtering;
    syncLanguage();
  }
  function update(url) {
    history.replaceState(null, '', url);
    render();
  }
  input?.addEventListener('input', () => {
    const url = new URL(location.href);
    if (input.value) url.searchParams.set('q', input.value);
    else url.searchParams.delete('q');
    update(url);
  });
  section.querySelectorAll('[data-blog-reset]').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      update(link.href);
      input?.focus();
    });
  });
  window.addEventListener('popstate', render);
  render();
})();
