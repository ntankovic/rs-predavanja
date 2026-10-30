# Course introduction and assessment

- Number: 00
- Owner: coordinating agent
- Status: review (historical assessment rules need lecturer confirmation)
- Format: slides only; no chapter and no inclusion in the student book
- Languages: Croatian draft (`slides.hr.qmd`) and existing English reference (`slides.qmd`)
- Duration: 20 minutes including questions, separate from Lecture 01's 60 minutes
- Deliverable: 14-slide orientation deck with speaker notes

## Purpose

Introduce learning goals, the course sequence, practical work, assessment, participation, and help. Historical 2022/23 rules are visibly labelled. Study suggestions are not an official marking rubric. Current deadlines, grading, retakes, channels, and collaboration/attribution rules remain unresolved. AI-use policy was supplied by the lecturer on 2026-09-17.

## Timing

- 00–00:30: Course introduction and assessment
- 00:30–01:30: Attendance and participation
- 01:30–02: Mark your presence (shared slide)
- 02–03: Teaching staff and course obligations
- 03–04: What this course is about
- 04–06: The route through the course
- 06–07: From lectures to practical work
- 07–08: Project preparation
- 08–09: Course information and help
- 09–12: How to pass the course (BPMN)
- 12–13: Submission, exemption, and defence
- 13–16: Prepare to explain your project
- 16–18: AI use and your responsibility
- 18–20: Before the first technical lecture

## Build

`just slides 00-course-introduction`

`just browser-check 00-course-introduction`

`just all` includes the deck. `just lecture 00-course-introduction` intentionally has no PDF chapter to build. `lecture.json` declares the slides-only format and 20-minute timing exception.

## Review

- [x] Extracted administrative statements mapped to original pages.
- [x] Historical rules distinguished from current confirmed requirements.
- [x] No invented weights, deadlines, retake rules, or current contact links.
- [x] Rendered-output verification complete: all 14 slides visually reviewed; headless Chrome passed with no overflow, missing images, or JavaScript errors. Structural checks confirm 20-minute timing and exclusion from the book. Build-all dispatch checked for 12 chapter PDFs, 13 decks, and one book.
- [ ] Lecturer has confirmed the current policy and student-facing links.

Attendance update (2026-09-17): the shared build adds presence check-in as slide 2. Welcome and check-in together occupy 00–01 min; subsequent teaching segments retain their timing.

2026-09-17 source review: added the lecturer-supplied BPMN original and the confirmed staff responsibility split. English process summary remains pending translation review. Luka’s full name/title confirmed: Luka Blašković, mag. inf. Current calendar dates and grading weights remain unresolved.

AI policy review: lecturer-approved substance recorded in `sources.md`; Croatian wording in `ai-policy.hr.md`, English slide wording pending lecturer review. The orientation remains 20 minutes.

Editorial separation (2026-09-17): internal review comments moved to `design-review.md`, which is excluded from exports. Speaker notes now contain teaching cues, timing, and diagram attribution. Unconfirmed attendance requirements are recorded only in the internal review file.

Visual update (2026-09-17): added five original diagrams for practical examples, attendance, course completion, deadlines, and AI responsibility. Editable bilingual SVG sources and vector PDF derivatives are in `assets/`. HTML layout and PDF figure renders reviewed; the 14-slide / 20-minute structure is preserved. English diagram labels remain pending lecturer review.

2026-09-17: lecture 00 only places the attendance explanation on slide 2 and QR check-in on slide 3. Attendance is optional, as confirmed by the lecturer. Other decks retain QR check-in on slide 2.

2026-09-17: removed the simplified course-completion overview at the lecturer’s request. The original BPMN is the sole course-passing diagram and receives the removed slide’s minute; total remains 20 minutes across 14 slides.

## Croatian translation review, 2026-09-17

- Direction: English → Croatian, explicitly requested by the lecturer to establish the Croatian source for review.
- Source revision: `slides.qmd` as present on 2026-09-17, including optional attendance, current help channels, and corrected defence timing. This workspace has no Git metadata.
- Croatian content/language review: pending lecturer review.
- English translation review: pending; existing English remains a reference, not an approved translation of the new Croatian draft.
- Timing: the same 14 slides and 20-minute outline above, including the shared QR slide at 01:30–02 min. All teaching notes and alternative text translated; existing Croatian diagram variants reused.
- [x] Slide-by-slide coverage, links, source attribution, and confirmed policy checked against the supplied English deck and local confirmation record.
- [x] `just slides 00-course-introduction hr` completed.
- [x] `just browser-check 00-course-introduction hr` passed for all 14 slides, with no overflow, missing images, or runtime errors. All slide screenshots visually reviewed.
- [x] Croatian title, footer, diagram selection, and QR timing checked in generated HTML.
- [ ] Lecturer review of Croatian wording, especially provisional terminology in `references/terminology.md`.
- [ ] Resolve the preserved original BPMN image's superseded 7-day rule and calendar-day wording before classroom release. The following deadline slide and notes use the current rule: at least 3 working days before defence, defence by exam day. No policy was invented during translation.

Build the Croatian deck with `just slides 00-course-introduction hr`; verify with `just browser-check 00-course-introduction hr`. Lecture 00 has no chapter/PDF chapter by design. Existing diagram PDF derivatives were unchanged in this translation pass.

2026-09-17 terminology review: lecturer chose **Proces 1/2** instead of **Radnik 1/2** in the practical-work diagram. Updated editable source, Croatian/English SVG and PDF derivatives, and slide alternative text. English **Process 1/2** remains pending translation review.

2026-09-17 terminology review: lecturer approved **ispad** instead of **otkaz**. Applied throughout Croatian Lecture 00; English continues to use **failure**.

2026-09-18 wording review: lecturer approved the course-overview row “Sigurnost i procjena arhitekture” with “Koja jamstva sustav može pružiti i pod kojim pretpostavkama?”. English row aligned; translation review pending. Slide count and 20-minute timing unchanged.

2026-09-18 project-work wording: lecturer approved “Rad na projektu: Postavi problem → predloži rješenje → implementiraj → testiraj i doradi”. Added spacing between steps and before the diagram; notes clarify applicability to practical-class tasks and iteration. English aligned, pending language review.

2026-09-18: renamed the preparation slide to “Priprema za projekt” / “Project preparation” to clarify the purpose of the prerequisite checklist.

## Visuals adapted from Web Applications lecture 00, 2026-10-12

Lecturer request: apply the WA orientation graphics except the attendance QR slide, which stays as is. The lecturer confirmed that the WA defence rules also apply here: live code change, commit verification, the 20 Jul–25 Aug leave and the 30 Sep academic-year end.

- Croatian deck only (`slides.hr.qmd`): 14 → 19 slides, still 20 minutes. The English deck and `timing.json` (which `just test` checks against `slides.qmd`) are unchanged until the Croatian revision is reviewed and translated. `just language-check` will report the structural difference until then.
- New slides: Rok predaje: brojite radne dane; Ako projekt ne obranite ove godine; Commitovi i individualni doprinos; Izmjena koda uživo; Preporučeni AI alati. Revised slides: Priprema za projekt (technology cards) and Pripremite se objasniti svoj projekt (three-step diagram).
- Shared attendance link changed to `https://bit.ly/rs-tu-sam`; QR regenerated (see `sources.md`).

Croatian timing (19 slides):

- 00–00:30 Uvod · 00:30–01:30 Prisutnost · 01:30–02 QR (shared) · 02–02:30 Nastavnici · 02:30–03:30 Čime se kolegij bavi · 03:30–04:30 Teme · 04:30–05:30 Praktični rad · 05:30–06:30 Priprema za projekt · 06:30–07:30 Informacije i pomoć · 07:30–09:30 BPMN · 09:30–10:30 Predaja, oslobođenje i obrana · 10:30–11 Rok predaje · 11–12 Akademska godina · 12–13 Commitovi · 13–14:30 Objasnite projekt · 14:30–15:30 Izmjena koda uživo · 15:30–16:30 Uporaba AI-ja · 16:30–17:30 AI alati · 17:30–20 Prije prvog tehničkog predavanja i pitanja

Checks: `just slides 00-course-introduction` and `just browser-check 00-course-introduction` (Croatian) passed for 19 slides: no overflow, missing images or runtime errors. Screenshots of changed slides visually reviewed; the QR payload was decoded.

- [ ] Lecturer review of the new Croatian slides, especially the team wording ("rad svakog člana") and the live-change examples.
- [ ] English translation of this revision, followed by `timing.json` update and `just language-check 00-course-introduction`.

2026-10-13 wording: lecturer chose the course-overview row "Arhitekture i komunikacija komponenti" instead of "Osnove i komunikacija". Croatian only; English row pending translation.

2026-10-13 — Lecturer replaced the live code change with an explanation of a change on the student's own code: where the change would go, how it would be made, and its consequences, followed by the lecturer's questions. Reason: a live-change task can be pasted into an AI tool. Optionally, a small change may be shown in code without AI tools. The slide "Izmjena koda uživo" became "Dorada projekta: objasnite izmjenu"; `live-change` assets were removed and replaced by `design-change.{hr,en}.svg/.pdf`. This rule differs from the WA deck, which still uses a live code change.

2026-10-13 — Typography and order (Croatian):
- `assets/lecture.css` now defines tokens for one type scale (body 28 px, cards 23 px, captions 20 px), one accent colour (#105d80) for bold text and links, and one card style. Links no longer use Reveal's default bright blue. The deadlines diagram lost its uppercase coloured labels; booking moved to the slide text, and the exemption sits in a neutral card.
- At the lecturer's request, AI use and recommended tools now open the project block, followed by commits, passing rules and defence. New order and timing: Informacije i pomoć 04:30–05:30 · Praktični rad 05:30–06:30 · Priprema 06:30–07:30 · Uporaba AI-ja 07:30–08:30 · AI alati 08:30–09:30 · Commitovi 09:30–10:30 · BPMN 10:30–12:30 · Predaja, oslobođenje i obrana 12:30–13:30 · Rok predaje 13:30–14 · Akademska godina 14–15 · Objasnite projekt 15–16:30 · Dorada projekta 16:30–17:30 · Prije prvog tehničkog predavanja 17:30–20. Slides before Informacije keep their times; still 19 slides / 20 minutes.
- Browser check passed; all 19 screenshots reviewed.

2026-10-13 — Added two slides after the QR check-in: "Što predavanje daje, a AI i snimka ne daju?" (honest framing and four cards) and "Različiti studenti, različiti razlozi" (table of student types). 21 slides / 20 min: Prije prvog tehničkog predavanja 2.5 → 1.5 min, Pripremite se objasniti 1.5 → 1 min. The lecturer should confirm the wording "Ako samo slušate, snimka vam je jednako dobra" and the grade-focused row.

## Nadogradnja za diplomski rad / RITR — 2026-10-14



Na nastavnikov zahtjev u hrvatski deck je dodan slajd „Nadogradnja aplikacije za diplomski rad”, preuzet iz BA uvoda, iza „Priprema za projekt”. Sadržaj: nadogradnja po želji i uz odobrenje nastavnika; RITR (5. godina) 6 ECTS ≈ 180 h, diplomski rad 30 ECTS ≈ 900 h (NN 119/22, čl. 67. st. 2.: 1 ECTS = 30 h); vlastiti repozitorij i README s napomenama o tome što je napravljeno prije, što kasnije i za što. Bilješke prema AGENTS.md nemaju redak s vremenom. Otvoreno: timing.json i ovaj README još opisuju engleski deck od 14 slajdova; hrvatski deck sada ima 22 slajda, a engleski prijevod slijedi nakon pregleda. Headless provjera (hr): PASS.

2026-10-14: koraljni detalji kao u BA uvodu, uz zadržanu paletu: --coral #e4572e, samo ukrasno. Crta ispod naslova (centrirana na slajdu evidencije prisutnosti, izostavljena na BPMN slajdu) i traka slijeva na karticama. Prijašnji CSS spremljen je u scratchpad BA sesije. Headless provjera (hr): PASS.

## Hrvatsko poglavlje (PDF skripta), 2026-10-30

Na nastavnikov zahtjev dodan je `chapter.hr.qmd`: pisani pratitelj uvoda, izveden iz hrvatskih slajdova (v1.6) i potvrda u `sources.md`. Nema novih pravila. Izvorni BPMN prikazan je uz opis triju promijenjenih pravila (3 radna dana, ukinuto pravilo od 7 dana, commitovi). Poglavlje nije u knjizi; `lecture.json` i dalje označava format samo sa slajdovima za knjigu i `verify_builds.py`. Engleskog poglavlja nema.

- Build: `just lecture 00-course-introduction` → `output/hr/lectures/00-course-introduction.pdf` (10 stranica); sve stranice vizualno pregledane.
- `scripts/build.py all` sada gradi samo jezik koji ima izvor, pa EN `just all` ne pokušava graditi ovo poglavlje.
- [ ] Nastavnikov pregled teksta poglavlja.
