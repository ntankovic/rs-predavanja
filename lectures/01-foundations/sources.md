# Lecture 01 sources and provenance

## Croatian slide synchronization — 2026-09-19

The lecturer selected the current English deck as the anchor. Croatian slide text and speaker-note bullets preserve its claims, examples and linked sources. New `.hr.svg`/`.hr.pdf` variants of the system map, concurrency lanes, local/remote calls, performance comparison, TTFB, client roles, partial failure and timeout histories translate the original course artwork; existing bilingual diagrams retain their source records below. No new external images or technical claims were introduced. Croatian terms remain provisional pending lecturer review.

## Web Apps refresher: TTFB

- Public source consulted 2026-09-19: [web.dev, Time to First Byte](https://web.dev/articles/ttfb). Supports inclusion of setup and server/network waiting in navigation-start TTFB, distinct from downloading the full response. No login required.
- `assets/web-ttfb.svg` is original editable course artwork prompted by the lecturer's reference image; its PDF is generated with `just headless-preview`. Uses TLS terminology and a simplified fresh HTTPS-over-TCP path. Widths are schematic; caching/reuse and omitted phases are explained in notes.

All page numbers below are one-based PDF pages. References were read from the supplied local documents on 2026-09-14. No historical course administration or performance statistics are carried into this lecture.

## Content sources

| ID | Source | Pages used | Content developed |
| --- | --- | --- | --- |
| 1 | Nikola Tanković, `references/legacy/RS-01-Intro.pdf`, 2022/23 | 11–18, 24–38 | Definition, local autonomy, coherent service, concurrency versus parallelism, design goals, transparency, scaling, hidden assumptions |
| 2 | Nikola Tanković, `references/legacy/RS-02-RPC-Models.pdf`, 2022/23 | 3–18, 24–46 | Latency/bandwidth, remote-call boundary, uncertainty after missing communication, network/node/timing models |
| 3 | Martin Kleppmann, Cambridge, `references/legacy/dist-sys-notes.pdf`, 2021/22 | 2, 12–13, 17–20; sections 1.1, 2.1 and 2.3 | Cross-check of message-passing model, uncertainty, failure categories, timing terminology |
| 4 | Nikola Tanković, `references/legacy/RS-05-to-be-finished.pdf`, 2022/23 | 8–10 | Background for the retry/idempotency discussion in speaker notes; mechanisms deferred to later lectures |

The IDs in this internal table identify legacy provenance only. Student-facing references use a separate numbering scheme: [1] van Steen and Tanenbaum (2023), [2] Waldo et al. (1994), and [3] Kleppmann (2021/22). The chapter and slide notes link to public sources; internal filenames and adaptation workflow details are omitted from exports. Public author/university pages were checked on 2026-09-14. The textbook is recommended broad reading; detailed model and RPC citations point to the public Cambridge notes. Several RS-02 slides credit Martin Kleppmann. The supplied Cambridge notes state Creative Commons BY-SA. Preserve that attribution when further adapting their explanations or figures. The current diagrams do not reproduce Cambridge artwork; they are original vector compositions of the submission example.

## Original teaching material

The imagined university submission system, its task interleavings, exercises, proposed invariants, and suggested reasoning were written for this lecture. They are examples, not claims about the deployed university system. The timeout scenario applies the uncertain-outcome concept from sources 2 and 3 to a new domain.

## Diagram assets

Editable source: `assets/draw_diagrams.py`. Each drawing exports matching SVG and vector PDF versions. Use `.tools/qa-venv/bin/python lectures/01-foundations/assets/draw_diagrams.py` from the repository root, or another Python environment with PyMuPDF installed.

| Asset stem | Purpose | Provenance |
| --- | --- | --- |
| `system-map` | Participants, local state, communication | Original composition, informed by source 1's definition |
| `partial-failure` | Same participants with assignment service unavailable | Original state variant of `system-map` |
| `concurrency` | Interleaving versus simultaneous execution | Original lane diagram; concept from source 1 pp. 13–18 |
| `local-remote` | One address space versus network boundary | Original composition; concept from source 2 pp. 14–18 |
| `timeout-request-lost` | No effect before a missing request | Original timeline; uncertainty concept from sources 2 and 3 |
| `timeout-reply-lost` | Effect recorded before a missing reply | Original timeline; uncertainty concept from sources 2 and 3 |

Figures have captions and alternative text in the chapter, alternative text in slides, and explanatory speaker notes. Blue/dark arrows show ordinary communication; red plus text marks loss/unavailability. Labels carry the meaning independently of colour.

## Real-system synthesis — 2026-09-19

- etcd v3.6 [API guarantees](https://etcd.io/docs/v3.6/learning/api_guarantees/) and [failure modes](https://etcd.io/docs/v3.6/op-guide/failures/); Ongaro and Ousterhout, [Raft extended paper](https://raft.github.io/raft.pdf), sections 2 and 5.6. Verified atomic KV transactions, crash-recovery model, quorum availability and timing-independent safety. Claim-name invariant is an original application with no deletion/expiry/bypass assumed.
- Apache Cassandra [Dynamo architecture](https://cassandra.apache.org/doc/stable/cassandra/architecture/dynamo.html), [guarantees](https://cassandra.apache.org/doc/stable/cassandra/architecture/guarantees.html), and [hints](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/hints.html). Scoped to ordinary single-cell operations at ONE with three replicas; distinguish LWT and quorum overlap from atomic read-modify-write. Seat example demonstrates a missing application invariant. Convergence qualified by repair, retained updates and restored communication.
- Nakamoto, [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf), sections 5 and 11; [Bitcoin developer guide](https://developer.bitcoin.org/devguide/block_chain.html). Distinguish valid-chain no-double-spend invariant from probabilistic settlement and conditional transaction inclusion. Mining power is not node count; propagation and cryptographic assumptions matter.

All accessed 2026-09-19. New comparisons use original text and native tables; no external artwork. Croatian draft: `real-systems.hr.md`; English content and pacing remain pending lecturer review.

## Timeout and retry insight — 2026-09-19

AWS Builders’ Library, *Timeouts, retries, and backoff with jitter*: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ (public PDF: https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf). Supports retry amplification, overload, backoff and jitter. The slide's DDoS-like comparison describes accidental overload from distributed legitimate clients, not a claim of malicious attack. No external artwork reused.

## Branding assets

2026-09-19 visual review sources:

- Rob Pike, [Concurrency is not Parallelism](https://go.dev/talks/2012/waza.slide), Waza 2012. The short dealing/doing quotation is reproduced with visible author attribution. Cooking illustration is original vector artwork, not taken from the talk.
- Facebook [2012 billion-user milestone](https://about.fb.com/news/2012/10/one-billion-people-on-facebook/), [2019 results](https://investor.atmeta.com/investor-news/press-release-details/2020/Facebook-Reports-Fourth-Quarter-and-Full-Year-2019-Results/default.aspx), [2023 results](https://investor.atmeta.com/investor-news/press-release-details/2024/Meta-Reports-Fourth-Quarter-and-Full-Year-2023-Results-Initiates-Quarterly-Dividend/default.aspx), and [Q4 2023 remarks](https://investor.fb.com/files/doc_financials/2023/q4/META-Q4-2023-Prepared-Remarks.pdf): 1.00B, 2.50B, 3.07B Facebook MAU, with standalone reporting discontinued from Q1 2024. Latest Meta Family metrics deliberately excluded from this series. [Scaling engineering article](https://engineering.fb.com/2010/07/21/core-infra/scaling-facebook-to-500-million-users-and-beyond/) supports the technical motivation; no claim about today's complete architecture.
- Facebook logo: Simple Icons v16.23.0, https://cdn.jsdelivr.net/npm/simple-icons@16.23.0/icons/facebook.svg, downloaded with `just download-image` to `assets/facebook.svg`. Simple Icons distributes icons under CC0; brand trademark rights remain with their owners. Used only to identify the service in teaching.
- Hidden-assumptions slide: lecturer-supplied legacy screenshot, paraphrased with [Oracle's fallacies discussion](https://blogs.oracle.com/developers/fallacies-of-distributed-systems). Original wording associated with Deutsch and colleagues at Sun; no historical priority claim added.

The lecturer supplied `assets/shared/fipu-dark.pdf`. The derived `fipu-logo.svg` is used in the deck and `fipu-logo.pdf` on the standalone chapter title area. See `assets/shared/README.md` for the crop and provenance. Do not infer a general license for the faculty logo from the Cambridge reading material.

## Editorial corrections and scope decisions

- Treat a coherent user-facing service as a design goal rather than requiring perfect transparency to classify a system as distributed.
- Do not treat crash-stop as a promise of immediate or perfect crash detection.
- State a common eventual-synchrony formulation of partial synchrony and distinguish timing models from asynchronous programming APIs.
- Avoid unqualified hardware limits, historical platform user counts, availability percentages, and generalized Byzantine quorum claims.
- Use latency, bandwidth, and application throughput as different quantities; no measured performance is claimed.
- Show two indistinguishable client observations without claiming those histories exhaust all possibilities.
- Explain that a request identifier alone does not establish safe recovery or atomic duplicate detection.
- Introduce invariant, safety, and progress informally; formal algorithm properties and mechanisms are deferred.

## Public-reference access audit — 2026-09-14

- van Steen and Tanenbaum, *Distributed Systems*, 4th ed. (2023): authors' publication page and free-copy request form opened. https://www.distributed-systems.net/index.php/books/ds4/ds4-ebook/ requires an email address and CAPTCHA; a personalized download URL is sent by email. No form was submitted and delivery/full-book access was not tested. This is optional broad reading, not the only route to required concepts.
- Waldo, Wyant, Wollrath, and Kendall, *A Note on Distributed Computing*, SMLI TR-94-29 (November 1994): author page and actual 14-page PDF opened without login/payment. Verified title and all four authors on the PDF cover. Public full text: https://waldo.scholars.harvard.edu/sites/g/files/omnuum6261/files/waldo/files/waldo-94.pdf .
- Kleppmann, *Distributed Systems*, Cambridge 2021/22: actual 91-page PDF opened without login/payment at https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/dist-sys-notes.pdf . Verified title, author, course year and section numbering in its contents. Sections 1.1–1.3, 2.1, 2.3 and 5.1 match the listed reading topics. The PDF states CC BY-SA.

Public access was checked on this date, not guaranteed indefinitely. Internal legacy IDs above are provenance identifiers, distinct from the exported bibliography.

## Delivery analogy update — 2026-09-15

Inspected complete pages 6, 7, and 10 of `references/legacy/RS-02-RPC-Models.pdf` (Nikola Tanković, 2022/23): truck analogy, network bottleneck illustration, and physical data-transfer device. Page 6 motivates the new `latency-bandwidth-throughput` figure. Original third-party artwork attribution/license is not visible on these legacy pages; no original image pixels or icon outlines were reused. The new vector composition in `assets/draw_diagrams.py` uses simple original shapes and extends the analogy to completed deliveries. The source PDF is preserved. The chapter explains the analogy’s limits and distinguishes data volume from completed operations; performance quantities remain grounded in the previously verified Cambridge notes, section 1.2.

## Narrative and design-goal review — 2026-09-15

Revisited `RS-01-Intro.pdf`, especially complete pages 17, 28, 29, 33, and 34. Page 17 connects parallel work to performance; page 28 identifies resource sharing, transparency, openness, and scalability; pages 29, 33, and 34 expand resource sharing, interfaces, and size/geographical/administrative scaling. The revised lecture motivates throughput with a deadline rush in the submission portal, maps these goals to that example, and revisits concurrency as both a capacity opportunity and a coordination concern. Historical slides are conceptual background; no old performance measurements or unconditional scalability claims are carried over.

## Additional original figures (2026-09-17)

`assets/visual_review.py` creates upload-timeout, retry-race, safety-liveness, node-models and timing-models in Croatian and English (SVG/PDF). Original course artwork, no third-party assets. They visualize the existing chapter examples and system-model definitions, using the chapter’s existing Kleppmann reference. The portal is hypothetical. Timing lines are schematic, not measured data; Byzantine conflicting messages are one example, not an exhaustive definition.

2026-09-17 — Original `reply-wait` diagram illustrates the existing hypothetical 100/101 ms exercise; numbers are not measurements. No external artwork. Editable source `assets/draw_reply_wait.py`, Croatian/English SVG and vector PDF exports. Existing system-model source and exercise notes provide the conceptual context. Timing-model layout revised at lecturer request to identify stabilization explicitly and separate rows; model assumptions unchanged.

2026-09-17 — Reopened Kleppmann's public 91-page Cambridge 2021/22 full-text PDF for the timing-motivation addition (section 2.3; no login/payment). The new submission/retry explanation applies the existing safety and progress goals to timing assumptions. Qualified bounded failure detection with a full response bound and reliable communication, rather than treating a one-way network bound as proof of a process crash. No Raft/FLP claims added to this introductory section.

2026-09-17 story revision: network comparison uses the previously inspected Kleppmann 2021/22 public notes, section 2.3, printed pages 17–21: reliable, fair-loss and arbitrary links; partitions; node and timing models. New portal prompts and combined-model application are original teaching examples. Fair-loss progress is conditional on persistent retransmission between correct endpoints; no fixed response deadline follows. Durable storage and eventual communication are explicit assumptions, not automatic guarantees from the model or implementation.
