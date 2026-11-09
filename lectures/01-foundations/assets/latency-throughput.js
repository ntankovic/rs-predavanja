/* Latency, bandwidth and throughput of one transfer (2026-11-09).
   Self-contained widget for the slide after "Kašnjenje, kapacitet i dovršeni posao"; no libraries, no network.
   Usage: <div class="lt-widget" data-lang="hr|en"></div><script src="assets/latency-throughput.js"></script>
   Model: duration = latency + size / bandwidth + 1 / server rate; throughput = min(bandwidth / size, server rate).
   No queueing, retries or protocol overhead. */
(function () {
  'use strict';

  const LAT = [0.1, 1, 5, 20, 75, 150, 300, 1000, 5000, 60000, 3600000, 43200000]; // ms
  const BW = [1, 10, 100, 1000, 10000, 100000, 1e6, 1e9]; // Mbit/s
  const SIZE = [0.002, 0.1, 1, 20, 200, 1000, 1e4, 1e6, 1e8]; // MB (decimal)
  const PROC = [0.001, 0.01, 0.1, 0.5, 1, 5, 20, 100, 500, 5000]; // projects/s
  const PRESETS = [
    { lat: 150, bw: 1000, size: 0.002, proc: 500 },
    { lat: 20, bw: 100, size: 200, proc: 5 },
    { lat: 20, bw: 10000, size: 200, proc: 0.5 },
    { lat: 20, bw: 10000, size: 1e8, proc: 5000 },
    { lat: 43200000, bw: 1e9, size: 1e8, proc: 5000 },
  ];
  const TRUCK = 4;
  const TARGET_SECONDS = 4; // each scenario's default speed makes one transfer last about this long
  const SPEED_SERIES = [];
  for (let k = -6; k <= 9; k++) [1, 2, 5].forEach((m) => SPEED_SERIES.push(Number((m * Math.pow(10, k)).toPrecision(1))));
  const FLOW_PX_PER_S = 48; // chevron speed at the scenario's default speed
  const FLOW_MAX_PX_PER_S = 320; // faster chevrons would appear to run backwards
  const PAUSE_MS = 1500;
  const START_DELAY_MS = 1000; // pause after choosing a scenario, before the transfer starts
  const WIRE_SEND_DIVISOR = 5; // the animated block is 5x shorter per MB; the numbers are not scaled
  const MIN_BLOCK = 26; // keeps the first and last bit visibly apart on short transfers

  const T = {
    hr: {
      latNames: ['Isti rack', 'LAN', 'Isti grad', 'WAN, isti kontinent', 'Preko oceana', 'Druga strana svijeta', 'Geostacionarni satelit', 'Zagušena mreža', 'Jako zagušena mreža', 'USB stick do kolege', 'Kurir kroz grad', 'Kamion s diskovima'],
      bwNames: ['Slab mobilni signal', 'Stariji kućni priključak', 'Kućni internet', 'Gigabitni Ethernet', '10 GbE, podatkovni centar', '100 GbE, jezgra mreže', 'Podmorski optički kabel', 'Kamion s diskovima'],
      presets: ['Mali zahtjev', 'Veliki ZIP', 'Spora provjera', '100 TB mrežom', '100 TB kamionom'],
      lat: 'Latencija (jedan smjer)', bw: 'Kapacitet veze', size: 'Veličina projekta', proc: 'Obrada poslužitelja',
      proj: 'projekata', day: 'dan', time: 'Trajanje do prihvaćanja', procPart: 'obrada', processing: 'obrada…', done: '✓ gotovo', accepted: 'projekt prihvaćen', thr: 'Propusnost',
      latPart: 'latencija', sendPart: 'slanje', linkAllows: 'Veza dopušta', srvAllows: 'Poslužitelj dopušta',
      bottleneck: 'Usko grlo', link: 'veza', server: 'poslužitelj', client: 'Klijent', srv: 'Poslužitelj',
      elapsed: 'Proteklo vrijeme', firstBit: 'prvi bit', lastBit: 'zadnji bit', first: 'prvi bit stigao', last: 'zadnji bit stigao', decimal: ',',
      domLat: 'Dominira latencija: veći kapacitet veze gotovo ne skraćuje prijenos.',
      domSend: 'Dominira slanje: veći kapacitet veze skraćuje prijenos, a latencija malo utječe.',
      domProc: 'Dominira obrada: brži prijenos gotovo ne skraćuje čekanje.',
      foot: 'Model: trajanje = latencija + veličina / kapacitet + obrada jednog projekta; propusnost = min(veza, poslužitelj). Bez čekanja u redu, ponovnih slanja i troškova protokola. Nazivi su okvirni.',
      truck: 'Kamion: 12 h puta, a 1 Pbit/s gruba je zamjena za puni teret. Kopiranje na diskove, čitanje i provjera nisu uključeni.',
    },
    en: {
      latNames: ['Same rack', 'LAN', 'Same city', 'WAN, same continent', 'Transoceanic', 'Other side of the world', 'Geostationary satellite', 'Congested network', 'Severely congested network', 'USB stick to a colleague', 'Courier across town', 'Truck with drives'],
      bwNames: ['Weak mobile signal', 'Older home connection', 'Home internet', 'Gigabit Ethernet', '10 GbE, datacenter', '100 GbE, network core', 'Submarine fiber cable', 'Truck with drives'],
      presets: ['Small request', 'Large ZIP', 'Slow check', '100 TB by network', '100 TB by truck'],
      lat: 'Latency (one way)', bw: 'Link bandwidth', size: 'Project size', proc: 'Server processing',
      proj: 'projects', day: 'day', time: 'Time to acceptance', procPart: 'processing', processing: 'processing…', done: '✓ done', accepted: 'project accepted', thr: 'Throughput',
      latPart: 'latency', sendPart: 'sending', linkAllows: 'Link allows', srvAllows: 'Server allows',
      bottleneck: 'Bottleneck', link: 'link', server: 'server', client: 'Client', srv: 'Server',
      elapsed: 'Elapsed time', firstBit: 'first bit', lastBit: 'last bit', first: 'first bit arrived', last: 'last bit arrived', decimal: '.',
      domLat: 'Latency dominates: more bandwidth barely shortens the transfer.',
      domSend: 'Sending dominates: more bandwidth shortens the transfer; latency matters little.',
      domProc: 'Processing dominates: a faster transfer barely shortens the wait.',
      foot: 'Model: duration = latency + size / bandwidth + processing one project; throughput = min(link, server). No queueing, retransmissions, or protocol overhead. Names are approximate.',
      truck: 'Truck: 12 h on the road; 1 Pbit/s is a rough stand-in for a full load. Copying to drives, reading, and verification are not included.',
    },
  };

  const CSS = `
.lt-widget{box-sizing:border-box;width:1060px;height:560px;margin:0 auto;padding:12px 14px;display:grid;grid-template-rows:auto 1fr auto auto;gap:9px;
 border:1.5px solid #c6dbe8;border-radius:14px;background:#f8fbfd;color:#18344b;font-family:"Inter","Segoe UI",Arial,Helvetica,sans-serif;font-size:15px;line-height:1.25;text-align:left}
.lt-widget *{box-sizing:border-box}
.lt-top{display:flex;gap:7px}
.lt-widget button{font:inherit;color:#18344b;background:#fff;border:1px solid #c6dbe8;border-radius:9px;padding:5px 11px;cursor:pointer}
.lt-widget button:hover{background:#e7f3fb}
.lt-widget button[aria-pressed="true"]{border-color:#1585b4;background:#e7f3fb}
.lt-widget button:focus-visible,.lt-widget input:focus-visible{outline:2px solid #1585b4;outline-offset:2px}
.lt-main{display:grid;grid-template-columns:292px 1fr;gap:10px;min-height:0}
.lt-left{display:flex;flex-direction:column;gap:7px}
.lt-right{display:grid;grid-template-rows:auto 1fr;gap:8px;min-height:0}
.lt-card{background:#fff;border:1px solid #c6dbe8;border-radius:12px;padding:8px 11px}
.lt-left .lt-card{flex:1;display:flex;flex-direction:column;justify-content:center}
.lt-ctl{display:flex;justify-content:space-between;align-items:baseline;gap:8px;font-size:14px;color:#546573}
.lt-ctl b{font-size:19px;color:#105d80;white-space:nowrap}
.lt-widget input[type=range]{width:100%;margin:6px 0 0;accent-color:#3886ad}
.lt-name{margin-top:4px;font-size:14px;font-weight:600;color:#18344b}
.lt-clock{display:flex;justify-content:center;align-items:center;gap:14px;font-size:15px;color:#546573}
.lt-speed{display:inline-flex;gap:4px}
.lt-widget .lt-speed button{font-size:13px;padding:2px 8px}
.lt-clock b{font-family:"SF Mono",Menlo,Consolas,"DejaVu Sans Mono","Courier New",monospace;font-size:19px;color:#18344b}
.lt-wire svg{display:block;width:100%;height:112px}
.lt-res{display:grid;grid-template-columns:1fr 1fr;gap:8px;min-height:0}
.lt-res .lt-card{display:flex;flex-direction:column;justify-content:space-between;min-width:0}
.lt-label{font-size:13px;color:#546573}
.lt-big{font-size:33px;font-weight:750;line-height:1.1;font-variant-numeric:tabular-nums;white-space:nowrap}
.lt-stack{display:flex;height:18px;margin-top:6px;border-radius:5px;overflow:hidden;background:#e6eef3}
.lt-stack i{display:block;height:100%}
.lt-l{background:#3886ad}.lt-s{background:#b56a21}.lt-p{background:#d9a066}
.lt-legend{display:flex;justify-content:space-between;gap:6px;margin-top:5px;font-size:13px;color:#546573;white-space:nowrap}
.lt-legend b{color:#18344b;font-variant-numeric:tabular-nums}
.lt-row{display:grid;grid-template-columns:118px 1fr;align-items:center;gap:8px;margin-top:5px;font-size:13px;color:#546573}
.lt-row div{height:11px;background:#e6eef3;border-radius:4px;overflow:hidden}
.lt-row i{display:block;height:100%;background:#a3c9dc}
.lt-row i.lt-hit{background:#b33e44}
.lt-neck{font-size:13px;color:#546573;margin-top:5px}
.lt-neck b{color:#b33e44}
.lt-insight{font-size:16px;font-weight:600;text-align:center;padding:6px 10px;border-radius:10px;background:#e7f3fb;border:1px solid #c6dbe8}
.lt-foot{font-size:12px;color:#546573}
`;

  function stopwatch(ms) {
    const total = Math.round(ms);
    const pad = (v, n) => String(v).padStart(n, '0');
    return [pad(Math.floor(total / 3600000), 2), pad(Math.floor(total / 60000) % 60, 2), pad(Math.floor(total / 1000) % 60, 2)].join(':') + '.' + pad(total % 1000, 3);
  }

  function sig(x, dec) {
    return String(Number(x.toPrecision(3))).replace('.', dec);
  }

  function makeFormatters(t) {
    const dec = t.decimal;
    return {
      time(ms) {
        if (ms < 1) return sig(ms * 1000, dec) + ' µs';
        if (ms < 1000) return sig(ms, dec) + ' ms';
        if (ms < 60000) return sig(ms / 1000, dec) + ' s';
        if (ms < 3600000) return sig(ms / 60000, dec) + ' min';
        if (ms < 86400000) return sig(ms / 3600000, dec) + ' h';
        return sig(ms / 86400000, dec) + ' ' + t.day;
      },
      bw(v) {
        if (v >= 1e9) return sig(v / 1e9, dec) + ' Pbit/s';
        if (v >= 1e6) return sig(v / 1e6, dec) + ' Tbit/s';
        if (v >= 1e3) return sig(v / 1e3, dec) + ' Gbit/s';
        return sig(v, dec) + ' Mbit/s';
      },
      size(v) {
        if (v >= 1e6) return sig(v / 1e6, dec) + ' TB';
        if (v >= 1e3) return sig(v / 1e3, dec) + ' GB';
        if (v < 1) return sig(v * 1e3, dec) + ' KB';
        return sig(v, dec) + ' MB';
      },
      rate(r) {
        if (r >= 1) return sig(r, dec) + ' ' + t.proj + '/s';
        if (r * 60 >= 1) return sig(r * 60, dec) + ' ' + t.proj + '/min';
        if (r * 3600 >= 1) return sig(r * 3600, dec) + ' ' + t.proj + '/h';
        return sig(r * 86400, dec) + ' ' + t.proj + '/' + t.day;
      },
    };
  }

  function svgEl(name, attrs, parent) {
    const el = document.createElementNS('http://www.w3.org/2000/svg', name);
    Object.keys(attrs).forEach((k) => el.setAttribute(k, attrs[k]));
    parent.appendChild(el);
    return el;
  }

  function init(root) {
    if (root.dataset.ready) return;
    root.dataset.ready = '1';
    const t = T[root.dataset.lang] || T.hr;
    const fmt = makeFormatters(t);
    const controls = [
      { key: 'lat', values: LAT, label: t.lat, show: fmt.time, names: t.latNames },
      { key: 'bw', values: BW, label: t.bw, show: fmt.bw, names: t.bwNames },
      { key: 'size', values: SIZE, label: t.size, show: fmt.size },
      { key: 'proc', values: PROC, label: t.proc, show: fmt.rate },
    ];
    const state = Object.assign({}, PRESETS[0]);

    root.innerHTML = `
<div class="lt-top">${t.presets.map((name, i) => `<button type="button" data-preset="${i}" aria-pressed="false">${name}</button>`).join('')}</div>
<div class="lt-main">
  <div class="lt-left">${controls.map((c) => `
    <div class="lt-card">
      <div class="lt-ctl"><span>${c.label}</span><b data-val="${c.key}"></b></div>
      <input type="range" min="0" max="${c.values.length - 1}" step="1" data-in="${c.key}" aria-label="${c.label}">
      ${c.names ? `<div class="lt-name" data-name="${c.key}"></div>` : ''}
    </div>`).join('')}
  </div>
  <div class="lt-right">
    <div class="lt-card lt-wire"><div class="lt-clock"><span>${t.elapsed}: <b data-out="clock"></b></span><span class="lt-speed" data-out="speeds"></span></div><svg viewBox="0 0 710 112" aria-hidden="true"></svg></div>
    <div class="lt-res">
      <div class="lt-card">
        <div class="lt-label">${t.time}</div>
        <div class="lt-big" data-out="time"></div>
        <div class="lt-stack"><i class="lt-l" data-out="lBar"></i><i class="lt-s" data-out="sBar"></i><i class="lt-p" data-out="pBar"></i></div>
        <div class="lt-legend"><span>${t.latPart}: <b data-out="lNum"></b></span><span>${t.sendPart}: <b data-out="sNum"></b></span><span>${t.procPart}: <b data-out="pNum"></b></span></div>
      </div>
      <div class="lt-card">
        <div class="lt-label">${t.thr}</div>
        <div class="lt-big" data-out="thr"></div>
        <div>
          <div class="lt-row"><span>${t.linkAllows}</span><div><i data-out="linkBar"></i></div></div>
          <div class="lt-row"><span>${t.srvAllows}</span><div><i data-out="srvBar"></i></div></div>
          <div class="lt-neck">${t.bottleneck}: <b data-out="neck"></b></div>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="lt-insight" data-out="insight"></div>
<div class="lt-foot" data-out="foot"></div>`;

    const out = (k) => root.querySelector(`[data-out="${k}"]`);

    // ---------- Wire ----------
    const svg = root.querySelector('.lt-wire svg');
    const X0 = 96, X1 = 614, Y = 62;
    const box = (x, label) => {
      const rect = svgEl('rect', { x, y: Y - 22, width: 84, height: 44, rx: 9, fill: '#edf7fc', stroke: '#a3c9dc' }, svg);
      const text = svgEl('text', { x: x + 42, y: Y + 5, fill: '#18344b', 'font-size': 14, 'font-weight': 600, 'text-anchor': 'middle' }, svg);
      text.textContent = label;
      return { rect, text };
    };
    svgEl('line', { x1: X0, x2: X1, y1: Y, y2: Y, stroke: '#c6dbe8', 'stroke-width': 12, 'stroke-linecap': 'butt' }, svg);
    const defs = svgEl('defs', {}, svg);
    const flow = svgEl('pattern', { id: 'lt-flow', patternUnits: 'userSpaceOnUse', width: 16, height: 12 }, defs);
    svgEl('rect', { width: 16, height: 12, fill: '#8f5118' }, flow);
    svgEl('polygon', { points: '1,0 7,0 13,6 7,12 1,12 7,6', fill: '#d9a066' }, flow);
    const block = svgEl('rect', { y: Y - 6, height: 12, fill: 'url(#lt-flow)' }, svg);
    box(10, t.client);
    const server = box(616, t.srv);
    const procFill = svgEl('rect', { x: 616, y: Y - 22, height: 44, rx: 9, width: 0, fill: '#f6dcb8' }, svg);
    svg.insertBefore(procFill, server.text);
    const mark = (color) => svgEl('rect', { y: Y - 12, width: 6, height: 24, rx: 2, fill: color }, svg);
    const label = (y, color) => svgEl('text', { y, fill: color, 'font-size': 14, 'font-weight': 700, 'text-anchor': 'middle' }, svg);
    const firstBar = mark('#1585b4');
    const lastBar = mark('#18344b');
    const firstMark = label(30, '#1585b4');
    const lastMark = label(104, '#18344b');

    let wireLat = 0.5, wireSend = 0.5, latMs = 0, sendTimeMs = 0, procTimeMs = 0;
    let progress = 0, hold = 0, last = 0, speed = 1, defaultSpeed = 1, flowX = 0;

    function speedLabel(v) {
      return 'x' + String(v).replace('.', t.decimal).replace(/\B(?=(\d{3})+(?!\d))/g, '\u202f');
    }

    // x1 is real time. Offer it plus the speeds around the one that makes this transfer last a few seconds.
    function chooseSpeeds(totalMs) {
      const ideal = totalMs / 1000 / TARGET_SECONDS;
      let best = 0;
      SPEED_SERIES.forEach((v, i) => {
        if (Math.abs(Math.log(v / ideal)) < Math.abs(Math.log(SPEED_SERIES[best] / ideal))) best = i;
      });
      defaultSpeed = speed = SPEED_SERIES[best];
      const options = [1, SPEED_SERIES[best - 1], SPEED_SERIES[best], SPEED_SERIES[best + 1]].filter((v) => v !== undefined);
      out('speeds').innerHTML = Array.from(new Set(options)).sort((a, b) => a - b)
        .map((v) => `<button type="button" data-speed="${v}" aria-pressed="${v === speed}">${speedLabel(v)}</button>`).join('');
    }

    function drawWire(progressShare) {
      // The clock runs linearly in model time; only the drawing maps it onto the shortened block.
      const transferMs = latMs + sendTimeMs;
      const elapsed = progressShare * (transferMs + procTimeMs);
      const rawF = elapsed < latMs ? (elapsed / latMs) * wireLat : wireLat + (sendTimeMs > 0 ? ((elapsed - latMs) / sendTimeMs) * (1 - wireLat) : 0);
      const f = Math.min(1, rawF);
      const head = wireLat > 0 ? Math.min(f / wireLat, 1) : 1;
      const tail = f < wireSend || wireLat <= 0 ? 0 : Math.min((f - wireSend) / wireLat, 1);
      let a = X0 + tail * (X1 - X0);
      let b = X0 + head * (X1 - X0);
      if (b - a < MIN_BLOCK) {
        a = b - MIN_BLOCK;
        if (a < X0) { a = X0; b = X0 + MIN_BLOCK; }
      }
      block.setAttribute('x', a);
      block.setAttribute('width', f >= 1 ? 0 : b - a);
      firstBar.setAttribute('opacity', f >= 1 ? 0 : 1);
      lastBar.setAttribute('opacity', f >= 1 ? 0 : 1);
      firstBar.setAttribute('x', b - 6);
      lastBar.setAttribute('x', a);
      const labelX = (x) => Math.max(66, Math.min(644, x));
      firstMark.setAttribute('x', labelX(b - 3));
      lastMark.setAttribute('x', labelX(a + 3));
      firstMark.textContent = f >= wireLat ? t.first : t.firstBit;
      lastMark.textContent = progressShare >= 1 ? t.accepted : f >= 1 ? t.last : t.lastBit;
      lastMark.setAttribute('fill', progressShare >= 1 ? '#2e7d4f' : '#18344b');
      // Server states: waiting for the last bit, processing, done.
      const processing = f >= 1 && progressShare < 1;
      const done = progressShare >= 1;
      server.rect.setAttribute('fill', done ? '#dff0e4' : processing ? '#fff4e3' : '#edf7fc');
      server.rect.setAttribute('stroke', done ? '#2e7d4f' : processing ? '#b56a21' : '#a3c9dc');
      procFill.setAttribute('width', processing && procTimeMs > 0 ? 84 * Math.max(0, elapsed - transferMs) / procTimeMs : 0);
      server.text.textContent = done ? t.done : processing ? t.processing : t.srv;
      server.text.setAttribute('fill', done ? '#2e7d4f' : '#18344b');
      out('clock').textContent = stopwatch(elapsed);
    }

    function frame(now) {
      requestAnimationFrame(frame);
      const section = root.closest('section');
      if (document.hidden || (section && !section.classList.contains('present'))) return;
      const dt = Math.min(100, now - (last || now));
      last = now;
      // The pause before the next transfer stays in real time at every speed.
      if (hold > 0) {
        hold -= dt;
        if (hold <= 0) progress = 0;
      } else {
        progress += (dt * speed) / (latMs + sendTimeMs + procTimeMs);
        flowX = (flowX + (dt / 1000) * Math.min(FLOW_MAX_PX_PER_S, FLOW_PX_PER_S * speed / defaultSpeed)) % 16;
        flow.setAttribute('patternTransform', `translate(${flowX} ${Y - 6})`);
        if (progress >= 1) { progress = 1; hold = PAUSE_MS; }
      }
      drawWire(progress);
    }

    // ---------- Results ----------
    function update() {
      controls.forEach((c) => {
        root.querySelector(`[data-in="${c.key}"]`).value = c.values.indexOf(state[c.key]);
        root.querySelector(`[data-val="${c.key}"]`).textContent = c.show(state[c.key]);
        if (c.names) root.querySelector(`[data-name="${c.key}"]`).textContent = c.names[c.values.indexOf(state[c.key])];
      });
      const sendMs = (state.size * 8 / state.bw) * 1000;
      const procMs = 1000 / state.proc;
      const total = state.lat + sendMs + procMs;
      const latShare = state.lat / total;
      const sendShare = sendMs / total;
      const wireSendMs = sendMs / WIRE_SEND_DIVISOR;
      latMs = state.lat;
      sendTimeMs = sendMs;
      procTimeMs = procMs;
      wireLat = state.lat / (state.lat + wireSendMs);
      wireSend = wireSendMs / (state.lat + wireSendMs);
      const linkRate = state.bw / (8 * state.size);
      const throughput = Math.min(linkRate, state.proc);
      const linkLimits = linkRate <= state.proc;
      const scale = Math.max(linkRate, state.proc);

      out('time').textContent = fmt.time(total);
      out('lBar').style.width = latShare * 100 + '%';
      out('sBar').style.width = sendShare * 100 + '%';
      out('pBar').style.width = (procMs / total) * 100 + '%';
      out('pNum').textContent = fmt.time(procMs);
      out('lNum').textContent = fmt.time(state.lat);
      out('sNum').textContent = fmt.time(sendMs);
      out('thr').textContent = fmt.rate(throughput);
      out('linkBar').style.width = Math.max(1, 100 * linkRate / scale) + '%';
      out('srvBar').style.width = Math.max(1, 100 * state.proc / scale) + '%';
      out('linkBar').classList.toggle('lt-hit', linkLimits);
      out('srvBar').classList.toggle('lt-hit', !linkLimits);
      out('neck').textContent = (linkLimits ? t.link : t.server) + ' (' + fmt.rate(linkLimits ? linkRate : state.proc) + ')';
      out('insight').textContent = procMs >= state.lat && procMs >= sendMs ? t.domProc : state.lat > sendMs ? t.domLat : t.domSend;

      let active = -1;
      root.querySelectorAll('[data-preset]').forEach((b) => {
        const i = Number(b.dataset.preset);
        const preset = PRESETS[i];
        const on = controls.every((c) => preset[c.key] === state[c.key]);
        if (on) active = i;
        b.setAttribute('aria-pressed', String(on));
      });
      out('foot').textContent = active === TRUCK ? t.truck : t.foot;
      progress = 0;
      hold = START_DELAY_MS;
      chooseSpeeds(total);
    }

    root.addEventListener('input', (e) => {
      const c = controls.find((x) => x.key === e.target.dataset.in);
      if (!c) return;
      state[c.key] = c.values[Number(e.target.value)];
      update();
    });
    // Arrow keys must move the focused slider, not change the slide.
    root.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT') e.stopPropagation();
    });
    root.addEventListener('click', (e) => {
      const s = e.target.closest('[data-speed]');
      if (s) {
        speed = Number(s.dataset.speed);
        root.querySelectorAll('[data-speed]').forEach((x) => x.setAttribute('aria-pressed', String(x === s)));
        return;
      }
      const b = e.target.closest('[data-preset]');
      if (!b) return;
      Object.assign(state, PRESETS[Number(b.dataset.preset)]);
      update();
    });

    update();
    requestAnimationFrame(frame);
  }

  if (!document.getElementById('lt-style')) {
    const style = document.createElement('style');
    style.id = 'lt-style';
    style.textContent = CSS;
    document.head.appendChild(style);
  }
  document.querySelectorAll('.lt-widget').forEach(init);
})();
