"""TTFB refresher diagram in the card style of the newer lecture 01 figures (2026-11-03).

Writes web-ttfb.svg/.pdf (English) and web-ttfb.hr.svg/.pdf. Requires rsvg-convert.
Replaces the earlier hand-edited web-ttfb masters; widths remain schematic.
"""
from pathlib import Path
from html import escape
import subprocess

ROOT = Path(__file__).resolve().parent
INK = '#18344b'; GRAY = '#617886'; BLUE = '#1585b4'

LABELS = {
    'hr': {'file': 'web-ttfb.hr', 'setup': 'Uspostava veze', 'server': 'Mreža i poslužitelj',
           'wait': 'zahtjev → red → obrada → odgovor', 'download': 'Preuzimanje',
           'first': 'prvi bajt odgovora', 'ttfb': 'TTFB od početka navigacije',
           'rest': 'ostatak odgovora stiže poslije',
           'note': 'Nova HTTPS veza preko TCP-a; trajanja su shematska. DNS i veze mogu se ponovno koristiti.'},
    'en': {'file': 'web-ttfb', 'setup': 'Connection setup', 'server': 'Network and server',
           'wait': 'request → queue → processing → reply', 'download': 'Download',
           'first': 'first response byte', 'ttfb': 'TTFB from navigation start',
           'rest': 'the rest of the response follows',
           'note': 'A fresh HTTPS connection over TCP; durations are schematic. DNS and connections may be reused.'},
}
# (label key or literal, width, fill, edge)
SEGMENTS = [('DNS', 130, '#eaf5ec', '#3d7f4f'), ('TCP', 130, '#fff0dc', '#b56a21'),
            ('TLS', 130, '#f1ecf8', '#7a5aa6'), ('wait', 420, '#e6f6fd', BLUE),
            ('download', 210, '#f3f6f8', '#9aa9b4')]


def text(x, y, value, size, color=INK, weight=400, anchor='middle'):
    return (f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(value)}</text>')


def bracket(x1, x2, y, up, color):
    tick = -10 if up else 10
    return (f'<path d="M{x1} {y + tick}V{y}H{x2}V{y + tick}" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linejoin="round"/>')


def draw(lang):
    t = LABELS[lang]
    w, h = 1120, 276
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f'<rect width="{w}" height="{h}" fill="white"/>']
    x, y, bh, gap = 38, 68, 64, 6
    edges = []
    for key, width, fill, edge in SEGMENTS:
        dash = ' stroke-dasharray="6 5"' if key == 'download' else ''
        out.append(f'<rect x="{x}" y="{y}" width="{width}" height="{bh}" rx="12" fill="{fill}" stroke="{edge}" stroke-width="1.6"{dash}/>')
        label = t.get(key, key)
        size, weight = (20, 700) if key in ('DNS', 'TCP', 'TLS', 'download') else (18, 700)
        out.append(text(x + width / 2, y + bh / 2 + 7, label, size, edge if key != 'download' else GRAY, weight))
        edges.append((x, x + width))
        x += width + gap
    # Groups above the bar.
    setup_x1, setup_x2 = edges[0][0], edges[2][1]
    wait_x1, wait_x2 = edges[3]
    for x1, x2, label in [(setup_x1, setup_x2, t['setup']), (wait_x1, wait_x2, t['server'])]:
        out.append(bracket(x1 + 4, x2 - 4, y - 16, False, '#b8c6d0'))
        out.append(text((x1 + x2) / 2, y - 26, label, 17, GRAY, 700))
    # First-byte marker.
    fb = wait_x2 + gap / 2
    out.append(f'<line x1="{fb}" y1="{y - 8}" x2="{fb}" y2="{y + bh + 64}" stroke="{INK}" stroke-width="2" stroke-dasharray="4 4"/>')
    out.append(f'<circle cx="{fb}" cy="{y - 8}" r="6" fill="{INK}"/>')
    out.append(text(fb + 12, y + bh + 30, t['first'], 16, INK, 700, 'start'))
    # TTFB bracket below the bar, ending at the first byte.
    out.append(bracket(setup_x1, fb, y + bh + 50, True, BLUE))
    out.append(text((setup_x1 + fb) / 2, y + bh + 80, t['ttfb'], 20, BLUE, 700))
    out.append(text((edges[4][0] + edges[4][1]) / 2, y + bh + 80, t['rest'], 15, GRAY))
    out.append(text(w / 2, h - 14, t['note'], 15, GRAY))
    out.append('</svg>')
    svg = ROOT / f"{t['file']}.svg"
    svg.write_text('\n'.join(out))
    subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', str(svg.with_suffix('.pdf')), str(svg)], check=True)


for lang in LABELS:
    draw(lang)
