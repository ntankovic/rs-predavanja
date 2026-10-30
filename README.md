# Distributed Systems course materials

Lecturer: assoc. prof. Nikola Tankovic, PhD  
Faculty: Faculty of Informatics, Juraj Dobrila University of Pula

Read [COURSE.md](COURSE.md) for requirements and the proposed 12-lecture sequence, and [AGENTS.md](AGENTS.md) for agent working rules. Lecture 01 is developed for 60 minutes and in review; lectures 02–12 retain short sample chapters and four sample slides.

## Local setup

Use Python 3, Just, Quarto, and a LaTeX distribution for PDF output. On macOS:

```sh
brew install just
brew install --cask quarto
just check
```

If LaTeX is absent, run `quarto install tinytex`. This Mac already has XeLaTeX. R and Jupyter are not needed for these text-only builds. Initial installation and missing LaTeX packages may require internet access; publishing requires no hosted service or subscription.

This workspace also has the official portable Quarto 1.10.18 in the ignored `.tools/quarto/` directory. The build script uses `QUARTO_BIN` when set, then a system `quarto`, then this local copy. The portable copy is not versioned; on another machine install Quarto normally or unpack its [official Mac tarball](https://quarto.org/docs/download/release) into `.tools/quarto/`.

## Build commands

```sh
just                              # List commands
just book                         # Complete book PDF
just lecture 01-foundations       # One lecture PDF
just slides 01-foundations        # One standalone Reveal.js HTML deck
just preview 01-foundations       # Open the built deck in the default browser
just headless-preview 01-foundations # Save screenshots and check the built deck
just all                          # All lecture PDFs, slides, and book
just test                         # Build all and validate output content
just browser-check 01-foundations # Check a built deck in headless Chrome
just browser-check all            # Check every built deck in Chrome
```

Just is a command runner: these recipes rebuild their targets each time. Outputs go to `output/book/`, `output/lectures/`, and `output/slides/`. Open the HTML slide files in a browser; press S for speaker view.

`just test` additionally needs the Python package `pymupdf` (`python3 -m pip install pymupdf`). It checks book chapter order and coverage, PDF content, slide count and notes, and embedded resource references. It writes `output/build-report.md`. Slide counts are checked against source headings. Developed lectures with `timing.json` are also checked for a complete 60-minute plan. `just browser-check` checks the built HTML without rebuilding it: slide count, JavaScript errors, missing images, and overflow at a 1280 × 800 viewport. It saves screenshots and `browser-report.json` under `output/qa/<lecture>/` for visual review. It uses the isolated `.tools/qa-venv/bin/python` environment with Playwright; set `COURSE_QA_PYTHON` to another Python executable with Playwright installed if needed. It uses installed Chrome; set `CHROME_BIN` for a different Chromium executable. To recreate the isolated environment: `python3 -m venv .tools/qa-venv`, then `.tools/qa-venv/bin/python -m pip install playwright pymupdf`. No separate browser download is needed when Chrome is installed. Automated checks complement visual review.

Without Just, use `python3 scripts/build.py book`, `python3 scripts/build.py lecture 01-foundations`, `python3 scripts/build.py slides 01-foundations`, or `python3 scripts/build.py all`.

## Develop a lecture

1. Follow `COURSE.md` and register ownership in `lectures/README.md`. Copy `lectures/_template/` when adding a new lecture.
2. Write `chapter.qmd` and `slides.qmd`. Quarto Markdown supports ordinary Markdown plus publishing metadata and features.
3. Keep lecture assets in its `assets/` directory and record references in `sources.md`.
4. Maintain `book.chapters` in `publishing/book/_quarto.yml`, after `index.qmd` and in teaching order. The current draft samples are included to test assembly; final publication requires content review.
5. Build the lecture PDF, slides, and complete book; inspect the rendered outputs.

The build script copies sources into a temporary workspace, preserving relative paths. Book configuration is applied at that workspace's root, so chapter paths in it are relative to the repository root. Edit original sources only. Templates are excluded from `just all` and the book.

## Course orientation

Lecture 00 is a 20-minute slides-only administrative introduction, excluded from the book. Build it with `just slides 00-course-introduction` and check it with `just browser-check 00-course-introduction`. It is included in `just all` and `just test`. Historical assessment rules await lecturer confirmation; see `lectures/00-course-introduction/README.md`.

## Croatian-first workflow

Render a lecture PDF and its HTML slides together:

```sh
just render                       # Lecture 01, English
just render 01-foundations hr      # Lecture 01, Croatian
just render 02-architectures hr    # Lecture 02, Croatian
```

The Croatian source files must exist before rendering; the command does not translate material.

Develop and tune Croatian material first, then translate the reviewed version into English. The lecturer reviews translations; store preferred terms in [references/terminology.md](references/terminology.md) and consult it for every lecture. Track content review and translation review separately in each lecture brief.

Sources stay together: `chapter.hr.qmd` and `slides.hr.qmd` are Croatian; `chapter.qmd` and `slides.qmd` are English. Existing English lectures remain available while Croatian versions are developed. Localized figures use language suffixes in the same `assets/` directory.

```sh
just lecture 01-foundations hr
just slides 01-foundations hr
just preview 01-foundations hr
just headless-preview 01-foundations hr
just browser-check 01-foundations hr
just book hr
just all hr
```

Croatian outputs and browser reports go under `output/hr/`. Missing Croatian sources produce an error; English is never silently substituted. The Croatian book requires every listed chapter in Croatian. The Croatian templates are available now; Lecture 01 has not yet been translated into Croatian.

Single-lecture recipes (`render`, `lecture`, `slides`, `preview`, `browser-check`, `headless-preview`) default to Croatian; pass `en` for English. `all`, `book` and `test` default to English. `just test` currently checks the English course exports. For Croatian, build the relevant output, run its language-specific browser check, and visually review PDF text, diacritics, figures, footnotes, and layout. Full-course Croatian structural checks will be added when Croatian chapters exist; a successful build alone is not content approval.

For an SVG diagram, `just headless-preview lectures/00-course-introduction/assets/practical-work.hr.svg` updates its adjacent PDF derivative and saves a PNG under `output/qa/diagrams/`. This uses headless Chrome to preserve SVG arrow markers. For a lecture name, the command checks the existing HTML deck and saves the same screenshots/report as `just browser-check`; build slides first after edits.
