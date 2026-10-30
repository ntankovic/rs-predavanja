"""Lecture 02 diagrams, Croatian first, in the Lecture 01 card style (2026-10-27).

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
                      + ''.join(f'<marker id="arrow-{n}" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="14" refY="9" orient="auto"><path d="M2,2 L18,9 L2,16 Z" fill="{c}"/></marker>' for n, c in [('blue', ACCENT), ('red', RED), ('orange', ORANGE), ('gray', GRAY)])
                      + f'</defs><rect width="{w}" height="{h}" fill="white"/>']

    def text(self, x, y, value, size=22, color=INK, weight=400, anchor='middle'):
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')

    # Card: soft shadow, light border, left accent bar, bold title and grey description.
    def card(self, x, y, w, h, title, sub='', accent=ACCENT, failed=False):
        if failed:
            accent = RED
        fill, line = ('#fdf3f3', '#e3b9bc') if failed else ('#f8fbfd', '#c6dbe8')
        inset = min(22, h * .25)
        self.parts.append(f'<rect x="{x+1}" y="{y+5}" width="{w-2}" height="{h}" rx="14" fill="#24445c" opacity=".035"/>'
                          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{line}" stroke-width="1.2"/>'
                          f'<rect x="{x+10}" y="{y+inset}" width="6" height="{h-2*inset}" rx="3" fill="{accent}"/>')
        # Keep labels clear of the accent bar and border: shrink long labels (approximate Arial widths).
        room = w - 50
        ts = min(22, room / (max(len(title), 1) * .56))
        cx = x + w / 2 + 7
        if sub:
            ss = min(18, room / (len(sub) * .48))
            self.text(cx, y + h / 2 - 4, title, round(ts, 1), INK, 600)
            self.text(cx, y + h / 2 + 22, sub, round(ss, 1), RED if failed else GRAY)
        else:
            self.text(cx, y + h / 2 + 8, title, round(ts, 1), INK, 600)

    # Dashed region: a process, container, machine or data centre.
    def region(self, x, y, w, h, label, color=GRAY, fill='none', size=18, dash=True):
        d = ' stroke-dasharray="8 6"' if dash else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{color}" stroke-width="2"{d}/>')
        if label:
            self.text(x + 14, y + 26, label, size, color, 600, 'start')

    def arrow(self, points, color='blue', dash=False, width=3):
        path = 'M ' + ' L '.join(f'{x} {y}' for x, y in points)
        stroke = {'blue': ACCENT, 'red': RED, 'orange': ORANGE, 'gray': GRAY}[color]
        d = ' stroke-dasharray="9 7"' if dash else ''
        self.parts.append(f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{d} marker-end="url(#arrow-{color})"/>')

    def line(self, x1, y1, x2, y2, color=GRAY, width=2, dash=False):
        d = ' stroke-dasharray="7 6"' if dash else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d}/>')

    def save(self, name):
        p = ROOT / f'{name}.hr.svg'
        p.write_text(''.join(self.parts) + '</svg>')
        subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', str(p.with_suffix('.pdf')), str(p)], check=True)


# 1. Monolith versus services for the same portal.
f = Figure(h=470)
f.text(270, 34, 'Monolit: jedan proces, jedno izdanje', 23, INK, 700)
f.text(840, 34, 'Usluge: zasebni procesi', 23, INK, 700)
f.region(20, 55, 500, 300, 'Proces portala', ACCENT, '#f3f9fc', dash=False)
for i, (t, s) in enumerate([('Prijava', 'korisnici'), ('Predaja', 'prima ZIP'), ('Rokovi', 'pravila zadatka'), ('Provjera', 'raspakira, skenira')]):
    f.card(45 + (i % 2) * 235, 100 + (i // 2) * 120, 215, 92, t, s, ORANGE if t == 'Provjera' else ACCENT)
f.text(270, 345, 'Moduli se pozivaju lokalno.', 17, GRAY)
f.card(150, 375, 240, 76, 'Zajednička baza', 'svi moduli')
f.arrow([(270, 357), (270, 371)], 'gray')
f.line(560, 50, 560, 450, '#c6dbe8', 2)
f.card(600, 70, 210, 86, 'Prijava', 'vlastiti podaci')
f.card(880, 70, 220, 86, 'Rokovi', 'vlastiti podaci')
f.card(600, 220, 210, 86, 'Predaja', 'vlastiti podaci')
f.card(880, 220, 220, 86, 'Provjera', '× 3 replike', ORANGE)
f.arrow([(705, 216), (705, 160)]); f.text(642, 192, 'tko je?', 16, INK, 400, 'start')
f.arrow([(814, 245), (876, 140)]); f.text(812, 184, 'rok?', 16, INK, 400, 'start')
f.arrow([(814, 275), (876, 275)], 'orange', True); f.text(845, 300, 'posao', 16, ORANGE)
f.text(850, 360, 'Svaki poziv između usluga je poruka preko mreže.', 17, GRAY)
f.text(850, 388, 'Puna strelica: sinkroni zahtjev i odgovor.', 17, GRAY)
f.text(850, 414, 'Isprekidana: asinkrona poruka (posao u redu).', 17, ORANGE)
f.save('monolith-services')

# 2. Logical layers and two placements.
f = Figure(h=430)
f.text(190, 34, 'Logički slojevi', 23, INK, 700)
for i, (t, s) in enumerate([('Korisničko sučelje', 'preglednik, obrasci'), ('Aplikacijska logika', 'pravila predaje, rokovi'), ('Podaci', 'zapisi i datoteke')]):
    f.card(40, 60 + i * 120, 300, 92, t, s)
    if i:
        f.arrow([(190, 60 + i * 120 - 26), (190, 60 + i * 120 - 4)])
f.line(380, 50, 380, 410, '#c6dbe8', 2)
f.text(560, 34, 'Smještaj A: dva računala', 21, INK, 700)
f.region(420, 60, 290, 92, 'Računalo studenta', GRAY)
f.text(565, 125, 'sučelje', 19, INK, 600)
f.region(420, 180, 290, 212, 'Poslužitelj', GRAY)
f.text(565, 252, 'logika', 19, INK, 600); f.text(565, 300, '+', 22, GRAY); f.text(565, 348, 'podaci', 19, INK, 600)
f.arrow([(565, 154), (565, 178)])
f.text(920, 34, 'Smještaj B: tri računala', 21, INK, 700)
f.region(775, 60, 300, 92, 'Računalo studenta', GRAY)
f.text(925, 125, 'sučelje', 19, INK, 600)
f.region(775, 180, 300, 92, 'Aplikacijski poslužitelj', GRAY)
f.text(925, 245, 'logika', 19, INK, 600)
f.region(775, 300, 300, 92, 'Poslužitelj baze', GRAY)
f.text(925, 365, 'podaci', 19, INK, 600)
f.arrow([(925, 154), (925, 178)]); f.arrow([(925, 274), (925, 298)])
f.text(560, 420, 'Isti slojevi, različit broj mrežnih prijelaza i ispada.', 17, GRAY)
f.save('tiers')

# 3. Vertical versus horizontal distribution.
f = Figure(h=430)
f.text(270, 34, 'Vertikalno: po funkciji', 23, INK, 700)
f.text(840, 34, 'Horizontalno: replike iste funkcije', 23, INK, 700)
for i, (t, s) in enumerate([('Sučelje', 'računalo 1'), ('Usluga predaje', 'računalo 2'), ('Baza', 'računalo 3')]):
    f.card(140, 60 + i * 120, 260, 88, t, s)
    if i:
        f.arrow([(270, 60 + i * 120 - 30), (270, 60 + i * 120 - 4)])
f.line(560, 50, 560, 410, '#c6dbe8', 2)
f.card(700, 60, 280, 80, 'Raspoređivač opterećenja', 'load balancer')
for i in range(3):
    x = 610 + i * 165
    f.card(x, 220, 150, 88, 'Predaja', f'replika {i + 1}')
    f.arrow([(840, 144), (x + 75, 216)])
f.text(840, 350, 'Svaka replika obrađuje dio zahtjeva.', 18, GRAY)
f.text(840, 376, 'Replike moraju dijeliti ili uskladiti stanje.', 18, GRAY)
f.text(270, 420, 'Strelica: pozivatelj → komponenta koju treba.', 17, GRAY)
f.save('vertical-horizontal')

# 4. Cost of a synchronous call chain.
f = Figure(h=400)
names = [('Preglednik', ''), ('Usluga predaje', '99,9 %'), ('Usluga zadataka', '99,9 %'), ('Usluga korisnika', '99,9 %')]
for i, (t, s) in enumerate(names):
    x = 20 + i * 280
    f.card(x, 60, 240, 96, t, s or 'klijent')
    if i:
        f.arrow([(x - 36, 108), (x - 4, 108)])
f.text(560, 36, 'Jedna predaja treba odgovor sve tri usluge.', 21, INK, 700)
f.region(60, 200, 1000, 180, '', '#c6dbe8', '#f8fbfd', dash=False)
f.text(90, 240, 'Dostupnost lanca (uz neovisne ispade):', 21, INK, 700, 'start')
f.text(90, 276, '0,999 × 0,999 × 0,999 ≈ 0,997  →  oko 26 sati nedostupnosti godišnje umjesto oko 9', 21, INK, 400, 'start')
f.text(90, 322, 'Latencija lanca:', 21, INK, 700, 'start')
f.text(90, 356, 'vremena odgovora zbrajaju se, a ispad bilo koje usluge zaustavlja predaju', 21, INK, 400, 'start')
f.save('call-chain')

# 5. Client-server distribution versus BitTorrent-style peers.
f = Figure(h=440)
f.text(270, 34, 'Klijent–poslužitelj', 23, INK, 700)
f.text(840, 34, 'P2P uz tracker (BitTorrent)', 23, INK, 700)
f.card(170, 170, 200, 86, 'Poslužitelj', 'šalje cijelu datoteku')
for (x, y) in [(20, 60), (360, 60), (20, 320), (360, 320)]:
    f.card(x, y, 160, 70, 'Klijent', '')
f.arrow([(220, 168), (130, 132)]); f.arrow([(320, 168), (410, 132)])
f.arrow([(220, 258), (130, 318)]); f.arrow([(320, 258), (410, 318)])
f.line(560, 50, 560, 420, '#c6dbe8', 2)
f.card(740, 56, 200, 76, 'Tracker', 'tko ima datoteku?', GRAY)
peers = [(620, 190), (900, 190), (620, 330), (900, 330)]
for i, (x, y) in enumerate(peers):
    f.card(x, y, 180, 76, f'Sudionik {i + 1}', 'ima neke dijelove')
f.line(800, 228, 900, 228, ACCENT, 3); f.line(710, 266, 710, 330, ACCENT, 3)
f.line(990, 266, 990, 330, ACCENT, 3); f.line(800, 368, 900, 368, ACCENT, 3)
f.line(800, 266, 900, 330, ACCENT, 3)
for (x, y) in [(710, 190), (990, 190)]:
    f.line(840, 134, x, y, GRAY, 2, True)
f.text(840, 425, 'Pune crte: razmjena dijelova. Isprekidane: popis sudionika.', 16, GRAY)
f.text(270, 425, 'Strelica: tko kome šalje podatke.', 16, GRAY)
f.save('client-server-p2p')

# 6. Spark-style cluster: one coordinator, many executor processes.
f = Figure(h=400)
f.card(40, 150, 250, 100, 'Driver', 'dijeli posao na zadatke')
f.card(420, 30, 280, 90, 'Upravitelj klastera', 'dodjeljuje resurse', GRAY)
for i in range(3):
    x = 380 + i * 250
    f.card(x, 250, 230, 100, f'Executor {i + 1}', 'proces na čvoru')
    f.arrow([(290, 190 + i * 22), (x + 40, 246)])
f.arrow([(290, 170), (416, 85)], 'gray', True)
f.text(560, 385, 'Driver šalje zadatke executorima i skuplja rezultate. Executori su procesi na računalima klastera.', 17, GRAY)
f.text(372, 150, 'traži resurse', 16, GRAY, 400, 'start')
f.save('cluster-driver')

# 7. Nested deployment boundaries.
f = Figure(h=470)
f.region(20, 20, 700, 430, 'Podatkovni centar (zona)', GRAY, '#fbfcfd')
f.region(50, 70, 640, 250, 'Računalo (čvor)', ACCENT, '#f3f9fc')
f.region(80, 120, 280, 180, 'Kontejner', ORANGE)
f.card(105, 170, 230, 100, 'Proces', 'dretve dijele memoriju')
f.region(385, 120, 280, 180, 'Kontejner', ORANGE)
f.card(410, 170, 230, 100, 'Proces', 'druga usluga')
f.region(50, 345, 640, 85, 'Drugo računalo', ACCENT, '#f3f9fc')
f.text(370, 410, 'replika na drugom čvoru', 17, GRAY)
rows = [('Proces', 'zajednička memorija; lokalni poziv'), ('Kontejner', 'izolirani procesi; isto računalo'),
        ('Računalo', 'struja, disk, jezgra OS-a'), ('Podatkovni centar', 'mreža, napajanje, hlađenje')]
f.text(760, 50, 'Što dijeli ispad unutar granice?', 20, INK, 700, 'start')
for i, (a, b) in enumerate(rows):
    f.text(760, 100 + i * 70, a, 19, INK, 700, 'start')
    f.text(760, 126 + i * 70, b, 17, GRAY, 400, 'start')
f.arrow([(1090, 90), (1090, 360)], 'gray')
f.text(930, 400, 'Što je granica šira:', 17, GRAY); f.text(930, 424, 'neovisniji ispadi, skuplja komunikacija', 17, GRAY)
f.save('deployment-boundaries')

# 8. Same services, two deployments: Compose on one host, Swarm on three nodes.
f = Figure(h=430)
f.text(260, 34, 'Docker Compose: jedno računalo', 22, INK, 700)
f.text(830, 34, 'Docker Swarm: tri čvora', 22, INK, 700)
f.region(20, 55, 480, 350, 'Računalo', ACCENT, '#f3f9fc')
for i, (t, s) in enumerate([('predaja', ''), ('provjera', '× 3'), ('baza', '')]):
    f.card(60, 95 + i * 100, 400, 78, t, s or 'kontejner', ORANGE if t == 'provjera' else ACCENT)
f.line(550, 50, 550, 410, '#c6dbe8', 2)
cols = [['predaja', 'provjera'], ['provjera', 'baza'], ['predaja', 'provjera']]
for i, items in enumerate(cols):
    x = 580 + i * 180
    f.region(x, 55, 165, 300, f'Čvor {i + 1}', ACCENT, '#f3f9fc')
    for j, t in enumerate(items):
        f.card(x + 10, 100 + j * 110, 145, 80, t, 'kontejner', ORANGE if t == 'provjera' else ACCENT)
f.text(260, 425, 'Ispad računala zaustavlja sve.', 17, RED)
f.text(830, 395, 'Ispad jednog čvora: ostale replike rade.', 17, GREEN)
f.text(830, 421, 'Ali baza je i dalje samo na čvoru 2.', 17, RED)
f.save('compose-swarm')
