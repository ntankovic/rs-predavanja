# Nazivlje i otkrivanje usluga

- Number: 04
- Topic: Naming and service discovery
- Owner: coordinating agent
- Status: drafting (full Croatian draft, 2026-11-09)
- Authoring language: Croatian
- Croatian content review: pending lecturer review
- English translation review: not started (`chapter.qmd` and `slides.qmd` are still the old English build samples)
- Croatian revision translated: not yet recorded
- Terminology: consult `../../references/terminology.md`; new provisional terms recorded there
- Intended duration: 60 minutes, including discussion and recap; current plan 68 minutes after adding code→image→container, Swarm, etcd key-tree and DynamoDB slides (lecturer requests, 2026-11-10). Not shortened; lecturer to decide.
- Prerequisites and earlier lecture dependencies: Lecture 01 (etcd, timeout, silence vs crash), Lecture 02 (replicas, Docker Compose and Swarm, deployment boundaries), Lecture 03 (gRPC channel `predaja:50051`, retries, idempotency key)
- Learning outcomes: see `chapter.hr.qmd`; the COURSE.md outcome "separate a logical service name from a changing network address" is outcome 1.
- Scope and exclusions: names, addresses, identifiers, name resolution, DNS tree and resolvers, SRV, caching and TTL, negative caching, names in Compose/Swarm/Kubernetes/gRPC, service discovery (client-side vs server-side), registration (self vs third-party), leases (etcd), lease length trade-offs and false removal. Deferred: name security and certificates (12), replicating the registry (06, 07), failure detection (08), load balancing and partitioning (11).

## Story

Opens with the Lecture 03 closing challenge (two devices, email before saving), reframed as "how do we label things so we can recognise them later?". Running question: the portal's gRPC channel targets `predaja:50051`; with three Swarm replicas that move between nodes, how should the portal find the submission service? (vote: IP in config / name + DNS / service registry). Concepts follow: name vs address vs identifier → resolution → DNS tree and resolvers → caching and TTL (simulator 1) → names in containers → service discovery → client-side vs server-side → registration → leases in etcd (simulator 2) → lease-length trade-off → pair exercise (stale address + safe retry from 03) → back to the vote → anti-patterns → recap → design challenge (two registry replicas, leading to 06/07) → project application.

## Timed outline

Timings include explanation and student participation. `timing.json` is the machine-readable plan. This is a plan, not a classroom rehearsal.

| Slide | Minutes | Topic |
| --- | --- | --- |
| 1 | 0–0:30 | Nazivlje i otkrivanje usluga |
| 2 | 0:30–1 | Evidencija prisutnosti (zajednički slajd) |
| 3 | 1–4 | Zadatak: dva uređaja i e-pošta |
| 4 | 4–5:30 | Od koda do kontejnera |
| 5 | 5:30–7 | Docker Swarm: željeno stanje |
| 6 | 7–8:30 | Docker Swarm: čvor ispadne |
| 7 | 8:30–10:30 | Gdje je usluga predaje? |
| 8 | 10:30–11:30 | Što trebamo znati da bismo odlučili? |
| 9 | 11:30–14:30 | Primjeri nazivlja: ime, adresa i identifikator |
| 10 | 14:30–16:30 | Jedno ime, adrese koje se mijenjaju |
| 11 | 16:30–19:30 | DNS: stablo imena i razrješavanje |
| 12 | 19:30–22:30 | DNS: predmemorija (cache) i TTL |
| 13 | 22:30–27:30 | Simulator: TTL i premještanje usluge |
| 14 | 27:30–31:30 | Imena usluga u kontejnerima |
| 15 | 31:30–33:30 | Otkrivanje usluga |
| 16 | 33:30–36:30 | Na klijentu ili preko usmjernika |
| 17 | 36:30–38:30 | Tko upisuje instance u registar? |
| 18 | 38:30–41:30 | Najam (lease) |
| 19 | 41:30–43 | etcd kao registar: stablo ključeva |
| 20 | 43–45 | DynamoDB: TTL nije najam |
| 21 | 45–50 | Simulator: registar usluga s najmom |
| 22 | 50–52 | Koliko dug najam? |
| 23 | 52–57 | Vježba: zastarjela adresa |
| 24 | 57–60 | Natrag na početak: kako portal pronalazi uslugu predaje? |
| 25 | 60–61 | 🔥 Kako napraviti loše nazivlje |
| 26 | 61–63 | Sažetak |
| 27 | 63–66 | Osmislite sljedeći korak: dva registra |
| 28 | 66–68 | Za vaš projekt: imena i otkrivanje |

## Language workflow

Croatian is written first (`chapter.hr.qmd`, `slides.hr.qmd`, `*.hr.svg/pdf`, Croatian strings in `dns-ttl.js` and `lease-registry.js`). After lecturer review, translate into `chapter.qmd` and `slides.qmd`, produce English diagram variants from `assets/draw_diagrams.py` and add English strings to the simulators.

## Review checklist

- [x] Learning outcomes are covered by the chapter and slides.
- [x] Chapter is understandable without the slides.
- [x] Technical claims, examples, and sources have been checked (see `sources.md`).
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
- [ ] Timing totals 60 minutes, including student participation (currently 68 minutes).
- [x] Lecturer and faculty names are correct.
- [x] Review findings and remaining issues are recorded below.

## Review notes

2026-11-09 — Full Croatian draft: chapter (Definitions 4.1–4.5, five original diagrams, six exercises with suggested reasoning), 21 content slides plus title and the shared attendance slide (23 total, 60 minutes), two interactive simulators (`dns-ttl.js`: cache TTL and a moving service; `lease-registry.js`: leases, a crash and an optional pause). Both simulators were driven in headless Chrome for their main settings; the lease model was corrected so a resumed instance renews at once and removals of paused (not crashed) instances count as false removals. Croatian HTML and PDF built; browser check passed on all 23 slides. Open points for the lecturer:

- Docker was not running locally, so Compose/Swarm name resolution is cited from Docker documentation, not demonstrated; the `etcdctl` commands follow etcd documentation and were not executed (no etcd installed).
- Definitions 4.1–4.2 are the course's own wording (name, address, identifier, resolution); van Steen and Tanenbaum's naming chapter was not re-read in this session, so it is not cited.
- The Consul service-discovery page returned 404; Consul is not used.
- Kubernetes is mentioned only through verbatim statements from the Service page (no DNS name format claims).

2026-11-10 — Lecturer review: rewrote the opening exercise (two devices: scenario stated step by step, key that describes the submission, e.g. student + assignment + ZIP hash); removed the vague "Danas: imena" line; added two Swarm slides with diagrams (`swarm-overview`, `swarm-reschedule`) before the vote. Deck version 1.2. Timing is now 63 minutes.

2026-11-10 — Lecturer request: DynamoDB added to the lease slide and chapter as a contrast (TTL attribute deletes within a few days, so it is not a lease; DynamoDB Lock Client implements a lease with heartbeats). Deck version 1.4.

2026-11-10 — Lecturer terminology choice: „nazivlje” for naming (not „imenovanje”); lecture title is now „Nazivlje i otkrivanje usluga”. Vote slide now explains options A–C in one line each (DNS and the service registry were not introduced before the vote). Deck version 1.6.

2026-11-10 — Lecturer review: etcd key tree slide and diagram (`etcd-keys`); DynamoDB moved to its own slide explaining heartbeats (Lock Client changes a record version number; a waiting client checks it is unchanged after the lease duration; no absolute time stored); lease simulator renamed to „registar usluga s najmom”, with an intro sentence, heartbeats drawn as ♥ and requests labelled as portal requests. Deck version 1.8. Timing now 66.5 minutes; not shortened.

2026-11-10 — Lecturer request: slide and figure „Od koda do kontejnera” (code → docker build → image → docker push → image registry → docker pull/run → containers) before the Swarm slides; distinguishes the image registry from the service registry. Deck version 2.3. Timing now 68 minutes; not shortened.
