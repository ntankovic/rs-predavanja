/* Reliability of a chain of sequential remote calls: P = p^N (2026-11-03).
   Self-contained widget for slide "Lanac poziva" / "A chain of remote calls"; no libraries, no network.
   Usage: <div class="rc-widget" data-lang="hr|en" data-steps="4"></div><script src="assets/reliability-chain.js"></script>
   Assumptions shown in the widget: independent failures, sequential dependencies, every step required, no retries. */
(function () {
  'use strict';

  const T = {
    hr: {
      presets: ['Pouzdan sustav', 'Nepouzdan sustav', 'Usporedi scenarije'],
      steps: 'Broj uzastopnih koraka N', perStep: 'pouzdanost koraka p', overall: 'cijeli tok uspijeva',
      scenario: 'Scenarij', client: 'Klijent', service: 'Usluga', success: 'Uspjeh',
      present: 'Prezentacija', fullscreen: 'Cijeli zaslon', exitPresent: 'Sve kontrole',
      tabs: ['Simulacija', 'Prikaži izračun', 'Obrnuti izračun', 'Pretpostavke'],
      run: 'Pokreni simulaciju', runs: 'izvođenja', ok: 'uspjelo', fail: 'palo',
      observed: 'opaženo', theory: 'teorijski', first100: 'prvih 100 izvođenja',
      simHint: '1000 nasumičnih izvođenja s odabranim p i N. Rezultat se mijenja pri svakom pokretanju.',
      atLeastOne: 'barem jedan korak padne',
      target: 'Ciljana pouzdanost cijelog toka', need: 'Svaki korak mora imati najmanje',
      allowed: 'dopušteno padova po koraku', perMillion: 'na milijun poziva',
      assumptions: ['Ispadi koraka su neovisni.', 'Koraci su uzastopni: svaki ovisi o prethodnom.',
        'Tok uspijeva samo ako uspiju svi koraci.', 'Nema ponovnih pokušaja ni zamjenskih putova.'],
      assumptionsNote: 'U stvarnim sustavima ispadi su često povezani, a ponovni pokušaji mijenjaju p (i opterećenje).',
      insight: 'Pouzdanost pojedinih komponenti nije isto što i pouzdanost cijelog raspodijeljenog sustava.',
      xAxis: 'broj uzastopnih koraka N', yAxis: 'uspjeh toka', diff: 'razlika',
      pp: 'p. b.', decimal: ',', succ: 'uspjeh', formula: 'p<sub>min</sub> = P<sub>cilj</sub><sup>1/N</sup>',
    },
    en: {
      presets: ['Reliable system', 'Unreliable system', 'Compare scenarios'],
      steps: 'Number of sequential steps N', perStep: 'step reliability p', overall: 'whole workflow succeeds',
      scenario: 'Scenario', client: 'Client', service: 'Service', success: 'Success',
      present: 'Presentation', fullscreen: 'Full screen', exitPresent: 'All controls',
      tabs: ['Simulation', 'Show calculation', 'Reverse calculation', 'Assumptions'],
      run: 'Run simulation', runs: 'runs', ok: 'succeeded', fail: 'failed',
      observed: 'observed', theory: 'theoretical', first100: 'first 100 runs',
      simHint: '1000 random runs with the selected p and N. The result changes on every run.',
      atLeastOne: 'at least one step fails',
      target: 'Target reliability of the whole workflow', need: 'Every step needs at least',
      allowed: 'allowed failures per step', perMillion: 'per million calls',
      assumptions: ['Step failures are independent.', 'Steps are sequential: each depends on the previous one.',
        'The workflow succeeds only if every step succeeds.', 'No retries and no fallback paths.'],
      assumptionsNote: 'In real systems failures are often correlated, and retries change p (and the load).',
      insight: 'The reliability of individual components is not the reliability of the whole distributed system.',
      xAxis: 'number of sequential steps N', yAxis: 'workflow success', diff: 'difference',
      pp: 'pp', decimal: '.', succ: 'success', formula: 'p<sub>min</sub> = P<sub>target</sub><sup>1/N</sup>',
    },
  };

  const CSS = `
.rc-widget{--bg1:#0c1626;--bg2:#13243a;--card:rgba(255,255,255,.045);--line:rgba(160,190,220,.16);--text:#e8f0f8;--muted:#93a8bd;
 --a:#34d399;--b:#fb7185;--accent:#7cc4ff;position:relative;box-sizing:border-box;width:1060px;height:588px;margin:0 auto;padding:12px 14px;
 border-radius:16px;background:radial-gradient(120% 90% at 85% 0%,#1b3350 0%,transparent 55%),linear-gradient(160deg,var(--bg1),var(--bg2));
 color:var(--text);font-family:"Inter","Segoe UI",Arial,Helvetica,sans-serif;font-size:15px;line-height:1.25;text-align:left;
 display:grid;grid-template-rows:auto 1fr auto auto;gap:9px;overflow:hidden}
.rc-widget *{box-sizing:border-box}
.rc-widget button{font:inherit;color:inherit;cursor:pointer;border:1px solid var(--line);background:var(--card);border-radius:9px;padding:5px 11px;transition:background .2s,border-color .2s}
.rc-widget button:hover{background:rgba(255,255,255,.09)}
.rc-widget button:focus-visible,.rc-widget input:focus-visible,.rc-widget select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.rc-widget button[aria-pressed="true"],.rc-widget button[aria-selected="true"]{border-color:var(--accent);background:rgba(124,196,255,.16)}
.rc-top{display:flex;align-items:center;gap:7px;flex-wrap:nowrap}
.rc-top .rc-sp{flex:1}
.rc-chip{font-size:13px;padding:4px 9px!important}
.rc-main{display:grid;grid-template-columns:292px 1fr;gap:10px;min-height:0}
.rc-left{display:flex;flex-direction:column;gap:8px;min-height:0;overflow:hidden}
.rc-card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px 11px}
.rc-scn{position:relative;transition:opacity .3s}
.rc-scn.rc-dim{opacity:.32}
.rc-scn h4{margin:0;font-size:13px;font-weight:600;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;display:flex;justify-content:space-between;align-items:center}
.rc-scn .rc-tag{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:0}
.rc-row{display:flex;align-items:center;gap:8px;margin-top:4px}
.rc-row input[type=range]{flex:1;min-width:0}
.rc-widget input[type=range]{accent-color:var(--accent);height:18px}
.rc-scn[data-k=a] input[type=range]{accent-color:var(--a)}.rc-scn[data-k=b] input[type=range]{accent-color:var(--b)}
.rc-num{width:78px;background:rgba(0,0,0,.25);color:var(--text);border:1px solid var(--line);border-radius:7px;padding:3px 6px;font:inherit;font-size:15px;font-variant-numeric:tabular-nums;text-align:right}
.rc-big{font-size:32px;font-weight:750;font-variant-numeric:tabular-nums;letter-spacing:-.02em;line-height:1.05;margin-top:2px}
.rc-big small{display:block;font-size:13px;font-weight:500;color:var(--muted);letter-spacing:0;margin-top:1px}
.rc-a{color:var(--a)}.rc-b{color:var(--b)}
.rc-diff{position:absolute;right:11px;bottom:8px;font-size:13px;color:var(--muted);text-align:right}
.rc-diff b{color:var(--text);font-variant-numeric:tabular-nums}
.rc-nval{font-size:22px;line-height:1;font-weight:700;font-variant-numeric:tabular-nums;color:var(--accent)}
.rc-right{display:grid;grid-template-rows:auto 1fr;gap:8px;min-height:0}
.rc-chain svg,.rc-chart svg{display:block;width:100%;height:100%}
.rc-chain{padding:4px 8px}
.rc-chart{position:relative;padding:4px 6px 2px;min-height:0}
.rc-tip{position:absolute;pointer-events:none;background:rgba(8,16,28,.94);border:1px solid var(--line);border-radius:8px;padding:5px 8px;font-size:13px;white-space:nowrap;opacity:0;transition:opacity .12s;font-variant-numeric:tabular-nums}
.rc-bottom{height:142px;display:grid;grid-template-rows:auto 1fr;gap:6px}
.rc-tabs{display:flex;gap:6px}
.rc-tabs button{font-size:13px;padding:3px 10px}
.rc-panel{display:none;min-height:0}
.rc-panel.rc-on{display:grid}
.rc-sim{grid-template-columns:auto 1fr auto;gap:14px;align-items:center}
.rc-cells{display:grid;grid-template-columns:repeat(20,13px);grid-auto-rows:13px;gap:3px}
.rc-cells i{display:block;border-radius:3px;background:rgba(255,255,255,.08);transform:scale(.6);transition:transform .25s,background .25s}
.rc-cells i.rc-s{background:var(--a);transform:scale(1)}.rc-cells i.rc-f{background:var(--b);transform:scale(1)}
.rc-stats{display:flex;gap:18px;font-variant-numeric:tabular-nums}
.rc-stat{display:flex;flex-direction:column}
.rc-stat b{font-size:26px;font-weight:750}
.rc-stat span{font-size:12px;color:var(--muted)}
.rc-hint{font-size:12px;color:var(--muted);max-width:270px}
.rc-math{grid-template-columns:1fr 1fr;gap:10px;font-variant-numeric:tabular-nums}
.rc-math .rc-card{font-size:15px}
.rc-f1{font-family:"Cambria Math","STIX Two Math","Times New Roman",serif;font-size:18px;margin:2px 0 4px}
.rc-rev{grid-template-columns:1.1fr 1fr 1fr;gap:10px;align-items:stretch}
.rc-rev select,.rc-rev .rc-num{margin-top:6px}
.rc-widget select{background:#0e1d30;color:var(--text);border:1px solid var(--line);border-radius:7px;padding:3px 6px;font:inherit}
.rc-assume{grid-template-columns:repeat(4,1fr);gap:8px}
.rc-assume .rc-card{font-size:14px;display:flex;gap:8px;align-items:flex-start}
.rc-assume .rc-card b{color:var(--accent);font-size:18px;line-height:1}
.rc-assume p{grid-column:1/-1;margin:0;font-size:13px;color:var(--muted)}
.rc-insight{font-size:16px;font-weight:600;text-align:center;padding:6px 10px;border-radius:10px;background:linear-gradient(90deg,rgba(52,211,153,.12),rgba(251,113,133,.12));border:1px solid var(--line)}
.rc-label{font-size:12px;color:var(--muted)}
.rc-widget.rc-present .rc-secondary{display:none!important}
.rc-widget.rc-present .rc-bottom{display:none}
.rc-widget.rc-present .rc-big{font-size:52px}
.rc-widget.rc-present .rc-insight{font-size:20px;padding:10px}
.rc-widget:fullscreen{width:1060px;height:588px;border-radius:0}
.rc-widget:fullscreen::backdrop{background:#0c1626}
@media (prefers-reduced-motion:reduce){.rc-widget *{transition:none!important}}
`;

  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  // Work with the failure rate q = 1 - p to keep 99.99 % exact: log(p^N) = N * log1p(-q).
  const logSuccess = (pct, n) => n * Math.log1p(-(100 - pct) / 100);
  const success = (pct, n) => Math.exp(logSuccess(pct, n));
  const failure = (pct, n) => -Math.expm1(logSuccess(pct, n));

  // Croatian writes "99 %", English "99%"; the decimal separator identifies the language.
  const pctSuffix = (dec) => (dec === ',' ? ' %' : '%');
  function fmtNum(v, digits, dec) {
    return v.toFixed(digits).replace('.', dec);
  }
  // Percentages with enough digits to stay honest for tiny values: 1.3 × 10⁻²¹ %.
  function fmtPct(prob, dec, digits = 3) {
    const pct = prob * 100;
    if (pct === 0) return '0' + pctSuffix(dec);
    if (pct >= 0.001 || pct === 100) return fmtNum(pct, digits, dec) + pctSuffix(dec);
    const exp = Math.floor(Math.log10(pct));
    const mant = pct / 10 ** exp;
    const sup = String(exp).replace('-', '⁻').replace(/\d/g, (d) => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d]);
    return fmtNum(mant, 2, dec) + ' × 10' + sup + pctSuffix(dec);
  }

  function svgEl(tag, attrs, parent) {
    const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(el);
    return el;
  }

  function build(root) {
    if (root.dataset.ready) return;
    root.dataset.ready = '1';
    const t = T[root.dataset.lang] || T.hr;
    const dec = t.decimal;
    const state = {
      a: parseFloat(root.dataset.a || '99.99'), b: parseFloat(root.dataset.b || '98'), n: clamp(parseInt(root.dataset.steps || '100', 10), 1, 500),
      mode: 'compare', lane: 'a', tab: 0, present: false,
    };

    root.setAttribute('role', 'group');
    root.setAttribute('aria-label', t.insight);
    root.innerHTML = `
<div class="rc-top">
  <button type="button" data-preset="0" aria-pressed="false">${t.presets[0]}</button>
  <button type="button" data-preset="1" aria-pressed="false">${t.presets[1]}</button>
  <button type="button" data-preset="2" aria-pressed="true">${t.presets[2]}</button>
  <span class="rc-sp"></span>
  <span class="rc-label rc-secondary">N =</span>
  ${[1, 4, 10, 100, 500].map((v) => `<button type="button" class="rc-chip rc-secondary" data-n="${v}">${v}</button>`).join('')}
  <button type="button" data-act="present" aria-pressed="false">${t.present}</button>
  <button type="button" data-act="fs" aria-label="${t.fullscreen}" title="${t.fullscreen}">⛶</button>
</div>
<div class="rc-main">
  <div class="rc-left">
    ${['a', 'b'].map((k) => `
    <div class="rc-card rc-scn" data-k="${k}">
      <h4><span><span class="rc-tag" style="background:var(--${k})"></span>${t.scenario} ${k.toUpperCase()}</span><span class="rc-secondary">${t.perStep}</span></h4>
      <div class="rc-row rc-secondary">
        <input type="range" min="90" max="100" step="0.01" aria-label="${t.scenario} ${k.toUpperCase()}: ${t.perStep}">
        <input class="rc-num" type="number" min="90" max="100" step="0.01" aria-label="${t.scenario} ${k.toUpperCase()}: ${t.perStep} (%)"><span>%</span>
      </div>
      <div class="rc-big rc-${k}" aria-live="polite"><span data-out="${k}"></span><small>${t.overall}</small></div>
      ${k === 'b' ? '<div class="rc-diff" data-out="diff"></div>' : ''}
    </div>`).join('')}
    <div class="rc-card">
      <div class="rc-row" style="margin-top:0;justify-content:space-between"><span class="rc-label">${t.steps}</span><span class="rc-nval" data-out="n"></span></div>
      <div class="rc-row rc-secondary">
        <input type="range" min="1" max="500" step="1" data-in="n" aria-label="${t.steps}">
        <input class="rc-num" type="number" min="1" max="500" step="1" data-in="n2" aria-label="${t.steps}" style="width:64px">
      </div>
    </div>
  </div>
  <div class="rc-right">
    <div class="rc-card rc-chain"><svg data-svg="chain" viewBox="0 0 740 112" aria-hidden="true"></svg></div>
    <div class="rc-card rc-chart"><svg data-svg="chart" viewBox="0 0 740 230" role="img"></svg><div class="rc-tip"></div></div>
  </div>
</div>
<div class="rc-bottom">
  <div class="rc-tabs" role="tablist">${t.tabs.map((name, i) => `<button type="button" role="tab" data-tab="${i}" aria-selected="${i === 0}">${name}</button>`).join('')}</div>
  <div class="rc-panel rc-sim rc-on" role="tabpanel">
    <div style="display:flex;flex-direction:column;gap:6px"><button type="button" data-act="sim">▶ ${t.run}</button><span class="rc-hint">${t.simHint}</span></div>
    <div><div class="rc-cells" aria-label="${t.first100}"></div><div class="rc-label" style="margin-top:3px">${t.first100}</div></div>
    <div class="rc-stats" aria-live="polite"></div>
  </div>
  <div class="rc-panel rc-math" role="tabpanel"><div class="rc-card" data-out="mathA"></div><div class="rc-card" data-out="mathB"></div></div>
  <div class="rc-panel rc-rev" role="tabpanel">
    <div class="rc-card"><div class="rc-label">${t.target}</div>
      <select data-in="target" aria-label="${t.target}">${['90', '95', '99', '99.9', '99.99', '99.999'].map((v) => `<option value="${v}"${v === '99.9' ? ' selected' : ''}>${v.replace('.', dec)}${pctSuffix(dec)}</option>`).join('')}</select>
      <div class="rc-label" style="margin-top:8px">${t.formula}</div></div>
    <div class="rc-card"><div class="rc-label">${t.need}</div><div class="rc-big" style="color:var(--accent);font-size:30px" data-out="pmin"></div></div>
    <div class="rc-card"><div class="rc-label">${t.allowed}</div><div class="rc-big" style="font-size:30px" data-out="qmax"></div></div>
  </div>
  <div class="rc-panel rc-assume" role="tabpanel">${t.assumptions.map((s, i) => `<div class="rc-card"><b>${i + 1}</b><span>${s}</span></div>`).join('')}<p>${t.assumptionsNote}</p></div>
</div>
<div class="rc-insight">${t.insight}</div>`;

    const $ = (s) => root.querySelector(s);
    const $$ = (s) => Array.from(root.querySelectorAll(s));
    const scn = { a: $('.rc-scn[data-k=a]'), b: $('.rc-scn[data-k=b]') };

    // ---------- Controls ----------
    function setP(k, v) {
      if (!Number.isFinite(v)) return;
      state[k] = Math.round(clamp(v, 90, 100) * 100) / 100;
      update();
    }
    for (const k of ['a', 'b']) {
      const [range, num] = scn[k].querySelectorAll('input');
      range.addEventListener('input', () => setP(k, parseFloat(range.value)));
      num.addEventListener('change', () => setP(k, parseFloat(String(num.value).replace(',', '.'))));
    }
    $('[data-in=n]').addEventListener('input', (e) => { state.n = +e.target.value; update(); });
    $('[data-in=n2]').addEventListener('change', (e) => { state.n = clamp(Math.round(+e.target.value) || 1, 1, 500); update(); });
    $$('[data-n]').forEach((b) => b.addEventListener('click', () => { state.n = +b.dataset.n; update(); }));
    $$('[data-preset]').forEach((b) => b.addEventListener('click', () => {
      const i = +b.dataset.preset;
      state.n = 100;
      if (i === 0) { state.mode = 'single'; state.lane = 'a'; state.a = 99.99; }
      if (i === 1) { state.mode = 'single'; state.lane = 'b'; state.b = 98; }
      if (i === 2) { state.mode = 'compare'; state.a = 99.99; state.b = 98; }
      $$('[data-preset]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      resetSim();
      update();
    }));
    $$('[data-tab]').forEach((b) => b.addEventListener('click', () => {
      state.tab = +b.dataset.tab;
      $$('[data-tab]').forEach((x) => x.setAttribute('aria-selected', String(x === b)));
      $$('.rc-panel').forEach((p, i) => p.classList.toggle('rc-on', i === state.tab));
    }));
    $('[data-in=target]').addEventListener('change', update);
    $('[data-act=present]').addEventListener('click', (e) => {
      state.present = !state.present;
      root.classList.toggle('rc-present', state.present);
      e.currentTarget.setAttribute('aria-pressed', String(state.present));
      e.currentTarget.textContent = state.present ? t.exitPresent : t.present;
      drawChart(true);
    });
    $('[data-act=fs]').addEventListener('click', () => {
      if (document.fullscreenElement) document.exitFullscreen();
      else if (root.requestFullscreen) root.requestFullscreen();
    });
    document.addEventListener('fullscreenchange', () => {
      root.style.zoom = document.fullscreenElement === root
        ? String(Math.min(window.innerWidth / 1060, window.innerHeight / 588)) : '';
    });
    // Keep arrow keys inside inputs from changing the slide; buttons still let Reveal navigate.
    root.addEventListener('keydown', (e) => {
      if (/^(INPUT|SELECT)$/.test(e.target.tagName)) e.stopPropagation();
      if (e.key === 'Escape') e.target.blur();
    });

    // ---------- Chart ----------
    const chart = $('[data-svg=chart]');
    const tip = $('.rc-tip');
    const CW = 740, CH = 230, PL = 64, PR = 14, PT = 12, PB = 34;
    const SAMPLES = 160;
    let shown = null; // currently drawn curves, tweened towards the target
    let tween = 0;

    function domainMax() {
      const want = Math.max(10, state.n * 1.6);
      for (const m of [10, 20, 50, 100, 150, 200, 300, 500]) if (m >= want) return m;
      return 500;
    }
    const xs = (n, max) => PL + ((n - 1) / (max - 1)) * (CW - PL - PR);
    const ys = (prob) => PT + (1 - prob) * (CH - PT - PB);

    const g = svgEl('g', {}, chart);
    const grid = svgEl('g', {}, g);
    const pathA = svgEl('path', { fill: 'none', stroke: '#34d399', 'stroke-width': 3.2, 'stroke-linejoin': 'round' }, g);
    const pathB = svgEl('path', { fill: 'none', stroke: '#fb7185', 'stroke-width': 3.2, 'stroke-linejoin': 'round' }, g);
    const refLine = svgEl('line', { stroke: '#7cc4ff', 'stroke-width': 1.6, 'stroke-dasharray': '5 5' }, g);
    const refLabel = svgEl('text', { fill: '#7cc4ff', 'font-size': 13, 'font-weight': 700, 'text-anchor': 'start' }, g);
    const dotA = svgEl('circle', { r: 5.5, fill: '#34d399', stroke: '#0c1626', 'stroke-width': 2 }, g);
    const dotB = svgEl('circle', { r: 5.5, fill: '#fb7185', stroke: '#0c1626', 'stroke-width': 2 }, g);
    const hoverLine = svgEl('line', { stroke: 'rgba(232,240,248,.35)', 'stroke-width': 1, opacity: 0 }, g);
    svgEl('text', { x: CW - PR, y: CH - 4, fill: '#93a8bd', 'font-size': 12, 'text-anchor': 'end' }, g).textContent = t.xAxis;
    svgEl('text', { x: 12, y: PT + 2, fill: '#93a8bd', 'font-size': 12, transform: `rotate(-90 12 ${PT + 2})`, 'text-anchor': 'end' }, g).textContent = t.yAxis;

    function targetCurves(max) {
      const out = { max, a: [], b: [] };
      for (let i = 0; i < SAMPLES; i++) {
        const n = 1 + (i / (SAMPLES - 1)) * (max - 1);
        out.a.push(success(state.a, n));
        out.b.push(success(state.b, n));
      }
      return out;
    }
    function pathFor(vals, max) {
      return vals.map((v, i) => `${i ? 'L' : 'M'}${xs(1 + (i / (SAMPLES - 1)) * (max - 1), max).toFixed(1)} ${ys(v).toFixed(1)}`).join('');
    }
    function drawGrid(max) {
      grid.innerHTML = '';
      for (const v of [0, .25, .5, .75, 1]) {
        svgEl('line', { x1: PL, x2: CW - PR, y1: ys(v), y2: ys(v), stroke: 'rgba(160,190,220,.13)' }, grid);
        svgEl('text', { x: PL - 7, y: ys(v) + 4, fill: '#93a8bd', 'font-size': 12, 'text-anchor': 'end' }, grid).textContent = (v * 100) + pctSuffix(dec);
      }
      const stepN = [1, 2, 5, 10, 25, 50, 100].find((s) => max / s <= 6);
      const ticks = [1];
      for (let n = stepN; n <= max; n += stepN) if (n > 1) ticks.push(n);
      for (const n of ticks) {
        svgEl('text', { x: xs(n, max), y: CH - PB + 16, fill: '#93a8bd', 'font-size': 12, 'text-anchor': 'middle' }, grid).textContent = n;
      }
    }
    function drawChart(instant) {
      const target = targetCurves(domainMax());
      drawGrid(target.max);
      const from = shown && shown.max === target.max && !instant ? shown : target;
      const start = performance.now();
      const dur = from === target ? 0 : 380;
      const id = ++tween;
      const step = (now) => {
        if (id !== tween) return;
        const k = dur ? Math.min(1, (now - start) / dur) : 1;
        const e = 1 - Math.pow(1 - k, 3);
        const cur = { max: target.max, a: target.a.map((v, i) => from.a[i] + (v - from.a[i]) * e), b: target.b.map((v, i) => from.b[i] + (v - from.b[i]) * e) };
        pathA.setAttribute('d', pathFor(cur.a, cur.max));
        pathB.setAttribute('d', pathFor(cur.b, cur.max));
        shown = cur;
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      const x = xs(state.n, target.max);
      refLine.setAttribute('x1', x); refLine.setAttribute('x2', x);
      refLine.setAttribute('y1', PT); refLine.setAttribute('y2', CH - PB);
      refLabel.setAttribute('x', clamp(x + 8, PL, CW - PR - 50)); refLabel.setAttribute('y', CH - PB - 8);
      refLabel.textContent = 'N = ' + state.n;
      dotA.setAttribute('cx', x); dotA.setAttribute('cy', ys(success(state.a, state.n)));
      dotB.setAttribute('cx', x); dotB.setAttribute('cy', ys(success(state.b, state.n)));
      const single = state.mode === 'single';
      pathA.style.opacity = dotA.style.opacity = single && state.lane === 'b' ? .2 : 1;
      pathB.style.opacity = dotB.style.opacity = single && state.lane === 'a' ? .2 : 1;
      chart.setAttribute('aria-label', `${t.yAxis}: A ${fmtPct(success(state.a, state.n), dec)}, B ${fmtPct(success(state.b, state.n), dec)}, N = ${state.n}`);
    }
    chart.addEventListener('mousemove', (ev) => {
      const r = chart.getBoundingClientRect();
      const px = ((ev.clientX - r.left) / r.width) * CW;
      const max = domainMax();
      const n = clamp(Math.round(1 + ((px - PL) / (CW - PL - PR)) * (max - 1)), 1, max);
      const x = xs(n, max);
      hoverLine.setAttribute('x1', x); hoverLine.setAttribute('x2', x);
      hoverLine.setAttribute('y1', PT); hoverLine.setAttribute('y2', CH - PB);
      hoverLine.setAttribute('opacity', 1);
      tip.innerHTML = `<b>N = ${n}</b><br><span class="rc-a">A ${fmtPct(success(state.a, n), dec)}</span><br><span class="rc-b">B ${fmtPct(success(state.b, n), dec)}</span>`;
      const box = tip.parentElement.getBoundingClientRect();
      const scale = box.width / tip.parentElement.offsetWidth || 1;
      let left = (ev.clientX - box.left) / scale + 14;
      if (left > tip.parentElement.offsetWidth - 170) left -= 190;
      tip.style.left = left + 'px';
      tip.style.top = ((ev.clientY - box.top) / scale - 20) + 'px';
      tip.style.opacity = 1;
    });
    chart.addEventListener('mouseleave', () => { tip.style.opacity = 0; hoverLine.setAttribute('opacity', 0); });

    // ---------- Chain with travelling requests ----------
    const chain = $('[data-svg=chain]');
    const VW = 740;
    let lanes = [];
    let dots = [];
    let tally = { a: [0, 0], b: [0, 0] };

    function chainLabels() {
      const n = state.n;
      if (n <= 6) return Array.from({ length: n }, (_, i) => ({ label: 'S' + (i + 1), from: i, to: i + 1 }));
      // Representative subset: S1, S2, S3, …, S(N-1), SN; the ellipsis stands for the hidden steps.
      return [
        { label: 'S1', from: 0, to: 1 }, { label: 'S2', from: 1, to: 2 }, { label: 'S3', from: 2, to: 3 },
        { label: '…', from: 3, to: n - 2, gap: true },
        { label: 'S' + (n - 1), from: n - 2, to: n - 1 }, { label: 'S' + n, from: n - 1, to: n },
      ];
    }
    function drawChain() {
      chain.innerHTML = '';
      const ks = state.mode === 'compare' ? ['a', 'b'] : [state.lane];
      const laneH = ks.length === 2 ? 52 : 70;
      const top = ks.length === 2 ? 6 : 22;
      const nodes = chainLabels();
      const x0 = 78, x1 = VW - 92;
      lanes = ks.map((k, li) => {
        const y = top + li * laneH + laneH / 2 - 4;
        const color = k === 'a' ? '#34d399' : '#fb7185';
        svgEl('line', { x1: 40, x2: VW - 50, y1: y, y2: y, stroke: 'rgba(160,190,220,.25)', 'stroke-width': 2 }, chain);
        const g2 = svgEl('g', {}, chain); // dots pass behind the nodes
        // Client and success nodes.
        svgEl('rect', { x: 4, y: y - 15, width: 66, height: 30, rx: 8, fill: '#18304b', stroke: 'rgba(160,190,220,.35)' }, chain);
        svgEl('text', { x: 37, y: y + 5, fill: '#e8f0f8', 'font-size': 13, 'text-anchor': 'middle' }, chain).textContent = t.client;
        svgEl('rect', { x: VW - 84, y: y - 15, width: 80, height: 30, rx: 8, fill: 'rgba(52,211,153,.14)', stroke: '#34d399' }, chain);
        const okText = svgEl('text', { x: VW - 44, y: y + 5, fill: '#34d399', 'font-size': 13, 'text-anchor': 'middle', 'font-weight': 700 }, chain);
        const failText = svgEl('text', { x: VW - 92, y: y - 19, fill: '#fb7185', 'font-size': 11, 'font-weight': 700, 'text-anchor': 'end' }, chain);
        const slot = (x1 - x0) / nodes.length;
        const pos = nodes.map((nd, i) => {
          const cx = x0 + slot * (i + .5);
          if (nd.gap) {
            svgEl('text', { x: cx, y: y + 6, fill: '#93a8bd', 'font-size': 20, 'text-anchor': 'middle' }, chain).textContent = '· · ·';
          } else {
            svgEl('rect', { x: cx - 26, y: y - 13, width: 52, height: 26, rx: 13, fill: '#0f2135', stroke: color, 'stroke-width': 1.4 }, chain);
            svgEl('text', { x: cx, y: y + 5, fill: '#e8f0f8', 'font-size': 12.5, 'text-anchor': 'middle', 'font-weight': 600 }, chain).textContent = nd.label;
          }
          return { cx, ...nd };
        });
        svgEl('text', { x: 4, y: y - 19, fill: color, 'font-size': 11, 'font-weight': 700 }, chain).textContent = `${t.scenario} ${k.toUpperCase()} · p = ${fmtNum(state[k], 2, dec)}${pctSuffix(dec)}`;
        return { k, y, pos, g: g2, okText, failText, x0, x1 };
      });
      dots.forEach((d) => d.el.remove());
      dots = [];
      tally = { a: [0, 0], b: [0, 0] };
      updateTally();
    }
    function updateTally() {
      for (const ln of lanes) {
        const [ok, fail] = tally[ln.k];
        ln.okText.textContent = `${t.success} ${ok}`;
        ln.failText.textContent = fail ? `✕ ${fail}` : '';
      }
    }
    // Dots move at constant visual speed: u counts drawn slots (0..slots), and the hidden steps share the ellipsis slot.
    function stepToU(ln, step) {
      for (let i = 0; i < ln.pos.length; i++) {
        const p = ln.pos[i];
        if (step <= p.to) return i + (step - p.from) / Math.max(1, p.to - p.from);
      }
      return ln.pos.length;
    }
    const uToX = (ln, u) => ln.x0 + (u / ln.pos.length) * (ln.x1 - ln.x0);
    function spawn(ln) {
      // Sample how far this request gets: each step succeeds independently with probability p.
      const q = (100 - state[ln.k]) / 100;
      let failU = -1;
      if (q > 0) {
        // Geometric sampling: the first failing step, without looping over all N steps.
        const k = Math.floor(Math.log(1 - Math.random()) / Math.log1p(-q));
        if (k < state.n) failU = stepToU(ln, k + .5);
      }
      const el = svgEl('circle', { r: 5, fill: '#e8f0f8', cy: ln.y, cx: 40 }, ln.g);
      dots.push({ ln, el, u: -0.6, failU, dead: 0 });
    }
    let last = 0, acc = 0;
    function frame(now) {
      requestAnimationFrame(frame);
      const section = root.closest('section');
      const visible = !document.hidden && (!section || section.classList.contains('present')) && root.isConnected;
      const dt = Math.min(50, now - (last || now));
      last = now;
      if (!visible) return;
      acc += dt;
      if (acc > 380) { acc = 0; lanes.forEach(spawn); }
      for (const d of dots) {
        const slots = d.ln.pos.length;
        if (d.dead) { d.dead += dt; d.el.setAttribute('opacity', Math.max(0, 1 - d.dead / 700)); if (d.failed) d.el.setAttribute('cy', d.ln.y + d.dead / 30); continue; }
        d.u += dt * (slots + 1.2) / 2600; // the whole chain in ~2.6 s regardless of N
        if (d.failU >= 0 && d.u >= d.failU) {
          d.u = d.failU; d.dead = 1; d.failed = true; d.el.setAttribute('fill', '#fb7185'); d.el.setAttribute('r', 6);
          tally[d.ln.k][1]++; updateTally();
        } else if (d.u >= slots + .6) {
          d.el.setAttribute('fill', '#34d399'); d.dead = 1; tally[d.ln.k][0]++; updateTally();
        }
        d.el.setAttribute('cx', clamp(uToX(d.ln, d.u), 40, VW - 84));
      }
      dots = dots.filter((d) => { if (d.dead > 700) { d.el.remove(); return false; } return true; });
    }

    // ---------- Monte Carlo ----------
    const cells = $('.rc-cells');
    for (let i = 0; i < 100; i++) cells.appendChild(document.createElement('i'));
    let simId = 0;
    function resetSim() {
      simId++;
      $$('.rc-cells i').forEach((c) => (c.className = ''));
      $('.rc-stats').innerHTML = '';
    }
    function simulate() {
      const id = ++simId;
      const ks = state.mode === 'compare' ? ['a', 'b'] : [state.lane];
      const RUNS = 1000;
      const res = {};
      for (const k of ks) {
        const p = state[k] / 100;
        const runs = new Uint8Array(RUNS);
        let ok = 0;
        for (let r = 0; r < RUNS; r++) {
          let s = 1;
          for (let i = 0; i < state.n; i++) if (Math.random() >= p) { s = 0; break; }
          runs[r] = s; ok += s;
        }
        res[k] = { runs, ok };
      }
      // The 100 cells show the first 100 runs of the scenario that fails more (B when comparing).
      const showK = ks.includes('b') ? 'b' : ks[0];
      const cellEls = $$('.rc-cells i');
      cellEls.forEach((c) => (c.className = ''));
      $('.rc-stats').innerHTML = ks.map((k) => `
        <div class="rc-stat"><span>${t.scenario} ${k.toUpperCase()} · ${t.observed}</span><b class="rc-${k}" data-sim="${k}">0 / ${RUNS}</b>
        <span>${t.theory}: ${fmtPct(success(state[k], state.n), dec, 3)}</span><span data-simpct="${k}"></span></div>`).join('');
      const start = performance.now();
      const step = (now) => {
        if (id !== simId) return;
        const f = Math.min(1, (now - start) / 1400);
        const upto = Math.floor(f * 100);
        for (let i = 0; i < upto; i++) if (!cellEls[i].className) cellEls[i].className = res[showK].runs[i] ? 'rc-s' : 'rc-f';
        for (const k of ks) {
          const done = Math.round(f * RUNS);
          let ok = 0;
          for (let r = 0; r < done; r++) ok += res[k].runs[r];
          root.querySelector(`[data-sim=${k}]`).textContent = `${ok} / ${done}`;
          root.querySelector(`[data-simpct=${k}]`).textContent = `${t.observed}: ${fmtPct(done ? ok / done : 0, dec, 1)}`;
        }
        if (f < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }
    $('[data-act=sim]').addEventListener('click', simulate);

    // ---------- Text outputs ----------
    let lastKey = '';
    function update() {
      for (const k of ['a', 'b']) {
        const [range, num] = scn[k].querySelectorAll('input');
        range.value = state[k];
        if (document.activeElement !== num) num.value = state[k].toFixed(2);
        $(`[data-out=${k}]`).textContent = fmtPct(success(state[k], state.n), dec);
        scn[k].classList.toggle('rc-dim', state.mode === 'single' && state.lane !== k);
      }
      $('[data-in=n]').value = state.n;
      $('[data-in=n2]').value = state.n;
      $('[data-out=n]').textContent = state.n;
      $$('[data-n]').forEach((b) => b.setAttribute('aria-pressed', String(+b.dataset.n === state.n)));
      const d = (success(state.a, state.n) - success(state.b, state.n)) * 100;
      $('[data-out=diff]').innerHTML = state.mode === 'compare' ? `A − B: <b>${fmtNum(d, 3, dec)} ${t.pp}</b>` : '&nbsp;';
      for (const k of ['a', 'b']) {
        const p = fmtNum(state[k] / 100, 4, dec);
        const n = state.n;
        const shownFactors = n <= 4 ? Array(n).fill(p).join(' × ') : `${p} × ${p} × … × ${p}`;
        $(`[data-out=math${k.toUpperCase()}]`).innerHTML = `
          <div class="rc-label">${t.scenario} ${k.toUpperCase()}</div>
          <div class="rc-f1">P(${t.succ}) = ${shownFactors} = ${p}<sup>${n}</sup> = <b class="rc-${k}">${fmtPct(success(state[k], n), dec, 4)}</b></div>
          <div>P(${t.atLeastOne}) = 1 − ${p}<sup>${n}</sup> = <b>${fmtPct(failure(state[k], n), dec, 4)}</b></div>`;
      }
      const target = parseFloat($('[data-in=target]').value) / 100;
      const logP = Math.log(target) / state.n;
      $('[data-out=pmin]').textContent = fmtPct(Math.exp(logP), dec, 5);
      const qmax = -Math.expm1(logP);
      $('[data-out=qmax]').innerHTML = `${fmtNum(qmax * 1e6, qmax * 1e6 < 10 ? 2 : 0, dec)} <small>${t.perMillion}</small>`;
      const key = [state.mode, state.lane, state.n, state.a, state.b].join('|');
      if (key !== lastKey) {
        lastKey = key;
        drawChain();
        drawChart(false);
      }
    }

    update();
    requestAnimationFrame(frame);
  }

  function init() {
    if (!document.getElementById('rc-style')) {
      const style = document.createElement('style');
      style.id = 'rc-style';
      style.textContent = CSS;
      document.head.appendChild(style);
    }
    document.querySelectorAll('.rc-widget').forEach(build);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
