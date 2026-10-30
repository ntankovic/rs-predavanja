# Legacy materials inventory and migration map

Indexed 2026-09-14. All page references below are **one-based PDF page numbers**, which may differ from printed slide numbers. Original PDFs are unchanged.

## Inventory

| Source | Pages | Role and main topics | Extracted raster objects |
| --- | ---: | --- | ---: |
| [RS-01-Intro.pdf](RS-01-Intro.pdf) | 67 | Nikola Tanković's introduction: definitions, concurrency, transparency, scalability, system types | 44 |
| [RS-02-RPC-Models.pdf](RS-02-RPC-Models.pdf) | 53 | Networking, RPC, system models, generals problems, availability, failure detection | 35 |
| [RS-03-Time-Clocks-Ordering.pdf](RS-03-Time-Clocks-Ordering.pdf) | 33 | Physical clocks, NTP, causality, Lamport clocks, vector clocks | 28 |
| [RS-04-Broadcasting.pdf](RS-04-Broadcasting.pdf) | 19 | Delivery order, broadcast guarantees, gossip, algorithm exercises | 19 |
| [RS-05-to-be-finished.pdf](RS-05-to-be-finished.pdf) | 30 | Replication, retries, concurrent writes, quorums, state machine replication | 26 |
| [RS-06-to-be-finished.pdf](RS-06-to-be-finished.pdf) | 8 | Consensus introduction, total-order broadcast, two-phase commit | 5 |
| [dist-sys-notes.pdf](dist-sys-notes.pdf) | 91 | Martin Kleppmann, Cambridge: detailed notes, including Raft and consistency | Not extracted in this pass |
| [dist-sys-slides.pdf](dist-sys-slides.pdf) | 516 | Martin Kleppmann, Cambridge: corresponding slides, including progressive reveal frames | Not extracted in this pass |
| [concurrent.pdf](concurrent.pdf) | 238 | Cambridge concurrency material; first page credits David J. Greaves and Martin Kleppmann, with acknowledgements | Not extracted in this pass |

Total: **9 PDFs, 1,055 pages**. Searchable text is available in every document; individual sparse pages may contain figures. This is an inventory and selected-page visual review, not a full technical review of all pages.

The **157 raster objects** are unique within each RS PDF, not globally deduplicated teaching figures. They include repeated branding, screenshots, and diagram components. Vector artwork is not counted as a raster object.

## Extracted files

`extracted/inventory.json` contains document metadata and counts. Each document has:

- `extracted/<filename-without-extension>/text.txt`: text separated by PDF page number.
- `extracted/<filename-without-extension>/pages.json`: page previews, text length, image occurrence counts, and vector-path counts.

The six RS decks additionally have `images/` and `images.json`, linking each extracted image object to its source pages and dimensions. Transparency masks are applied where present. Raw PDF text can contain ligatures, reordered text, and broken formulas; check it against the page before reuse.

Tables have not yet been reconstructed. Vector diagrams and diagrams split across images and text should be cropped from the page or rebuilt during lecture development, preserving captions and attribution.

## Mapping to the proposed syllabus

| Target lecture | Primary legacy pages | Suggested use |
| --- | --- | --- |
| 01 Foundations | RS-01 pp. 7–38; RS-02 pp. 24–46 | Definitions, concurrency/parallelism, assumptions, network/node/timing models |
| 02 Architectures | RS-01 pp. 39–66 | Cluster, grid, cloud, integration, pervasive systems; add explicit service-boundary reasoning |
| 03 Communication | RS-02 pp. 3–22; RS-05 pp. 8–10 | Latency/bandwidth, RPC message flow, retries and idempotency |
| 04 Naming | RS-01 pp. 30–33 | Transparency motivation only; substantial discovery/naming material still needed |
| 05 Time | RS-03 pp. 3–33 | Physical time, clock synchronization, causality, logical/vector clocks and exercises |
| 06 Replication | RS-05 pp. 4–30 | Replica behaviour, conflict resolution, quorum examples, state machine replication |
| 07 Consensus | RS-06 pp. 2–5; dist-sys-notes pp. 56–65 | Consensus, relation to total-order broadcast, then detailed Raft development |
| 08 Fault tolerance | RS-02 pp. 47–52; RS-05 pp. 19–25 | Availability terminology, failure detection, replication failures and repair |
| 09 Transactions | RS-06 pp. 6–7; dist-sys-notes pp. 66–68 | Two-phase commit; add failure cases and application-level workflows |
| 10 Messaging | RS-04 pp. 3–19 | Reliable, FIFO, causal and total-order broadcast; gossip and algorithm exercises |
| 11 Scaling | RS-01 pp. 34–37 and 41–51 | Scalability motivation and system types; partitioning/rebalancing needs expansion |
| 12 Design review | RS-01 pp. 38 and 66; RS-02 pp. 47–50 | Hidden assumptions, security motivation, availability; observability needs expansion |

The detailed-note page ranges come from its contents page and should be read in full during development.

## Recommended sequence adjustment

The legacy sequence teaches **broadcast ordering before replication and consensus**. The proposed syllabus currently places messaging after both. Preserve this dependency by introducing broadcast guarantees between lectures 05 and 06, or by splitting foundational broadcast from later queues/stream processing. This is a recommendation; the existing numbering has not been changed.

## Selected visual assets reviewed

- RS-02 p. 17: RPC sequence and serialized request/response example; visible Martin Kleppmann attribution.
- RS-03 p. 23: happens-before timeline; visible Martin Kleppmann attribution.
- RS-03 p. 31: vector-clock timeline example.
- RS-04 p. 10: relationships between broadcast guarantees.
- RS-05 p. 23: read/write quorum overlap diagram.
- RS-06 p. 7: two-phase commit message timeline.

Some reusable diagrams are already embedded as raster images. Prefer the original Cambridge vector version where available and matched to the same figure.

## Review notes for migration

- RS-01 pp. 3–6 contain historical course administration; do not treat obligations, grading, or contact arrangements as current requirements.
- Attendance/quiz short links and 2022/23 footers belong to the old decks and should not carry into new course material automatically.
- Hardware examples, protocol versions, availability figures, and timekeeping policy require current verification when reused.
- The quorum diagram on RS-05 p. 23 needs accompanying assumptions: intersecting read/write sets alone are not a complete consistency argument under concurrency and failures.
- Keep atomic commit and consensus distinct when developing RS-06's short 2PC introduction.
- The two unfinished decks are useful sources but not complete lectures.
- The first pages of `dist-sys-notes.pdf` and `dist-sys-slides.pdf` explicitly state **Creative Commons BY-SA**. Preserve Martin Kleppmann's attribution and record the applicable source license when adapting those materials. Several RS slides already credit him; attribution should follow the material into its new location.

## Next migration step

Develop lecture 01 from the mapped introduction and system-model pages, preserving useful examples and self-assessment questions. Extract only the selected teaching assets into that lecture's `assets/`, and cite the source PDF and page in `sources.md`. Build and review the chapter and slides before expanding the next lecture.
