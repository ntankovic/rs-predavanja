# Arhitekture i granice usluga

- Number: 02
- Topic: Architectures and service boundaries
- Owner: coordinating agent
- Status: drafting (full Croatian draft, 2026-10-27)
- Authoring language: Croatian
- Croatian content review: pending lecturer review
- English translation review: not started (`chapter.qmd` and `slides.qmd` are still the old English build samples)
- Croatian revision translated: not yet recorded
- Terminology: consult `../../references/terminology.md`; new provisional terms recorded there
- Intended duration: 60 minutes, including discussion and recap
- Prerequisites and earlier lecture dependencies: Lecture 01 (distributed system, partial failure, timeout, retry, invariant, scale out); Lecture 00 project types
- Learning outcomes: see `chapter.hr.qmd`; the COURSE.md outcome "identify a service boundary and its communication costs" is outcome 3.
- Scope and exclusions: logical vs physical architecture, client–server and tiers, vertical/horizontal distribution, monolith vs services, service boundaries and their costs, P2P (BitTorrent), coordinator-based cluster (Spark), deployment boundaries (process, container, host, data centre; Compose vs Swarm). Deferred: RPC and serialization (03), discovery (04), replication (06), consensus (07), cross-service transactions (09), queues (10), partitioning (11).
- Syllabus note: follows `COURSE.md` (Lecture 02 row). `upute.md` uses a different 12-week order; the lecturer has not yet said which document is authoritative.

## Story

The Lecture 01 invoice homework (central counter) opens the lecture as a first architectural decision. The running question is where to put a new CPU-heavy project check in the portal (vote A/B/C). Concepts follow the question: architecture → client–server and tiers → replicas → monolith → service and boundary → three costs (latency, chain availability, data and rules) → pair exercise → P2P and why the portal still needs a server → coordinator cluster → deployment boundaries → back to the vote → anti-patterns → recap → notification design challenge → link to the project application.

## Timed outline

Timings include explanation and student participation. `timing.json` is the machine-readable plan. This is a plan, not a classroom rehearsal.

| Slide | Minutes | Topic |
| --- | --- | --- |
| 1 | 0–0.5 | Arhitekture i granice usluga |
| 2 | 0.5–1 | Evidencija prisutnosti (zajednički slajd) |
| 3 | 1–4 | Domaća zadaća: računi 1, 2, 3, … |
| 4 | 4–6 | Portal pred rok |
| 5 | 6–7 | Što trebamo znati da bismo odlučili? |
| 6 | 7–9 | Logička organizacija i fizički smještaj |
| 7 | 9–11 | Klijent–poslužitelj |
| 8 | 11–13 | Slojevi i njihov smještaj |
| 9 | 13–15 | Vertikalna i horizontalna raspodjela |
| 10 | 15–17 | Monolit: jedan proces, jedno izdanje |
| 11 | 17–19 | Usluga i granica usluge |
| 12 | 19–21 | Gdje povući granicu? |
| 13 | 21–24 | Cijena granice 1: latencija |
| 14 | 24–26 | Cijena granice 2: dostupnost lanca |
| 15 | 26–28 | Cijena granice 3: podaci i pravila |
| 16 | 28–32 | Podijelite portal u usluge |
| 17 | 32–34 | Jedno moguće rješenje |
| 18 | 34–36 | P2P: svi su klijenti i poslužitelji |
| 19 | 36–38 | BitTorrent: P2P uz tracker |
| 20 | 38–40 | Može li portal biti P2P? |
| 21 | 40–42 | Klaster s koordinatorom: Spark |
| 22 | 42–45 | Granice razmještaja |
| 23 | 45–47 | Ista arhitektura, različiti ispadi |
| 24 | 47–50 | Natrag na početak: kamo s provjerom? |
| 25 | 50–52 | 🔥 Kako napraviti lošu granicu |
| 26 | 52–54 | Sažetak |
| 27 | 54–58 | Osmislite sljedeći korak: obavijesti nastavniku |
| 28 | 58–60 | Za vaš projekt: granice i smještaj |

## Language workflow

Croatian is written first (`chapter.hr.qmd`, `slides.hr.qmd`, `*.hr.svg/pdf`). After lecturer review, translate into `chapter.qmd` and `slides.qmd` and produce English diagram variants from `assets/draw_diagrams.py`.

## Review checklist

- [x] Learning outcomes are covered by the chapter and slides.
- [x] Chapter is understandable without the slides.
- [x] Technical claims, examples, and sources have been checked (see `sources.md`, including one secondary-only confirmation).
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

2026-10-27 — Full Croatian draft: chapter (Definitions 2.1–2.6, eight original diagrams, six exercises with suggested reasoning) and a 27-slide deck plus the shared attendance slide, 60 minutes. Open points for the lecturer:

- Syllabus choice (`COURSE.md` vs `upute.md`); the draft follows `COURSE.md`.
- Dean's 2009 latency figures: the primary PDF could not be fetched in this session (certificate error); values confirmed via a secondary reproduction only.
- The legacy RS-01 pp. 39–66 material (HPC, grid, cloud, EAI, pervasive systems) is not used except the cluster-with-a-managing-node idea; decide whether system types belong here or in Lecture 11/12.
- The Spark driver-failure statement is simplified ("the application must be restarted"); Spark offers driver supervision in some cluster modes.
