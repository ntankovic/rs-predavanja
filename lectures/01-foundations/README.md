# Foundations and system models

## Current language synchronization (2026-09-19)

English `slides.qmd` is the anchor for this revision, explicitly selected by the lecturer. `slides.hr.qmd` mirrors its 39-slide sequence, definitions, examples, staged answers, source links and 60-minute timing. Both versions use concise speaker-note bullets. Croatian introduces technical vocabulary with English terms in parentheses; proposed translations remain pending lecturer review. The detailed chapter remains English; this pass translates the slide deck, not the chapter.

Diagram labels have Croatian variants; geometry and colour semantics follow the English sources. PDF attendance layout now uses normal flow rather than percentage-based absolute positioning. Browser verification includes a PDF-mode check of the QR and link and saves a full slide PDF for review.

Earlier progress entries below are historical; their slide counts describe previous revisions.

Synchronization review checklist:

- [x] Same slide sequence and 60-minute timing; English remains the anchor.
- [x] Definitions 1.1–1.7, classification reveals and safety/liveness reveals retained.
- [x] Technical examples, conditional guarantees and sources preserved.
- [x] Concise bullet notes in both languages; English technical terms introduced in Croatian slides.
- [x] Croatian diagram labels and PDF derivatives prepared; dense translated slides visually inspected and adjusted.
- [x] `just language-check 01-foundations` verifies timing, definitions, reveals, links and asset correspondence.
- [x] English and Croatian browser checks pass for 39 slides; QR/link fit in PDF mode. Review PDFs are saved alongside QA screenshots as `slides-print.pdf`.
- [ ] Lecturer review of Croatian wording and classroom pacing. No unresolved technical question introduced in this synchronization.

Safety/liveness comparison added immediately after the definitions: payments, seat booking, job queues and distributed locks. Deck now has 33 slides with the 39–41 minute segment split between definitions and examples; total remains 60 minutes. Chapter and Croatian drafting notes include the corresponding claims and progress assumptions.

Retry transition: 32 slides, still 60 minutes. The 37–39 minute segment now gives one minute to why attempts overlap and one minute to the invariant. Explicit teaching point: a timeout means the caller gave up waiting; it does not destroy the request. Multi-tier caller roles and chapter explanations are included.

Multi-tier timeout introduction added before History A: 31 slides, still 60 minutes. The 26–28 minute segment now gives one minute to partial failure and one minute to client roles and waiting deadlines. Chapter, diagram, Croatian drafting notes and timing.json updated; lecturer review remains pending.

History C added: server process crash after durable acceptance, before reply. Histories A–C and their comparison now share a consistent visual style. There are 30 slides; the 28–32 minute history segment is split 1.5 + 1.5 + 1 minutes, preserving the 60-minute total. Chapter, timing and illustration sources are aligned.

TTFB refresher added after latency/bandwidth/throughput: 29 slides, 60 minutes. The existing 23–26 minute segment now assigns 23–25 to performance concepts and 25–26 to Web Apps recall. Chapter, editable diagram, source record and timing.json updated. Croatian draft and English wording remain subject to lecturer review.

Latest classification exercise: added “Distributed system or not?” immediately after Definition 1.1, with six examples including the three-process MPI temperature average. The deck now has 28 slides; 10–12 minutes cover this discussion and 12–14 minutes cover the workload question. Total remains 60 minutes. Chapter examples and Croatian draft updated; lecturer review pending.

Latest model-example revision: 26 slides, 60 minutes. The model introduction now defines the abstraction and gives a portal model. Node models have concrete portal examples; a separate timing-example slide shares the existing 51–53 minute segment with the diagram. Croatian draft: `model-examples.hr.md`; language review remains pending.

- Number: 01
- Owner: coordinating agent
- Status: review
- Teaching languages: English anchor; synchronized Croatian slide draft pending review
- Intended duration: 60 minutes, including discussion and recap
- Prerequisites: programming, functions, processes, and basic networking
- Deliverables: English student chapter; 39-slide English and Croatian decks with bilingual terminology, vector diagrams and discussion exercises

## Learning outcomes

Students should be able to identify participants and messages; justify distribution and its costs; distinguish concurrency from parallelism; explain partial failure and uncertain outcomes; and state basic models and invariants.

## Scope

The project-submission running example connects definitions, transparency, communication, failures, and assumptions. Detailed architectures, RPC implementations, clock algorithms, consensus, Byzantine agreement, and transactional mechanisms are deferred. The depicted system is hypothetical.

## Timed outline

Timings include explanation and student participation. `timing.json` is the machine-readable plan; matching cues appear in speaker notes. This is a 60-minute plan, not a claim of completed classroom rehearsal.

| Slide | Minutes | Topic |
| --- | --- | --- |
| 1 | 00–0:30 | Foundations and system models |
| 2 | 0:30–01 | Mark your presence (shared slide) |
| 3 | 01–03 | A timeout after submission |
| 4 | 03–04 | What do we need to know to answer? |
| 5 | 04–07 | A project-submission system |
| 6 | 07–09 | What makes it distributed? |
| 7 | 09–11 | Distributed system or not? |
| 8 | 11–13 | Must everyone wait for one submission? |
| 9 | 13–15 | Several submissions can make progress together |
| 10 | 15–16 | Dealing with tasks vs. doing them |
| 11 | 16–18 | Why distribute the work? |
| 12 | 18–19 | Facebook: scale changes the architecture |
| 13 | 19–21 | Local function calls and remote requests |
| 14 | 21–23 | Delay, capacity, and completed work |
| 15 | 23–24 | Recall Web Apps: time to first byte |
| 16 | 24–25 | One component fails; others keep running |
| 17 | 25–26 | A client can be another service |
| 18 | 26–27:30 | History A: the request is lost |
| 19 | 27:30–29 | History B: the reply is lost |
| 20 | 29–30 | History C: the server process crashes |
| 21 | 30–31 | Same observation, different outcomes |
| 22 | 31–34 | Pair exercise: should the client retry? |
| 23 | 34–35 | A retry can overlap the original request |
| 24 | 35–36 | State the rule before choosing the protocol |
| 25 | 36–37 | Safety and liveness |
| 26 | 37–38 | Safety and liveness in different systems |
| 27 | 38–40 | A system model makes assumptions explicit |
| 28 | 40–42 | Network assumptions: can messages get through? |
| 29 | 42–44 | Three node-failure models |
| 30 | 44–45 | How long should the portal wait? |
| 31 | 45–47 | Timing models: what may we assume? |
| 32 | 47–49 | etcd: one successful claim |
| 33 | 49–51 | Cassandra: choose what a reply promises |
| 34 | 51–53 | Bitcoin: confidence grows with confirmations |
| 35 | 53–54 | Our portal: assumptions behind the promise |
| 36 | 54–56 | No reply after 101 ms |
| 37 | 56–57 | 🔥 How to develop a bad system |
| 38 | 57–58 | A checklist for distributed-system reasoning |
| 39 | 58–60 | Design the next step: did I submit on time? |

## Review checklist

- [x] Chapter and slides cover the planned learning outcomes.
- [x] Legacy sources are mapped and cited; historical administration and statistics are excluded.
- [x] Seven original diagrams have editable sources, vector exports, captions, and alternative text.
- [x] Network, node, and timing assumptions are distinguished.
- [x] Exercises include suggested reasoning in the student chapter.
- [x] Speaker notes include teaching prompts and timing totaling 60 minutes.
- [x] Lecturer and faculty names and the supplied logo are included.
- [x] Final rendered-output review recorded below.
- [ ] Lecturer has reviewed pacing and emphasis for classroom delivery.

## Build and visual verification

Build with `just lecture 01-foundations`, `just slides 01-foundations`, and `just book`. Structural checks run through `python3 scripts/verify_builds.py` or a full `just test`.

Rendered-output review completed: the 12-page lecture PDF, all 22 slide screenshots, and the 28-page combined book were visually inspected for layout and diagram readability. Structural verification passed for all course outputs. `just browser-check 01-foundations` passed in headless Chrome with no detected slide overflow, missing images, or JavaScript errors; screenshots and the browser report are saved in `output/qa/01-foundations/`.

Table and reference update verified: bold headers and alternating white/light-gray body rows render in both PDF formats and HTML slides. Public references replace internal filenames in the exported chapter and speaker notes; legacy provenance remains in `sources.md`. The rebuilt deck passed the 22-slide browser check.

The lecture remains in review pending the lecturer's assessment of pacing and emphasis. The 60-minute timing is a plan, not a completed classroom rehearsal. The remaining eleven lectures are still sample scaffolds.

The running example is a signed-in, enrolled student submitting a 20 MB project. The four participants are the browser, submission service, assignment service (deadlines and file rules), and submission storage (files and accepted records). Upload completion is distinct from acceptance. The core invariant is one accepted entry per intended submission despite retries; intentional revisions follow a separate version policy.

Project-submission revision verified: all 22 slides passed headless Chrome checks; changed slides and all lecture pages were visually reviewed, along with the revised chapter in the combined book. Final outputs remain a 12-page lecture PDF and 28-page book. Public-reference access conditions and verification evidence are recorded in `sources.md`.

Lecturer feedback update (2026-09-15): standalone PDFs now identify the course and lecture number above the topic. Learning outcomes explain invariants in plain language, with a footnote recalling idempotency from Web Apps; speaker notes carry the same connection. The opening example describes a ZIP containing a Unity game project, source code, scenes, and resources. The heading uses “Example”. These preferences are recorded in `COURSE.md`. Rebuilt the lecture PDF, combined book, and slides; structural verification and the 22-slide browser check passed. Visually checked the revised title, footnote, example pages in both PDF formats, and the two changed slides. The lecture remains in review while lecturer feedback continues.

Diagram and definition review (2026-09-15): centered complete label groups using glyph bounds; added explicit caller/dependency arrow semantics and a separate footer area below the system-map and partial-failure diagrams. Added the shared red definition style with Definition 1.1 in chapter and slides. Updated `COURSE.md` with these conventions. Rebuilt SVG/PDF artwork, the lecture PDF (now 13 pages), the combined book (28 pages), and all 22 slides. Structural checks and the browser check passed; visually reviewed the changed diagram and definition pages in lecture/book PDFs and slides 4, 5, 9, and 11. Lecturer review remains ongoing.

Definition expansion (2026-09-15): added matching Definitions 1.2–1.7 for concurrency, parallelism, partial failure, invariants, safety, and liveness. The shared style now uses a 10 px left border in HTML and 5 pt in PDF. Added one safety/liveness slide and split the existing 53–57 minute segment into two two-minute segments; total teaching time remains 60 minutes. Updated chapter, slides, timing plan, shared definition filter, and course conventions. All seven definition texts and numbers match between chapter and slides. Rebuilt the 14-page lecture PDF, 29-page combined book, and 24-slide deck. Structural verification and the 24-slide browser check passed; visually reviewed new definitions, thicker borders, and associated diagrams in PDF and HTML. Lecturer review remains ongoing.

Illustration and model explanation update (2026-09-15): replaced the text-only performance slide with an original delivery analogy informed by the inspected legacy RPC slides (provenance in `sources.md`), added matching chapter artwork and explanation, and explained how treating typical latency as a bound can mistake a slow server for a crashed one. Renamed slide 9 to “Local function calls and remote requests” in slides and timing records. The shared footer and stronger progress bar are also rendered. Rebuilt the lecture PDF (15 pages), combined book (30 pages), and slides (23); structural and browser checks passed. Visually checked both changed slides and the corresponding lecture/book pages. Timing remains 60 minutes; lecturer review is ongoing.

100 TB thinking question (2026-09-15): added to the performance slide and chapter, with guided comparison of network transfer and physical drive transport. Speaker notes reserve the last minute of the existing 24–27 minute segment for student suggestions. The 60-minute plan and slide count are unchanged.

100 TB export verification: rebuilt lecture PDF, book, and slides; structural checks and the 24-slide browser check passed. Visually reviewed the question on slide 10 and its discussion in both PDF outputs. No new unresolved issues; lecturer review remains ongoing.

Narrative review (2026-09-15): aligned chapter and slides around problem → motivation → communication/failure → retry → concurrency → correctness → assumptions. Concurrency is now slide 15, immediately after the retry exercise, and connects both to capacity and to overlapping attempts. Invariants and safety/liveness follow before the system models. Renumbered Definitions 1.2–1.4 in order of introduction and updated all slide timing cues, the timed outline, and illustration placements. The large-university example explicitly asks whether 20-minute checks prevent others from submitting; the chapter distinguishes receiving, queueing, overlapping waits, and parallel workers. Reference review restored explicit resource-sharing, openness, transparency, and scalability motivations. All seven definitions match between chapter and slides; the deck remains 23 slides and 60 minutes. Structural and browser checks passed, and changed slide layouts and PDF story sections were visually reviewed. Lecturer review remains ongoing.

Second narrative review (2026-09-15): implemented the five review improvements and recorded the result in `narrative-review.md`. Workload and concurrency are now adjacent on slides 6–7, broader motivations follow on slide 8, and retries reuse concurrency on slides 15–16. Corrected the liveness example, added the explicit return from 100 TB to portal response time, and reserved the numerical timing example for the final exercise. Updated chapter order, seven definition numbers, slide notes, the 60-minute plan, and illustration placements. Built the 16-page lecture PDF, 31-page combined book, and 24-slide deck. Structural and browser checks passed; changed PDF/HTML layouts were visually reviewed. No further ordering change recommended; lecturer pacing review remains open.

Closing-question review (2026-09-15): replaced the abstract “two histories” exit prompt with a classmate's timeout/retry claim. Students explain what the timeout establishes and what a retry must avoid. Rewrote recap and final-slide notes as purpose, timed teaching cues, expected answers, misconceptions, and a transition. Added the same final check to the chapter and recorded the notes convention in `COURSE.md`. Fixed singular “1 minute” in the notes. Rebuilt PDF/book/slides; structural and 24-slide browser checks passed, and the final slide and PDF check were visually reviewed. The planned lecture still totals 60 minutes and remains in review.

Open design ending (2026-09-15): replaced recall-based closing with the midnight deadline / 23:59 upload / 00:19 checks challenge. Notes guide proposals about saved evidence and displayed status, distinguish receipt from validation, and end with a crash-during-checks question. The recap now takes 57–58 minutes and the design discussion 58–60; the 24-slide plan still totals 60 minutes. Updated chapter, slides, timing, narrative review, and course-wide ending convention. Rebuilt all affected exports; structural and browser checks passed, and final slide/PDF sections were visually reviewed. Lecturer review remains open.

Title-slide logo (2026-09-15): added a 140 px FIPU logo above the title, aligned left, using the existing shared SVG. Adjusted title-slide spacing and recorded the preference in COURSE.md. Rebuilt the HTML deck and visually checked the title slide.

Attendance update (2026-09-17): the shared build adds presence check-in as slide 2. Welcome and check-in together occupy 00–01 min; subsequent teaching segments retain their timing.

### Visual update, 2026-09-17

Five additional bilingual vector figures added to the existing chapter and slides. Duration remains 60 minutes and deck remains 24 slides. Croatian labels are drafted; lecturer language review remains pending.

Visual review: HTML rebuilt, all 24 slides passed `just browser-check 01-foundations`, and all five changed slides were inspected as rendered screenshots. Chapter PDF rebuilt and page layouts inspected; retry figure placement corrected to its matching section. Source provenance and illustration plan updated. No new technical claims or timing changes. Lecturer review remains pending.

2026-09-17 visual review: added the client-observation timeline to “No reply after 101 ms” and chapter exercise 4. Clarified timing-model rows with explicit before/after stabilization labels, more vertical space, and a shaded middle row. Updated bilingual SVG/PDF assets, editable generators, illustration/source records, and the matching timing.json slide title. `just slides 01-foundations`, `just lecture 01-foundations`, and `just headless-preview 01-foundations` passed. Slides 21–22 and PDF pages 16–17 visually inspected; 24 slides / 60 minutes retained. Croatian figure labels and English translations remain pending lecturer language review. Lecture status remains review.

2026-09-17 motivation review: added “Why timing assumptions matter” after the timing-model diagram, connecting failure suspicion, safe overlapping retries, and conditional progress. Expanded the chapter explanation and teaching notes; Croatian review draft retained in `timing-motivation.hr.md`, language review pending. Timing-model explanation now takes 51–53 min and motivation 53–54 min; 25 slides still total 60 minutes. Updated the brief's full timing table from timing.json. HTML/PDF rebuilt, new slide and chapter pages 15–16 visually checked, and headless checks passed for all 25 slides. Status remains review.

## Story-first revision, 2026-09-17

Implemented the lecturer-approved narrative: situation → prediction → examples → definition → consequence for the portal. Visible warmups precede the distributed-system definition, concurrency/parallelism, remote calls, performance measures, partial failure, safety/liveness, and system models. The retry race motivates the invariant. Assumptions now occupy 41–53 min; repeated timeout walkthroughs are shorter. The lecture has 27 slides and retains 60 minutes including discussion, QR check-in, recap and a three-minute final design challenge.

- Updated: `slides.qmd`, `chapter.qmd`, `timing.json`, this brief, `illustrations.md`, `sources.md`, and `story-review.hr.md`.
- Chapter: added network assumptions and a combined portal model; exercise 7 asks students to state assumptions and reason about permanent partitions. WWW/local/LAN comparisons are optional reading.
- Croatian editorial plan: `story-review.hr.md`. Croatian wording and English implementation remain pending lecturer language review; this is not a completed Croatian lecture translation.
- [x] Outcome coverage checked; all five chapter outcomes appear on the opening slide.
- [x] Definitions 1.1–1.7 retain numbering and meaning.
- [x] Timing is contiguous and totals 60 minutes; all slide notes match timing.json.
- [x] `just slides 01-foundations` and `just lecture 01-foundations` completed.
- [x] `just headless-preview 01-foundations` passed for 27 slides with no overflow, missing images or runtime errors. All slide screenshots and affected PDF pages visually inspected.
- [ ] Lecturer pacing and wording review. Status remains `review`; the 60-minute allocation is a plan, not a classroom rehearsal.

2026-09-18 — Lecturer classified slide 3, “A timeout after submission”, as an Example. Updated its slide class and added a matching Example label in lecture.css; content and timing unchanged.

2026-09-18 — Slide 4 now frames the learning route as questions needed to resolve the opening timeout, and transitions directly to tracing the project through the portal. Formal chapter outcomes unchanged; timing remains 04–05 min.

## Real-system examples — 2026-09-19

Added slides 30–32 (etcd, Cassandra, Bitcoin) before the portal summary. Six minutes for these examples are balanced by one-minute reductions in the concurrency walkthrough, pair retry exercise, network comparison, timing comparison, 101 ms exercise, and final design exercise. Total remains 60 minutes, including discussion and recap. Chapter explanations and primary-source notes match the slides. Croatian draft in `real-systems.hr.md`; lecturer content, translation and pacing review remain pending.

Verification: slides and chapter PDF build successfully; browser checks pass for all 36 slides. New example slides visually inspected for readable text, complete qualifications and no clipping. Claims checked against linked primary documentation. No known unresolved technical claims; classroom pacing and language review remain open.

## Visual and legacy-slide review — 2026-09-19

Restyled the 101 ms observation and illustrated the reasoning checklist. Added the Rob Pike quote with original cooking analogy, a Facebook scaling example with logo and verified historical MAUs, and the eight hidden assumptions near the recap. Three new one-minute slides are funded by one minute each from the opening vote, concurrency walkthrough and motivations discussion. Total remains 60 minutes, now 39 slides. Scaling details remain in Lecture 11; asynchronous communication and replication remain in 03/10 and 06. Croatian draft and English translation pending lecturer review. See `visual-additions.hr.md`.

Validation: English slides and chapter PDF rebuilt successfully; all 39 slides passed browser layout checks. Inspected the new quote/illustration, Facebook, hidden-assumptions, checklist and 101 ms slides. Simplified the concurrency lead afterward to leave more space above its definitions, then rebuilt. Editable SVGs and PDF derivatives were generated for both languages; language and classroom pacing approval remain open.

2026-10-13 wording: lecturer chose "Pratimo tijek predaje našeg projekta kroz komponente portala." (slide 2). English anchor aligned: "Let’s follow our project’s submission through the portal’s components." Translation review pending.

2026-10-13 — At the lecturer's request, "Why distribute the work?" (slides hr/en and chapter section 6) now centres on three main reasons: components are physically apart, more capacity is needed, and the system must survive failures (redundancy). Hence almost every information system is distributed. Resource sharing, openness and transparency moved to further goals (chapter) and speaker notes. Slide timing unchanged. Checks: hr browser check passed (39 slides); English slides and the English chapter PDF built; the chapter page was reviewed. Translation review pending.

2026-10-13 — Homework slide added at the lecturer's request: "Domaća zadaća: računi 1, 2, 3, …" / "Homework: invoices 1, 2, 3, …", a sequential invoice-numbering problem from the lecturer's practice. It is assigned, not solved in class (59:30–60). The design challenge before it is 58–59:30. Now 40 slides / 60 min; `timing.json` updated. Chapter exercise 8 and its suggested reasoning added. The speaker-note hint about Croatian fiscal invoice numbering (number/premises/device) is flagged for verification against the current regulation. Checks: hr browser check passed; English slides and chapter PDF built; language check passed.

2026-10-13 — The homework closing question now asks whether any solution gives up nothing (availability, speed, strict sequence), and if not, what to give up. Notes and chapter reasoning state the expected conclusion: a gapless sequence needs coordination, so a partition or coordinator crash forces waiting or losing the sequence. Links to Lectures 06, 07 and 09.

2026-10-13 — Story review, points 1 and 3, both languages:
- New "Istek čekanja (timeout)" / "Timeout" slide (25:30–26) before histories A–C. It takes the timeout definition out of "Klijent može biti i druga usluga" (now 25–25:30, roles only).
- The checklist slide became the recap "Natrag na početak: je li portal prihvatio projekt?" (57–58). It answers the opening vote (C) and lists five key concepts; the reasoning checklist remains in the chapter.
- 41 slides / 60 min; `timing.json` updated. hr and en browser checks passed; language check passed.

2026-10-13 — Story reorder at the lecturer's request; nothing removed or merged. "Zašto raspodijeliti posao?" and Facebook now follow the definition and classification exercise, before the workload and concurrency slides. "Kako razviti loš sustav" (the fallacies) now follows "Naš portal: pretpostavke", before the 101 ms exercise. Chapter section "Why distribute the work?" (with the Facebook subsection) moved to the same place; the sentence about overlapping with remote waits moved into the concurrency section. Note transitions, timing (41 slides / 60 min) and the COURSE.md narrative order updated. Checks: hr/en browser checks, language check, English chapter PDF.

2026-10-13 — Speaker notes: each slide starts with a one-line **Priča:** / **Story:** cue; note items are separated by blank lines; timing lines were removed from notes and the title slide (timing stays in `timing.json` and this brief). The language check passes.

## Hrvatsko poglavlje, 2026-10-30

Na nastavnikov zahtjev dodan je `chapter.hr.qmd`, prijevod engleskog `chapter.qmd` (stanje 2026-10-13) prema iznimci za predavanje 01 (engleski kao sidro). Pojmovi i definicije 1.1–1.7 preuzeti su doslovno iz `slides.hr.qmd` i `references/terminology.md` (npr. „svojstvo napredovanja”, „raspodijeljeno zaključavanje”); nazivi sudionika prate hrvatske dijagrame (Preglednik, Usluga predaje, Usluga zadataka, Pohrana predaja). Sve slike koriste `.hr.pdf` inačice. Jedina sadržajna dopuna: rečenica da svojstvo sigurnosti (safety) nije zaštita od napadača (security), prema rječniku.

- Build: `just lecture 01-foundations` → `output/hr/lectures/01-foundations.pdf` (31 stranica); pregled svih stranica u smanjenom prikazu, stranice 17–18 detaljno; oznake „Slika”/„Definicija” provjerene.
- [ ] Nastavnikov jezični i sadržajni pregled hrvatskog poglavlja.
