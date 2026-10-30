# List the available build commands.
default:
    @just --list

# Check Quarto and its rendering dependencies.
check:
    python3 scripts/build.py check

# Render a lecture PDF and HTML slides; defaults to Lecture 01 in Croatian.
render name="01-foundations" lang="hr":
    python3 scripts/build.py lecture {{quote(name)}} --lang {{quote(lang)}}
    python3 scripts/build.py slides {{quote(name)}} --lang {{quote(lang)}}

# Build the complete student book PDF.
book lang="en":
    python3 scripts/build.py book --lang {{quote(lang)}}

# Build one lecture PDF, e.g. just lecture 01-foundations.
lecture name lang="hr":
    python3 scripts/build.py lecture {{quote(name)}} --lang {{quote(lang)}}

# Build one standalone HTML slide deck.
slides name lang="hr":
    python3 scripts/build.py slides {{quote(name)}} --lang {{quote(lang)}}

# Open a built slide deck in the default browser (use en for English).
preview name="01-foundations" lang="hr":
    #!/usr/bin/env bash
    set -eu
    preview_name={{quote(name)}}
    preview_lang={{quote(lang)}}
    case "$preview_lang" in
        en) preview_root="output/slides" ;;
        hr) preview_root="output/hr/slides" ;;
        *) echo "Language must be en or hr." >&2; exit 1 ;;
    esac
    preview_file="$preview_root/$preview_name.html"
    if [ ! -f "$preview_file" ]; then
        echo "Slide deck not found. Build it with: just slides $preview_name $preview_lang" >&2
        exit 1
    fi
    open "$preview_file"

# Build every numbered lecture, every slide deck, and the complete book.
all lang="en":
    python3 scripts/build.py all --lang {{quote(lang)}}

# Build all materials and check the generated PDFs and slide decks.
test: (all "en")
    python3 scripts/verify_builds.py

# Compare English and Croatian slide structure, timing, reveals and references.
language-check name="01-foundations":
    python3 scripts/verify_slide_languages.py {{quote(name)}}

# Check a built deck in headless Chrome; use all to check every deck.
browser-check name="01-foundations" lang="hr":
    {{quote(env("COURSE_QA_PYTHON", ".tools/qa-venv/bin/python"))}} scripts/verify_slides_browser.py {{quote(name)}} --lang {{quote(lang)}}

# Preview a built deck, or render an SVG to its PDF derivative and a QA screenshot.
headless-preview target="01-foundations" lang="hr":
    {{quote(env("COURSE_QA_PYTHON", ".tools/qa-venv/bin/python"))}} scripts/headless_preview.py {{quote(target)}} --lang {{quote(lang)}}

# Download a direct HTTPS image into project assets; never overwrite an existing file.
download-image url destination:
    python3 scripts/download_image.py {{quote(url)}} {{quote(destination)}}
