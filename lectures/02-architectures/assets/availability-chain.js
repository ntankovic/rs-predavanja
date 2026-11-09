/* Availability of a synchronous service chain: A = a1 x a2 x ... x an (2026-11-09).
   Self-contained widget for the Lecture 02 slide after "Cijena granice 2"; no libraries, no network.
   Usage: <div class="ac-widget"></div><script src="assets/availability-chain.js"></script>
   Croatian first; add strings for English after the Croatian slide is reviewed.
   Assumptions shown in the widget: independent failures, every synchronous service required, no retries. */
(function () {
  'use strict';

  const NAMES = ['Predaja', 'Zadaci', 'Korisnici', 'Pohrana', 'Obavijesti', 'Provjera'];
  const LEVELS = [90, 95, 98, 99, 99.5, 99.9, 99.95, 99.99, 99.999];
  const DEFAULT_LEVEL = 5; // 99.9 %
  const HOURS_PER_YEAR = 8760;

  const CSS = `
.ac-widget{box-sizing:border-box;width:1060px;height:470px;margin:0 auto;padding:14px 16px;display:grid;grid-template-rows:auto auto 1fr auto;gap:12px;
 border:1.5px solid #c6dbe8;border-radius:14px;background:#f8fbfd;color:#18344b;font-family:"Source Sans 3","Source Sans Pro",Arial,sans-serif;font-size:18px;line-height:1.25;text-align:left}
.ac-widget *{box-sizing:border-box}
.ac-top{display:flex;align-items:center;gap:8px}
.ac-top .ac-sp{flex:1}
.ac-widget button{font:inherit;font-size:16px;color:#18344b;background:#fff;border:1.5px solid #a3c9dc;border-radius:999px;padding:4px 14px;cursor:pointer}
.ac-widget button:hover:not(:disabled){background:#e7f3fb}
.ac-widget button:disabled{opacity:.4;cursor:default}
.ac-widget button:focus-visible,.ac-widget input:focus-visible{outline:2px solid #1585b4;outline-offset:2px}
.ac-count{font-size:16px;color:#546573;min-width:82px;text-align:center}
.ac-chain{display:flex;align-items:stretch;gap:0}
.ac-client{flex:0 0 88px;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:600;color:#546573;background:#fff;border:1.5px dashed #a3c9dc;border-radius:12px}
.ac-arrow{flex:0 0 22px;align-self:center;text-align:center;color:#3886ad;font-size:20px;font-weight:700}
.ac-card{flex:1 1 0;min-width:0;padding:9px 9px 7px;background:#fff;border:1.5px solid #c6dbe8;border-left:6px solid #3886ad;border-radius:12px;transition:opacity .15s}
.ac-card.ac-async{border-style:dashed;border-left-color:#b56a21;opacity:.72}
.ac-name{font-size:16px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ac-val{font-size:25px;font-weight:700;color:#105d80;white-space:nowrap}
.ac-async .ac-val{color:#795219}
.ac-card input[type=range]{width:100%;margin:3px 0;accent-color:#3886ad}
.ac-down{font-size:14px;color:#546573;white-space:nowrap}
.ac-sync{display:flex;align-items:center;gap:5px;margin-top:3px;font-size:14px;color:#546573;white-space:nowrap}
.ac-sync input{margin:0;accent-color:#3886ad}
.ac-res{display:grid;grid-template-columns:330px 1fr;gap:16px;min-height:0}
.ac-big{display:flex;flex-direction:column;justify-content:center;padding:8px 16px;background:#18344b;color:#fff;border-radius:12px}
.ac-big small{font-size:16px;color:#c6dbe8}
.ac-big b{font-size:48px;line-height:1.1;color:#fff}
.ac-big span{font-size:18px;color:#fff}
.ac-bars{display:flex;flex-direction:column;justify-content:center;gap:9px;min-width:0}
.ac-bar-row{display:grid;grid-template-columns:190px 1fr 90px;align-items:center;gap:10px;font-size:16px}
.ac-track{height:20px;background:#e6eef3;border-radius:5px;overflow:hidden}
.ac-fill{height:100%;background:#3886ad;transition:width .15s}
.ac-fill.ac-red{background:#b33e44}
.ac-num{text-align:right;font-weight:700;white-space:nowrap}
.ac-formula{font-size:17px;color:#18344b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ac-foot{font-size:14px;color:#546573}
@media (prefers-reduced-motion:reduce){.ac-widget *{transition:none!important}}
`;

  const comma = (s) => s.replace('.', ',');

  function percent(a) {
    return comma((a * 100).toFixed(3)) + ' %';
  }

  function level(v) {
    return comma(String(v)) + ' %';
  }

  function downtime(a) {
    const hours = (1 - a) * HOURS_PER_YEAR;
    if (hours >= 100) return Math.round(hours) + ' h';
    if (hours >= 1) return comma(hours.toFixed(1)) + ' h';
    return Math.round(hours * 60) + ' min';
  }

  function init(root) {
    const state = NAMES.map(() => ({ level: DEFAULT_LEVEL, sync: true }));
    let count = 3;

    root.innerHTML = `
      <div class="ac-top">
        <button data-preset="even">Sve 99,9 %</button>
        <button data-preset="weak">Jedna slaba karika</button>
        <button data-preset="async">Obavijesti i provjera asinkrono</button>
        <span class="ac-sp"></span>
        <button data-delta="-1" aria-label="Ukloni uslugu">−</button>
        <span class="ac-count"></span>
        <button data-delta="1" aria-label="Dodaj uslugu">+</button>
      </div>
      <div class="ac-chain"></div>
      <div class="ac-res">
        <div class="ac-big"><small>Dostupnost cijele usluge</small><b data-out="total"></b><span data-out="down"></span></div>
        <div class="ac-bars">
          <div class="ac-bar-row"><span>Najslabija komponenta</span><div class="ac-track"><div class="ac-fill" data-out="weakBar"></div></div><span class="ac-num" data-out="weakNum"></span></div>
          <div class="ac-bar-row"><span>Cijeli lanac</span><div class="ac-track"><div class="ac-fill ac-red" data-out="chainBar"></div></div><span class="ac-num" data-out="chainNum"></span></div>
          <div class="ac-formula" data-out="formula"></div>
        </div>
      </div>
      <div class="ac-foot">Trake: nedostupnost godišnje. Pretpostavke: ispadi su neovisni, svaka sinkrona usluga je nužna, nema ponovnih pokušaja.</div>`;

    const chain = root.querySelector('.ac-chain');
    const out = (k) => root.querySelector(`[data-out="${k}"]`);

    function buildChain() {
      let html = '<div class="ac-client">Preglednik</div>';
      for (let i = 0; i < count; i++) {
        html += `<div class="ac-arrow">→</div><div class="ac-card" data-i="${i}">
          <div class="ac-name">${NAMES[i]}</div>
          <div class="ac-val"></div>
          <input type="range" min="0" max="${LEVELS.length - 1}" step="1" aria-label="Dostupnost: ${NAMES[i]}">
          <div class="ac-down"></div>
          <label class="ac-sync"><input type="checkbox"${i === 0 ? ' disabled' : ''}>sinkrono</label>
        </div>`;
      }
      chain.innerHTML = html;
    }

    function update() {
      const active = state.slice(0, count).filter((s) => s.sync).map((s) => LEVELS[s.level] / 100);
      const total = active.reduce((p, a) => p * a, 1);
      const weakest = Math.min(...active);
      chain.querySelectorAll('.ac-card').forEach((card) => {
        const s = state[Number(card.dataset.i)];
        const a = LEVELS[s.level] / 100;
        card.classList.toggle('ac-async', !s.sync);
        card.querySelector('.ac-val').textContent = level(LEVELS[s.level]);
        card.querySelector('input[type=range]').value = s.level;
        card.querySelector('.ac-down').textContent = s.sync ? downtime(a) + ' / god.' : 'ne ruši predaju';
        card.querySelector('input[type=checkbox]').checked = s.sync;
      });
      const weakHours = (1 - weakest) * HOURS_PER_YEAR;
      const chainHours = (1 - total) * HOURS_PER_YEAR;
      const scale = Math.max(chainHours, 1e-9);
      out('total').textContent = percent(total);
      out('down').textContent = 'oko ' + downtime(total) + ' nedostupnosti godišnje';
      out('weakBar').style.width = (100 * weakHours / scale) + '%';
      out('chainBar').style.width = '100%';
      out('weakNum').textContent = downtime(weakest);
      out('chainNum').textContent = downtime(total);
      out('formula').textContent = active.map((a) => comma(String(Number(a.toFixed(5))))).join(' × ') + ' ≈ ' + comma(total.toFixed(5));
      root.querySelector('.ac-count').textContent = count + (count >= 2 && count <= 4 ? ' usluge' : ' usluga');
      root.querySelector('[data-delta="-1"]').disabled = count <= 1;
      root.querySelector('[data-delta="1"]').disabled = count >= NAMES.length;
    }

    function rebuild() {
      buildChain();
      update();
    }

    root.addEventListener('input', (e) => {
      const card = e.target.closest('.ac-card');
      if (!card) return;
      const s = state[Number(card.dataset.i)];
      if (e.target.type === 'range') s.level = Number(e.target.value);
      else s.sync = e.target.checked;
      update();
    });

    // Arrow keys must move the focused slider, not change the slide.
    root.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT') e.stopPropagation();
    });

    root.addEventListener('click', (e) => {
      const button = e.target.closest('button');
      if (!button) return;
      if (button.dataset.delta) {
        count = Math.min(NAMES.length, Math.max(1, count + Number(button.dataset.delta)));
      } else {
        state.forEach((s) => { s.level = DEFAULT_LEVEL; s.sync = true; });
        if (button.dataset.preset === 'weak') {
          count = Math.max(count, 3);
          state[2].level = 1;
        } else if (button.dataset.preset === 'async') {
          count = NAMES.length;
          state[4].sync = false;
          state[5].sync = false;
        }
      }
      rebuild();
    });

    rebuild();
  }

  if (!document.getElementById('ac-style')) {
    const style = document.createElement('style');
    style.id = 'ac-style';
    style.textContent = CSS;
    document.head.appendChild(style);
  }
  document.querySelectorAll('.ac-widget').forEach(init);
})();
