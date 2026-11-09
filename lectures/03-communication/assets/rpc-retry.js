/* Retry simulator: recording a submission with timeouts, retries and an idempotency key (2026-11-09, rev. 2).
   Self-contained widget for the Lecture 03 slide "Simulator: ponovni pokušaj i ključ"; no libraries, no network.
   Usage: <div class="rr-widget"></div><script src="assets/rpc-retry.js"></script>
   Croatian first; add English strings after the Croatian slide is reviewed.
   Operation: the portal calls SnimiPredaju(p-2026-0812) on the submission service,
   which inserts a row into the submissions table. Defaults: no retries, no fault (lecturer, 2026-11-09). Without a key every executed attempt inserts a row;
   with a key the service finds K and returns the saved reply instead.
   Model (shown in the footer): deadline 2 s per attempt, next attempt 0.3 s after the deadline,
   one-way delay 0.3 s, processing 0.5 s (slow: 3.2 s); the server does not stop work when the client gives up. */
(function () {
  'use strict';

  const DELAY = 0.3, PROC = 0.5, SLOW = 3.2, DEADLINE = 2.0, GAP = 0.3, QUICK = 0.1;
  const FAULTS = [
    ['none', 'Bez kvara'],
    ['lostReq', 'Izgubljen zahtjev'],
    ['slow', 'Spora obrada'],
    ['lostResp', 'Izgubljen odgovor'],
  ];
  const PRESETS = {
    once: { attempts: 1, key: false, label: 'Bez ponavljanja' },
    retry: { attempts: 3, key: false, label: 'Ponavljanje' },
    retryKey: { attempts: 3, key: true, label: 'Ponavljanje + ključ' },
  };

  const CSS = `
.rr-widget{box-sizing:border-box;width:1060px;margin:0 auto;padding:12px 16px;display:grid;gap:9px;
 border:1.5px solid #c6dbe8;border-radius:14px;background:#f8fbfd;color:#18344b;font-family:"Source Sans 3","Source Sans Pro",Arial,sans-serif;font-size:17px;line-height:1.25;text-align:left}
.rr-widget *{box-sizing:border-box}
.rr-row{display:flex;align-items:center;gap:8px;flex-wrap:nowrap}
.rr-row .rr-sp{flex:1}
.rr-lbl{font-size:15px;color:#546573;margin-right:2px;white-space:nowrap}
.rr-widget button{font:inherit;font-size:15px;color:#18344b;background:#fff;border:1.5px solid #a3c9dc;border-radius:999px;padding:3px 12px;cursor:pointer;white-space:nowrap}
.rr-widget button:hover:not(:disabled){background:#e7f3fb}
.rr-widget button:disabled{opacity:.4;cursor:default}
.rr-widget button.rr-on{background:#18344b;border-color:#18344b;color:#fff}
.rr-widget button:focus-visible,.rr-widget input:focus-visible{outline:2px solid #1585b4;outline-offset:2px}
.rr-check{display:flex;align-items:center;gap:5px;font-size:15px;white-space:nowrap}
.rr-check input{margin:0;accent-color:#3886ad}
.rr-count{min-width:22px;text-align:center;font-weight:700}
.rr-sem{padding:3px 12px;border-radius:999px;background:#e7f3fb;border:1.5px solid #8cbad7;font-size:15px;font-weight:700;color:#184d70;white-space:nowrap}
.rr-svg{display:block;width:1026px;height:236px;background:#fff;border:1.2px solid #c6dbe8;border-radius:10px}
.rr-svg text{font-family:Arial,sans-serif}
.rr-res{display:grid;grid-template-columns:.9fr 1fr 1.5fr 1.7fr;gap:10px}
.rr-tile{padding:6px 12px;background:#fff;border:1.2px solid #c6dbe8;border-left:6px solid #3886ad;border-radius:10px;min-width:0}
.rr-tile small{display:block;font-size:14px;color:#546573}
.rr-tile b{display:block;font-size:23px;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rr-tile.rr-good{border-left-color:#3d7f4f;background:#f1f8f3}
.rr-tile.rr-bad{border-left-color:#b33e44;background:#fdf3f3}
.rr-tile.rr-warn{border-left-color:#b56a21;background:#fff6ea}
.rr-foot{font-size:13.5px;color:#546573}
`;

  function guarantee(attempts, key) {
    if (attempts === 1) return 'najviše jednom';
    return key ? 'učinak točno jednom' : 'barem jednom';
  }

  // Event model for one run. Times are in seconds from the first attempt.
  function simulate(fault, persistent, attempts, useKey) {
    const att = [];
    let rows = 0, known = false, outcome = null, keyDoneAt = null, end = 0;
    for (let k = 0; k < attempts; k++) {
      const start = k * (DEADLINE + GAP);
      const f = (k === 0 || persistent) ? fault : 'none';
      const a = { k, start, deadline: start + DEADLINE, lostReq: f === 'lostReq', lostResp: f === 'lostResp' };
      if (!a.lostReq) {
        a.arrive = start + DELAY;
        if (useKey && keyDoneAt !== null) {
          a.kind = keyDoneAt <= a.arrive ? 'saved' : 'busy';
          a.proc = QUICK;
        } else {
          a.kind = 'run';
          a.proc = f === 'slow' ? SLOW : PROC;
          rows += 1;
          a.rowNo = rows;
          if (useKey) keyDoneAt = a.arrive + a.proc;
        }
        a.sent = a.arrive + a.proc;
        a.replyAt = a.sent + DELAY;
        a.late = !a.lostResp && a.replyAt > a.deadline;
      }
      if (!a.lostReq && !a.lostResp && !a.late) {
        known = true;
        outcome = a.kind;
        a.success = true;
        att.push(a);
        break;
      }
      a.timeout = true;
      att.push(a);
    }
    att.forEach((a) => {
      end = Math.max(end, a.start + DELAY, a.timeout ? a.deadline : 0, a.sent || 0, a.replyAt || 0);
    });
    return { att, rows, known, outcome, end: Math.max(end + .3, 5.2) };
  }

  function init(root) {
    const st = { fault: 'none', persistent: false, attempts: 1, key: false };
    root.innerHTML = `
      <div class="rr-row">
        <span class="rr-lbl">Klijent:</span>
        ${Object.entries(PRESETS).map(([id, p]) => `<button data-preset="${id}">${p.label}</button>`).join('')}
        <span class="rr-lbl" style="margin-left:10px">Jamstvo:</span><span class="rr-sem"></span>
        <span class="rr-sp"></span>
        <button data-play>▶ Ponovi</button>
      </div>
      <div class="rr-row">
        <span class="rr-lbl">Kvar:</span>
        ${FAULTS.map(([id, label]) => `<button data-fault="${id}">${label}</button>`).join('')}
        <label class="rr-check"><input type="checkbox" data-persist>u svakom pokušaju</label>
        <span class="rr-sp"></span>
        <span class="rr-lbl">Pokušaja:</span>
        <button data-delta="-1" aria-label="Manje pokušaja">−</button><span class="rr-count"></span><button data-delta="1" aria-label="Više pokušaja">+</button>
        <label class="rr-check"><input type="checkbox" data-key>ključ K</label>
      </div>
      <svg class="rr-svg" viewBox="0 0 1026 236" role="img" aria-label="Vremenska crta snimanja predaje, ponovnih pokušaja i tablice u bazi"></svg>
      <div class="rr-res">
        <div class="rr-tile" data-tile="att"><small>Pokušaja poslano</small><b></b></div>
        <div class="rr-tile" data-tile="rows"><small>Zapisa u bazi</small><b></b></div>
        <div class="rr-tile" data-tile="know"><small>Što portal zna</small><b></b></div>
        <div class="rr-tile" data-tile="inv"><small>Jedna predaja, jedan zapis</small><b></b></div>
      </div>
      <div class="rr-foot">Operacija: SnimiPredaju(p-2026-0812); ključ K = predaja_id. Rok 2 s po pokušaju; sljedeći pokušaj 0,3 s nakon isteka; mreža 0,3 s u svakom smjeru; snimanje 0,5 s (sporo 3,2 s). Kad klijent odustane, poslužitelj ne prekida posao. Vremena su ilustrativna.</div>`;

    const svg = root.querySelector('svg');
    const NS = 'http://www.w3.org/2000/svg';
    const X0 = 132, X1 = 724, YC = 66, YS = 170, TX = 744;
    let run, scale, raf = 0;

    const x = (t) => X0 + t * scale;
    function el(tag, attrs, text) {
      const e = document.createElementNS(NS, tag);
      for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function arrow(g, x1, y1, x2, y2, color, dash) {
      g.appendChild(el('line', { x1, y1, x2, y2, stroke: color, 'stroke-width': 2.6, 'stroke-dasharray': dash ? '6 5' : 'none', 'marker-end': `url(#rr-m-${color.slice(1)})` }));
    }
    function cross(g, cx, cy) {
      g.appendChild(el('path', { d: `M${cx - 8},${cy - 8} L${cx + 8},${cy + 8} M${cx + 8},${cy - 8} L${cx - 8},${cy + 8}`, stroke: '#b33e44', 'stroke-width': 3.2, 'stroke-linecap': 'round' }));
    }

    let rowEls = [];
    function draw() {
      run = simulate(st.fault, st.persistent, st.attempts, st.key);
      scale = (X1 - X0) / run.end;
      svg.innerHTML = '';
      const defs = el('defs', {});
      ['#3886ad', '#b33e44', '#8a99a6', '#3d7f4f'].forEach((c) => {
        const m = el('marker', { id: `rr-m-${c.slice(1)}`, markerUnits: 'userSpaceOnUse', markerWidth: 14, markerHeight: 14, refX: 11, refY: 7, orient: 'auto' });
        m.appendChild(el('path', { d: 'M1,1 L13,7 L1,13 Z', fill: c }));
        defs.appendChild(m);
      });
      const clip = el('clipPath', { id: 'rr-clip' });
      const clipRect = el('rect', { x: 0, y: 0, width: X0, height: 236 });
      clip.appendChild(clipRect);
      defs.appendChild(clip);
      svg.appendChild(defs);

      // Lanes and time axis.
      [[YC, 'Portal', 'klijent'], [YS, 'Usluga predaje', 'poslužitelj']].forEach(([y, a, b]) => {
        svg.appendChild(el('text', { x: 12, y: y - 2, 'font-size': 16, 'font-weight': 700, fill: '#18344b' }, a));
        svg.appendChild(el('text', { x: 12, y: y + 17, 'font-size': 14, fill: '#546573' }, b));
        svg.appendChild(el('line', { x1: X0, y1: y, x2: X1, y2: y, stroke: '#c6dbe8', 'stroke-width': 2 }));
      });
      for (let t = 0; t <= run.end; t += 1) {
        svg.appendChild(el('line', { x1: x(t), y1: 214, x2: x(t), y2: 220, stroke: '#8a99a6', 'stroke-width': 1.5 }));
        svg.appendChild(el('text', { x: x(t), y: 232, 'font-size': 12.5, fill: '#546573', 'text-anchor': 'middle' }, `${t} s`));
      }

      // Database table on the right; rows appear when the playhead passes the moment they are saved.
      svg.appendChild(el('rect', { x: TX, y: 10, width: 270, height: 214, rx: 10, fill: '#f8fbfd', stroke: '#c6dbe8' }));
      svg.appendChild(el('text', { x: TX + 14, y: 34, 'font-size': 15, 'font-weight': 700, fill: '#18344b' }, 'Baza: tablica predaja'));
      svg.appendChild(el('text', { x: TX + 14, y: 56, 'font-size': 12.5, fill: '#546573' }, st.key ? 'zapis · predaja · ključ' : 'zapis · predaja'));
      svg.appendChild(el('line', { x1: TX + 10, y1: 63, x2: TX + 260, y2: 63, stroke: '#c6dbe8' }));
      rowEls = [];
      run.att.filter((a) => a.kind === 'run').forEach((a, i) => {
        const dup = a.rowNo > 1;
        const g = el('g', {});
        const y = 72 + i * 38;
        g.appendChild(el('rect', { x: TX + 10, y, width: 250, height: 32, rx: 6, fill: dup ? '#fdf3f3' : '#f1f8f3', stroke: dup ? '#e3b9bc' : '#b9d8c2' }));
        g.appendChild(el('text', { x: TX + 20, y: y + 21, 'font-size': 14, 'font-weight': 700, fill: dup ? '#b33e44' : '#3d7f4f' }, `#${a.rowNo}`));
        g.appendChild(el('text', { x: TX + 50, y: y + 21, 'font-size': 14, fill: '#18344b' }, 'p-2026-0812' + (st.key ? '  ·  K' : '')));
        if (dup) g.appendChild(el('text', { x: TX + 252, y: y + 21, 'font-size': 13, 'font-weight': 700, fill: '#b33e44', 'text-anchor': 'end' }, 'duplikat'));
        g.style.display = 'none';
        svg.appendChild(g);
        rowEls.push({ g, t: a.sent });
      });

      const g = el('g', { 'clip-path': 'url(#rr-clip)' });
      svg.appendChild(g);
      run.att.forEach((a) => {
        g.appendChild(el('text', { x: x(a.start) + 2, y: YC - 26, 'font-size': 13.5, 'font-weight': 700, fill: '#18344b' }, `pokušaj ${a.k + 1}` + (st.key ? ' · K' : '')));
        g.appendChild(el('circle', { cx: x(a.start), cy: YC, r: 5, fill: '#3886ad' }));
        if (a.lostReq) {
          const t = a.start + DELAY * .6;
          arrow(g, x(a.start), YC, x(t), YC + (YS - YC) * .6, '#3886ad');
          cross(g, x(t) + 6, YC + (YS - YC) * .6 + 6);
        } else {
          arrow(g, x(a.start), YC, x(a.arrive), YS, '#3886ad');
          const w = Math.max(x(a.sent) - x(a.arrive), 7);
          const dup = a.kind === 'run' && a.rowNo > 1;
          const color = a.kind === 'run' ? (dup ? '#b33e44' : '#3886ad') : '#8a99a6';
          g.appendChild(el('rect', { x: x(a.arrive), y: YS + 5, width: w, height: 13, rx: 3, fill: color }));
          const label = a.kind === 'run' ? `snimi zapis #${a.rowNo}` : (a.kind === 'saved' ? 'K poznat: isti odgovor' : 'K u obradi');
          g.appendChild(el('text', { x: x(a.arrive), y: YS + 34, 'font-size': 13.5, 'font-weight': a.kind === 'run' ? 700 : 400, fill: a.kind === 'run' ? (dup ? '#b33e44' : '#105d80') : '#546573' }, label));
          if (a.lostResp) {
            const t = a.sent + DELAY * .6;
            arrow(g, x(a.sent), YS, x(t), YS - (YS - YC) * .6, '#3886ad');
            cross(g, x(t) + 6, YS - (YS - YC) * .6 - 6);
          } else if (a.late) {
            arrow(g, x(a.sent), YS, x(a.replyAt), YC, '#8a99a6', true);
            g.appendChild(el('text', { x: x(a.replyAt) + 4, y: YC + 22, 'font-size': 13, fill: '#546573' }, 'prekasno'));
          } else {
            arrow(g, x(a.sent), YS, x(a.replyAt), YC, '#3d7f4f');
            g.appendChild(el('text', { x: x(a.replyAt) + 4, y: YC - 8, 'font-size': 14, 'font-weight': 700, fill: '#3d7f4f' }, 'odgovor ✓'));
          }
        }
        if (a.timeout) {
          g.appendChild(el('line', { x1: x(a.deadline), y1: YC - 12, x2: x(a.deadline), y2: YC + 12, stroke: '#b33e44', 'stroke-width': 3 }));
          g.appendChild(el('text', { x: x(a.deadline), y: YC + 30, 'font-size': 13.5, 'font-weight': 700, fill: '#b33e44', 'text-anchor': 'middle' }, 'istek'));
        }
      });
      const head = el('line', { x1: X0, y1: 24, x2: X0, y2: 208, stroke: '#18344b', 'stroke-width': 1.2, 'stroke-dasharray': '3 4', opacity: .5 });
      svg.appendChild(head);

      // Animate a playhead from left to right; table rows and counters follow it.
      cancelAnimationFrame(raf);
      const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const total = run.end * 650;
      const t0 = performance.now();
      function frame(now) {
        const p = reduce ? 1 : Math.min(1, (now - t0) / total);
        const t = p * run.end;
        clipRect.setAttribute('width', x(t) + 2);
        head.setAttribute('x1', x(t)); head.setAttribute('x2', x(t));
        head.style.display = p >= 1 ? 'none' : '';
        rowEls.forEach((r) => { r.g.style.display = (p >= 1 || r.t <= t) ? '' : 'none'; });
        tiles(t, p >= 1);
        if (p < 1) raf = requestAnimationFrame(frame);
      }
      raf = requestAnimationFrame(frame);
    }

    function tile(name, value, cls) {
      const t = root.querySelector(`[data-tile="${name}"]`);
      t.querySelector('b').textContent = value;
      t.classList.remove('rr-good', 'rr-bad', 'rr-warn');
      if (cls) t.classList.add(cls);
    }

    function tiles(t, done) {
      const sent = run.att.filter((a) => a.start <= t).length;
      const rows = done ? run.rows : run.att.filter((a) => a.kind === 'run' && a.sent <= t).length;
      tile('att', String(sent));
      tile('rows', String(rows), rows > 1 ? 'rr-bad' : null);
      if (!done) {
        tile('know', 'čeka…');
        tile('inv', rows > 1 ? 'prekršena' : '…', rows > 1 ? 'rr-bad' : null);
        return;
      }
      if (run.known) tile('know', run.outcome === 'busy' ? 'predaja se snima' : 'predaja je snimljena', 'rr-good');
      else tile('know', 'ishod nepoznat', 'rr-warn');
      if (run.rows > 1) tile('inv', `prekršena: ${run.rows} zapisa`, 'rr-bad');
      else if (run.rows === 0) tile('inv', 'nema zapisa: nije snimljeno', 'rr-warn');
      else tile('inv', 'očuvana', 'rr-good');
    }

    function sync() {
      root.querySelectorAll('[data-fault]').forEach((b) => b.classList.toggle('rr-on', b.dataset.fault === st.fault));
      root.querySelectorAll('[data-preset]').forEach((b) => {
        const p = PRESETS[b.dataset.preset];
        b.classList.toggle('rr-on', p.attempts === st.attempts && p.key === st.key);
      });
      root.querySelector('.rr-sem').textContent = guarantee(st.attempts, st.key);
      root.querySelector('[data-persist]').checked = st.persistent;
      root.querySelector('[data-key]').checked = st.key;
      root.querySelector('.rr-count').textContent = st.attempts;
      root.querySelector('[data-delta="-1"]').disabled = st.attempts <= 1;
      root.querySelector('[data-delta="1"]').disabled = st.attempts >= 4;
      draw();
    }

    root.addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b) return;
      if (b.dataset.preset) Object.assign(st, { attempts: PRESETS[b.dataset.preset].attempts, key: PRESETS[b.dataset.preset].key });
      else if (b.dataset.fault) st.fault = b.dataset.fault;
      else if (b.dataset.delta) st.attempts = Math.min(4, Math.max(1, st.attempts + Number(b.dataset.delta)));
      sync();
    });
    root.addEventListener('change', (e) => {
      if (e.target.matches('[data-persist]')) st.persistent = e.target.checked;
      else if (e.target.matches('[data-key]')) st.key = e.target.checked;
      else return;
      sync();
    });
    // Keys on controls must not change the slide.
    root.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'BUTTON') e.stopPropagation();
    });

    // Replay when the slide becomes visible, so the animation is not missed.
    if (window.Reveal && Reveal.on) {
      Reveal.on('slidechanged', (ev) => { if (ev.currentSlide && ev.currentSlide.contains(root)) draw(); });
    }
    sync();
  }

  if (!document.getElementById('rr-style')) {
    const style = document.createElement('style');
    style.id = 'rr-style';
    style.textContent = CSS;
    document.head.appendChild(style);
  }
  document.querySelectorAll('.rr-widget').forEach(init);
})();
