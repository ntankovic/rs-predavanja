"""Build course outputs with Quarto without modifying lecture sources."""

import argparse
import os
import re
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def quarto_command():
    local = ROOT / '.tools/quarto/bin/quarto'
    return os.environ.get('QUARTO_BIN') or shutil.which('quarto') or (str(local) if local.is_file() else None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', choices=['book', 'lecture', 'slides', 'all', 'check'])
    parser.add_argument('lecture', nargs='?', help='Lecture directory name, e.g. 01-introduction')
    parser.add_argument('--lang', choices=['en', 'hr'], default='en')
    args = parser.parse_args()
    quarto = quarto_command()
    if not quarto:
        parser.error('Quarto is missing. Install with: brew install --cask quarto')
    if args.target in ('all', 'check'):
        if args.lecture:
            parser.error('This target does not take a lecture name.')
        if args.target == 'check':
            subprocess.run([quarto, 'check'], check=True)
        else:
            import sys
            for directory in sorted((ROOT / 'lectures').glob('[0-9][0-9]-*')):
                for target, filename in (('lecture', 'chapter.qmd'), ('slides', 'slides.qmd')):
                    if (directory / filename).is_file() or (directory / Path(filename).with_suffix('.hr.qmd')).is_file():
                        subprocess.run([sys.executable, __file__, target, directory.name, '--lang', args.lang], check=True)
            subprocess.run([sys.executable, __file__, 'book', '--lang', args.lang], check=True)
        return
    if args.target != 'book':
        if not args.lecture or Path(args.lecture).name != args.lecture:
            parser.error('Provide a lecture directory name.')
        source = ROOT / 'lectures' / args.lecture
        filename = 'slides.qmd' if args.target == 'slides' else 'chapter.qmd'
        if args.lang == 'en' and not (source / filename).is_file():
            parser.error(f'Missing source: {source / filename}')
    elif args.lecture:
        parser.error('The book target does not take a lecture name.')

    output_root = ROOT / 'output' / ('hr' if args.lang == 'hr' else '')
    localized_sources = []
    if args.lang == 'hr':
        if args.target == 'book':
            config = (ROOT / 'publishing/book/_quarto.yml').read_text()
            localized_sources = [Path(path) for path in re.findall(r'^    - (.+\.qmd)$', config, re.M)
                                 if path != 'index.qmd']
            localized_sources.append(Path('publishing/book/index.qmd'))
        else:
            localized_sources = [Path('lectures') / args.lecture / filename]
        for relative in localized_sources:
            translated = ROOT / relative.with_suffix('.hr.qmd')
            if not translated.is_file():
                parser.error(f'Missing Croatian source: {translated}. Create and review it before building Croatian output.')

    with tempfile.TemporaryDirectory(prefix='distributed-systems-') as temporary:
        stage = Path(temporary)
        # Preserve repository-relative links to lecture and shared assets.
        for name in ('lectures', 'assets', 'references', 'publishing'):
            shutil.copytree(ROOT / name, stage / name)
        for relative in localized_sources:
            shutil.copy2(ROOT / relative.with_suffix('.hr.qmd'), stage / relative)
        if args.target == 'book':
            shutil.copy2(ROOT / 'publishing/book/_quarto.yml', stage / '_quarto.yml')
            shutil.copy2(stage / 'publishing/book/index.qmd', stage / 'index.qmd')
            command = [quarto, 'render', '.', '--to', 'pdf']
            result = stage / '_book/distributed-systems.pdf'
            destination = output_root / 'book/distributed-systems.pdf'
            cwd = stage
        else:
            cwd = stage / 'lectures' / args.lecture
            slides = args.target == 'slides'
            metadata = stage / ('publishing/slides/revealjs.yml' if slides else 'publishing/book/lecture.yml')
            if slides:
                # Insert the shared check-in immediately after Quarto's title slide.
                staged_slides = cwd / filename
                slide_text = staged_slides.read_text()
                frontmatter = re.match(r'\A---\s*\n.*?\n---[ \t]*\n', slide_text, re.S)
                if not frontmatter:
                    parser.error(f'Slide sources require YAML title metadata: {source / filename}')
                attendance = (stage / f'publishing/slides/attendance.{args.lang}.qmd').read_text()
                marker = '<!-- attendance-slide -->'
                if marker in slide_text:
                    if slide_text.count(marker) != 1:
                        parser.error('Use exactly one attendance-slide marker.')
                    # An explicit placement is used by the introductory deck.
                    attendance = attendance.replace('00:30–01 min', '01:30–02 min').replace(
                        'within the opening minute', 'after the attendance explanation').replace(
                        'unutar uvodne minute', 'nakon objašnjenja prisutnosti')
                    staged_slides.write_text(slide_text.replace(marker, attendance))
                else:
                    staged_slides.write_text(slide_text[:frontmatter.end()] + '\n' + attendance
                                             + slide_text[frontmatter.end():])
            if slides:
                footer = 'Distributed Systems · assoc. prof. Nikola Tankovic, PhD'
                localized = footer if args.lang == 'en' else 'Raspodijeljeni sustavi · izv. prof. dr. sc. Nikola Tanković'
                # An optional deck version from front matter is appended to the footer.
                version = re.search(r'^version:\s*"?([^"\n]+?)"?\s*$', frontmatter.group(0), re.M)
                if version:
                    localized += ' · v' + version.group(1)
                metadata.write_text(metadata.read_text().replace(footer, localized))
            output_name = args.lecture + ('.html' if slides else '.pdf')
            command = [quarto, 'render', filename, '--to', 'revealjs' if slides else 'pdf',
                       '--metadata-file', str(metadata), '--output', output_name]
            if not slides:
                lecture_number = args.lecture.split('-', 1)[0]
                staged_chapter = cwd / filename
                chapter_text = staged_chapter.read_text()
                label = 'Raspodijeljeni sustavi, Predavanje ' if args.lang == 'hr' else 'Distributed Systems, Lecture '
                subject = r'\subject{' + label + lecture_number + '}'
                if '      text: |\n' in chapter_text:
                    chapter_text = chapter_text.replace('      text: |\n',
                                                        '      text: |\n        ' + subject + '\n', 1)
                else:
                    chapter_text = chapter_text.replace('---\n',
                        '---\ninclude-in-header:\n  text: |\n    ' + subject + '\n', 1)
                staged_chapter.write_text(chapter_text)
            result = cwd / output_name
            destination = output_root / ('slides' if slides else 'lectures') / output_name
        command.extend(['--metadata', f'lang:{args.lang}'])
        if args.lang == 'hr':
            command.extend(['--metadata', 'author:izv. prof. dr. sc. Nikola Tanković'])
            if args.target != 'slides':
                command.extend(['--metadata', 'subtitle:Fakultet informatike, Sveučilište Jurja Dobrile u Puli'])
            if args.target == 'book':
                command.extend(['--metadata', 'title:Raspodijeljeni sustavi'])
        command.extend(['--lua-filter', str(stage / 'publishing/table-style.lua')])
        command.extend(['--lua-filter', str(stage / 'publishing/definitions.lua')])
        subprocess.run(command, cwd=cwd, check=True)
        if args.target == 'slides':
            # Prefix only the browser tab title; preserve the visible title slide.
            prefix = f"RS-{args.lecture.split('-', 1)[0]}"
            html = result.read_text()
            def prefix_title(match):
                title = match.group(1)
                if not title.startswith(prefix + ' '):
                    title = f'{prefix} · {title}'
                return f'<title>{title}</title>'
            html, count = re.subn(r'<title>(.*?)</title>', prefix_title, html,
                                  count=1, flags=re.S)
            if count != 1:
                raise RuntimeError(f'Missing browser title in {result}')
            result.write_text(html)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(result, destination)
        print(f'Created {destination.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
