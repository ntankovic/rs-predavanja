# Teaching slides

Each lecture's editable slide source is `lectures/NN-short-topic/slides.qmd`.

- Begin with the lecture title, course name, lecturer, and faculty as specified in `COURSE.md`.
- Use a focused idea per slide and readable diagrams.
- Put extended explanations in speaker notes and the student chapter.
- Include checks for understanding and a recap linked to the learning outcomes.
- Keep shared themes and export configuration here.
- Place generated decks in `output/slides/`.

Use Quarto Reveal.js with `revealjs.yml`. Run `just slides NN-short-topic` from the repository root to generate a standalone HTML deck. Write speaker notes inside `::: {.notes}` blocks.

The shared configuration supplies the FIPU logo to every deck: a proportional 140 px logo above the left-aligned title and a small logo on every slide. Keep title metadata in YAML (as in `lectures/_template/`) so Quarto generates `#title-slide`. Do not duplicate logo settings or title-logo CSS in individual lectures.

Every build inserts `attendance.hr.qmd` or `attendance.en.qmd` as slide 2, after the YAML title slide. It embeds `assets/shared/attendance-qr.svg`, encoding exactly `https://bit.ly/rs-tu-sam`, and includes a clickable text link. Do not add a duplicate check-in to lecture sources or templates. The welcome and check-in share the first minute; timing files include this generated slide.

Editorial comments belong in each lecture's `design-review.md` or review checklist, labelled **DESIGN-TIME REVIEW ONLY — excluded from slide exports**. Keep `.notes` and title `data-notes` exclusively for timing, teaching cues, discussion, and source attribution. Do not place authoring instructions or release-review messages in exported speaker notes.

Lecture 00 exception: its source includes `<!-- attendance-slide -->` after the attendance explanation. The build inserts QR check-in there (slide 3); other decks keep slide 2.

2026-09-18 — Lecturer requested a 15% larger shared QR and slightly higher vertical placement. Both languages use a 455.4 px square (previously 396 px). The QR/link block is centred with translateY(-50%) at 54% of slide height, preserving room below the heading. Applies to all decks.

Browser tab titles carry the lecture prefix (`RS-00 · Course introduction and assessment`, `RS-01 · Foundations and system models`, etc.) in both languages. `scripts/build.py` applies the prefix to the generated HTML `<title>` only, preserving visible slide headings.

Shell commands on slides use the terminal look: inline `` `npm start`{.cmd} `` and multi-line ```` ```{.terminal code-line-numbers="false"} ```` blocks (CSS in `revealjs.yml`; rule in `COURSE.md`, Content guidelines).
