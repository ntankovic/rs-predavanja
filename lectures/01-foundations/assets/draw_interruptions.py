"""Where a worker switches tasks: await on I/O, OS preemption, voluntary yield (2026-11-02).

Writes interruption-points.{hr,en}.svg and .pdf in the style of concurrency.hr.svg. Requires rsvg-convert.
"""
from pathlib import Path
from html import escape
import subprocess

ROOT = Path(__file__).resolve().parent
INK = '#18344b'; GRAY = '#617886'; BLUE = '#1585b4'; ORANGE = '#b56a21'; RED = '#b33e44'
FILL = {'A': ('#e6f6fd', BLUE), 'B': ('#fff0dc', ORANGE)}

LABELS = {
    'hr': {
        'worker': 'Izvršitelj',
        'time': 'Vrijeme',
        'points': [('A čeka pohranu', 'await pohrana.spremi()'),
                   ('OS prekida dretvu', 'istekao vremenski odsječak'),
                   ('A ustupa bez I/O', 'await asyncio.sleep(0)')],
        'coop': ('Kooperativno (asyncio)', 'samo na await: ① i ③'),
        'pre': ('Preemptivno (dretve OS-a)', 'između bilo koje dvije instrukcije: ②'),
    },
    'en': {
        'worker': 'Worker',
        'time': 'Time',
        'points': [('A waits for storage', 'await storage.save()'),
                   ('OS preempts the thread', 'time slice expired'),
                   ('A yields without I/O', 'await asyncio.sleep(0)')],
        'coop': ('Cooperative (asyncio)', 'only at await: ① and ③'),
        'pre': ('Preemptive (OS threads)', 'between any two instructions: ②'),
    },
}


def text(x, y, value, size, color=INK, weight=400, anchor='middle', family='Arial, Helvetica, sans-serif'):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{color}">{escape(value)}</text>')


def draw(lang):
    t = LABELS[lang]
    w, h = 1120, 350
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f'<defs><marker id="time" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
           f'<path d="M0 0L9 4.5L0 9Z" fill="{GRAY}"/></marker></defs>',
           f'<rect width="{w}" height="{h}" fill="white"/>']
    # Timeline A1 | B1 | A2 | B2 with a switch point between consecutive segments.
    x0, y, sw, sh, gap = 190, 20, 190, 62, 50
    out.append(text(24, y + 40, t['worker'], 21, INK, 400, 'start'))
    segments = ['A1', 'B1', 'A2', 'B2']
    colors = [RED if i == 1 else BLUE for i in range(3)]
    for i, label in enumerate(segments):
        x = x0 + i * (sw + gap)
        fill, edge = FILL[label[0]]
        out.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" rx="10" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>')
        out.append(text(x + sw / 2, y + 41, label, 25, INK, 700))
    for i, (head, sub) in enumerate(t['points']):
        cx = x0 + (i + 1) * (sw + gap) - gap / 2
        color = colors[i]
        dash = ' stroke-dasharray="6 5"' if i != 1 else ''
        out.append(f'<line x1="{cx}" y1="{y - 8}" x2="{cx}" y2="{y + sh + 30}" stroke="{color}" stroke-width="2.5"{dash}/>')
        out.append(f'<circle cx="{cx}" cy="{y + sh + 50}" r="17" fill="{color}"/>')
        out.append(text(cx, y + sh + 58, str(i + 1), 21, 'white', 700))
        out.append(text(cx, y + sh + 100, head, 21, INK, 700))
        out.append(text(cx, y + sh + 126, sub, 17, GRAY, 400, family='Menlo, Consolas, monospace' if 'await' in sub else 'Arial, Helvetica, sans-serif'))
    out.append(f'<path d="M{x0} {y + sh + 145}H{x0 + 4 * sw + 3 * gap}" stroke="{GRAY}" stroke-width="2" marker-end="url(#time)"/>')
    out.append(text(x0 + 4 * sw + 3 * gap, y + sh + 168, t['time'], 17, GRAY, 400, 'end'))
    # Legend: which switch points each scheduling style allows.
    for i, ((head, sub), color) in enumerate([(t['coop'], BLUE), (t['pre'], RED)]):
        x = 40 + i * 540
        out.append(f'<rect x="{x}" y="268" width="500" height="68" rx="12" fill="#f8fbfd" stroke="#c6dbe8" stroke-width="1.2"/>')
        out.append(f'<rect x="{x + 10}" y="282" width="6" height="40" rx="3" fill="{color}"/>')
        out.append(text(x + 30, 296, head, 20, INK, 700, 'start'))
        out.append(text(x + 30, 322, sub, 18, GRAY, 400, 'start'))
    out.append('</svg>')
    svg = ROOT / f'interruption-points.{lang}.svg'
    svg.write_text('\n'.join(out))
    subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', str(svg.with_suffix('.pdf')), str(svg)], check=True)


LAYERS = {
    'hr': {
        'top': ('Jezgra · OS', 'dretve T1, T2'), 'bottom': ('Petlja u T1', 'korutine A, B, C'),
        'idle': 'naša petlja stoji', 'await': 'await', 'preempt': 'OS prekid: B ne zna', 'time': 'Vrijeme',
        'os': ('OS raspoređuje dretve', 'preemptivno, prekid bilo gdje'),
        'loop': ('Petlja događaja raspoređuje korutine', 'kooperativno, samo na await'),
    },
    'en': {
        'top': ('Core · OS', 'threads T1, T2'), 'bottom': ('Loop in T1', 'coroutines A, B, C'),
        'idle': 'our loop is paused', 'await': 'await', 'preempt': 'OS preempts: B unaware', 'time': 'Time',
        'os': ('The OS schedules threads', 'preemptive, can stop anywhere'),
        'loop': ('The event loop schedules coroutines', 'cooperative, only at await'),
    },
}
GREEN = '#3d7f4f'
TASKS = {'A': ('#e6f6fd', BLUE), 'B': ('#fff0dc', ORANGE), 'C': ('#eaf5ec', GREEN),
         'T1': ('#e8eef3', '#546573'), 'T2': ('#f6f6f6', '#a3adb5')}


def draw_layers(lang):
    """Two schedulers: OS threads on a core above, event-loop coroutines inside thread T1 below."""
    t = LAYERS[lang]
    w, h = 1120, 370
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f'<defs><marker id="time" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
           f'<path d="M0 0L9 4.5L0 9Z" fill="{GRAY}"/></marker></defs>',
           f'<rect width="{w}" height="{h}" fill="white"/>']

    def seg(x1, x2, y, label, hh=56):
        fill, edge = TASKS[label]
        out.append(f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="{hh}" rx="10" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>')
        out.append(text((x1 + x2) / 2, y + 37, label, 24, INK, 700))

    top, bottom = 30, 150
    for y, (head, sub) in [(top, t['top']), (bottom, t['bottom'])]:
        out.append(text(24, y + 26, head, 21, INK, 700, 'start'))
        out.append(text(24, y + 50, sub, 16, GRAY, 400, 'start'))
    # OS level: T1 and T2 alternate; red solid lines are preemptions.
    threads = [(230, 520, 'T1'), (530, 680, 'T2'), (690, 1000, 'T1'), (1010, 1090, 'T2')]
    for x1, x2, label in threads:
        seg(x1, x2, top, label)
        if label == 'T2':  # The loop lives in T1: while T2 runs, no coroutine runs.
            out.append(f'<rect x="{x1}" y="{bottom}" width="{x2 - x1}" height="56" rx="10" fill="none" stroke="#c3ccd3" stroke-width="1.5" stroke-dasharray="6 5"/>')
        for x in (x1, x2):
            out.append(f'<line x1="{x}" y1="{top + 60}" x2="{x}" y2="{bottom - 4}" stroke="#d5dee5" stroke-width="1.5" stroke-dasharray="3 5"/>')
    out.append(text(605, bottom + 35, t['idle'], 17, GRAY))
    # Loop level inside T1: A, B, C switch only at await (blue dashed); B continues after the preemption.
    for x1, x2, label in [(230, 360, 'A'), (372, 520, 'B'), (690, 830, 'B'), (842, 1000, 'C')]:
        seg(x1, x2, bottom, label)
    for x, color, dash, label in [(366, BLUE, True, t['await']), (836, BLUE, True, t['await']), (525, RED, False, t['preempt'])]:
        d = ' stroke-dasharray="6 5"' if dash else ''
        y1 = bottom - 10 if dash else top - 8
        out.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{bottom + 72}" stroke="{color}" stroke-width="2.5"{d}/>')
        family = 'Menlo, Consolas, monospace' if dash else 'Arial, Helvetica, sans-serif'
        out.append(text(x, bottom + 94, label, 17, color, 700, family=family))
    out.append(f'<path d="M230 {bottom + 112}H1090" stroke="{GRAY}" stroke-width="2" marker-end="url(#time)"/>')
    out.append(text(1090, bottom + 134, t['time'], 16, GRAY, 400, 'end'))
    # Legend: the two schedulers.
    for i, ((head, sub), color) in enumerate([(t['os'], RED), (t['loop'], BLUE)]):
        x = 40 + i * 540
        out.append(f'<rect x="{x}" y="292" width="500" height="68" rx="12" fill="#f8fbfd" stroke="#c6dbe8" stroke-width="1.2"/>')
        out.append(f'<rect x="{x + 10}" y="306" width="6" height="40" rx="3" fill="{color}"/>')
        out.append(text(x + 30, 320, head, 20, INK, 700, 'start'))
        out.append(text(x + 30, 346, sub, 18, GRAY, 400, 'start'))
    out.append('</svg>')
    svg = ROOT / f'scheduler-layers.{lang}.svg'
    svg.write_text('\n'.join(out))
    subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', str(svg.with_suffix('.pdf')), str(svg)], check=True)


for lang in LABELS:
    draw(lang)
    draw_layers(lang)
