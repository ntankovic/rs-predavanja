"""Check structural parity of Croatian slides against the English anchor.

This verifies synchronization markers, not translation quality or correctness.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lecture')
    args = parser.parse_args()
    if not re.fullmatch(r'\d{2}-[a-z0-9-]+', args.lecture):
        parser.error('Use a numbered lecture directory name.')
    folder = ROOT / 'lectures' / args.lecture
    texts = [(folder / f).read_text() for f in ('slides.qmd', 'slides.hr.qmd')]
    sections = [re.split(r'^## ', text, flags=re.M) for text in texts]
    problems = []
    if len(sections[0]) != len(sections[1]):
        problems.append('Different slide counts')
    checks = {
        'timing': r'Timing: ([^\n(]+)',
        'definitions': r'number="([\d.]+)"',
        'reveals': r'fragment-index=(\d+)',
        'links': r'https?://[^\s)"<>]+',
        'images': r'!\[[^\]]*\]\(([^)]+)\)',
    }
    for index, (en, hr) in enumerate(zip(*sections)):
        for label, pattern in checks.items():
            a, b = (re.findall(pattern, s) for s in (en, hr))
            if label == 'images':
                a, b = ([re.sub(r'\.(en|hr)(?=\.)', '', x) for x in items]
                        for items in (a, b))
            if a != b:
                problems.append(f'Section {index}: {label} differ')
    for image in re.findall(checks['images'], texts[1]):
        if not (folder / image).is_file():
            problems.append(f'Missing Croatian asset: {image}')
    report = {
        'anchor': 'slides.qmd',
        'anchor_sha256': hashlib.sha256(texts[0].encode()).hexdigest(),
        'croatian_sha256': hashlib.sha256(texts[1].encode()).hexdigest(),
        'slides_including_title_and_attendance': len(sections[0]) + 1,
        'checks': list(checks),
        'problems': problems,
        'passed': not problems,
        'language_review': 'pending lecturer review',
    }
    output = ROOT / 'output/hr/qa' / args.lecture
    output.mkdir(parents=True, exist_ok=True)
    (output / 'language-report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if problems:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
