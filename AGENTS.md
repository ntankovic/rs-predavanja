# Agent working rules

Read `COURSE.md` before creating or editing course material.

- The lecturer authorizes routine project `just` build and verification commands without further confirmation. Run them directly, subject to the execution environment's enforced permissions.

- Develop and tune teaching material in Croatian first, then translate the reviewed Croatian version into English. Read `references/terminology.md` before writing or translating; record lecturer-approved translations there and reuse them across lectures. Plan each full lecture for 60 minutes, including discussion and recap, and record timing in the brief and `timing.json`; speaker notes carry no timing lines (lecturer, 2026-10-13).
- Follow the illustration workflow in `COURSE.md`: plan explanatory diagrams with the content, preserve source attribution, and verify them in both PDF and HTML output.

- Work lecture by lecture using `lectures/_template/`.
- Check the lecture registry before starting. Respect existing ownership and changes.
- Keep an assigned lecture's chapter, slides, sources, and assets together in its directory.
- Coordinate changes to shared files, the lecture registry, and book assembly order with the coordinating agent.
- Do not edit another agent's assigned lecture without coordination.
- Treat `chapter.qmd` as the detailed explanation from which `slides.qmd` is derived; keep both consistent.
- Verify technical claims and references. Explicitly flag unresolved questions rather than inventing facts or citations.
- Before handoff, complete the lecture review checklist and report changed files, checks performed, and unresolved issues.
- A draft is not a finished export. Mark a lecture `ready` only when its chapter and slides have passed review.
