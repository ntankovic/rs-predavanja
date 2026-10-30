"""Check built Reveal.js decks in headless Chrome and save review screenshots."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lecture', nargs='?', default='01-foundations',
                        help='Lecture directory name, or all')
    parser.add_argument('--lang', choices=['en', 'hr'], default='en')
    args = parser.parse_args()
    source_name = 'slides.hr.qmd' if args.lang == 'hr' else 'slides.qmd'
    output_root = ROOT / 'output' / ('hr' if args.lang == 'hr' else '')
    if args.lecture == 'all':
        sources = sorted((ROOT / 'lectures').glob(f'[0-9][0-9]-*/{source_name}'))
    elif re.fullmatch(r'\d{2}-[a-z0-9-]+', args.lecture):
        sources = [ROOT / 'lectures' / args.lecture / source_name]
    else:
        parser.error('Use a numbered lecture directory name or all.')
    if not sources:
        parser.error(f'No {args.lang} slide sources found.')
    chrome = (os.environ.get('CHROME_BIN')
              or shutil.which('google-chrome') or shutil.which('chromium')
              or '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    if not Path(chrome).is_file():
        parser.error('Chrome was not found. Set CHROME_BIN to its executable path.')
    for source in sources:
        if not source.is_file():
            parser.error(f'Missing source: {source}')
        if not (output_root / 'slides' / (source.parent.name + '.html')).is_file():
            parser.error(f'Build the deck first: just slides {source.parent.name}')

    results = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=chrome, headless=True)
        try:
            for source in sources:
                name = source.parent.name
                deck = output_root / 'slides' / (name + '.html')
                output = output_root / 'qa' / name
                output.mkdir(parents=True, exist_ok=True)
                expected = 2 + len(re.findall(r'^## ', source.read_text(), re.M))
                errors = []
                page = browser.new_page(viewport={'width': 1280, 'height': 800}, device_scale_factor=1)
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.goto(deck.as_uri())
                page.wait_for_function('window.Reveal && Reveal.isReady()')
                page.evaluate('document.fonts.ready')
                count = page.evaluate('Reveal.getTotalSlides()')
                problems = []
                attendance_index = 2 if '<!-- attendance-slide -->' in source.read_text() else 1
                attendance = page.evaluate('''(index) => {
                  const slide = Reveal.getSlides()[index];
                  return slide && slide.id === 'attendance'
                    && !!slide.querySelector('a[href="https://bit.ly/rs-tu-sam"]')
                    && !!slide.querySelector('img');
                }''', attendance_index)
                if not attendance:
                    problems.append({'kind': 'attendance', 'message': f'Slide {attendance_index + 1} must contain the check-in QR and URL'})
                if count != expected:
                    problems.append({'kind': 'count', 'expected': expected, 'actual': count})
                for index in range(count):
                    page.evaluate('(index) => Reveal.slide(index)', index)
                    page.wait_for_timeout(350)
                    overflow = page.evaluate('''() => {
                      const slide = Reveal.getCurrentSlide(), r = slide.getBoundingClientRect();
                      return [...slide.querySelectorAll('h1,h2,p,li,img,table')]
                        .filter(el => !el.closest('aside'))
                        .filter(el => {
                          const b = el.getBoundingClientRect();
                          return b.width && b.height &&
                            (b.left < r.left-2 || b.right > r.right+2 ||
                             b.top < r.top-2 || b.bottom > r.bottom+2 ||
                             b.top < -2 || b.bottom > innerHeight+2 ||
                             b.left < -2 || b.right > innerWidth+2);
                        }).map(el => el.innerText || el.getAttribute('alt') || el.tagName);
                    }''')
                    missing_images = page.evaluate('''() => [...Reveal.getCurrentSlide().querySelectorAll('img')]
                      .filter(img => !img.complete || !img.naturalWidth)
                      .map(img => img.getAttribute('alt') || 'image')''')
                    if overflow or missing_images:
                        problems.append({'slide': index+1, 'overflow': overflow, 'missing_images': missing_images})
                    page.screenshot(path=str(output / f'slide-{index+1:02d}.png'))
                # Reveal's PDF layout differs from the interactive slide layout.
                page.goto(deck.as_uri() + '?print-pdf')
                page.wait_for_function('document.querySelector(".pdf-page #attendance")')
                page.evaluate('document.fonts.ready')
                page.emulate_media(media='print')
                attendance_print = page.evaluate('''() => {
                  const slide = document.querySelector('#attendance');
                  const page = slide.closest('.pdf-page').getBoundingClientRect();
                  const image = slide.querySelector('img').getBoundingClientRect();
                  const link = slide.querySelector('a[href="https://bit.ly/rs-tu-sam"]').getBoundingClientRect();
                  return {fits: [image, link].every(b => b.width > 0 && b.height > 0 &&
                    b.left >= page.left && b.right <= page.right &&
                    b.top >= page.top && b.bottom <= page.bottom - 35)};
                }''')
                page.locator('.pdf-page').filter(has=page.locator('#attendance')).screenshot(
                    path=str(output / 'attendance-print.png'))
                if not attendance_print['fits']:
                    problems.append({'kind': 'attendance-print', 'message': 'QR/link overlap the PDF page edge or footer'})
                page.pdf(path=str(output / 'slides-print.pdf'), prefer_css_page_size=True,
                         print_background=True)
                report = {'lecture': name, 'slides': count, 'expected_slides': expected,
                          'viewport': {'width': 1280, 'height': 800},
                          'runtime_errors': errors, 'problems': problems,
                          'passed': not errors and not problems}
                (output / 'browser-report.json').write_text(json.dumps(report, indent=2))
                results.append(report)
                page.close()
                print(f'{name}: {count} slides; {"PASS" if report["passed"] else "FAIL"}; screenshots in {output.relative_to(ROOT)}')
        finally:
            browser.close()
    if any(not report['passed'] for report in results):
        raise SystemExit('Browser checks failed; see output/qa/<lecture>/browser-report.json')


if __name__ == '__main__':
    main()
