"""Bilingual sequence diagrams: timeout histories A-C and the retry race."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
FONT = 'Arial, sans-serif'
MONO = 'Menlo, Consolas, monospace'
INK, MUTED, BLUE, RED, GREEN, AMBER = '#18344b', '#546573', '#3886ad', '#b33e44', '#28674b', '#bc8439'

DEFS = f'''<defs>
<marker id="arrow-blue" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="14" refY="9" orient="auto"><path d="M2,2 L18,9 L2,16 Z" fill="{BLUE}"/></marker>
<marker id="arrow-red" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="14" refY="9" orient="auto"><path d="M2,2 L18,9 L2,16 Z" fill="{RED}"/></marker>
<marker id="arrow-amber" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="14" refY="9" orient="auto"><path d="M2,2 L18,9 L2,16 Z" fill="{AMBER}"/></marker>
<marker id="arrow-axis" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto"><path d="M2,2 L16,8 L2,14 Z" fill="#90a5b3"/></marker>
</defs>'''


def text(x, y, s, size=20, weight=400, fill=INK, anchor='middle', family=FONT):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(s)}</text>')


def card(x, y, w, h, fill='#f8fbfd', stroke='#c6dbe8', accent=BLUE, bar=True):
    """Card with soft shadow and left accent bar, as in system-map."""
    out = (f'<rect x="{x + 1}" y="{y + 5}" width="{w - 2}" height="{h}" rx="14" fill="#24445c" opacity=".035"/>'
           f'<rect x="{x}" y="{y + 2}" width="{w}" height="{h}" rx="14" fill="#24445c" opacity=".025"/>'
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
    if bar:
        out += f'<rect x="{x + 12}" y="{y + h / 2 - 15}" width="6" height="30" rx="3" fill="{accent}"/>'
    return out


def arrow(d, colour=BLUE, marker='blue', dash=''):
    dash = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="3.2" stroke-linecap="round"'
            f'{dash} marker-end="url(#arrow-{marker})"/>')


def loss(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="17" fill="#fbecee" stroke="{RED}" stroke-width="2.4"/>'
            f'<path d="M{x - 7} {y - 7}L{x + 7} {y + 7}M{x + 7} {y - 7}L{x - 7} {y + 7}" '
            f'stroke="{RED}" stroke-width="3.6" stroke-linecap="round"/>')


def svg(w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<title>{escape(title)}</title>{DEFS}<rect width="{w}" height="{h}" fill="white"/>'
            + ''.join(body) + '</svg>\n')


def timeout_history(t, variant):
    """Shared frame for histories A-C; variant adds the middle of the story."""
    cx, sx = 225, 810
    service_end = 268 if variant == 'crash' else 372
    body = [
        card(80, 14, 290, 60), text(cx + 6, 52, t('Preglednik studenta', 'Student browser'), 23, 600),
        card(650, 14, 320, 60), text(sx + 6, 52, t('Usluga predaje', 'Submission service'), 23, 600),
        f'<path d="M{cx} 86V132 M{sx} 86V{service_end}" stroke="#b5c7d2" stroke-width="2" stroke-dasharray="5 7"/>',
        # The client is blocked from sending until its deadline expires.
        f'<rect x="{cx - 8}" y="132" width="16" height="246" rx="5" fill="#fff1df" stroke="#e1be89" stroke-width="1.4"/>',
        text(cx - 22, 262, t('čeka odgovor', 'waiting for reply'), 18, 400, '#976023', 'end'),
        '<path d="M1062 100V352" stroke="#90a5b3" stroke-width="2" marker-end="url(#arrow-axis)"/>',
        text(1062, 386, t('Vrijeme', 'Time'), 18, 400, MUTED),
        text(517, 112, 'submit(assignment, project)', 20, 400, INK, family=MONO),
        card(47, 392, 356, 54, '#fbecee', '#e8c2c5', RED),
        text(cx + 6, 426, t('Timeout: odgovor nije primljen', 'Timeout: no reply received'), 22, 600, '#a23b43'),
    ]
    accepted = [arrow(f'M{cx + 10} 134L{sx - 6} 182'),
                card(660, 198, 300, 52, '#eef7f2', '#b9dcc8', GREEN),
                text(sx + 6, 231, t('Predaja prihvaćena', 'Submission accepted'), 22, 600, GREEN)]
    if variant == 'request':
        body += [arrow(f'M{cx + 10} 134L512 181', RED, 'red', '9 7'), loss(540, 186),
                 text(540, 234, t('Zahtjev izgubljen', 'Request lost'), 21, 600, RED),
                 card(660, 272, 300, 58, '#f2f5f7', '#cfd9df', '#90a5b3'),
                 text(sx + 6, 308, t('Predaja nije prihvaćena', 'No submission accepted'), 22, 600, '#506676')]
    elif variant == 'reply':
        body += accepted + [arrow(f'M{sx} 274L466 323', RED, 'red', '9 7'),
                            text(652, 281, t('potvrda prihvaćanja', 'acceptance reply'), 20, 400, RED),
                            loss(440, 327),
                            text(440, 372, t('Odgovor izgubljen', 'Reply lost'), 21, 600, RED)]
    else:
        body += accepted + [loss(sx, 290),
                            text(sx, 340, t('Proces se ruši', 'Process crashes'), 22, 600, RED),
                            text(sx, 370, t('Odgovor nije poslan; zapis ostaje',
                                            'No reply sent; stored record survives'), 19, 400, MUTED)]
    return body


def retry_race(t):
    lanes = [(54, t('Klijent', 'Client')), (177, t('Pokušaj A', 'Attempt A')), (286, t('Pokušaj B', 'Attempt B'))]
    body = []
    for y, label in lanes:
        body += [f'<path d="M182 {y}L1094 {y}" stroke="#c6dbe8" stroke-width="2.4" marker-end="url(#arrow-axis)"/>',
                 card(8, y - 26, 158, 52), text(32, y + 8, label, 21, 600, INK, 'start')]

    def event(x, y, w, lines, fill, stroke, accent, colour=INK, weight=400):
        out = [card(x, y, w, 67, fill, stroke, accent)]
        out += [text(x + w / 2 + 6, y + 28 + 25 * i, s, 21, weight if i == 0 else 400, colour)
                for i, s in enumerate(lines)]
        return out

    body += [f'<circle cx="235" cy="54" r="7" fill="white" stroke="{BLUE}" stroke-width="3"/>',
             text(235, 30, t('pošalji A', 'send A'), 20, 400, BLUE),
             arrow('M240 64L322 137'),
             *event(220, 143, 220, [t('Provjeri pohranu:', 'Check storage:'), t('još nije prihvaćeno', 'not yet accepted')],
                    '#eef6fb', '#b7d5e6', BLUE),
             *event(395, 19, 210, ['Timeout', t('pošalji ponovo B', 'send retry B')],
                    '#fbecee', '#e8c2c5', RED, '#a23b43', 600),
             arrow('M512 90L592 244', AMBER, 'amber'),
             *event(490, 252, 220, [t('Provjeri pohranu:', 'Check storage:'), t('još nije prihvaćeno', 'not yet accepted')],
                    '#fff6ea', '#ebcf9f', AMBER),
             text(810, 118, t('drugi rad ili čekanje', 'other work or waiting'), 19, 400, MUTED),
             *event(720, 143, 180, [t('Stvori zapis', 'Create record'), '1'], '#eef6fb', '#b7d5e6', BLUE, INK, 600),
             *event(900, 252, 180, [t('Stvori zapis', 'Create record'), '2'], '#fff6ea', '#ebcf9f', AMBER, INK, 600),
             text(620, 364, t('Ista predaja, dva prihvaćena zapisa — duplikat.',
                              'Same submission, two accepted records — a duplicate.'), 23, 600, '#a23b43')]
    return body


for lang in ('hr', 'en'):
    def t(hr, en):
        return hr if lang == 'hr' else en
    # Timeout histories keep their historical English names without a language suffix.
    suffix = '.hr' if lang == 'hr' else ''
    for name, variant, title in [
        ('timeout-request-lost', 'request', t('Zahtjev se izgubi prije primitka', 'Request lost before arrival')),
        ('timeout-reply-lost', 'reply', t('Odgovor se izgubi nakon prihvaćanja', 'Reply lost after acceptance')),
        ('timeout-process-crash', 'crash', t('Proces se ruši nakon trajnog prihvaćanja',
                                             'Server process crashes after durable acceptance')),
    ]:
        (ROOT / f'{name}{suffix}.svg').write_text(svg(1120, 460, title, timeout_history(t, variant)))
    (ROOT / f'retry-race.{lang}.svg').write_text(
        svg(1120, 378, t('Timeout i preklapanje pokušaja', 'Timeout and overlapping attempts'), retry_race(t)))
