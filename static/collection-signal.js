// Three static diagrams. Redraw only when the display size or palette changes.
(() => {
  const canvas = document.querySelector('canvas[data-signal]');
  const ctx = canvas?.getContext('2d');
  if (!ctx) return;

  function draw() {
    const width = canvas.clientWidth;
    if (!width) return;
    const scale = width * Math.min(window.devicePixelRatio || 1, 2) / 360;
    canvas.width = Math.round(360 * scale);
    canvas.height = Math.round(220 * scale);
    ctx.setTransform(scale, 0, 0, scale, 0, 0);
    const palette = getComputedStyle(canvas);
    const primary = palette.getPropertyValue('--accent').trim();
    const secondary = palette.getPropertyValue('--signal').trim();
    const surface = palette.getPropertyValue('--surface').trim();

    function line(points, color, alpha = 1, weight = 1, fill = '') {
      ctx.beginPath();
      for (const [i, [x, y]] of points.entries()) {
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      if (fill) {
        ctx.fillStyle = fill;
        ctx.fill();
        ctx.closePath();
      }
      ctx.strokeStyle = color;
      ctx.globalAlpha = alpha;
      ctx.lineWidth = weight;
      ctx.stroke();
      ctx.globalAlpha = 1;
    }
    if (canvas.dataset.signal === 'ai') {
      // Project a torus with a gently undulating radius onto the reading plane.
      function surfacePoint(u, v) {
        const r = 65 + (25 + 7 * Math.cos(3 * u)) * Math.cos(v);
        const x = r * Math.cos(u), y = r * Math.sin(u), z = 28 * Math.sin(v);
        return [180 + x * 1.28 + y * .17, 108 - x * .27 + y * .56 - z * .95];
      }
      const tau = Math.PI * 2;
      for (let i = 0; i < 46; i++) {
        line(Array.from({length: 61}, (_, j) => surfacePoint(tau*i/46,tau*j/60)), primary, .68);
      }
      for (let j = 0; j < 15; j++) {
        line(Array.from({length: 93}, (_, i) => surfacePoint(tau*i/92,tau*j/15)), secondary, .62);
      }
    } else if (canvas.dataset.signal === 'algorithms') {
      // Each compare/exchange stage moves a value towards its sorted position.
      const values = [4, 1, 5, 2, 0, 3];
      for (let stage = 0; stage < values.length; stage++) {
        const before = values.slice();
        for (let i = stage % 2; i + 1 < values.length; i += 2) {
          if (values[i] > values[i + 1]) [values[i], values[i + 1]] = [values[i + 1], values[i]];
        }
        before.forEach((value, row) => {
          const x = 42 + stage * 45, y = 47 + row * 25;
          const end = 47 + values.indexOf(value) * 25;
          const color = value % 2 ? primary : secondary;
          line([[x,y],[x+10,y],[x+34,end],[x+45,end]], color, .9, 1.7);
          ctx.fillStyle = color;
          ctx.fillRect(x-2,y-2,4,4);
          if (stage === values.length-1) ctx.fillRect(x+43,end-2,4,4);
        });
      }
    } else {
      const diamond = y => [[74,y],[178,y-48],[286,y],[180,y+48],[74,y]];
      for (const y of [153, 134, 112, 88]) {
        line(diamond(y), primary, .95, 1.5, surface);
        line([[74,y],[74,y+6],[180,y+54],[286,y+6],[286,y]], secondary, .8);
      }
      for (let i=0; i<5; i++) {
        const x=119+i*13, y=81-i*6;
        line([[x,y],[x+21,y+10],[x+41,y+1],[x+68,y+14]], secondary, .9);
      }
    }
  }
  new MutationObserver(draw).observe(document.documentElement, {attributes:true, attributeFilter:['data-theme']});
  if ('ResizeObserver' in window) new ResizeObserver(draw).observe(canvas);
  else window.addEventListener('resize', draw);
  draw();
})();
