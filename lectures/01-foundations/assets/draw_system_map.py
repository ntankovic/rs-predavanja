"""System map and partial-failure diagrams, Croatian first, in the shared card style (2026-10-13).

Writes system-map / partial-failure as .hr.svg/.hr.pdf and English .svg/.pdf (used by the chapter).
"""
from pathlib import Path
from html import escape
import subprocess
ROOT = Path(__file__).resolve().parent
INK = '#18344b'; GRAY = '#546573'; ACCENT = '#3886ad'; RED = '#b33e44'


class Figure:
    def __init__(self, w=1120, h=455):
        self.w, self.h = w, h
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>'
                      + ''.join(f'<marker id="arrow-{n}" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="14" refY="9" orient="auto"><path d="M2,2 L18,9 L2,16 Z" fill="{c}"/></marker>' for n, c in [('blue', ACCENT), ('red', RED)])
                      + f'</defs><rect width="{w}" height="{h}" fill="white"/>']

    def text(self, x, y, value, size=22, color=INK, weight=400, anchor='middle'):
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')

    # Card: soft shadow, light border, left accent bar, bold title and grey description.
    def card(self, x, y, w, h, title, sub, failed=False):
        accent = RED if failed else ACCENT
        fill, line = ('#fdf3f3', '#e3b9bc') if failed else ('#f8fbfd', '#c6dbe8')
        inset = min(28, h * .28)
        self.parts.append(f'<rect x="{x+1}" y="{y+5}" width="{w-2}" height="{h}" rx="16" fill="#24445c" opacity=".035"/>'
                          f'<rect x="{x}" y="{y+2}" width="{w}" height="{h}" rx="16" fill="#24445c" opacity=".025"/>'
                          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{line}" stroke-width="1.2"/>'
                          f'<rect x="{x+12}" y="{y+inset}" width="7" height="{h-2*inset}" rx="3.5" fill="{accent}"/>')
        # Keep labels clear of the accent bar and border: shrink long labels (approximate Arial widths).
        room = w - 60
        ts = min(23, room / (len(title) * .56)); ss = min(19, room / (len(sub) * .47))
        cx = x + w / 2 + 8
        self.text(cx, y + h / 2 - 4, title, round(ts, 1), INK, 600)
        self.text(cx, y + h / 2 + 26, sub, round(ss, 1), RED if failed else GRAY, 600 if failed else 400)

    def arrow(self, points, failed=False):
        path = 'M ' + ' L '.join(f'{x} {y}' for x, y in points)
        color, marker = (RED, 'red') if failed else (ACCENT, 'blue')
        dash = ' stroke-dasharray="9 7"' if failed else ''
        self.parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"{dash} marker-end="url(#arrow-{marker})"/>')

    def save(self, name):
        p = ROOT / f'{name}.svg'
        p.write_text(''.join(self.parts) + '</svg>')
        subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', str(p.with_suffix('.pdf')), str(p)], check=True)


for lang, suffix in [('hr', '.hr'), ('en', '')]:
    def tr(hr, en):
        return hr if lang == 'hr' else en
    for failed in [False, True]:
        # The failure variant omits the arrow legend: the system map introduces it first.
        f = Figure(h=392 if failed else 455)
        f.card(10, 150, 240, 104, tr('Preglednik', 'Student browser'), tr('vlastito lokalno stanje', 'own local state'))
        f.card(372, 150, 270, 104, tr('Usluga predaje', 'Submission service'), tr('provjerava i prihvaća', 'checks and accepts'))
        f.card(835, 20, 275, 104, tr('Usluga zadataka', 'Assignment service'), tr('nedostupna', 'unavailable') if failed else tr('rokovi i pravila datoteka', 'deadlines and file rules'), failed)
        f.card(835, 270, 275, 104, tr('Pohrana predaja', 'Submission storage'), tr('datoteke i zapisi', 'files and records'))
        # Arrows point from caller to the component it needs; labels name the request.
        f.arrow([(254, 202), (368, 202)]); f.text(311, 186, tr('predaj projekt', 'submit project'), 18)
        f.arrow([(646, 180), (690, 180), (690, 72), (831, 72)], failed); f.text(760, 56, tr('provjeri pravila', 'check rules'), 18, RED if failed else INK)
        f.arrow([(646, 224), (690, 224), (690, 322), (831, 322)]); f.text(760, 306, tr('pohrani projekt', 'store project'), 18)
        if failed:
            f.text(972, 194, tr('Ostali procesi', 'Other processes'), 20, GRAY); f.text(972, 220, tr('i dalje rade.', 'can still run.'), 20, GRAY)
        if not failed:
            f.text(560, 414, tr('Strelica: pozivatelj → potrebna komponenta. Oznaka: zahtjev. Odgovori su izostavljeni.', 'Arrow: caller → component it needs. Label: request. Replies are omitted.'), 18, GRAY)
            f.text(560, 440, tr('Okviri su logički procesi, ne zadani broj računala.', 'Boxes show logical processes, not a fixed number of machines.'), 18, GRAY)
        f.save(('partial-failure' if failed else 'system-map') + suffix)
