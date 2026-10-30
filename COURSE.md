# Distributed Systems — course plan and teaching requirements

## Course identity

- **Course:** Distributed Systems
- **Lecturer:** assoc. prof. Nikola Tankovic, PhD
- **Faculty:** Faculty of Informatics, Juraj Dobrila University of Pula
- **Teaching languages:** Croatian first; English translated from the reviewed Croatian version, including chapters, slides, labels, exercises, and speaker notes.
- **Lecture duration:** 60 minutes, including examples, student questions, discussion, and recap.

Use these lecturer and faculty names on the book title page and the title slide of each lecture deck.

Standalone lecture PDFs must also display **Distributed Systems, Lecture NN** above the lecture topic, using the two-digit lecture number (for example, **Distributed Systems, Lecture 01**).

## Croatian-first authoring and English translation

Lecture 01 exception, requested 2026-09-19: use the current English slides as the anchor when synchronizing Croatian. Introduce Croatian technical terms with their English equivalents in parentheses. Keep translation review pending until the lecturer approves it.

1. Develop and tune the Croatian chapter and derive Croatian slides from it. Review examples, pacing, diagrams, and wording with the lecturer.
2. Translate the reviewed Croatian material into English, preserving technical meaning, examples, citations, and teaching intent. Do not develop the two versions independently.
3. The lecturer reviews the English translation. Record preferred terms and rejected alternatives in [the shared terminology dictionary](references/terminology.md), then apply each decision consistently across existing translations and later lectures. Mark suggestions as provisional until the lecturer chooses them.
4. Track Croatian content review and English translation review separately in each lecture brief. A change to the Croatian source makes the affected English translation pending review again. Never mark a translation reviewed merely because it builds.
5. Consult the dictionary before every drafting, translation, and review pass. Keep grammatical inflections natural while retaining the approved term's meaning. Explain technical terms in familiar language when first introduced.

Store Croatian sources as `chapter.hr.qmd` and `slides.hr.qmd` beside the existing English `chapter.qmd` and `slides.qmd`. Keep assets together in the lecture directory; use `.hr` / `.en` suffixes for artwork whose labels differ. Shared editable geometry and source attribution remain common. Existing English material is preserved as a reference during migration; it is not automatically an approved translation of a Croatian source that has not yet been written.

Single-lecture `just` recipes (`render`, `lecture`, `slides`, `preview`, `browser-check`, `headless-preview`) default to Croatian (lecturer request, 2026-10-12); select English with `en`. `just all`, `just book` and `just test` default to English until Croatian chapters exist for the whole book. Python scripts default to English; select Croatian with `--lang hr`. The authoring workflow remains Croatian-first. English builds retain existing output paths. Croatian builds use `output/hr/` and must fail clearly when Croatian sources are missing, rather than substitute English. A Croatian book requires Croatian versions of all chapters in its assembly order. See `README.md` for language-specific commands.

## Purpose and deliverables

Build the course lecture by lecture, with agents working on clearly assigned lectures. The two final deliverables are:

1. A learning book for students, assembled from Markdown lecture chapters, built locally with Quarto, with a PDF per lecture and a single PDF containing the complete book.
2. Teaching slides for each lecture, with speaker notes where useful.

The book must be readable independently of the slides. Slides should support classroom teaching with concise explanations, diagrams, examples, and discussion prompts rather than reproduce book paragraphs.

## Lecture 00: course introduction and assessment

A separate [slides-only orientation](lectures/00-course-introduction/README.md) introduces course organization and assessment. It takes 20 minutes, is excluded from the student book, and does not reduce Lecture 01's 60-minute plan. This is an explicit exception to the chapter-plus-slides and 60-minute requirements below. `lecture.json` declares its format and duration. Historical 2022/23 administrative rules remain visibly marked pending lecturer confirmation; the deck is not ready for classroom release until current policies and student-facing links are supplied.

## Syllabus status

This **proposed 12-lecture plan** is an editorial proposal, not an official university syllabus. Assessment weights and credits remain unspecified. Course identity, language, and duration are defined above.

Lecture 01 has a full chapter, a 23-slide deck, and a timed 60-minute plan, and is in review. Lectures 02–12 retain short sample chapters and four-slide decks for build verification; those samples remain `drafting`.

## Course outcomes

Students should be able to explain partial failures and timing assumptions; reason about communication and ordering; compare replication, consistency, and coordination choices; and defend a distributed application design using concrete invariants and failure scenarios.

Assumed entry knowledge: basic programming, processes, networking, and database operations. The developed Lecture 01 uses a university project-submission portal: a student uploads a 20 MB project, receives a timeout, and considers retrying. Assignment rules, submission acceptance, and duplicate entries anchor the discussion. Lectures 02–12 still contain registration-service build samples; adapt them to the project-submission example when developing each lecture.

## Lecture sequence

| Lecture | Topic | Planned scope | Outcome | Prerequisites |
| --- | --- | --- | --- | --- |
| 01 | [Foundations and system models](lectures/01-foundations/README.md) | Distribution, system boundaries, timing assumptions, and failure models | Distinguish a partial failure from a complete system failure. | Programming, processes, and basic networking |
| 02 | [Architectures and service boundaries](lectures/02-architectures/README.md) | Client-server systems, services, peer-to-peer designs, and deployment boundaries | Identify a service boundary and its communication costs. | Lecture 01 |
| 03 | [Communication and remote calls](lectures/03-communication/README.md) | Request-response, RPC, serialization, timeouts, retries, and idempotency | Explain why retrying a remote request can duplicate an effect. | Lectures 01–02 |
| 04 | [Naming and service discovery](lectures/04-naming/README.md) | Names, addresses, lookup, discovery, leases, and caching | Separate a logical service name from a changing network address. | Lectures 02–03 |
| 05 | [Time and event ordering](lectures/05-time/README.md) | Clock drift, logical clocks, happens-before, and concurrency | Distinguish causal order from wall-clock timestamp order. | Lectures 01 and 03 |
| 06 | [Replication and consistency](lectures/06-replication/README.md) | Leader-based replication, read guarantees, linearizability, and eventual consistency | Explain how replication lag can produce a stale read. | Lectures 03 and 05 |
| 07 | [Consensus and leader election](lectures/07-consensus/README.md) | Replicated logs, terms, leader election, Raft, safety, and liveness | Explain the role of a majority in a three-node consensus group. | Lectures 05–06 |
| 08 | [Fault tolerance and recovery](lectures/08-fault-tolerance/README.md) | Failure detection, durable state, retries, backoff, and recovery | Describe a recovery plan for a crash during request processing. | Lectures 03 and 07 |
| 09 | [Distributed transactions and workflows](lectures/09-transactions/README.md) | Atomic commit, two-phase commit, sagas, and compensation | Identify an invariant that spans two services. | Lectures 06–08 |
| 10 | [Messaging and stream processing](lectures/10-messaging/README.md) | Queues, publish-subscribe, ordering, acknowledgements, and backpressure | Explain why a message consumer may see the same event twice. | Lectures 03, 05, and 08 |
| 11 | [Partitioning and scalability](lectures/11-scaling/README.md) | Partition keys, load distribution, rebalancing, caching, and bottlenecks | Identify how a partition key can create a hotspot. | Lectures 04, 06, and 10 |
| 12 | [Security, observability, and system design](lectures/12-design-review/README.md) | Authentication, authorization, tracing, metrics, and integrated design review | Justify a design using an invariant, failure scenario, and observable evidence. | Lectures 01–11 |

## Narrative structure

Begin with a concrete problem and let the running example guide definitions and reasoning. Introduce each concept when that problem creates a reason to need it. Use workload questions to expose assumptions: for example, a large university with many simultaneous submissions and a hypothetical 20-minute checking process. Distinguish receiving, queueing, and processing jobs; do not infer system throughput from one job’s elapsed time without a sequential-processing assumption. Include positive motivations for distribution—more completed work per unit time, resource sharing, openness, reach, and resilience—alongside failure and coordination costs. Revisit earlier motivations when explaining mechanisms, so concurrency connects both to capacity and to overlapping retries. For Lecture 01, follow (reordered at the lecturer’s request, 2026-10-13): timeout and system → definition → reasons to distribute (geography, capacity, resilience) and scale → workload and overlapping jobs (concurrency versus parallelism) → communication costs → partial failure and uncertain outcomes → retry discussion (reuse concurrency) → invariants, safety, and liveness → explicit system assumptions, including the fallacies of distributed computing → recap answering the opening vote. State the question each section answers and use a short transition to the next. Keep chapter and slide progression consistent; avoid inserting vocabulary comparisons before their purpose is clear.

## Development and review

Expand one lecture at a time. Follow the teaching requirements below for independent book explanations, concise slides, explicit assumptions and tradeoffs, worked scenarios, exercises, citations, and review. Use the registry for ownership and progress. The present sample sequence is included in the book to test assembly; final publication requires the content review checklist.

## Suggested integration exercise

Design the project-submission service across the course: start with a client and server, introduce retries and discovery, add replicated state and events, then justify partitioning, access control, and failure recovery. Assessment format and weighting are not yet defined.

## Planning a 60-minute lecture

Record a timed outline in each lecture brief, with segments totaling 60 minutes. Include student participation in that total; do not allocate the entire hour to uninterrupted explanation. Keep timing in the brief and `timing.json`, not in speaker notes (lecturer, 2026-10-13). Separate note items with blank lines and start each slide’s notes with a one-line **Priča:** / **Story:** cue describing how the story develops. The book can provide deeper explanations and optional reading beyond what fits in class. Current sample decks are build fixtures, not complete 60-minute lectures.

## Illustration workflow

- Plan illustrations alongside the learning outcomes, before writing a long text-only draft. Record each figure's teaching purpose and its placement in the chapter and slides in the lecture's `illustrations.md`.
- Use diagrams to explain processes, message exchange, ordering, shared state, and failures. Each core mechanism should have a worked visual example when this makes it easier to understand; avoid decorative images and arbitrary image quotas.
- Start with relevant legacy figures. Inspect the complete source page, verify labels and assumptions, and record the original PDF, page, author, and attribution/license information in `sources.md`. Preserve the original source.
- Reuse a clear extracted figure; rebuild a low-resolution, crowded, outdated, or inconsistent diagram as editable vector artwork. Keep the editable diagram source in the lecture's `assets/` directory. Use SVG for HTML and a corresponding vector PDF or suitable PNG for PDF output.
- Create original technical diagrams with precise shapes, labels, and connectors. Prefer code-based vector drawing or a diagram description language over generated raster artwork for protocol logic, equations, or readable text. Use generated illustrations only when a conceptual scene or visual analogy helps, and review their technical meaning.
- Use consistent node names, colours, arrow meanings, and time direction. Label failures and state changes explicitly; colour alone must not convey meaning. Prefer the same running example across figures.
- Use explanatory pictures from the legacy teaching material as starting points for abstract comparisons; inspect their source pages and attribution, and redraw or extend them when needed. Explain why a warning or distinction matters with a concrete consequence, rather than leaving it as a slogan.
- Explain arrow direction and meaning in each diagram with a legend or nearby text. Distinguish calls/dependencies from chronological message exchanges and state explicitly when replies are omitted.
- Center the complete label group vertically inside diagram boxes, accounting for font size and text baselines. Check that the visible top and bottom padding are balanced, including boxes with a heading and subtitle.
- Share the same underlying artwork between chapter and slides. Leave generous inner margins in diagram boxes; fit long labels without letting text touch borders. Give book figures descriptive captions and surrounding explanation; use shorter labels and staged steps on slides where useful. A PDF must still explain every essential step without animation.
- Add alternative text for figures. Check every figure in the rendered lecture PDF and browser slides for label size, clipping, contrast, and correct sequence. Dense legacy slides should be split or redrawn instead of shrunk to fit.

## Folder structure

```text
COURSE.md                 Course identity, syllabus, and teaching requirements
AGENTS.md                 Working rules for agents
justfile                  Build and verification commands
lectures/
  README.md               Lecture registry, ownership, and progress
  _template/              Copy this directory to start a lecture
    README.md             Lecture brief and review checklist
    chapter.qmd            Student book chapter
    slides.qmd             Slide outline and speaker notes
    sources.md            References and verification notes
    illustrations.md      Figure purposes, sources, and placement
    assets/               Lecture-specific diagrams and images
references/               Shared bibliography and source notes
assets/shared/            Reusable visual assets
publishing/
  book/                   Book assembly order and front matter
  slides/                 Shared slide conventions
scripts/                  Local build commands
output/lectures/          Individual lecture PDFs
output/book/              Generated book exports
output/slides/            Generated teaching slide exports
```

## Lecture-by-lecture workflow

1. Define the lecture topic, prerequisites, learning outcomes, and scope. Register it in `lectures/README.md`.
2. Copy `lectures/_template/` to `lectures/NN-short-topic/`, using a two-digit sequence number and a descriptive slug.
3. Assign an agent to the lecture directory. Record ownership and status in the lecture registry so agents do not overwrite each other's work.
4. Collect and verify sources, then write the chapter with explanations, examples, exercises, and a recap.
5. Derive the slide deck from the reviewed chapter. Include teaching notes and checks for understanding.
6. Review technical accuracy, prerequisites, terminology, references, and consistency between chapter and slides.
7. Add the completed chapter to the book assembly order and build the deliverables locally with Quarto (see `README.md`).

Use these statuses: `planned`, `drafting`, `review`, `ready`. Only mark a lecture `ready` after both its chapter and slides have passed review.

## Content guidelines

- Write speaker notes as usable teaching cues: purpose, what to say or ask, expected answers, likely misconceptions, and a transition where useful. Use short labelled blocks or bullets instead of dense procedural paragraphs. End each lecture by widening the running problem into a small, open design challenge. Students should propose how to solve something using the ideas learned, with several defensible answers; avoid merely recalling an example already answered. Include a follow-up failure or constraint and a bridge to later lectures. The preceding recap consolidates the lesson. Explain the purpose, discussion prompts, and possible reasoning to the lecturer without scripting a single required answer.
- Lecturer preference (2026-09-19): concise bullet speaker notes, not prose scripts. Retain timing, essential caveats, questions and source links; keep detailed explanations in the chapter.
- Default regular presentation text uses dark gray (`#333333`). Preserve the established title and bold-text colors, red definition labels, and diagram colors.
- Title slides place a larger FIPU logo above the title, aligned with its left edge. Preserve the logo proportions.
- Presentations use a visible 6 px bottom progress bar and a small footer identifying the course and lecturer, localized to the presentation language. A deck with `version: "X.Y"` in its front matter shows ` · vX.Y` at the end of the footer. Increase the minor version by 0.1 with every change to a versioned deck, keeping the Croatian and English decks of a lecture on the same number (lecturer, 2026-10-20; lectures 00 and 01 start at 1.6).

- Put key definitions in a distinctive red-bordered box with a thicker left edge and a pale red background. Number them by lecture and definition: **Definition 1.1**, **Definition 1.2**, **Definition 2.1**. Use a fenced Div such as `::: {.definition number="1.1"}`; keep the same explicit number in the chapter, slides, and translation. The shared filter labels Croatian boxes **Definicija**. Keep each definition short enough to fit together on one page or slide; introduce its concrete meaning before the box.
- State learning outcomes and prerequisite knowledge at the start of each lecture.
- Write learning outcomes in language students understand before attending the lecture. Introduce unfamiliar technical terms with a plain-language explanation and a concrete example; use a short chapter footnote when it helps without interrupting the flow.
- Ground examples in recognizable student work and explain what concrete objects contain (for example, a ZIP file containing a Unity game project, its source code, scenes, images, and sounds).
- Connect new concepts to relevant prior coursework explicitly; students have encountered idempotency in Web Apps, so use a brief reminder when introducing safe retries.
- Use familiar section labels such as **Example**, rather than **Worked scenario**.
- Introduce concepts before formal definitions; explain assumptions, failure models, and tradeoffs explicitly.
- Use concrete distributed systems examples, diagrams, and worked scenarios.
- Include exercises or discussion questions tied to the learning outcomes.
- Cite external claims and adapted material, and record asset provenance and licensing.
- Verify every reference exists, confirm author/title/year and the cited section, and open the actual public full text where available. Record access date and any email, login, or payment requirement in `sources.md`; never claim full-text access from a landing page alone. Required reading must be accessible without institutional subscriptions; clearly label optional resources with access conditions.
- Use publicly accessible books, papers, and university notes in exported references, with author, title, year, and a direct public link. Keep internal legacy filenames and adaptation notes in `sources.md`; preserve required public attribution.
- Format table headers in bold and alternate white and light-gray body rows, starting with white. Use a slightly smaller table font and generous horizontal and vertical cell padding. Apply this consistently in PDF chapters, the combined book, and HTML slides.
- Keep terminology and notation consistent across lectures. Identify dependencies on earlier chapters.
- Keep editable source files in lecture directories and generated exports in `output/`.
- Use the lecture sequence in this document as the proposed syllabus plan requested by the lecturer. Keep editorial proposals distinct from confirmed institutional requirements. Do not invent assessment weights, credits, or lecture durations.

### Terminal commands on slides — lecturer decision, 2026-10-28

Shell commands on slides use a terminal look, not ordinary inline code.

- **Inline command:** `` `npm start`{.cmd} `` renders as a dark pill with a green `$ ` prompt added automatically; do not type `$` yourself. Example: ``Run `cd code/01-introduction`{.cmd} then `npm start`{.cmd}.``
- **Terminal session or output (several lines):** use a fenced block ```` ```{.terminal code-line-numbers="false"} ````. Type `$ ` before each command; output lines have no prompt. It renders as a dark terminal window with three dots.
- Use `.cmd` / `.terminal` only for commands a person types in a shell (`npm`, `node`, `curl`, `nc`, `git`, `docker`, `PORT=3001 npm start` …). File names, URLs, identifiers, HTTP messages and program code keep ordinary code formatting (` ```http `, ` ```javascript `).
- Syntax highlighting is switched off inside terminal styling; colour must not split a command.
- Speaker notes and PDF chapters keep ordinary code formatting; the shared CSS lives in `publishing/slides/revealjs.yml`.

## Initial project state

The proposed 12-lecture sequence is recorded above. Lecture 01 is developed and in review; lectures 02–12 retain sample text for build verification. Quarto Markdown (`.qmd`) is the editable source. Use local Quarto builds for lecture PDFs, the complete book PDF, and Reveal.js teaching slides. No GitBook account or subscription is required. See `README.md` for installation and build commands.
