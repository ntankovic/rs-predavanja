/* Service registry with leases: crash, pause and false removal (2026-11-09).
   Self-contained widget for the Lecture 04 slide "Simulator: registar s najmom"; no libraries, no network.
   Usage: <div class="lr-widget"></div><script src="assets/lease-registry.js"></script>
   Croatian first; add English strings after the Croatian slide is reviewed.
   Model (shown in the footer): instances A, B, C renew their lease every H seconds (phases staggered);
   the registry drops an instance TTL seconds after its last renewal; B crashes at 15 s; optionally C pauses
   for 8 s from 30 s (e.g. a garbage-collection pause): it neither renews nor serves, then resumes and
   registers again with a new lease. Portal requests arrive as a Poisson process (mean gap 0.5 s, fixed seed),
   round-robin over the instances currently in the registry, without retries. */
(function () {
  'use strict';

  const T_END = 60, CRASH = 15, PAUSE_AT = 30, PAUSE = 8, REQ = 0.5, STEP = 0.05;
  const TTLS = [2, 5, 10, 20, 30];
  const HS = [1, 2, 5, 10];
  const NAMES = ['A', 'B', 'C'];

  const CSS = `
.lr-widget{box-sizing:border-box;width:1060px;margin:0 auto;padding:12px 16px;display:grid;gap:9px;
 border:1.5px solid #c6dbe8;border-radius:14px;background:#f8fbfd;color:#18344b;font-family:"Source Sans 3","Source Sans Pro",Arial,sans-serif;font-size:17px;line-height:1.25;text-align:left}
.lr-widget *{box-sizing:border-box}
.lr-row{display:flex;align-items:center;gap:8px}
.lr-row .lr-sp{flex:1}
.lr-lbl{font-size:15px;color:#546573;white-space:nowrap}
.lr-widget button{font:inherit;font-size:15px;color:#18344b;background:#fff;border:1.5px solid #a3c9dc;border-radius:999px;padding:3px 12px;cursor:pointer;white-space:nowrap}
.lr-widget button:hover{background:#e7f3fb}
.lr-widget button.lr-on{background:#18344b;border-color:#18344b;color:#fff}
.lr-widget button:focus-visible,.lr-widget input:focus-visible{outline:2px solid #1585b4;outline-offset:2px}
.lr-check{display:flex;align-items:center;gap:5px;font-size:15px;white-space:nowrap}
.lr-check input{margin:0;accent-color:#3886ad}
.lr-warn{font-size:14.5px;font-weight:700;color:#b33e44}
.lr-svg{display:block;width:1026px;height:236px;background:#fff;border:1.2px solid #c6dbe8;border-radius:10px}
.lr-svg text{font-family:Arial,sans-serif}
.lr-res{display:grid;grid-template-columns:1fr 1.3fr 1fr 1fr;gap:10px}
.lr-tile{padding:6px 12px;background:#fff;border:1.2px solid #c6dbe8;border-left:6px solid #3886ad;border-radius:10px;min-width:0}
.lr-tile small{display:block;font-size:14px;color:#546573}
.lr-tile b{display:block;font-size:23px;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lr-tile.lr-good{border-left-color:#3d7f4f;background:#f1f8f3}
.lr-tile.lr-bad{border-left-color:#b33e44;background:#fdf3f3}
.lr-tile.lr-warn{border-left-color:#b56a21;background:#fff6ea}
.lr-foot{font-size:13.5px;color:#546573}
.lr-intro{font-size:15.5px;line-height:1.3;color:#18344b}
.lr-intro b{color:#105d80}
`;

  function simulate(ttl, h, pause) {
    // Per instance: alive(t), serving(t); registry membership is derived from renewals.
    const alive = (i, t) => !(i === 1 && t >= CRASH);
    const paused = (i, t) => pause && i === 2 && t >= PAUSE_AT && t < PAUSE_AT + PAUSE;
    const serving = (i, t) => alive(i, t) && !paused(i, t);
    const lastRenew = [0, 0, 0];
    const inReg = [true, true, true];
    const renewals = [[], [], []];
    const segs = [[], [], []];
    const state = (i, t) => (inReg[i] ? (serving(i, t) ? 'ok' : 'dead') : (serving(i, t) ? 'out' : 'gone'));
    const cur = NAMES.map((_, i) => ({ s: state(i, 0), from: 0 }));
    const wasServing = [true, true, true];
    let falseRemovals = 0, removedB = null, renewCount = 0;
    const reqs = [];
    // Portal requests arrive as a Poisson process (mean gap REQ); fixed seed so every replay looks the same.
    let seed = 20261110;
    const rand = () => { seed = (seed + 0x6D2B79F5) | 0; let z = Math.imul(seed ^ (seed >>> 15), 1 | seed); z = (z + Math.imul(z ^ (z >>> 7), 61 | z)) ^ z; return ((z ^ (z >>> 14)) >>> 0) / 4294967296; };
    const gap = () => -Math.log(1 - rand()) * REQ;
    let rr = 0, nextReq = gap();
    for (let k = 0; k * STEP <= T_END + 1e-9; k++) {
      const t = +(k * STEP).toFixed(3);
      for (let i = 0; i < 3; i++) {
        const phase = (i * h) / 3;
        // The registry checks expiry first: a renewal that arrives exactly at expiry is too late.
        if (inReg[i] && t - lastRenew[i] >= ttl - 1e-9) {
          inReg[i] = false;
          if (alive(i, t)) falseRemovals += 1; // removed although not crashed (e.g. paused)
          if (i === 1 && removedB === null && t >= CRASH) removedB = t;
        }
        // Renewal moments: phase, phase + h, ...
        // An instance that resumes after a pause renews at once.
        const due = (t >= phase && Math.abs((t - phase) - Math.round((t - phase) / h) * h) < STEP / 2)
          || (serving(i, t) && !wasServing[i]);
        if (due && serving(i, t)) {
          if (!inReg[i]) inReg[i] = true; // re-register with a new lease
          lastRenew[i] = t; renewals[i].push(t); renewCount += 1;
        }
        wasServing[i] = serving(i, t);
        const s = state(i, t);
        if (s !== cur[i].s) { segs[i].push({ s: cur[i].s, from: cur[i].from, to: t }); cur[i] = { s, from: t }; }
      }
      while (t >= nextReq - 1e-9 && nextReq <= T_END) {
        const members = [0, 1, 2].filter((i) => inReg[i]);
        if (members.length) {
          const i = members[rr % members.length]; rr += 1;
          reqs.push({ t: nextReq, i, ok: serving(i, t) });
        } else {
          reqs.push({ t: nextReq, i: -1, ok: false });
        }
        nextReq += gap();
      }
    }
    for (let i = 0; i < 3; i++) segs[i].push({ s: cur[i].s, from: cur[i].from, to: T_END });
    const fails = reqs.filter((r) => !r.ok).length;
    return { segs, renewals, reqs, fails, falseRemovals, removedB, renewPerMin: Math.round(renewCount * 60 / T_END) };
  }

  function init(root) {
    const st = { ttl: 10, h: 2, pause: false };
    root.innerHTML = `
      <div class="lr-intro"><b>Registar usluga</b> drži popis instanci usluge predaje. Svaka instanca u registru ima <b>najam</b> i obnavlja ga <b>otkucajem ♥</b>; ako otkucaji izostanu dulje od TTL-a, registar je briše. Portal šalje zahtjeve samo instancama iz registra.</div>
      <div class="lr-row">
        <span class="lr-lbl">TTL najma:</span>
        ${TTLS.map((v) => `<button data-ttl="${v}">${v} s</button>`).join('')}
        <span class="lr-lbl" style="margin-left:12px">Otkucaj svakih:</span>
        ${HS.map((v) => `<button data-h="${v}">${v} s</button>`).join('')}
        <span class="lr-sp"></span>
        <button data-play>▶ Ponovi</button>
      </div>
      <div class="lr-row">
        <label class="lr-check"><input type="checkbox" data-pause>instanca C zastane 8 s (npr. pauza skupljača smeća)</label>
        <span class="lr-sp"></span>
        <span class="lr-warn"></span>
      </div>
      <svg class="lr-svg" viewBox="0 0 1026 236" role="img" aria-label="Stanje instanci u registru kroz vrijeme"></svg>
      <div class="lr-res">
        <div class="lr-tile" data-tile="fails"><small>Neuspjelih zahtjeva</small><b></b></div>
        <div class="lr-tile" data-tile="removed"><small>Srušena B u registru još</small><b></b></div>
        <div class="lr-tile" data-tile="false"><small>Lažnih uklanjanja</small><b></b></div>
        <div class="lr-tile" data-tile="load"><small>Otkucaja u minuti</small><b></b></div>
      </div>
      <div class="lr-foot">B se sruši u 15. sekundi. Portal šalje zahtjeve u nasumičnim trenucima (Poissonov proces, prosječno 2 u sekundi) instancama koje su trenutno u registru, redom i bez ponavljanja. Instanca koja se vrati nakon pauze ponovno se registrira s novim najmom. Vremena su ilustrativna.</div>`;

    const svg = root.querySelector('svg');
    const NS = 'http://www.w3.org/2000/svg';
    const X0 = 96, X1 = 1010;
    const x = (t) => X0 + (X1 - X0) * t / T_END;
    const COLORS = { ok: '#d7eedd', dead: '#f6d6d8', out: '#fbe5c8', gone: '#eef1f3' };
    let raf = 0, run;
    function el(tag, attrs, text) {
      const e = document.createElementNS(NS, tag);
      for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
      if (text !== undefined) e.textContent = text;
      return e;
    }

    function draw() {
      run = simulate(st.ttl, st.h, st.pause);
      svg.innerHTML = '';
      const defs = el('defs', {});
      const clip = el('clipPath', { id: 'lr-clip' });
      const clipRect = el('rect', { x: 0, y: 0, width: X0, height: 236 });
      clip.appendChild(clipRect); defs.appendChild(clip); svg.appendChild(defs);
      const g = el('g', { 'clip-path': 'url(#lr-clip)' });
      NAMES.forEach((n, i) => {
        const y = 22 + i * 58;
        svg.appendChild(el('text', { x: 12, y: y + 24, 'font-size': 15, 'font-weight': 700, fill: '#18344b' }, `Instanca ${n}`));
        svg.appendChild(el('rect', { x: X0, y, width: X1 - X0, height: 34, rx: 6, fill: '#fbfcfd', stroke: '#e1ebf1' }));
        run.segs[i].forEach((s) => g.appendChild(el('rect', { x: x(s.from), y, width: Math.max(x(s.to) - x(s.from), 0), height: 34, fill: COLORS[s.s] })));
        run.renewals[i].forEach((t) => g.appendChild(el('text', { x: x(t), y: y - 3, 'font-size': 12, fill: '#3d7f4f', 'text-anchor': 'middle' }, '♥')));
        run.reqs.filter((r) => r.i === i).forEach((r) => g.appendChild(el('circle', { cx: x(r.t), cy: y + 17, r: 3.3, fill: r.ok ? '#3d7f4f' : '#b33e44' })));
      });
      svg.appendChild(g);
      const marks = [[CRASH, '⚡ B se sruši']];
      if (st.pause) marks.push([PAUSE_AT, 'C zastane']);
      marks.forEach(([t, lab]) => {
        svg.appendChild(el('line', { x1: x(t), y1: 14, x2: x(t), y2: 196, stroke: '#b33e44', 'stroke-width': 2, 'stroke-dasharray': '5 4' }));
        svg.appendChild(el('text', { x: x(t) + 4, y: 12, 'font-size': 12.5, 'font-weight': 700, fill: '#b33e44' }, lab));
      });
      for (let t = 0; t <= T_END; t += 10) {
        svg.appendChild(el('line', { x1: x(t), y1: 198, x2: x(t), y2: 204, stroke: '#8a99a6', 'stroke-width': 1.5 }));
        svg.appendChild(el('text', { x: x(t), y: 217, 'font-size': 12.5, fill: '#546573', 'text-anchor': 'middle' }, `${t} s`));
      }
      const lg = [['ok', 'u registru, radi'], ['dead', 'u registru, ne radi'], ['out', 'radi, ali uklonjena'], ['gone', 'nije u registru']];
      lg.forEach(([k, t], i) => {
        const lx = 12 + i * 165;
        svg.appendChild(el('rect', { x: lx, y: 222, width: 14, height: 11, rx: 2, fill: COLORS[k], stroke: '#c6dbe8' }));
        svg.appendChild(el('text', { x: lx + 19, y: 232, 'font-size': 12.5, fill: '#546573' }, t));
      });
      svg.appendChild(el('circle', { cx: 672, cy: 228, r: 3.3, fill: '#3d7f4f' }));
      svg.appendChild(el('text', { x: 680, y: 232, 'font-size': 12.5, fill: '#546573' }, 'zahtjev portala uspio'));
      svg.appendChild(el('circle', { cx: 816, cy: 228, r: 3.3, fill: '#b33e44' }));
      svg.appendChild(el('text', { x: 824, y: 232, 'font-size': 12.5, fill: '#546573' }, 'pao'));
      svg.appendChild(el('text', { x: 862, y: 233, 'font-size': 13, fill: '#3d7f4f' }, '♥'));
      svg.appendChild(el('text', { x: 876, y: 232, 'font-size': 12.5, fill: '#546573' }, 'otkucaj (obnova najma)'));

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
      t.classList.remove('lr-good', 'lr-bad', 'lr-warn');
      if (cls) t.classList.add(cls);
    }

    function tiles(done) {
      if (!done) { ['fails', 'removed', 'false', 'load'].forEach((n) => tile(n, '…')); return; }
      tile('fails', String(run.fails), run.fails ? 'lr-bad' : 'lr-good');
      const stayed = run.removedB === null ? null : run.removedB - CRASH;
      tile('removed', stayed === null ? 'do kraja' : `${stayed.toFixed(1).replace('.', ',')} s`, stayed !== null && stayed <= 5 ? 'lr-good' : 'lr-bad');
      tile('false', String(run.falseRemovals), run.falseRemovals ? 'lr-warn' : 'lr-good');
      tile('load', String(run.renewPerMin), run.renewPerMin > 100 ? 'lr-warn' : null);
    }

    function sync() {
      root.querySelectorAll('[data-ttl]').forEach((b) => b.classList.toggle('lr-on', Number(b.dataset.ttl) === st.ttl));
      root.querySelectorAll('[data-h]').forEach((b) => b.classList.toggle('lr-on', Number(b.dataset.h) === st.h));
      root.querySelector('[data-pause]').checked = st.pause;
      root.querySelector('.lr-warn').textContent = st.h >= st.ttl ? 'Otkucaj nije češći od TTL-a: ispravne instance ispadaju iz registra.' : '';
      draw();
    }

    root.addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b) return;
      if (b.dataset.ttl) st.ttl = Number(b.dataset.ttl);
      else if (b.dataset.h) st.h = Number(b.dataset.h);
      sync();
    });
    root.addEventListener('change', (e) => {
      if (e.target.matches('[data-pause]')) { st.pause = e.target.checked; sync(); }
    });
    root.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'BUTTON') e.stopPropagation();
    });
    if (window.Reveal && Reveal.on) {
      Reveal.on('slidechanged', (ev) => { if (ev.currentSlide && ev.currentSlide.contains(root)) draw(); });
    }
    sync();
  }

  if (!document.getElementById('lr-style')) {
    const style = document.createElement('style');
    style.id = 'lr-style';
    style.textContent = CSS;
    document.head.appendChild(style);
  }
  document.querySelectorAll('.lr-widget').forEach(init);
})();
