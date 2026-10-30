"""Preview a built lecture or export a local SVG with headless Chrome."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', nargs='?', default='01-foundations',
                        help='Lecture directory name, all, or a project SVG path')
    parser.add_argument('--lang', choices=['en', 'hr'], default='en')
    args = parser.parse_args()
    if not args.target.endswith('.svg'):
        subprocess.run([sys.executable, str(ROOT / 'scripts/verify_slides_browser.py'),
                        args.target, '--lang', args.lang], check=True)
        return

    source = (ROOT / args.target).resolve()
    if not source.is_relative_to(ROOT / 'lectures') or not source.is_file():
        parser.error('Use an existing SVG inside lectures/.')
    svg = source.read_text()
    viewbox = ET.fromstring(svg).get('viewBox', '').split()
    if len(viewbox) != 4:
        parser.error('SVG must have a four-number viewBox.')
    width, height = map(float, viewbox[2:])
    if width <= 0 or height <= 0:
        parser.error('SVG dimensions must be positive.')
    chrome = (os.environ.get('CHROME_BIN') or shutil.which('google-chrome')
              or shutil.which('chromium')
              or '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    output = ROOT / 'output/qa/diagrams' / source.relative_to(ROOT / 'lectures')
    output.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=chrome, headless=True)
        try:
            page = browser.new_page(viewport={'width': round(width), 'height': round(height)})
            page.set_content('<html><head><style>@page {margin:0} body {margin:0} '
                             'svg {display:block}</style></head><body>' + svg + '</body></html>')
            page.evaluate('document.fonts.ready')
            page.pdf(path=str(source.with_suffix('.pdf')), width=f'{width}px',
                     height=f'{height}px', print_background=True)
            page.screenshot(path=str(output.with_suffix('.png')))
        finally:
            browser.close()
    print(f'PDF: {source.with_suffix(".pdf").relative_to(ROOT)}')
    print(f'Preview: {output.with_suffix(".png").relative_to(ROOT)}')


if __name__ == '__main__':
    main()
