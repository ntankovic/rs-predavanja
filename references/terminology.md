# Croatian–English terminology dictionary

Consult this file before writing or translating any lecture. Croatian is the authoring language; English is the reviewed translation.

**Lecture 01 synchronization exception (2026-09-19):** the lecturer selected the current English deck as the anchor. Synchronize Croatian slides from it, including examples, diagrams, reveals and concise bullet speaker notes. Introduce Croatian technical terms with the English term in parentheses. This direction does not approve the proposed Croatian translations.

## Rules

- Lecturer choices take precedence over suggested translations. Record each choice immediately and apply it across lectures, including headings, captions, diagrams, exercises, and speaker notes.
- Status is `provisional` or `approved`. Never label an agent suggestion as lecturer-approved.
- Record a term's meaning and context: one word may require different translations in different contexts. Use natural Croatian inflections and English grammar.
- Keep rejected alternatives and the reason for a decision so they are not suggested again. Record revisions in the decision log and identify existing lectures requiring updates.
- When a term is unresolved, use a clearly recorded provisional choice and flag it for translation review.

## Technical terms

Lecturer-approved choices and provisional suggestions are tracked separately below.

| Croatian term | Preferred English | Meaning / context | Avoid | Status | Decision date / source |
| --- | --- | --- | --- | --- | --- |
| procjena arhitekture | architecture review | Evaluating system structure, decisions and guarantees; Lecture 00 course overview. | pregled dizajna (ambiguous here) | approved (Croatian); provisional (English) | 2026-09-18, lecturer approved revised row |
| jamstvo | guarantee | What a system can promise under stated assumptions. | | approved (Croatian); provisional (English) | 2026-09-18, lecturer approved revised row |
| proces | process | Lecture 00 data-analysis diagram labels: Proces 1/2. Croatian label approved; English equivalent pending review. | radnik (in this diagram) | approved (Croatian); provisional (English) | 2026-09-17, lecturer request |
| ispad | failure | Failure of a participant or service; use across lectures. | otkaz | approved | 2026-09-17, lecturer correction: Otkaz > Ispad |
| konkurentnost | concurrency | Overlapping work; distinct from parallelism. | | provisional | 2026-09-17, initial Croatian Lecture 00 draft |
| zajedničko stanje | shared state | State shared by system participants. | | provisional | 2026-09-17, initial Croatian Lecture 00 draft |
| usluga | service | Service boundaries and existing Croatian diagram labels. | | provisional | 2026-09-17, initial Croatian Lecture 00 draft |
| istek vremena čekanja | timeout | Waiting ends without a confirmed outcome. | | provisional | 2026-09-17, initial Croatian Lecture 00 draft |
| kompromis | tradeoff | Consequences accepted when choosing among alternatives. | | provisional | 2026-09-17, initial Croatian Lecture 00 draft |
| skup dretvi / procesa | thread / process pool | Programming preparation checklist. | | provisional | 2026-09-17, initial Croatian Lecture 00 draft |
| sažeti zapisi kolekcija | comprehensions | Python syntax; retain the English term in parentheses for review. | | provisional | 2026-09-17, initial Croatian Lecture 00 draft |

## Lecture 02 provisional terms (2026-10-27)

Agent suggestions from the Croatian Lecture 02 draft; none is lecturer-approved.

| Croatian term | English term | Context | Status |
| --- | --- | --- | --- |
| arhitektura raspodijeljenog sustava | system architecture | Definition 2.1: components, responsibilities, connections and placement | provisional |
| klijent–poslužitelj | client–server | Definition 2.2; roles, not machine types | provisional |
| granica usluge | service boundary | Definition 2.4 | provisional |
| granica razmještaja | deployment boundary | Definition 2.6: process, container, host, data centre | provisional |
| smještaj | placement / deployment | Physical placement of components on machines and processes | provisional |
| vertikalna / horizontalna raspodjela | vertical / horizontal distribution | By function vs replicas of the same function (van Steen & Tanenbaum) | provisional |
| replika | replica | Copy of a service or data; Lecture 02 introduces service replicas | provisional |
| raspoređivač opterećenja | load balancer | Keep English in parentheses on first use | provisional |
| monolit / raspodijeljeni monolit | monolith / distributed monolith | Single process and release; services that must be released together or share one database | provisional |
| razgovorljivo sučelje | chatty interface | Many small calls for one user action | provisional |
| P2P sustav, sudionik | peer-to-peer system, peer | Definition 2.5; „sudionik” for peer | provisional |
| izmjena sudionika | churn | Peers joining and leaving | provisional |
| dio (datoteke) | piece | BitTorrent piece | provisional |
| upravitelj klastera | cluster manager | Spark; driver and executor kept in English | provisional |
| dvoslojni / troslojni smještaj | two-tier / three-tier | Placement of UI, logic and data | provisional |

## Confirmed English teaching preferences

Additional provisional terms used in the synchronized Lecture 01 draft:

| Croatian term | English term | Context |
| --- | --- | --- |
| raspodijeljeni sustav | distributed system | Definition 1.1 |
| lokalno stanje | local state | State belonging to one process |
| paralelizam | parallelism | Simultaneous execution |
| latencija | latency | Time from request to reply |
| kapacitet veze | bandwidth | Link capacity, distinct from achieved throughput |
| propusnost | throughput | Actual completed work per unit time |
| djelomični ispad | partial failure | Some components fail while others continue |
| ponovni pokušaj | retry | Another attempt at the same intended operation |
| atomarnost | atomicity | Indivisibility relative to other operations |
| invarijanta | invariant | Rule in every permitted state |
| svojstvo sigurnosti | safety | Forbidden events never occur; distinct from security |
| svojstvo napredovanja | liveness | Specified progress eventually occurs; not "živost" (lecturer, 2026-10-20) |
| raspodijeljeno zaključavanje | distributed lock | At most one holder at a time; lecturer rejected "brava" (2026-10-20); confirm term |
| model sustava | system model | Explicit allowed behaviour and assumptions |
| mrežna particija | network partition | Communication unavailable between groups |
| ispad bez oporavka | crash-stop | Participant never resumes in the analysed execution |
| ispad s oporavkom | crash-recovery | Participant can restart; specify retained state |
| bizantski model | Byzantine | Arbitrary deviation from the protocol |
| sinkroni / asinkroni / djelomično sinkroni | synchronous / asynchronous / partially synchronous | Timing assumptions, not API styles |
| vertikalno / horizontalno skaliranje | scale up / scale out | Larger components / more components |
| razina konzistentnosti | consistency level | Cassandra acknowledgement requirement |
| dokaz rada | proof of work | Bitcoin chain selection and mining |

These are wording decisions from Lecture 01 review, not approved Croatian translations.

| Context | Preferred wording | Guidance |
| --- | --- | --- |
| Example section heading | Example | Avoid “Worked scenario”. |
| Invariant in introductory outcomes | a rule the system must always obey | Introduce “invariant” with a concrete example or footnote; avoid “invariant worth protecting”. |
| Prior knowledge | idempotency from Web Apps | Remind students that repeating an operation has the same effect as doing it once; replies may differ. |
| Project archive | ZIP file containing a Unity game project | Explain that it includes source code, scenes, and resources such as images and sounds. |

## Decision log

- 2026-09-19 — Lecturer-approved English definition: “A distributed system consists of independently executing components that communicate and coordinate through message passing to achieve a shared goal.” Applied to Definition 1.1 in the Lecture 01 chapter and slides. This approves the English wording, not a Croatian translation.

- 2026-09-15 — Lecturer established Croatian-first drafting and tuning, followed by English translation and lecturer review. Reuse lecturer-selected terminology across lectures.

- 2026-09-17 — Lecturer requested English-to-Croatian translation of Lecture 00. Terms above are agent suggestions for review, not lecturer-approved choices.

- 2026-09-17 — Lecturer chose „Proces” instead of „Radnik” for the Lecture 00 data-analysis diagram. Updated both diagram variants, editable source and alternative text; English „Process” remains pending translation review. This is a contextual label choice, not a general replacement of every use of „worker”.

- 2026-09-17 — Lecturer selected „ispad” instead of „otkaz”. Applied to all three occurrences in Lecture 00, including natural noun phrasing in the course overview. No other Croatian slide/chapter sources currently contain the rejected term.

- 2026-09-18 — Lecturer approved the Lecture 00 row: „Sigurnost i procjena arhitekture” / „Koja jamstva sustav može pružiti i pod kojim pretpostavkama?”. English wording updated consistently, pending translation review.
