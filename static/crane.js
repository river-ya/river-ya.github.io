// This parser-blocking entry runs before the destination's first paint.
(() => {
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let entry;
  try {
    const key = 'river:crane-entry';
    entry = JSON.parse(sessionStorage.getItem(key));
    sessionStorage.removeItem(key);
  } catch { return; }
  if (!entry || entry.to !== location.pathname || Date.now() - entry.at > 30000 ||
      reduced.matches || performance.getEntriesByType('navigation')[0]?.type !== 'navigate') return;

  const optIn = document.createElement('style');
  optIn.textContent = '@view-transition { navigation: auto; }';
  document.head.append(optIn);
  root.classList.add('crane-entry');

  // Perimeter vertices run clockwise. The last vertex is the central ridge.
  // All faces share their edges as the rectangle folds into a diamond and a bird.
  const sheet = [
    [-.5,0], [-.5,-.5], [-.25,-.5], [0,-.5], [.5,-.5], [.5,-.22],
    [.5,0], [.5,.5], [0,.5], [-.22,.5], [-.5,.5], [0,0]
  ];
  const bird = [
    [-132,-26], [-43,3], [-83,-102], [9,-4], [78,-64], [107,-44],
    [72,-48], [35,15], [7,33], [-72,79], [-42,24], [0,10]
  ];
  const faces = [
    { corners: [0,1,10], tone: '#c0cfc6' },       // tail
    { corners: [1,2,3], tone: '#a6bab1' },        // far wing
    { corners: [3,4,6], tone: '#edeee2' },        // neck
    { corners: [4,5,6], tone: '#b2c1b7' },        // beak
    { corners: [3,6,7], tone: '#a2b6ac' },
    { corners: [1,3,11], tone: '#d4dfcf' },
    { corners: [3,7,11], tone: '#e7ebda' },
    { corners: [7,8,11], tone: '#8aa79b' },
    { corners: [1,9,10], tone: '#91ada0' },      // near wing
    { corners: [1,11,9], tone: '#f6f4e6' },
    { corners: [11,8,9], tone: '#c6d4c6' }
  ];
  const width = innerWidth, height = innerHeight;
  const unit = Math.min(width / 395, height / 375, 1.65);
  const radius = 125 * unit;
  root.style.setProperty('--fold-width', 2 * radius / width);
  root.style.setProperty('--fold-height', 2 * radius / height);
  const start = sheet.map(([x,y]) => [x * width, y * height]);
  const diamond = sheet.map(([x,y]) => {
    const edge = Math.abs(x) + Math.abs(y);
    return edge ? [x * radius / edge, y * radius / edge] : [0,0];
  });
  const svgNamespace = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(svgNamespace, 'svg');
  svg.setAttribute('class', 'crane-sheet');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('focusable', 'false');
  svg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
  const group = document.createElementNS(svgNamespace, 'g');
  svg.append(group);
  const polygons = faces.map(face => {
    const polygon = document.createElementNS(svgNamespace, 'polygon');
    group.append(polygon);
    return polygon;
  });

  const smooth = n => n * n * (3 - 2 * n);
  const clamp = n => Math.max(0, Math.min(1, n));
  const mix = (a,b,n) => a + (b-a)*n;
  const base = entry.theme === 'light' ? [246,247,242] : [13,17,16];
  const tones = faces.map(({tone}) => [1,3,5].map(i => parseInt(tone.slice(i,i+2),16)));

  function draw(time) {
    const gather = smooth(clamp(time / 560));
    const fold = smooth(clamp((time - 440) / 610));
    const fly = clamp((time - 1060) / 940);
    const travel = fly * fly;
    const flap = Math.sin(fly * Math.PI * 3) * Math.sin(fly * Math.PI);
    const points = start.map(([x,y], i) => {
      let [bx,by] = bird[i];
      if (i === 2) { bx += 13 * flap; by += 51 * flap; }
      if (i === 9) { bx -= 15 * flap; by -= 95 * flap; }
      // The wing tips lift clear of the central crease before they fan out.
      const lift = (i === 2 || i === 9) ? -26 * unit * Math.sin(fold * Math.PI) : 0;
      return [mix(mix(x,diamond[i][0],gather),bx*unit,fold),
              mix(mix(y,diamond[i][1],gather),by*unit,fold) + lift];
    });
    const x = width/2 + (width*.58 + radius) * travel;
    const y = height/2 - height*.55*travel - 18*unit*Math.sin(fly*Math.PI);
    group.setAttribute('transform', 'translate('+x+' '+y+') rotate('+(-9*fly)+') scale('+(1-.42*fly)+')');
    faces.forEach((face,i) => {
      const wingLight = face.corners.includes(9) ? -12 * flap : face.corners.includes(2) ? 10 * flap : 0;
      const color = 'rgb(' + tones[i].map((v,c) => Math.round(mix(base[c],v + wingLight,gather))).join(',') + ')';
      polygons[i].setAttribute('points', face.corners.map(j => points[j].join(',')).join(' '));
      polygons[i].setAttribute('fill',color);
      polygons[i].setAttribute('stroke',color);
    });
  }

  let frame, finished = false, mounted = false, transition;
  function finish() {
    if (finished) return;
    finished = true;
    cancelAnimationFrame(frame);
    transition?.skipTransition();
    svg.remove();
    optIn.remove();
    root.classList.remove('crane-entry');
    root.style.removeProperty('--fold-width');
    root.style.removeProperty('--fold-height');
    reduced.removeEventListener('change', finish);
    window.removeEventListener('pagehide', finish);
    window.removeEventListener('resize', finish);
    window.removeEventListener('keydown', escape);
  }
  function escape(event) { if (event.key === 'Escape') finish(); }
  function play() {
    if (mounted || finished) return;
    if (!document.body) {
      document.addEventListener('DOMContentLoaded', play, { once: true });
      return;
    }
    mounted = true;
    document.body.append(svg);
    draw(0);
    let started;
    function tick(now) {
      started ??= now;
      const elapsed = now - started;
      if (elapsed >= 2000) { finish(); return; }
      draw(elapsed);
      frame = requestAnimationFrame(tick);
    }
    frame = requestAnimationFrame(tick);
  }
  reduced.addEventListener('change', finish);
  window.addEventListener('pagehide', finish);
  window.addEventListener('resize', finish);
  window.addEventListener('keydown', escape);

  // The browser composites a snapshot of the actual departing viewport over
  // the mesh. Without native snapshots the same mesh begins as a plain sheet.
  if ('onpagereveal' in window) {
    window.addEventListener('pagereveal', event => {
      transition = event.viewTransition;
      play();
    }, { once: true });
  } else {
    document.addEventListener('DOMContentLoaded', play, { once: true });
  }
})();
