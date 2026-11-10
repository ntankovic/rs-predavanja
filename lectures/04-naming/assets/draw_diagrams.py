"""Lecture 04 diagrams, Croatian first, in the Lecture 01-03 card style (2026-11-09).

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



# 1. One logical name, several changing addresses; an instance identifier names one process.
f = Figure(h=420)
f.card(30, 150, 250, 100, 'predaja', 'ime usluge')
f.text(330, 62, 'razrješavanje imena', 18, ACCENT, 700)
addrs = [('10.0.1.17:50051', 'instanca a3f9', False), ('10.0.2.31:50051', 'instanca 7c02', False), ('10.0.3.5:50051', 'instanca e51b', True)]
for i, (a, s, failed) in enumerate(addrs):
    y = 40 + i * 120
    f.card(520, y, 330, 90, a, s, failed=failed)
    f.arrow([(284, 200), (510, y + 45)])
f.text(990, 82, 'adresa: gdje je', 18, INK, 700); f.text(990, 106, 'instanca sada', 18, INK, 700)
f.text(990, 330, 'srušena ili', 17, RED); f.text(990, 352, 'premještena', 17, RED)
f.text(560, 405, 'Ime ostaje isto; skup adresa iza njega mijenja se pri skaliranju, premještanju i ispadu.', 17, GRAY)
f.save('name-address')

# 2. DNS name space as a tree and an iterative lookup by a resolver (names illustrative).
f = Figure(h=470)
f.text(250, 34, 'Prostor imena je stablo', 22, INK, 700)
f.card(170, 60, 160, 64, '.', 'korijen')
f.card(30, 170, 140, 64, 'com', '')
f.card(190, 170, 120, 64, 'hr', '')
f.card(330, 170, 140, 64, 'org', '')
f.card(160, 280, 180, 64, 'unipu.hr', '')
f.card(130, 390, 240, 64, 'portal.unipu.hr', 'ilustrativno')
for x in (100, 250, 400):
    f.arrow([(250, 126), (x, 166)], 'gray')
f.arrow([(250, 236), (250, 276)], 'gray'); f.arrow([(250, 346), (250, 386)], 'gray')
f.line(560, 40, 560, 460, '#c6dbe8', 2)
f.text(840, 34, 'Razrješavanje: tko zna adresu?', 22, INK, 700)
f.card(600, 60, 210, 70, 'Klijent', 'portal.unipu.hr?')
f.card(840, 60, 260, 70, 'Resolver', 'predmemorija (cache) + upiti')
f.arrow([(814, 95), (836, 95)])
steps = [('1. korijen', 'uputi na .hr'), ('2. poslužitelj .hr', 'uputi na unipu.hr'), ('3. poslužitelj unipu.hr', 'adresa i TTL')]
for i, (t, s) in enumerate(steps):
    y = 170 + i * 92
    f.card(830, y, 270, 72, t, s, ACCENT if i < 2 else GREEN)
    f.arrow([(965, y - 18), (965, y - 4)], 'gray')
f.text(700, 290, 'Resolver pita redom,', 17, GRAY); f.text(700, 314, 'a odgovor sprema', 17, GRAY); f.text(700, 338, 'u predmemoriju', 17, GRAY); f.text(700, 362, 'do isteka TTL-a.', 17, GRAY)
f.text(840, 458, 'Imena i koraci su ilustrativni; adresa se ne izmišlja nego čita iz zapisa.', 15, GRAY)
f.save('dns-tree')

# 3. A cached address goes stale when the service moves before the TTL expires.
f = Figure(h=360)
X0, X1 = 140, 1080
def tx(t): return X0 + (X1 - X0) * t / 60
f.text(20, 40, 'Klijent', 19, INK, 700, 'start')
f.text(20, 140, 'DNS', 19, INK, 700, 'start')
f.line(X0, 60, X1, 60, '#c6dbe8', 3); f.line(X0, 150, X1, 150, '#c6dbe8', 3)
f.rect(tx(0), 72, tx(15) - tx(0), 22, '#d7eedd'); f.rect(tx(15), 72, tx(30) - tx(15), 22, '#f6d6d8'); f.rect(tx(30), 72, tx(60) - tx(30), 22, '#d7eedd')
f.text(tx(7.5), 88, 'stara adresa radi', 15, GREEN, 700)
f.text(tx(22.5), 88, 'stara adresa: pozivi padaju', 15, RED, 700)
f.text(tx(45), 88, 'nova adresa iz DNS-a', 15, GREEN, 700)
f.rect(tx(0), 160, tx(15) - tx(0), 22, '#edf7fc'); f.rect(tx(15), 160, tx(60) - tx(15), 22, '#e7f3fb')
f.text(tx(7.5), 176, '10.0.1.17', 15, INK, 600); f.text(tx(37.5), 176, '10.0.2.31 (nova adresa odmah u DNS-u)', 15, INK, 600)
for t, lab in [(0, 'upit, TTL 30 s'), (30, 'TTL istekao: novi upit')]:
    f.arrow([(tx(t) + 2, 140), (tx(t) + 2, 66)], 'blue')
    f.text(tx(t) + 8, 125, lab, 15, ACCENT, 700, 'start')
f.line(tx(15), 40, tx(15), 200, RED, 3, True)
f.text(tx(15), 222, 'usluga premještena', 16, RED, 700)
for t in range(0, 61, 10):
    f.line(tx(t), 240, tx(t), 248, GRAY, 2); f.text(tx(t), 268, f'{t} s', 14, GRAY)
f.text(560, 310, 'Zastarjelost traje do isteka TTL-a: najviše TTL nakon premještanja.', 19, INK, 700)
f.text(560, 340, 'Kraći TTL: kraće zastarjeli zapisi, ali više upita DNS-u. Vremena su ilustrativna.', 17, GRAY)
f.save('ttl-stale')

# 4. Client-side vs server-side discovery (patterns as named by C. Richardson, microservices.io).
f = Figure(h=470)
f.text(270, 34, 'Otkrivanje na klijentu', 22, INK, 700)
f.text(840, 34, 'Otkrivanje preko usmjernika', 22, INK, 700)
f.card(30, 70, 200, 80, 'Portal', 'klijent')
f.card(300, 70, 230, 80, 'Registar usluga', 'ime → adrese', GRAY)
f.arrow([(234, 100), (296, 100)]); f.text(265, 92, '1. upit', 15, INK, 600)
f.arrow([(296, 128), (234, 128)], 'gray', True); f.text(265, 146, 'adrese', 15, GRAY)
for i in range(3):
    y = 200 + i * 85
    f.card(300, y, 230, 70, f'predaja {i + 1}', 'instanca')
    f.arrow([(130, 154), (130, y + 35), (296, y + 35)] if i == 0 else [(130, y + 35), (296, y + 35)])
f.line(130, 154, 130, 405, ACCENT, 3)
f.text(30, 440, '2. Portal sam bira instancu i poziva je.', 16, GRAY, 400, 'start')
f.line(560, 50, 560, 460, '#c6dbe8', 2)
f.card(600, 70, 190, 80, 'Portal', 'zna samo usmjernik')
f.card(840, 70, 240, 80, 'Usmjernik', 'load balancer')
f.arrow([(794, 110), (836, 110)])
f.card(600, 200, 200, 70, 'Registar usluga', 'ime → adrese', GRAY)
f.arrow([(804, 222), (846, 156)], 'gray', True)
f.text(790, 186, 'adrese', 15, GRAY, 400, 'end')
f.line(870, 154, 870, 368, ACCENT, 3)
for i in range(3):
    y = 190 + i * 72
    f.card(895, y, 185, 58, f'predaja {i + 1}', '')
    f.arrow([(870, y + 29), (891, y + 29)])
f.text(600, 440, 'Usmjernik na poznatoj adresi bira instancu umjesto portala.', 16, GRAY, 400, 'start')
f.save('discovery-modes')

# 5. Lease: an instance renews every 2 s; the registry keeps it until 6 s after the last renewal.
f = Figure(h=380)
X0, X1 = 170, 1080
def lx(t): return X0 + (X1 - X0) * t / 24
f.text(20, 70, 'Instanca', 19, INK, 700, 'start')
f.text(20, 190, 'Registar', 19, INK, 700, 'start')
f.line(X0, 64, X1, 64, '#c6dbe8', 3); f.line(X0, 184, X1, 184, '#c6dbe8', 3)
f.rect(lx(0), 52, lx(9) - lx(0), 24, '#d7eedd'); f.text(lx(4.5), 70, 'radi', 15, GREEN, 700)
f.text(lx(9) + 8, 70, '⚡ srušena u 9 s', 16, RED, 700, 'start')
for t in range(0, 9, 2):
    f.arrow([(lx(t), 80), (lx(t), 176)], 'green')
f.text(lx(9.3), 132, 'obnova najma', 15, GREEN, 700, 'start')
f.rect(lx(0), 196, lx(9) - lx(0), 24, '#d7eedd'); f.text(lx(4.5), 214, 'u registru', 15, GREEN, 700)
f.rect(lx(9), 196, lx(14) - lx(9), 24, '#f6d6d8'); f.text(lx(11.5), 214, 'u registru, ne radi', 15, RED, 700)
f.rect(lx(14), 196, lx(24) - lx(14), 24, '#eef1f3'); f.text(lx(19), 214, 'uklonjena', 15, GRAY, 700)
f.line(lx(14), 40, lx(14), 240, RED, 2, True)
f.text(lx(14) + 8, 254, 'najam istekao: 8 s + TTL 6 s', 16, RED, 700, 'start')
for t in range(0, 25, 2):
    f.line(lx(t), 270, lx(t), 278, GRAY, 2); f.text(lx(t), 298, f'{t} s', 14, GRAY)
f.text(560, 336, 'Srušena instanca ostaje u registru najviše TTL nakon posljednje obnove.', 19, INK, 700)
f.text(560, 364, 'Obnova svake 2 s, TTL 6 s. Vremena su ilustrativna.', 17, GRAY)
f.save('lease-timeline')

# 6. Docker Swarm: the manager keeps the desired state and places tasks (containers) on worker nodes.
def container(f, x, y, w, h, name, ip, state='ok'):
    fill, line, col = {'ok': ('#f8fbfd', ACCENT, INK), 'down': ('#fdf3f3', RED, RED), 'new': ('#f1f8f3', GREEN, GREEN)}[state]
    f.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{line}" stroke-width="2.2"/>')
    f.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="6" fill="{line}"/><rect x="{x}" y="{y + 12}" width="{w}" height="12" fill="{line}"/>')
    f.text(x + w / 2, y + 17, 'kontejner', 14, 'white', 700)
    # Container name in a fixed-width font on its own background, like code in the text.
    cw = len(name) * 11.4 + 18
    f.parts.append(f'<rect x="{x + w / 2 - cw / 2}" y="{y + 32}" width="{cw}" height="26" rx="5" fill="#e6edf3" stroke="#c3d2de"/>')
    f.parts.append(f'<text x="{x + w / 2}" y="{y + 51}" text-anchor="middle" font-family="Menlo, Consolas, \'DejaVu Sans Mono\', monospace" font-size="18" font-weight="700" fill="{INK}">{escape(name)}</text>')
    f.text(x + w / 2, y + 74, ip, 16, col, 600 if state != 'ok' else 400)


def swarm(failed):
    f = Figure(h=470)
    f.card(300, 16, 440, 84, 'Upravitelj (manager)', 'želimo: 3 kontejnera usluge predaja')
    if failed:
        f.card(770, 16, 330, 84, 'stvarno: 2 kontejnera', 'manje od željenog: pokreni novi', ORANGE)
    else:
        f.card(770, 16, 330, 84, 'stvarno: 3 kontejnera', 'jednako željenom: ništa', ok=True)
    f.line(520, 100, 520, 128, GRAY, 2, True)
    f.line(205, 128, 925, 128, GRAY, 2, True)
    nodes = [('Čvor 1', 'predaja.1', '10.0.1.17'), ('Čvor 2', 'predaja.2', '10.0.2.31'), ('Čvor 3', 'predaja.3', '10.0.3.5')]
    for i, (n, t, ip) in enumerate(nodes):
        x = 40 + i * 360
        down = failed and i == 1
        f.region(x, 150, 330, 270, n + ('  ✕ ispao' if down else ''), RED if down else ACCENT, '#fdf3f3' if down else '#f3f9fc')
        container(f, x + 60, 196, 210, 90, t, ip, 'down' if down else 'ok')
        f.arrow([(x + 165, 128), (x + 165, 146)], 'gray')
    if failed:
        container(f, 780, 310, 210, 90, 'predaja.2', '10.0.3.9 (nova)', 'new')
        f.arrow([(1050, 102), (1050, 330), (996, 350)], 'orange')
        f.text(560, 452, 'Novi kontejner na drugom čvoru, s novom adresom. Stara adresa više ne radi.', 17, INK, 600)
    else:
        f.text(560, 452, 'Upravitelj stalno uspoređuje stvarno stanje sa željenim i ispravlja razliku.', 17, GRAY)
    return f


swarm(False).save('swarm-overview')
swarm(True).save('swarm-reschedule')

# 8. etcd keys as a tree of prefixes; each instance key is attached to its own lease.
f = Figure(h=280)
mono = "Menlo, Consolas, 'DejaVu Sans Mono', monospace"
def key(x, y, label, color=INK, weight=700, bg='#e6edf3'):
    w = len(label) * 10.8 + 18
    f.parts.append(f'<rect x="{x}" y="{y - 19}" width="{w}" height="27" rx="5" fill="{bg}" stroke="#c3d2de"/>')
    f.parts.append(f'<text x="{x + 9}" y="{y}" font-family="{mono}" font-size="17" font-weight="{weight}" fill="{color}">{escape(label)}</text>')
    return x + w
f.region(52, 62, 690, 140, '', ACCENT, '#f3f9fc')
f.text(728, 86, 'get --prefix /usluge/predaja/', 16, ACCENT, 700, 'end')
key(20, 36, '/usluge/')
f.line(40, 44, 40, 236, GRAY, 2)
f.line(40, 90, 70, 90, GRAY, 2); key(74, 96, 'predaja/')
f.line(100, 104, 100, 172, GRAY, 2)
for y, (k, ip, lease) in zip((136, 178), [('a3f9', '10.0.1.17:50051', '694d'), ('7c02', '10.0.2.31:50051', '81e0')]):
    f.line(100, y - 6, 126, y - 6, GRAY, 2)
    end = key(130, y, f'{k}  {ip}', INK, 400, '#ffffff')
    f.text(end + 14, y, f'najam {lease}, TTL 10 s', 15, GREEN, 600, 'start')
f.line(40, 236, 70, 236, GRAY, 2); end = key(74, 242, 'rokovi/')
f.line(end + 4, 236, end + 26, 236, GRAY, 2)
end = key(end + 30, 242, 'b1d4  10.0.4.2:50052', INK, 400, '#ffffff')
f.text(end + 14, 242, 'najam 3c11, TTL 10 s', 15, GREEN, 600, 'start')
f.text(790, 110, 'Ključevi su putanje,', 17, INK, 600, 'start')
f.text(790, 136, 'kao datoteke u mapama.', 17, INK, 600, 'start')
f.text(790, 172, '„Grana” je zajednički prefiks.', 16, GRAY, 400, 'start')
f.text(790, 198, 'Istekne li najam, nestaje', 16, GRAY, 400, 'start')
f.text(790, 222, 'samo ključ vezan uz njega.', 16, GRAY, 400, 'start')
f.save('etcd-keys')

# 9. From code to containers: build an image, push it to an image registry, pull and run containers.
f = Figure(h=380)
mono = "Menlo, Consolas, 'DejaVu Sans Mono', monospace"
def mtext(x, y, value, size=15, color=INK, weight=400, anchor='start'):
    f.parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{mono}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')
# Code
f.parts.append(f'<rect x="16" y="90" width="184" height="170" rx="10" fill="#f8fbfd" stroke="#c6dbe8" stroke-width="1.5"/>')
f.text(108, 80, 'Kod', 19, INK, 700)
for i, line in enumerate(['Dockerfile', 'app.py', 'predaja.proto', 'requirements.txt']):
    f.parts.append(f'<rect x="28" y="{108 + i * 36}" width="160" height="26" rx="5" fill="#ffffff" stroke="#d5e3ec"/>')
    mtext(38, 126 + i * 36, line, 14)
# Image as stacked read-only layers
f.text(410, 80, 'Slika (image)', 19, INK, 700)
for i in range(3):
    f.parts.append(f'<rect x="{322 + i * 8}" y="{112 + i * 18}" width="170" height="100" rx="8" fill="{["#dcebf5", "#e7f2f9", "#f3f9fc"][i]}" stroke="{ACCENT}" stroke-width="1.6"/>')
f.parts.append(f'<rect x="353" y="168" width="126" height="26" rx="5" fill="#e6edf3" stroke="#c3d2de"/>')
mtext(416, 186, 'predaja:1.4', 15, INK, 700, 'middle')
f.text(416, 266, 'predložak, samo za čitanje', 15, GRAY)
# Registry
f.text(682, 80, 'Registar slika', 19, INK, 700)
f.parts.append(f'<path d="M597,112 a85,16 0 0 0 170,0 a85,16 0 0 0 -170,0 v120 a85,16 0 0 0 170,0 v-120" fill="#fff6ea" stroke="{ORANGE}" stroke-width="1.8"/>')
f.parts.append(f'<path d="M597,112 a85,16 0 0 0 170,0" fill="none" stroke="{ORANGE}" stroke-width="1.8"/>')
for i, t in enumerate(['predaja:1.3', 'predaja:1.4', 'portal:2.0']):
    mtext(682, 160 + i * 26, t, 14, INK, 700 if t == 'predaja:1.4' else 400, 'middle')
f.text(682, 266, 'npr. Docker Hub', 15, GRAY)
# Containers
f.text(980, 22, 'Kontejneri', 19, INK, 700)
for i in range(3):
    container(f, 880, 34 + i * 104, 200, 90, f'predaja.{i + 1}', 'pokrenuta slika')
# Arrows with commands
for (x1, x2, y, cmd) in [(204, 318, 170, 'docker build'), (514, 594, 170, 'docker push')]:
    f.arrow([(x1, y), (x2 - 4, y)])
    mtext((x1 + x2) / 2, y - 12, cmd, 13, ACCENT, 700, 'middle')
for i in range(3):
    f.arrow([(770, 172), (874, 78 + i * 104)], 'blue')
mtext(812, 300, 'docker pull', 13, ACCENT, 700, 'middle'); mtext(812, 318, '+ run', 13, ACCENT, 700, 'middle')
f.text(560, 362, 'Iz jedne slike nastaje mnogo kontejnera. Registar slika čuva slike; registar usluga (kasnije) čuva adrese živih kontejnera.', 15, GRAY)
f.save('code-image-container')
