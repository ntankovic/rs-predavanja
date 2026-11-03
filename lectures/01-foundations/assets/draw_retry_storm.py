"""Retry storm: ten clients retrying against one struggling service, and the goodput curve (2026-11-03).

Writes retry-storm.{hr,en}.svg and .pdf. Requires rsvg-convert. The curve is schematic, not a measurement.
"""
from pathlib import Path
from html import escape
import subprocess

ROOT = Path(__file__).resolve().parent
INK = '#18344b'; GRAY = '#617886'; BLUE = '#1585b4'; RED = '#b33e44'; GREEN = '#3d7f4f'

LABELS = {
    'hr': {'client': 'K', 'service': 'Usluga zadataka', 'overloaded': 'preopterećena',
           'legend': 'Puna crta: prvi pokušaj · svjetlije: ponovni pokušaji',
           'x': 'Pristigli zahtjevi u sekundi', 'y': 'Obrađeno u sekundi', 'capacity': 'kapacitet',
           'ok': 'radi dobro', 'ideal': 'idealno', 'real': 'stvarno: timeouti → još pokušaja'},
    'en': {'client': 'C', 'service': 'Task service', 'overloaded': 'overloaded',
           'legend': 'Solid: first attempt · lighter: retries',
           'x': 'Incoming requests per second', 'y': 'Completed per second', 'capacity': 'capacity',
           'ok': 'works well', 'ideal': 'ideal', 'real': 'real: timeouts → more retries'},
}


def text(x, y, value, size, color=INK, weight=400, anchor='middle', extra=''):
    return (f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{color}"{extra}>{escape(value)}</text>')


def draw(lang):
    t = LABELS[lang]
    w, h = 1120, 432
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f'<defs><marker id="hit" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
           f'<path d="M0 0L8 4L0 8Z" fill="{RED}"/></marker>'
           f'<marker id="axis" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
           f'<path d="M0 0L9 4.5L0 9Z" fill="{GRAY}"/></marker></defs>',
           f'<rect width="{w}" height="{h}" fill="white"/>']
    # Left: ten clients, each with a first attempt and two retries converging on one service.
    sx, sy, sw, sh = 350, 140, 210, 110
    for i in range(10):
        y = 18 + i * 37
        out.append(f'<rect x="20" y="{y}" width="78" height="30" rx="8" fill="#e6f6fd" stroke="{BLUE}" stroke-width="1.4"/>')
        out.append(text(59, y + 21, f"{t['client']}{i + 1}", 16, INK, 700))
        for k, opacity in enumerate((1, .55, .3)):
            ty = sy + 12 + (i * 3 + k) * (sh - 24) / 29
            out.append(f'<line x1="100" y1="{y + 15 + (k - 1) * 6}" x2="{sx - 6}" y2="{ty:.1f}" stroke="{RED}" '
                       f'stroke-width="1.6" opacity="{opacity}" marker-end="url(#hit)"/>')
    out.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="14" fill="#fdf3f3" stroke="#e3b9bc" stroke-width="1.5"/>')
    out.append(f'<rect x="{sx + 10}" y="{sy + 22}" width="6" height="{sh - 44}" rx="3" fill="{RED}"/>')
    out.append(text(sx + sw / 2 + 7, sy + 50, t['service'], 19, INK, 700))
    out.append(text(sx + sw / 2 + 7, sy + 76, t['overloaded'], 17, RED))
    out.append(text(275, 412, t['legend'], 15, GRAY))
    # Right: schematic goodput curve; fine below capacity, collapsing above it.
    ox, oy, ax, ay = 640, 360, 1090, 40
    out.append(f'<path d="M{ox} {oy}H{ax}" stroke="{GRAY}" stroke-width="2" marker-end="url(#axis)"/>')
    out.append(f'<path d="M{ox} {oy}V{ay}" stroke="{GRAY}" stroke-width="2" marker-end="url(#axis)"/>')
    out.append(text(ax, oy + 28, t['x'], 16, GRAY, 400, 'end'))
    out.append(text(ox - 14, ay + 10, t['y'], 16, GRAY, 400, 'end', f' transform="rotate(-90 {ox - 14} {ay + 10})"'))
    cap = 840
    out.append(f'<rect x="{ox + 2}" y="{ay}" width="{cap - ox - 2}" height="{oy - ay}" fill="#eaf5ec" opacity=".55"/>')
    out.append(text((ox + cap) / 2, oy - 14, t['ok'], 16, GREEN, 700))
    out.append(f'<line x1="{cap}" y1="{ay + 10}" x2="{cap}" y2="{oy}" stroke="{GRAY}" stroke-width="1.5" stroke-dasharray="5 5"/>')
    out.append(text(cap, ay + 4, t['capacity'], 16, GRAY))
    out.append(f'<path d="M{ox} {oy}L{cap} 110H{ax - 10}" fill="none" stroke="{GRAY}" stroke-width="2" stroke-dasharray="7 6"/>')
    out.append(f'<path d="M{ox} {oy}L{cap - 30} 125 Q{cap + 10} 92 {cap + 60} 150 T{ax - 20} 320" fill="none" stroke="{RED}" stroke-width="4"/>')
    # Legend below the axis label, so no label crosses a curve.
    out.append(f'<line x1="{ox}" y1="412" x2="{ox + 34}" y2="412" stroke="{GRAY}" stroke-width="2" stroke-dasharray="7 6"/>')
    out.append(text(ox + 42, 417, t['ideal'], 15, GRAY, 400, 'start'))
    out.append(f'<line x1="{ox + 130}" y1="412" x2="{ox + 164}" y2="412" stroke="{RED}" stroke-width="4"/>')
    out.append(text(ox + 172, 417, t['real'], 15, RED, 700, 'start'))
    out.append('</svg>')
    svg = ROOT / f'retry-storm.{lang}.svg'
    svg.write_text('\n'.join(out))
    subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', str(svg.with_suffix('.pdf')), str(svg)], check=True)


for lang in LABELS:
    draw(lang)
