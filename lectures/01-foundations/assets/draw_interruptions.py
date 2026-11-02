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


for lang in LABELS:
    draw(lang)
