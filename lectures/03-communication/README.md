# Komunikacija i udaljeni pozivi

- Number: 03
- Topic: Communication and remote calls
- Owner: coordinating agent
- Status: drafting (full Croatian draft, 2026-11-09)
- Authoring language: Croatian
- Croatian content review: pending lecturer review
- English translation review: not started (`chapter.qmd` and `slides.qmd` are still the old English build samples)
- Croatian revision translated: not yet recorded
- Terminology: consult `../../references/terminology.md`; new provisional terms recorded there
- Intended duration: 60 minutes, including discussion and recap
- Prerequisites and earlier lecture dependencies: Lecture 01 (timeout, retry, Histories A–C, invariant, idempotency from Web Apps, promised Idempotency-Key), Lecture 02 (service boundary, check as a separate service, sync vs async, chain of calls, "notifications" closing challenge)
- Learning outcomes: see `chapter.hr.qmd`; the COURSE.md outcome "explain why retrying a remote request can duplicate an effect" is outcome 5.
- Scope and exclusions: request–response, RPC (stubs, marshalling, location transparency), gRPC and Protocol Buffers, JSON vs Protobuf, compatible contract changes, deadlines and deadline propagation, retry semantics, retry amplification, gRPC retry policy, idempotency, idempotency keys, atomic key + effect. Deferred: service discovery (04), backoff/jitter and failure detection (08), cross-service transactions and outbox (09), queues (10). Latency/bandwidth from the legacy RS-02 pp. 4–10 is not repeated (covered in Lectures 01 and 02).

## Story

Opens with the Lecture 02 closing challenge (notification sent twice). Running question: the portal calls `SnimiPredaju` on the submission service to record a submission, gets no reply within 2 s; may it call again? A duplicate is a second record of the same submission (Lecture 01 invariant). (vote A/B/C). Concepts follow the question: local vs remote call → request–response and three outcomes → RPC and stubs → gRPC contract and Python client → serialization (JSON 79 B vs Protobuf 30 B, measured) → compatible contract changes → recap of Histories A–C for this call → deadlines in gRPC (with a measured experiment) → choosing and propagating deadlines → retry semantics → multiplied retries → gRPC retry policy → idempotency → idempotency key → atomic key and effect → simulator → back to the vote → anti-patterns → recap → design challenge (two devices; email before saving).

## Timed outline

Timings include explanation and student participation. `timing.json` is the machine-readable plan. This is a plan, not a classroom rehearsal.

| Slide | Minutes | Topic |
| --- | --- | --- |
| 1 | 0–0:30 | Komunikacija i udaljeni pozivi |
| 2 | 0:30–1 | Evidencija prisutnosti (zajednički slajd) |
| 3 | 1–4 | Zadatak: obavijest poslana dvaput |
| 4 | 4–6 | Provjera ne odgovara |
| 5 | 6–7 | Što trebamo znati da bismo odlučili? |
| 6 | 7–9 | Lokalni i udaljeni poziv |
| 7 | 9–11 | Zahtjev–odgovor: tri ishoda |
| 8 | 11–13 | RPC: udaljeni poziv koji izgleda lokalno |
| 9 | 13–16 | Tijek jednog RPC poziva |
| 10 | 16–18 | gRPC: ugovor u datoteci `.proto` |
| 11 | 18–20 | Poziv iz Pythona |
| 12 | 20–22 | Serijalizacija: JSON i Protocol Buffers |
| 13 | 22–25 | Promjena ugovora bez rušenja klijenata |
| 14 | 25–26 | Istek čekanja ne kaže što se dogodilo |
| 15 | 26–28 | Rok u gRPC-u |
| 16 | 28–31 | Kako odabrati rok i prenijeti ga lancem |
| 17 | 31–34 | Semantike ponovnih pokušaja |
| 18 | 34–36 | Ponovni pokušaji se množe |
| 19 | 36–38 | Ponovni pokušaj u gRPC-u |
| 20 | 38–41 | Idempotentnost |
| 21 | 41–44 | Ključ idempotentnosti |
| 22 | 44–47 | Ključ i učinak u jednoj transakciji |
| 23 | 47–52 | Simulator: ponovni pokušaj i ključ |
| 24 | 52–54 | Natrag na početak: smije li predaja ponoviti poziv? |
| 25 | 54–55 | 🔥 Kako napraviti loš udaljeni poziv |
| 26 | 55–57 | Sažetak |
| 27 | 57–60 | Osmislite sljedeći korak: dva uređaja i e-pošta |

## Language workflow

Croatian is written first (`chapter.hr.qmd`, `slides.hr.qmd`, `*.hr.svg/pdf`, Croatian strings in `rpc-retry.js`). After lecturer review, translate into `chapter.qmd` and `slides.qmd`, produce English diagram variants from `assets/draw_diagrams.py` and add English strings to the simulator.

## Review checklist

- [x] Learning outcomes are covered by the chapter and slides.
- [x] Chapter is understandable without the slides.
- [x] Technical claims, examples, and sources have been checked (see `sources.md`; two classic papers cited only via Kleppmann).
- [x] Assumptions, failure models, and tradeoffs are explicit where relevant.
- [x] Exercises and discussion prompts align with the outcomes; the chapter includes suggested reasoning.
- [x] Terminology recorded as provisional in the shared dictionary.
- [ ] Croatian chapter and slides have passed lecturer review.
- [ ] English translation reflects the recorded Croatian revision.
- [ ] Lecturer translation choices are recorded in the dictionary and applied consistently.
- [ ] Both language exports have passed visual review (Croatian only so far).
- [x] Slide sequence and speaker notes support classroom teaching.
- [x] Diagrams are readable and asset provenance is recorded.
- [x] Essential visual steps are understandable in the static PDF as well as the slides.
- [x] Timing totals 60 minutes, including student participation.
- [x] Lecturer and faculty names are correct.
- [x] Review findings and remaining issues are recorded below.

## Review notes

2026-11-09 — Full Croatian draft: chapter (Definitions 3.1–3.6, four original diagrams, six exercises with suggested reasoning), 25 content slides plus title and the shared attendance slide (27 total, 60 minutes), interactive retry simulator (`assets/rpc-retry.js`) and a runnable gRPC demo (`assets/kod/`). Code was executed with grpcio 1.63 / protobuf (Python): message sizes, DEADLINE_EXCEEDED while the server still scheduled the check, idempotent retry returning the same job, and acceptance of the retry service config. Croatian HTML and PDF built; browser check passed on all 27 slides; key slides and chapter pages visually checked. Open points for the lecturer:

- Running example (lecturer, 2026-11-09): recording a submission, `SnimiPredaju` (portal → submission service); the simulator shows the submissions table with a visible duplicate row. Simulator defaults: no retries, no fault (lecturer).
- Retry semantics are framed as guarantees on the number of executions; at-most-once may use retries with server-side duplicate detection (RFC 5531 xid), so exactly-once effect = at-least-once + at-most-once (lecturer question, 2026-11-09).
- Code language: Python for gRPC, JavaScript `fetch` for the browser. Confirm, or switch to the language students use in the project.
- Waldo et al. (1994) and Birrell & Nelson (1984) could not be fetched; Waldo is mentioned only "as cited by Kleppmann", Birrell & Nelson is not cited.
- The IETF Idempotency-Key header is an Internet-Draft (-08), not an RFC; the text says so.
