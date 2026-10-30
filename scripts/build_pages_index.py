"""Write the GitHub Pages catalog (index.html) of the published Croatian slide decks.

Usage: python3 scripts/build_pages_index.py SITE_DIR

Lists every deck in output/hr/slides/ with its title, version and subtitle from
lectures/<name>/slides.hr.qmd, slide count and duration from timing.json, and a
link to the Croatian lecture PDF when output/hr/lectures/<name>.pdf exists (the
workflow copies those PDFs into SITE_DIR/pdf/). Upcoming lectures appear only as
the approved Croatian topic blocks, so no unreviewed title is published.
"""

import argparse
from datetime import date
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / 'output/hr/slides'
PDFS = ROOT / 'output/hr/lectures'
YOUTUBE = 'https://www.youtube.com/playlist?list=PLIeA2EYS12RVaj1GdVP4fkNrLiK5k6VD-'

# Topic blocks from the "Teme kolegija" slide of Lecture 00, with their lecture numbers (COURSE.md).
BLOCKS = [
    ('Arhitekture i komunikacija komponenti', 'Tko s kim komunicira? Gdje može doći do ispada?', range(1, 5)),
    ('Vrijeme, replikacija i konsenzus', 'Što se dogodilo prvo? O čemu se možemo usuglasiti?', range(5, 8)),
    ('Oporavak, tijekovi rada i skaliranje', 'Kako se oporaviti i povećati kapacitet?', range(8, 12)),
    ('Sigurnost i procjena arhitekture', 'Koja jamstva sustav može pružiti i pod kojim pretpostavkama?', range(12, 13)),
]


def front_matter(path):
    """Top-level scalar fields of a Quarto YAML header (title, subtitle, version)."""
    text = path.read_text(encoding='utf-8')
    header = text.split('---', 2)[1] if text.startswith('---') else ''
    fields = {}
    for line in header.splitlines():
        match = re.match(r'^(\w[\w-]*):\s*"?(.*?)"?\s*$', line)
        if match and match.group(2):
            fields[match.group(1)] = match.group(2)
    return fields


def deck(html_path):
    name = html_path.stem
    lecture = ROOT / 'lectures' / name
    meta = front_matter(lecture / 'slides.hr.qmd')
    timing_path = lecture / 'timing.json'
    timing = json.loads(timing_path.read_text(encoding='utf-8')) if timing_path.is_file() else []
    return {
        'name': name,
        'number': int(name[:2]),
        'title': meta.get('title', name),
        'version': meta.get('version'),
        'slides': len(timing) or None,
        'minutes': round(max(s['end'] for s in timing)) if timing else None,
        'pdf': f'pdf/{name}.pdf' if (PDFS / f'{name}.pdf').is_file() else None,
    }


def slides_label(n):
    """Croatian plural: 1, 21 slajd · 2-4, 22-24 slajda · otherwise slajdova."""
    if n % 10 == 1 and n % 100 != 11:
        return f'{n} slajd'
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return f'{n} slajda'
    return f'{n} slajdova'


def card(d):
    e = html.escape
    label = 'Uvod' if d['number'] == 0 else f"Predavanje {d['number']:02d}"
    facts = [f"{d['minutes']} min" if d['minutes'] else None, slides_label(d['slides']) if d['slides'] else None,
             f"v{e(d['version'])}" if d['version'] else None]
    pdf = (f'<a class="btn ghost" href="{e(d["pdf"])}" download>PDF skripta</a>' if d['pdf'] else '')
    return f'''
      <article class="card">
        <a class="cover" href="{e(d['name'])}.html" aria-label="Otvori slajdove: {e(d['title'])}">
          <span class="num">{d['number']:02d}</span>
        </a>
        <div class="body">
          <p class="kicker">{label}</p>
          <h3><a href="{e(d['name'])}.html">{e(d['title'])}</a></h3>
          <p class="facts">{' · '.join(f for f in facts if f)}</p>
          <div class="actions">
            <a class="btn" href="{e(d['name'])}.html">Otvori slajdove</a>{pdf}
          </div>
        </div>
      </article>'''


def block(title, question, numbers, published):
    ready = [n for n in numbers if n in published]
    status = (f'{len(ready)} od {len(numbers)} objavljeno' if ready else 'u pripremi')
    dots = ''.join(f'<span class="dot{" on" if n in published else ""}" title="Predavanje {n:02d}"></span>'
                   for n in numbers)
    return f'''
        <li>
          <div><strong>{html.escape(title)}</strong><span>{html.escape(question)}</span></div>
          <div class="progress" aria-label="{status}">{dots}<em>{status}</em></div>
        </li>'''


def page(decks):
    published = {d['number'] for d in decks}
    cards = ''.join(card(d) for d in decks)
    blocks = ''.join(block(*b, published) for b in BLOCKS)
    return f'''<!doctype html>
<html lang="hr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Raspodijeljeni sustavi · Predavanja</title>
<meta name="description" content="Slajdovi predavanja iz kolegija Raspodijeljeni sustavi, Fakultet informatike u Puli.">
<link rel="icon" href="fipu-logo.svg">
<style>
  :root {{
    --bg: #f5f7f9; --surface: #ffffff; --ink: #1e2b36; --muted: #5b6875; --line: #dde3e8;
    --accent: #1585b4; --accent-ink: #ffffff; --accent-soft: #e3f1f7; --cover: #1e2b36; --cover-ink: #e6edf3;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #11181f; --surface: #1a232c; --ink: #e6edf3; --muted: #9aa7b3; --line: #2b3742;
      --accent: #4fb3dd; --accent-ink: #0d1a22; --accent-soft: #17303d; --cover: #0b1117; --cover-ink: #e6edf3;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink);
    font: 16px/1.5 "Source Sans Pro", "Source Sans 3", -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
  a {{ color: inherit; }}
  .wrap {{ max-width: 1040px; margin: 0 auto; padding: 0 16px; }}
  header {{ background: var(--surface); border-bottom: 4px solid var(--accent); }}
  .hero {{ display: flex; gap: 24px; align-items: center; padding: 36px 16px 32px; }}
  .logo {{ width: 84px; height: 84px; flex: none; background: #fff; border-radius: 14px; padding: 8px; }}
  .hero p {{ margin: 0; color: var(--muted); }}
  .hero h1 {{ margin: 2px 0 6px; font-size: clamp(28px, 5vw, 40px); line-height: 1.1; letter-spacing: -0.01em; }}
  .hero .links {{ margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px 18px; }}
  .hero .links a {{ color: var(--accent); font-weight: 600; text-decoration: none; }}
  .hero .links a:hover {{ text-decoration: underline; }}
  h2 {{ font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin: 40px 0 14px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; }}
  .card {{ display: flex; flex-direction: column; background: var(--surface); border: 1px solid var(--line);
    border-radius: 14px; overflow: hidden; transition: transform .15s ease, box-shadow .15s ease; }}
  .card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 24px rgba(16, 32, 48, .12); }}
  .cover {{ position: relative; display: block; aspect-ratio: 16 / 7; background: var(--cover); text-decoration: none;
    background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,.09) 1px, transparent 0);
    background-size: 18px 18px; }}
  .cover::after {{ content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 4px; background: var(--accent); }}
  .num {{ position: absolute; left: 20px; bottom: 12px; font-size: 64px; font-weight: 700; line-height: 1;
    color: var(--cover-ink); opacity: .92; font-variant-numeric: tabular-nums; }}
  .body {{ padding: 16px 20px 20px; display: flex; flex-direction: column; flex: 1; }}
  .kicker {{ margin: 0; font-size: 13px; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: .06em; }}
  .card h3 {{ margin: 4px 0 6px; font-size: 21px; line-height: 1.25; }}
  .card h3 a {{ text-decoration: none; }}
  .facts {{ margin: 0 0 16px; color: var(--muted); font-size: 14px; }}
  .actions {{ margin-top: auto; display: flex; flex-wrap: wrap; gap: 8px; }}
  .btn {{ display: inline-block; padding: 8px 14px; border-radius: 8px; background: var(--accent); color: var(--accent-ink);
    font-weight: 600; font-size: 15px; text-decoration: none; border: 1px solid var(--accent); }}
  .btn:hover {{ filter: brightness(1.08); }}
  .btn.ghost {{ background: transparent; color: var(--accent); }}
  .btn.ghost:hover {{ background: var(--accent-soft); filter: none; }}
  .plan {{ list-style: none; margin: 0; padding: 0; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; }}
  .plan li {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 14px 20px; }}
  .plan li + li {{ border-top: 1px solid var(--line); }}
  .plan strong {{ display: block; }}
  .plan span {{ color: var(--muted); font-size: 15px; }}
  .progress {{ display: flex; align-items: center; gap: 5px; flex: none; }}
  .dot {{ width: 10px; height: 10px; border-radius: 50%; border: 2px solid var(--accent); }}
  .dot.on {{ background: var(--accent); }}
  .progress em {{ font-style: normal; font-size: 13px; color: var(--muted); margin-left: 6px; min-width: 104px; }}
  footer.wrap {{ margin-top: 48px; margin-bottom: 32px; color: var(--muted); font-size: 14px; }}
  kbd {{ font: 12px/1 ui-monospace, Menlo, monospace; border: 1px solid var(--line); border-bottom-width: 2px;
    border-radius: 4px; padding: 2px 5px; background: var(--surface); }}
  @media (max-width: 560px) {{
    .hero {{ flex-direction: column; align-items: flex-start; gap: 14px; padding-top: 24px; }}
    .logo {{ width: 64px; height: 64px; }}
    .plan li {{ flex-direction: column; align-items: flex-start; gap: 8px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{ .card {{ transition: none; }} .card:hover {{ transform: none; }} }}
</style>
</head>
<body>
<header>
  <div class="wrap hero">
    <img class="logo" src="fipu-logo.svg" alt="FIPU">
    <div>
      <p>Fakultet informatike · Sveučilište Jurja Dobrile u Puli</p>
      <h1>Raspodijeljeni sustavi</h1>
      <p>izv. prof. dr. sc. Nikola Tanković · slajdovi predavanja</p>
      <div class="links"><a href="{YOUTUBE}">Snimke predavanja na YouTubeu</a></div>
    </div>
  </div>
</header>
<main class="wrap">
  <h2>Objavljena predavanja</h2>
  <div class="grid">{cards}
  </div>

  <h2>Plan kolegija</h2>
  <ul class="plan">{blocks}
  </ul>
</main>
<footer class="wrap">
  Slajdovi se otvaraju u pregledniku. <kbd>F</kbd> cijeli zaslon · <kbd>S</kbd> bilješke · <kbd>Esc</kbd> pregled svih slajdova.
  Kratke poveznice: <code>01.html</code>, <code>02.html</code>… · Ažurirano {date.today().strftime('%d. %m. %Y.')}
</footer>
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('site', type=Path, help='Directory that receives index.html')
    args = parser.parse_args()
    decks = sorted((deck(p) for p in SLIDES.glob('*.html')), key=lambda d: d['number'])
    args.site.mkdir(parents=True, exist_ok=True)
    (args.site / 'index.html').write_text(page(decks), encoding='utf-8')
    print(f"Wrote {args.site / 'index.html'} with {len(decks)} decks.")


if __name__ == '__main__':
    main()
