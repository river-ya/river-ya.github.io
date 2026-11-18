// Apply a saved choice before first paint, including on direct article visits.
(() => {
  const root = document.documentElement;
  try {
    if (localStorage.getItem('notebook-type') === 'print') root.dataset.type = 'print';
  } catch {}
  document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('[data-type-toggle]');
    if (!button) return;
    const sync = () => button.setAttribute('aria-pressed', String(root.dataset.type !== 'print'));
    sync();
    button.hidden = false;
    button.addEventListener('click', () => {
      root.dataset.type = root.dataset.type === 'print' ? 'hand' : 'print';
      try { localStorage.setItem('notebook-type', root.dataset.type); } catch {}
      sync();
    });
    window.addEventListener('pageshow', event => {
      if (!event.persisted) return;
      try { root.dataset.type = localStorage.getItem('notebook-type') === 'print' ? 'print' : 'hand'; } catch {}
      sync();
    });
  });
})();
