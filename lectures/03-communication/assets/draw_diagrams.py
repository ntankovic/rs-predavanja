"""Lecture 03 diagrams, Croatian first, in the Lecture 01/02 card style (2026-11-09).

Writes <name>.hr.svg and <name>.hr.pdf. English variants follow after Croatian review.
Requires rsvg-convert.
"""
from pathlib import Path
from html import escape
import subprocess
ROOT = Path(__file__).resolve().parent
INK = '#18344b'; GRAY = '#546573'; ACCENT = '#3886ad'; RED = '#b33e44'; ORANGE = '#b56a21'; GREEN = '#3d7f4f'


class Figure:
    def __init__(self, w=1120, h=455):
        self.w, self.h = w, h
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>'
                      + ''.join(f'<marker id="arrow-{n}" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="14" refY="9" orient="auto"><path d="M2,2 L18,9 L2,16 Z" fill="{c}"/></marker>' for n, c in [('blue', ACCENT), ('red', RED), ('orange', ORANGE), ('gray', GRAY), ('green', GREEN)])
                      + f'</defs><rect width="{w}" height="{h}" fill="white"/>']

    def text(self, x, y, value, size=22, color=INK, weight=400, anchor='middle'):
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')

    # Card: soft shadow, light border, left accent bar, bold title and grey description.
    def card(self, x, y, w, h, title, sub='', accent=ACCENT, failed=False, ok=False):
        if failed:
            accent = RED
        if ok:
            accent = GREEN
        fill, line = ('#fdf3f3', '#e3b9bc') if failed else (('#f1f8f3', '#b9d8c2') if ok else ('#f8fbfd', '#c6dbe8'))
        inset = min(22, h * .25)
        self.parts.append(f'<rect x="{x+1}" y="{y+5}" width="{w-2}" height="{h}" rx="14" fill="#24445c" opacity=".035"/>'
                          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{line}" stroke-width="1.2"/>'
                          f'<rect x="{x+10}" y="{y+inset}" width="6" height="{h-2*inset}" rx="3" fill="{accent}"/>')
        room = w - 50
        ts = min(21, room / (max(len(title), 1) * .56))
        cx = x + w / 2 + 7
        if sub:
            ss = min(17, room / (len(sub) * .48))
            self.text(cx, y + h / 2 - 4, title, round(ts, 1), INK, 600)
            self.text(cx, y + h / 2 + 21, sub, round(ss, 1), RED if failed else (GREEN if ok else GRAY))
        else:
            self.text(cx, y + h / 2 + 7, title, round(ts, 1), INK, 600)

    def region(self, x, y, w, h, label, color=GRAY, fill='none', size=18, dash=True):
        d = ' stroke-dasharray="8 6"' if dash else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{color}" stroke-width="2"{d}/>')
        if label:
            self.text(x + 14, y + 26, label, size, color, 600, 'start')

    def arrow(self, points, color='blue', dash=False, width=3):
        path = 'M ' + ' L '.join(f'{x} {y}' for x, y in points)
        stroke = {'blue': ACCENT, 'red': RED, 'orange': ORANGE, 'gray': GRAY, 'green': GREEN}[color]
        d = ' stroke-dasharray="9 7"' if dash else ''
        self.parts.append(f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{d} marker-end="url(#arrow-{color})"/>')

    def line(self, x1, y1, x2, y2, color=GRAY, width=2, dash=False):
        d = ' stroke-dasharray="7 6"' if dash else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d}/>')

    def rect(self, x, y, w, h, fill, stroke='none', rx=6):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')

    def save(self, name):
        p = ROOT / f'{name}.hr.svg'
        p.write_text(''.join(self.parts) + '</svg>')
        subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', str(p.with_suffix('.pdf')), str(p)], check=True)


# 1. One RPC through client and server stubs (adapted from Kleppmann, dist-sys-notes, slide 16).
f = Figure(h=590)
lanes = [(150, 'Portal', 'kod koji poziva'), (420, 'RPC klijent', 'generirani stub'),
         (700, 'RPC poslužitelj', 'generirani kod'), (970, 'Usluga predaje', 'implementacija')]
f.parts.append('<rect x="505" y="92" width="140" height="440" fill="#fff6ea"/>')
f.text(575, 552, 'mreža', 17, ORANGE, 700)
for x, t, s in lanes:
    f.card(x - 120, 14, 240, 70, t, s)
    f.line(x, 86, x, 536, '#c6dbe8', 2, True)
# Caller waits for the whole round trip.
f.rect(143, 116, 14, 400, '#d7e8f2')
f.text(132, 310, 'čeka', 16, GRAY, 400, 'end')


def msg(x1, x2, y, label, color='blue', size=16):
    f.arrow([(x1 + (8 if x2 > x1 else -8), y), (x2 - (10 if x2 > x1 else -10), y)], color)
    f.text((x1 + x2) / 2, y - 9, label, size, INK if color == 'blue' else ORANGE, 600)


def step(x, y, label):
    f.rect(x - 92, y - 17, 184, 30, '#edf7fc', '#a3c9dc', 8)
    f.text(x, y + 4, label, 15, INK)


msg(150, 420, 116, 'SnimiPredaju(zahtjev)')
step(420, 152, 'serijalizira argumente')
msg(420, 700, 198, 'm1: zahtjev u bajtovima', 'orange')
step(700, 232, 'deserijalizira')
msg(700, 970, 276, 'poziva funkciju')
f.rect(963, 288, 14, 54, ACCENT)
f.text(990, 322, 'snima', 16, GRAY, 400, 'start')
msg(970, 700, 366, 'rezultat')
step(700, 400, 'serijalizira rezultat')
msg(700, 420, 446, 'm2: odgovor u bajtovima', 'orange')
step(420, 480, 'deserijalizira')
msg(420, 150, 516, 'vraća odgovor')
f.text(560, 582, 'Vrijeme teče prema dolje. Pozivatelj vidi samo poziv i povrat; sve između radi RPC okvir.', 17, GRAY)
f.save('rpc-flow')

# 2. Deadline propagation: the same absolute deadline versus a fresh timeout at every hop.
f = Figure(h=430)
names = [('Preglednik', 'čeka do 5 s'), ('Portal', ''), ('Usluga predaje', ''), ('Pohrana datoteka', '')]
f.text(20, 34, 'Bez prijenosa roka: svaka usluga bira svoj istek čekanja', 21, RED, 700, 'start')
for i, (t, s) in enumerate(names):
    x = 20 + i * 280
    f.card(x, 50, 240, 84, t, s if i == 0 else 'čeka 5 s', failed=(i == 3))
    if i:
        f.arrow([(x - 36, 92), (x - 4, 92)])
f.text(20, 166, 'Preglednik odustane nakon 5 s, a usluge iza njega i dalje čekaju i rade posao koji nitko više ne čeka.', 18, INK, 400, 'start')
f.line(20, 190, 1100, 190, '#c6dbe8', 2)
f.text(20, 228, 'S prijenosom roka: svi pozivi dijele isti apsolutni rok 10:00:05,000', 21, GREEN, 700, 'start')
rem = ['preostalo 5,0 s', 'preostalo 4,6 s', 'preostalo 4,1 s', 'preostalo 3,7 s']
for i, (t, s) in enumerate(names):
    x = 20 + i * 280
    f.card(x, 246, 240, 84, t, rem[i], ok=True)
    if i:
        f.arrow([(x - 36, 288), (x - 4, 288)], 'green')
f.text(20, 364, 'Svaki skok troši dio vremena. Usluga koja vidi da je rok prošao ne započinje posao.', 18, INK, 400, 'start')
f.text(20, 400, 'Primjer: zahtjev je krenuo u 10:00:00,000 s rokom od 5 s. Vremena su ilustrativna.', 16, GRAY, 400, 'start')
f.save('deadline-chain')

# 3. Retries multiply across layers (Google SRE book, ch. 22: 4^3 = 64 attempts).
f = Figure(h=340)
layers = [('JavaScript', 'do 4 pokušaja'), ('Frontend', 'do 4 × 4 = 16'), ('Backend', 'do 4 × 16 = 64'), ('Baza', 'do 64 pokušaja')]
f.text(560, 34, 'Svaki sloj ponavlja do 3 puta (4 pokušaja) i ne zna za ostale.', 21, INK, 700)
for i, (t, s) in enumerate(layers):
    x = 20 + i * 280
    f.card(x, 70, 240, 100, t, s, failed=(i == 3))
    if i:
        f.arrow([(x - 36, 120), (x - 4, 120)], 'red' if i == 3 else 'blue')
f.region(60, 210, 1000, 110, '', '#c6dbe8', '#f8fbfd', dash=False)
f.text(90, 250, 'Jedna radnja korisnika: do 4 × 4 × 4 = 64 pokušaja na bazi.', 21, INK, 700, 'start')
f.text(90, 290, 'Baza je preopterećena upravo onda kad bi trebala odgovoriti. Ponavljajte na jednom mjestu.', 19, INK, 400, 'start')
f.save('retry-multiply')

# 4. Idempotency key and effect in one transaction versus two separate steps.
f = Figure(h=500)
f.text(270, 34, 'Loše: učinak i ključ u dva koraka', 22, RED, 700)
f.text(840, 34, 'Dobro: učinak i ključ u jednoj transakciji', 22, GREEN, 700)
f.card(60, 60, 420, 70, '1. Snimi predaju', 'zapis #1')
f.card(60, 150, 420, 70, '⚡ Rušenje usluge', 'prije sljedećeg koraka', failed=True)
f.card(60, 240, 420, 70, '2. Spremi ključ K i odgovor', 'nikad se ne izvrši', ORANGE)
f.arrow([(270, 132), (270, 147)], 'gray'); f.arrow([(270, 222), (270, 237)], 'gray', True)
f.card(60, 360, 420, 90, 'Ponovni pokušaj s ključem K', 'K nepoznat → zapis #2, duplikat', failed=True)
f.line(560, 50, 560, 470, '#c6dbe8', 2)
f.region(620, 56, 440, 210, 'jedna transakcija: sve ili ništa', GREEN, '#f1f8f3')
f.card(640, 96, 400, 62, 'Spremi ključ K', '')
f.card(640, 180, 400, 62, 'Snimi predaju i spremi odgovor', '')
f.card(620, 280, 440, 62, '⚡ Rušenje prije slanja odgovora', '', failed=True)
f.card(620, 360, 440, 90, 'Ponovni pokušaj s ključem K', 'K postoji → isti spremljeni odgovor', ok=True)
f.arrow([(840, 268), (840, 277)], 'gray'); f.arrow([(840, 344), (840, 357)], 'gray')
f.text(560, 488, 'Rušenje usred transakcije poništava sve; ponovni pokušaj tada radi ispočetka.', 17, GRAY)
f.save('idempotency-atomic')
