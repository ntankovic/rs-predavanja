# Internal sources and confirmation record

Reviewed 2026-09-14. Internal provenance is not displayed as student reading.

| Source | PDF page | Used for | Status |
| --- | --- | --- | --- |
| Nikola Tanković, RS-01-Intro.pdf, 2022/23 | 1 | Author and historical year | Historical identity confirmed on cover |
| Same | 3 | Theory plus small-project learning goals | Rephrased as course goals |
| Same | 4 | Microservices and distributed data analysis practical themes | Historical; current briefs not confirmed |
| Same | 5 | Optional attendance; individual projects; GitHub progress; project defence and oral exam | Exact administrative content checked in text and rendered source page; current applicability unconfirmed |
| Same | 6 | Help through documentation, Slack, colleagues, assistant, consultations | Rewritten as generic study guidance; current channels unconfirmed |
| Same | 2 | Old attendance short link | Excluded; not verified as a current student resource |
| COURSE.md | Current plan | Identity, proposed sequence, language | Project requirements, not official university assessment policy |

No numerical weights, pass thresholds, number of projects, deadlines, retake arrangements, contact address, or current policy URL were established. No public reference is offered as evidence for current local assessment rules. Project-defence preparation prompts are original study guidance, not an official rubric.

Before classroom release, the lecturer must confirm or replace the historical rules, supply the missing administrative details and official student-accessible links, and remove draft/historical labels only for confirmed content. Record the confirmation date and source here.

2026-09-17 — Lecturer explicitly supplied `http://bit.ly/rs-tu-sam` as the presence check-in URL and requested it with a QR code on slide 2 of every deck. This supersedes the earlier decision to exclude the old attendance link; it does not confirm an attendance obligation. Teaching staff and assessment-flow revision remains pending the newer PDF offered by the lecturer.
2026-10-12 — Lecturer requested the HTTPS form `https://bit.ly/rs-tu-sam`; the shared QR code was regenerated with Python `qrcode` 8.2 (medium error correction, four-module quiet zone) and decoded to confirm the URL.

## Lecturer-supplied BPMN and staff update, 2026-09-17

- Original image: `assets/hodogram_rs.png`, copied unchanged from the lecturer-supplied `/Users/ntankovic/Downloads/hodogram_rs.png`. This is the visual authority for the included process and its annotations.
- Supporting editable source: `assets/hodogram-original.bpmn`, copied unchanged from `../hodogram.bpmn`; retained for provenance, not assumed pixel-identical to the supplied PNG.
- Staff responsibility confirmed in conversation: lectures — Nikola Tanković; practical classes — Luka. Full name/title for Luka awaits the newer deck.
- The diagram supplies previously missing information: practical points and project work in parallel; 7-day submission lead time; oral-exam exemption conditions (at least 50% of practical points, no disputed project parts, lecturer discretion, valid through academic year); defence at least 3 days after submission and by exam day; re-registration after failure; commits every 1–2 days and authenticity checks. These supersede earlier claims that the supplied material established no thresholds or timing. No overall grading weights or current calendar dates are inferred.
- English process overview is a provisional translation of the lecturer-supplied Croatian diagram; original Croatian artwork is preserved.

## AI policy confirmed 2026-09-17

The lecturer explicitly permits AI use, restricted to technologies used in lectures or approved by the professor. Students must understand every part of generated code and prove that they guided architectural decisions, including the reasoning, alternatives, and tradeoffs. “Architecture is a set of informed choices” is the lecturer's framing. No prompt-log submission or specific disclosure format was requested. This supersedes the earlier statement that AI-use permission was unresolved. Croatian wording is recorded in `ai-policy.hr.md`; English slide wording remains pending language review.

2026-09-17 — Lecturer confirmed the practical-class instructor’s full name and title: **Luka Blašković, mag. inf.** This resolves the earlier pending staff-name item.

2026-09-17 — Lecturer clarified that the BPMN describes how to pass the **course**, not merely the exam. The oral exam is one possible path; exemption provides another. Updated slide titles and teaching notes accordingly.

2026-09-17 — Lecturer rejected the “Assessment details still to be announced” placeholder: the supplied BPMN is authoritative for these process rules. Replaced the slide with submission timing, exemption conditions and validity, registration on both paths, defence timing, and re-registration after an unsuccessful result.

2026-09-17 — Lecturer confirmed course-information locations: E-Učenje, https://e-ucenje.unipu.hr/, and the course web page, https://ntankovic.unipu.hr/rs. Added both as clickable links. This resolves the previously missing course-information links.

2026-09-17 — Lecturer confirmed: consult course materials before asking; all questions go first to Google Chat under **FIPU RS**. Email is discouraged. This resolves the current help-channel question and supersedes legacy Slack guidance.

## Course page review, 2026-09-17

Reviewed public Notion course page https://fiputreca.notion.site/Raspodijeljeni-sustavi-544564d5cc9e48b3a38d4143216e5dd6 through its public page-data response.

- Lecturer confirmed all lectures are recorded on YouTube. Page supplies playlist: https://www.youtube.com/playlist?list=PLIeA2EYS12RVaj1GdVP4fkNrLiK5k6VD-. Added to the course-information slide.
- “Potrebna znanja programskog jezika Python” supplies the programming-preparation checklist. Summarised in English; language review pending.
- Page confirms Nikola Tanković, Luka Blašković, and the attendance short link.
- Do not copy stale/conflicting communication details: page includes Slack, “FIPU 24/25 RS”, a 2025–2026 Moodle link, and a statement that the traditional e-learning portal is unused. Current lecturer instructions take precedence: Google Chat **FIPU RS**, https://e-ucenje.unipu.hr/, and https://ntankovic.unipu.hr/rs.
- Other links (old Zoom and assignment submission) were not promoted as current instructions.

2026-09-17 — Lecturer added: exempt students must note their exemption; appointment booking is at https://ntankovic.unipu.hr/termin, with appointments available 10 days in advance. Added to the assessment slide and teaching notes.

2026-09-17 — Lecturer correction: the minimum interval between submission and defence is **3 working days**, not 3 calendar days. This supersedes the original BPMN image’s “3 dana”. The source image is preserved unchanged; its slide explicitly displays the corrected rule, and all teaching notes use working days.

2026-09-17 — Lecturer added Docker Compose and Docker Swarm to the programming-preparation checklist.

## Original explanatory diagrams, 2026-09-17

Created five editable bilingual diagrams in `assets/build_diagrams.py`, with `.hr.svg`, `.en.svg`, and corresponding vector PDF exports. No third-party stock artwork was incorporated.

- `course-completion`: simplified from the lecturer-supplied `hodogram_rs.png`; preserve original attribution and use the full BPMN on the following slide. Arrows show parallel inputs, exemption alternatives, and repeat registration after an unsuccessful result.
- `deadlines`: lecturer-supplied rules and corrections: ≥7 days before exam, ≥3 working days between submission and defence, defence by exam day, booking availability 10 days ahead. Intervals are schematic, not a calendar.
- `attendance-explained`: lecturer-confirmed check-in link and participation guidance; no claim that attendance is compulsory or points-bearing.
- `ai-responsibility`: lecturer-confirmed policy; student chooses architecture, directs AI, and remains accountable for code and reasoning.
- `practical-work`: original illustrative request-flow and split/process/combine examples of the already stated themes. Request arrows omit replies; data arrows show data flow.

Croatian and English labels were authored together with Croatian first in the source; English wording remains pending lecturer review.

2026-09-17 — Lecturer confirmed attendance is optional. In lecture 00 only, attendance explanation precedes the QR slide and has no repeated URL.

2026-09-17 — Lecturer removed the 7-day submission rule. Current deadline guidance uses at least 3 working days between submission and defence, with defence no later than the exam date. Removed the 7-day interval from both language diagrams, alt text, and teaching notes. The unchanged source BPMN image contains historical wording superseded by this instruction.

## External artwork added 2026-09-17

- **Teaching**, Katerina Limpitsouni / unDraw: https://undraw.co/illustration/teaching_58yg. Original SVG: https://cdn.undraw.co/illustrations/teaching_58yg.svg. Original saved as `assets/undraw-teaching.original.svg`; derivative `undraw-teaching.svg` changes only the purple accent to FIPU blue (#1585b4). Attendance slide.
- **Online learning**, Katerina Limpitsouni / unDraw: https://undraw.co/illustration/online-learning_tgmv. Original SVG: https://cdn.undraw.co/illustrations/online-learning_tgmv.svg. Original saved as `assets/undraw-online-learning.original.svg`; derivative changes only the accent to FIPU blue. Course information slide. Both use https://undraw.co/license (free use/modification; no required attribution); visible source links are included voluntarily.
- **Server racks in data center**, imgix / Unsplash, published 2017-09-26: https://unsplash.com/photos/server-racks-in-data-center-klWUhr-wPJ8. Image CDN: https://images.unsplash.com/photo-1506399558188-acca6f8cbf41?fit=max&fm=jpg&q=85&w=1800. Saved as `assets/server-racks.jpg`; CSS crops the display, source bytes unchanged. License: https://unsplash.com/license. Course-goals slide, with visible credit. This is illustrative infrastructure, not claimed to belong to the university.
- **YouTube icon**, official source https://brand.youtube/youtube-icon/. Image: https://www.gstatic.com/marketing-cms/assets/images/96/ff/14b02dc0467e8875e062e9565cbd/external-icon-core-1.png. Saved unchanged as `assets/youtube-icon.png`. CSS crops surrounding presentation whitespace while preserving the full mark and proportions. Icon is next to and linked to the course playlist; colours unchanged. Brand guidance: https://brand.youtube/ and https://about.google/brand-resource-center/guidance/ (educational use). No endorsement implied.

All assets retrieved via `just download-image`. Accessed 2026-09-17. Originals retained; not redistributed as an asset pack.

2026-09-17 — At the lecturer’s request, removed visible unDraw and Unsplash credits from slides. Their licenses do not require attribution. Full source and license records remain here.

2026-09-18 — Lecturer replaced the E-Učenje URL with https://moodle.srce.hr/. Applied to Croatian and English slides; supersedes the previously confirmed e-ucenje.unipu.hr URL.

2026-10-12 — Visuals adapted from the Web Applications lecture 00 (`FIPU-WA/wa-predavanja-v2/lectures/00-course-introduction`) at the lecturer's request:
- Calendar, academic-year, commit-history and step diagrams were redrawn from that deck's `build_orientation_visuals.py` and `build_wa_diagrams.py`, with distributed-systems labels. Commit names, dates and hashes are fictional.
- Annual leave (20 Jul–25 Aug), the 30 Sep academic-year end, the rule for an undefended project (re-register and build a new individual project, approved by the lecturer), the live code change and commit checks: the lecturer confirmed on 2026-10-12 that the WA rules also apply to this course.
- Technology icons (Python, asyncio, FastAPI, Docker) are original simplified identifiers in the style of the familiar marks. They are not downloaded official logos, and the trademarks belong to their owners.
- `claude-app.png` and `codex-app.png` were copied unchanged from the WA deck. That deck extracted them from the installed `Claude.app` and `Codex.app` `electron.icns`. AI-tool and open-model links and claims follow the WA deck's sources, checked on 2026-10-07; they were not re-verified on 2026-10-12.

2026-10-13 — Lecturer relaxed the commit rule: a few commits a week, with work on the project spanning at least 2–3 weeks. This supersedes "a commit every 1–2 days" in the original BPMN (`hodogram_rs.png` / `hodogram-original.bpmn`), which still shows the old wording; the speaker notes say so. The Croatian slide, notes and commit-history visual were updated; English pending translation.

2026-10-13 — Lecturer replaced the live code change with an explanation of a change on the student's own code: where the change would go, how it would be made, and its consequences, followed by the lecturer's questions. Reason: a live-change task can be pasted into an AI tool. Optionally, a small change may be shown in code without AI tools. The slide "Izmjena koda uživo" became "Dorada projekta: objasnite izmjenu"; `live-change` assets were removed and replaced by `design-change.{hr,en}.svg/.pdf`. This rule differs from the WA deck, which still uses a live code change.
- Zakon o visokom obrazovanju i znanstvenoj djelatnosti, NN 119/22, čl. 67. st. 2. (https://narodne-novine.nn.hr/clanci/sluzbeni/2022_10_119_1834.html, provjereno 2026-10-14): 1 ECTS = 30 sati studentskog rada. UNIPU Pravilnik o studiranju (pročišćeni tekst 2019., https://www.unipu.hr/_download/repository/2019-09-30-Pravilnik_o_studiranju-procisceni_tekst%5B1%5D.pdf) ne propisuje sate po bodu. Koristi se na slajdu o diplomskom radu i RITR-u.
