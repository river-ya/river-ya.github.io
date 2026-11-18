// Opt in only when a personal-site link opens a blog page in this tab.
(() => {
  const key = 'river:crane-entry';
  let optIn;
  document.addEventListener('click', event => {
    const link = event.target.closest?.('a[href]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey ||
        event.ctrlKey || event.shiftKey || event.altKey || link.hasAttribute('download') ||
        (link.target && link.target !== '_self')) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin || !/^\/(en\/)?blog\//.test(url.pathname) ||
        matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    try {
      sessionStorage.setItem(key, JSON.stringify({
        to: url.pathname, at: Date.now(), theme: document.documentElement.dataset.theme
      }));
    } catch { return; }
    if (!optIn) {
      optIn = document.createElement('style');
      optIn.textContent = '@view-transition { navigation: auto; }';
      document.head.append(optIn);
    }
  });
  window.addEventListener('pageshow', () => {
    optIn?.remove();
    optIn = undefined;
    try { sessionStorage.removeItem(key); } catch {}
  });
})();
