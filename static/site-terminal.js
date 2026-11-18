(() => {
  'use strict';
  const catalog = new Map(Object.entries(JSON.parse(document.querySelector('#shell-catalog').textContent)));
  const ui = JSON.parse(document.querySelector('#ui-data').textContent);
  const log = document.querySelector('#shell-log');
  const input = document.querySelector('#shell-input');
  const history = [];
  let historyCursor = 0, draft = '', lastCompletion = null;
  let cwd = '/';

  const commands = {
    help: ['', ui.terminal_help], ls: ['[path]', ui.terminal_list],
    cd: ['[path]', ui.terminal_cd], pwd: ['', ui.terminal_pwd],
    cat: ['<note>', ui.terminal_cat],
    open: ['[path]', ui.terminal_open], search: ['<text>', ui.terminal_search],
    clear: ['', ui.terminal_clear], exit: ['', ui.terminal_exit]
  };

  function resolve(path) {
    const raw = path.replace(/^~(?=\/|$)/, '/');
    const parts = [];
    for (const part of (raw.startsWith('/') ? raw : cwd + '/' + raw).split('/')) {
      if (part === '..') parts.pop();
      else if (part && part !== '.') parts.push(part);
    }
    return '/' + parts.join('/');
  }

  function setDirectory(path) {
    cwd = path;
    const url = new URL(location.href);
    if (cwd === '/') url.searchParams.delete('cwd');
    else url.searchParams.set('cwd', cwd);
    window.history.replaceState(null, '', url);
    const language = document.querySelector('#language-switch');
    const alternate = new URL(language.href);
    alternate.search = url.search;
    language.href = alternate.href;
    document.querySelector('#shell-path').textContent = cwd;
  }

  function element(tag, text = '', className = '') {
    const node = document.createElement(tag);
    node.textContent = text;
    if (className) node.className = className;
    return node;
  }

  function message(text, className) {
    log.append(element('div', text, className));
  }

  function children(path) {
    const parent = path === '/' ? '/' : path + '/';
    return [...catalog].filter(([key]) => key !== path && key.startsWith(parent) &&
      !key.slice(parent.length).includes('/'));
  }

  function list(entries, absolute = false) {
    if (!entries.length) {
      message(ui.terminal_empty);
      return;
    }
    const rows = element('div', '', 'shell-list');
    for (const [path, item] of entries) {
      const name = absolute ? path : path.split('/').pop();
      let action;
      if (item.directory) {
        action = element('button', path === '/' ? '/' : name + '/');
        action.type = 'button';
        action.addEventListener('click', () => {
          execute('cd ' + path);
          input.focus({preventScroll:true});
        });
      } else {
        action = element('a', name);
        action.href = item.url;
      }
      rows.append(action, element('span', item.title));
    }
    log.append(rows);
  }

  function showHelp() {
    const rows = element('div', '', 'shell-list');
    for (const [cmd, [arg, description]] of Object.entries(commands)) {
      rows.append(element('code', [cmd,arg].filter(Boolean).join(' ')), element('span', description));
    }
    log.append(rows);
  }

  function find(query) {
    const hits = new Map();
    const term = query.toLocaleLowerCase();
    for (const [path, item] of catalog) {
      const label = [path, item.title, item.summary || ''].join(' ').toLocaleLowerCase();
      if (label.includes(term) && !hits.has(item.url)) hits.set(item.url, [path, item]);
    }
    if (hits.size) list([...hits.values()], true);
    else message(ui.terminal_no_hits);
  }

  function visit(url) {
    // Use a link activation so blog entries also get the site's page transition.
    const link = element('a');
    link.href = url;
    link.hidden = true;
    document.body.append(link);
    link.click();
    link.remove();
  }

  async function readNote(item) {
    const output = element('div', '', 'shell-reading');
    const link = element('a', item.title + ' ↗');
    link.href = item.url;
    output.append(link);
    log.append(output);
    try {
      const response = await fetch(item.url);
      if (!response.ok) throw new Error('Missing note');
      const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
      const body = doc.querySelector('[data-terminal-text]');
      if (!body) throw new Error('Missing note text');
      body.querySelectorAll('.source-code,script,style,[hidden]').forEach(node => node.remove());
      body.querySelectorAll('li').forEach(node => node.prepend('• '));
      body.querySelectorAll('br,p,li,pre,tr,h1,h2,h3,h4,h5,h6').forEach(node => node.append('\n'));
      output.append(element('div', body.textContent.trim()));
    } catch {
      output.append(element('div', ui.terminal_read_error, 'shell-error'));
    }
  }

  function execute(raw) {
    const text = raw.trim();
    if (!text) return;
    if (history.at(-1) !== text) history.push(text);
    historyCursor = history.length;
    draft = '';
    lastCompletion = null;
    const echo = element('div', '', 'shell-command');
    echo.append(element('span', 'river-ya:' + (cwd === '/' ? '~' : '~' + cwd) + '$ ', 'shell-prompt'),
      document.createTextNode(text));
    log.append(echo);
    const [name, ...args] = text.split(/\s+/);
    const cmd = name.toLowerCase();
    const arg = args.join(' ');
    if (!Object.hasOwn(commands, cmd)) {
      message(ui.terminal_unknown, 'shell-error');
    } else if ((['search','cat'].includes(cmd) && !arg) || (cmd !== 'search' && args.length > (commands[cmd][0] ? 1 : 0))) {
      message(ui.terminal_usage + ' · ' + cmd + ' ' + commands[cmd][0], 'shell-error');
    } else if (cmd === 'help') showHelp();
    else if (cmd === 'clear') log.replaceChildren();
    else if (cmd === 'pwd') message(cwd);
    else if (cmd === 'search') find(arg);
    else if (cmd === 'exit') visit(catalog.get('/').url);
    else {
      const path = resolve(arg || (cmd === 'cd' ? '/' : '.'));
      const item = catalog.get(path);
      if (!item) message(ui.terminal_missing + ' · ' + path, 'shell-error');
      else if (cmd === 'cat' && !Object.hasOwn(item, 'summary')) message(ui.terminal_note_only, 'shell-error');
      else if (cmd === 'cat') readNote(item);
      else if (cmd === 'open') visit(item.url);
      else if (cmd === 'cd' && !item.directory) message(ui.terminal_not_dir + ' · ' + path, 'shell-error');
      else if (!item.directory) list([[path, item]]);
      else {
        if (cmd === 'cd') setDirectory(path);
        list(children(path));
      }
    }
    input.value = '';
    log.scrollTop = log.scrollHeight;
  }

  function complete() {
    const value = input.value;
    if (!value || value === lastCompletion || input.selectionStart !== value.length ||
        input.selectionEnd !== value.length) return false;
    const parts = value.split(/\s+/);
    let prefix = '', stem = parts[0], choices;
    if (parts.length === 1) {
      choices = Object.keys(commands).map(cmd => cmd+' ');
    } else if (parts.length === 2 && ['ls','cd','open','cat'].includes(parts[0])) {
      const slash = parts[1].lastIndexOf('/') + 1;
      const folder = parts[1].slice(0, slash);
      stem = parts[1].slice(slash);
      prefix = value.slice(0, value.length - stem.length);
      choices = children(resolve(folder)).filter(([,item]) => parts[0] !== 'cd' || item.directory)
        .map(([path, item]) => path.split('/').pop() + (item.directory ? '/' : ' '));
    } else return false;
    const matches = choices.filter(choice => choice.startsWith(stem));
    if (!matches.length) return false;
    let common = matches[0];
    while (!matches.every(match => match.startsWith(common))) common = common.slice(0,-1);
    input.value = prefix + common;
    if (matches.length > 1) {
      message(matches.join('  '));
      log.scrollTop = log.scrollHeight;
    }
    lastCompletion = input.value;
    return true;
  }

  document.querySelector('#shell-form').addEventListener('submit', event => {
    event.preventDefault();
    execute(input.value);
    input.focus({preventScroll:true});
  });
  input.addEventListener('input', () => { lastCompletion = null; });
  input.addEventListener('keydown', event => {
    if (event.isComposing || event.shiftKey || event.ctrlKey || event.altKey || event.metaKey) return;
    if (event.key === 'Tab' && complete()) event.preventDefault();
    if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
      if (!history.length) return;
      event.preventDefault();
      if (historyCursor === history.length) draft = input.value;
      historyCursor = Math.max(0, Math.min(history.length, historyCursor + (event.key === 'ArrowUp' ? -1 : 1)));
      input.value = history[historyCursor] ?? draft;
      input.setSelectionRange(input.value.length, input.value.length);
      lastCompletion = null;
    }
  });
  document.querySelectorAll('[data-command]').forEach(button => button.addEventListener('click', () => {
    execute(button.dataset.command);
    input.focus({preventScroll:true});
  }));
  const initial = resolve(new URL(location.href).searchParams.get('cwd') || '/');
  setDirectory(catalog.get(initial)?.directory ? initial : '/');
  document.querySelectorAll('[data-web-shell]').forEach(part => { part.hidden = false; });
  execute('ls');
  if (matchMedia('(pointer:fine)').matches) input.focus({preventScroll:true});
})();
