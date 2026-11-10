/* DNS cache simulator: a service moves while clients hold cached addresses (2026-11-09).
   Self-contained widget for the Lecture 04 slide "Simulator: TTL i premještanje"; no libraries, no network.
   Usage: <div class="dt-widget"></div><script src="assets/dns-ttl.js"></script>
   Croatian first; add English strings after the Croatian slide is reviewed.
   Model (shown in the footer): every client calls the service every 2 s; at 40 s the service moves to a new
   address and DNS answers with the new address immediately; each client cached the old answer at a different
   moment (staggered), so cache expiries are spread over one TTL. */
(function () {
  'use strict';

  const T_END = 120, MOVE = 40, PERIOD = 2;
  const TTLS = [0, 5, 15, 30, 60, 300];
  const OLD = '10.0.1.17', NEW = '10.0.2.31';

  const CSS = `
.dt-widget{box-sizing:border-box;width:1060px;margin:0 auto;padding:12px 16px;display:grid;gap:9px;
 border:1.5px solid #c6dbe8;border-radius:14px;background:#f8fbfd;color:#18344b;font-family:"Source Sans 3","Source Sans Pro",Arial,sans-serif;font-size:17px;line-height:1.25;text-align:left}
.dt-widget *{box-sizing:border-box}
.dt-row{display:flex;align-items:center;gap:8px}
.dt-row .dt-sp{flex:1}
.dt-lbl{font-size:15px;color:#546573;white-space:nowrap}
.dt-widget button{font:inherit;font-size:15px;color:#18344b;background:#fff;border:1.5px solid #a3c9dc;border-radius:999px;padding:3px 12px;cursor:pointer;white-space:nowrap}
.dt-widget button:hover:not(:disabled){background:#e7f3fb}
.dt-widget button:disabled{opacity:.4;cursor:default}
.dt-widget button.dt-on{background:#18344b;border-color:#18344b;color:#fff}
.dt-widget button:focus-visible,.dt-widget input:focus-visible{outline:2px solid #1585b4;outline-offset:2px}
.dt-check{display:flex;align-items:center;gap:5px;font-size:15px;white-space:nowrap}
.dt-check input{margin:0;accent-color:#3886ad}
.dt-count{min-width:22px;text-align:center;font-weight:700}
.dt-svg{display:block;width:1026px;height:268px;background:#fff;border:1.2px solid #c6dbe8;border-radius:10px}
.dt-svg text{font-family:Arial,sans-serif}
.dt-res{display:grid;grid-template-columns:1fr 1fr 1fr 1.3fr;gap:10px}
.dt-tile{padding:6px 12px;background:#fff;border:1.2px solid #c6dbe8;border-left:6px solid #3886ad;border-radius:10px;min-width:0}
.dt-tile small{display:block;font-size:14px;color:#546573}
.dt-tile b{display:block;font-size:23px;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dt-tile.dt-good{border-left-color:#3d7f4f;background:#f1f8f3}
.dt-tile.dt-bad{border-left-color:#b33e44;background:#fdf3f3}
.dt-tile.dt-warn{border-left-color:#b56a21;background:#fff6ea}
.dt-foot{font-size:13.5px;color:#546573}
`;

  function simulate(ttl, clients, refresh) {
    const rows = [];
    let lookups = 0, fails = 0, lastFail = -1;
    for (let c = 0; c < clients; c++) {
      const offset = (c * PERIOD) / clients;
      // The client looked up the name before t = 0, at a different phase of the TTL than the others.
      let expires = ttl === 0 ? 0 : ttl - (c / clients) * ttl;
      let addr = OLD;
      const ev = [];
      for (let t = offset; t <= T_END; t += PERIOD) {
        let lookup = false;
        if (t >= expires) {
          lookup = true; lookups += 1;
          addr = t < MOVE ? OLD : NEW;
          expires = t + ttl;
        }
        const ok = t < MOVE || addr === NEW;
        if (!ok) {
          fails += 1; lastFail = Math.max(lastFail, t);
          if (refresh) expires = t; // resolve again before the next call
        }
        ev.push({ t, ok, lookup });
      }
      rows.push(ev);
    }
    return { rows, lookups, fails, stale: lastFail < 0 ? 0 : lastFail - MOVE + PERIOD / clients, toEnd: lastFail >= T_END - PERIOD };
  }

  function init(root) {
    const st = { ttl: 30, clients: 5, refresh: false };
    root.innerHTML = `
      <div class="dt-row">
        <span class="dt-lbl">TTL u predmemoriji:</span>
        ${TTLS.map((v) => `<button data-ttl="${v}">${v === 0 ? '0 (bez predmemorije)' : v + ' s'}</button>`).join('')}
        <span class="dt-sp"></span>
        <button data-play>▶ Ponovi</button>
      </div>
      <div class="dt-row">
        <span class="dt-lbl">Klijenata:</span>
        <button data-delta="-1" aria-label="Manje klijenata">−</button><span class="dt-count"></span><button data-delta="1" aria-label="Više klijenata">+</button>
        <label class="dt-check" style="margin-left:14px"><input type="checkbox" data-refresh>nakon neuspjeha ponovno razriješi ime</label>
      </div>
      <svg class="dt-svg" viewBox="0 0 1026 268" role="img" aria-label="Pozivi klijenata prije i nakon premještanja usluge"></svg>
      <div class="dt-res">
        <div class="dt-tile" data-tile="fails"><small>Neuspjelih poziva</small><b></b></div>
        <div class="dt-tile" data-tile="stale"><small>Zastarjelost nakon premještanja</small><b></b></div>
        <div class="dt-tile" data-tile="lookups"><small>Upita DNS-u u 2 minute</small><b></b></div>
        <div class="dt-tile" data-tile="note"><small>Kompromis</small><b></b></div>
      </div>
      <div class="dt-foot">Svaki klijent poziva uslugu predaje svake 2 s. U 40. sekundi usluga prelazi s 10.0.1.17 na 10.0.2.31, a DNS odmah vraća novu adresu. Klijenti su staru adresu spremili u različitim trenucima. Vremena su ilustrativna.</div>`;

    const svg = root.querySelector('svg');
    const NS = 'http://www.w3.org/2000/svg';
    const X0 = 108, X1 = 1010;
    const x = (t) => X0 + (X1 - X0) * t / T_END;
    let raf = 0, run;
    function el(tag, attrs, text) {
      const e = document.createElementNS(NS, tag);
      for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
      if (text !== undefined) e.textContent = text;
      return e;
    }

    function draw() {
      run = simulate(st.ttl, st.clients, st.refresh);
      svg.innerHTML = '';
      const defs = el('defs', {});
      const clip = el('clipPath', { id: 'dt-clip' });
      const clipRect = el('rect', { x: 0, y: 0, width: X0, height: 268 });
      clip.appendChild(clipRect); defs.appendChild(clip); svg.appendChild(defs);
      svg.appendChild(el('rect', { x: x(MOVE), y: 14, width: X1 - x(MOVE), height: 200, fill: '#f8fbfd' }));
      svg.appendChild(el('text', { x: x(MOVE / 2), y: 26, 'font-size': 13.5, fill: '#546573', 'text-anchor': 'middle' }, `usluga na ${OLD}`));
      svg.appendChild(el('text', { x: x((MOVE + T_END) / 2), y: 26, 'font-size': 13.5, fill: '#546573', 'text-anchor': 'middle' }, `usluga na ${NEW}; DNS već vraća novu adresu`));
      const h = 176 / st.clients;
      run.rows.forEach((ev, c) => {
        const y = 40 + c * h + h / 2;
        svg.appendChild(el('text', { x: 12, y: y + 5, 'font-size': 14.5, 'font-weight': 700, fill: '#18344b' }, `Klijent ${c + 1}`));
        svg.appendChild(el('line', { x1: X0, y1: y, x2: X1, y2: y, stroke: '#e1ebf1', 'stroke-width': 1.5 }));
      });
      const g = el('g', { 'clip-path': 'url(#dt-clip)' });
      svg.appendChild(g);
      run.rows.forEach((ev, c) => {
        const y = 40 + c * h + h / 2;
        const half = Math.min(10, h * .32);
        ev.forEach((e) => {
          g.appendChild(el('rect', { x: x(e.t) - 2.2, y: y - half, width: 4.4, height: 2 * half, rx: 1.5, fill: e.ok ? '#3d7f4f' : '#b33e44' }));
          if (e.lookup) g.appendChild(el('path', { d: `M${x(e.t)},${y - half - 9} l5,5 l-5,5 l-5,-5 Z`, fill: '#3886ad' }));
        });
      });
      svg.appendChild(el('line', { x1: x(MOVE), y1: 14, x2: x(MOVE), y2: 214, stroke: '#b33e44', 'stroke-width': 2.5, 'stroke-dasharray': '6 5' }));
      for (let t = 0; t <= T_END; t += 20) {
        svg.appendChild(el('line', { x1: x(t), y1: 220, x2: x(t), y2: 226, stroke: '#8a99a6', 'stroke-width': 1.5 }));
        svg.appendChild(el('text', { x: x(t), y: 242, 'font-size': 12.5, fill: '#546573', 'text-anchor': 'middle' }, `${t} s`));
      }
      // Legend.
      const lg = [['#3d7f4f', 'poziv uspio'], ['#b33e44', 'poziv na staru adresu pao'], ['#3886ad', 'upit DNS-u']];
      lg.forEach(([c, t], i) => {
        const lx = 108 + i * 210;
        svg.appendChild(el(i === 2 ? 'path' : 'rect', i === 2 ? { d: `M${lx + 4},251 l5,5 l-5,5 l-5,-5 Z`, fill: c } : { x: lx, y: 250, width: 8, height: 12, rx: 2, fill: c }));
        svg.appendChild(el('text', { x: lx + 14, y: 261, 'font-size': 12.5, fill: '#546573' }, t));
      });

      cancelAnimationFrame(raf);
      const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const t0 = performance.now();
      function frame(now) {
        const p = reduce ? 1 : Math.min(1, (now - t0) / 3500);
        clipRect.setAttribute('width', x(p * T_END) + 4);
        tiles(p >= 1);
        if (p < 1) raf = requestAnimationFrame(frame);
      }
      raf = requestAnimationFrame(frame);
    }

    function tile(name, value, cls) {
      const t = root.querySelector(`[data-tile="${name}"]`);
      t.querySelector('b').textContent = value;
      t.classList.remove('dt-good', 'dt-bad', 'dt-warn');
      if (cls) t.classList.add(cls);
    }

    function tiles(done) {
      if (!done) { ['fails', 'stale', 'lookups', 'note'].forEach((n) => tile(n, '…')); return; }
      tile('fails', String(run.fails), run.fails ? 'dt-bad' : 'dt-good');
      tile('stale', !run.fails ? '0 s' : (run.toEnd ? `više od ${Math.round(run.stale)} s` : `oko ${Math.round(run.stale)} s`), run.fails ? 'dt-bad' : 'dt-good');
      const heavy = run.lookups > st.clients * 20;
      tile('lookups', String(run.lookups), heavy ? 'dt-warn' : null);
      let note;
      if (st.ttl === 0) note = 'točno, ali upit po pozivu';
      else if (run.fails && st.refresh) note = 'neuspjeh skraćuje grešku';
      else if (st.ttl >= 60) note = 'malo upita, duga greška';
      else note = 'kraći TTL: više upita';
      tile('note', note, null);
    }

    function sync() {
      root.querySelectorAll('[data-ttl]').forEach((b) => b.classList.toggle('dt-on', Number(b.dataset.ttl) === st.ttl));
      root.querySelector('.dt-count').textContent = st.clients;
      root.querySelector('[data-delta="-1"]').disabled = st.clients <= 2;
      root.querySelector('[data-delta="1"]').disabled = st.clients >= 8;
      root.querySelector('[data-refresh]').checked = st.refresh;
      draw();
    }

    root.addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b) return;
      if (b.dataset.ttl !== undefined) st.ttl = Number(b.dataset.ttl);
      else if (b.dataset.delta) st.clients = Math.min(8, Math.max(2, st.clients + Number(b.dataset.delta)));
      sync();
    });
    root.addEventListener('change', (e) => {
      if (e.target.matches('[data-refresh]')) { st.refresh = e.target.checked; sync(); }
    });
    root.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'BUTTON') e.stopPropagation();
    });
    if (window.Reveal && Reveal.on) {
      Reveal.on('slidechanged', (ev) => { if (ev.currentSlide && ev.currentSlide.contains(root)) draw(); });
    }
    sync();
  }

  if (!document.getElementById('dt-style')) {
    const style = document.createElement('style');
    style.id = 'dt-style';
    style.textContent = CSS;
    document.head.appendChild(style);
  }
  document.querySelectorAll('.dt-widget').forEach(init);
})();
