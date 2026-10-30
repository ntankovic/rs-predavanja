# Lecture 01 — second narrative review

Reviewed after implementing lecturer-requested story improvements, 2026-09-15.

## Result

The slide and chapter order now follows the submission problem consistently. No further section move is recommended. Concurrency immediately answers the workload question; the later retry discussion explicitly reuses it with A and B representing two attempts of one submission.

| Slides | Student question | How the sequence answers it |
| --- | --- | --- |
| 1–5 | Did my Unity project arrive, and who is involved? | Opening vote, system map, then the distributed-system definition. The uncertainty is intentionally held open. |
| 6–7 | If processing takes 20 minutes, must everyone wait? | Distinguish receiving/queueing from processing, then show interleaved and simultaneous work. Definitions follow a concrete need. |
| 8 | Why distribute beyond handling more work? | Tie resource sharing, resilience, reach, interfaces, and transparency to university needs. End with the communication dependency. |
| 9–10 | What changes when work crosses a network? | Local/remote comparison and performance illustration; the 100 TB question returns explicitly to one student's response time. |
| 11–14 | What could explain the opening timeout? | Partial failure, two contrasting histories, and an explicit return to the vote. |
| 15–17 | Should I retry, and what must stay correct? | Pair discussion, reuse concurrency for original/retry, then invariant, safety, and liveness. |
| 18–21 | Under which assumptions can we promise correctness? | Network/node/timing questions, model vocabulary, then an application exercise whose numerical answer was not given earlier. |
| 22–23 | How can I use these ideas to design the next step? | One-minute recap, then a two-minute open deadline/receipt design challenge, ending with a crash-during-checks follow-up. |

## Corrections verified

- Workload question and concurrency are adjacent (slides 6–7).
- Workload reasoning and broader motivations have separate slides and time allocations.
- A and B first mean different students' jobs; their later use for original/retry is explicit.
- Liveness consistently requires eventual acceptance of valid submissions under stated recovery, delivery, retention/retry, and processing assumptions. Rejecting all work fails this selected property.
- The model overview explains guarantees generally; the 100 ms assertion is left for the final exercise.
- The 100 TB illustration explicitly returns to portal latency. Its 22.2-hour calculation is optional follow-up, not required within the one-minute discussion.
- Definition numbers and text agree across chapter and slides and follow introduction order.

## Verification and remaining judgment

The 23-slide plan totals 60 minutes, including discussion and recap. Structural verification and the full browser layout check passed. Visually reviewed the changed slide layouts and corresponding chapter/book sections. Lecture PDF: 16 pages; combined draft book: 31 pages.

Pacing is still a teaching plan, not a classroom rehearsal. Keep the 100 TB detour to its allotted minute and model taxonomy introductory. Detailed scaling mechanisms, retry implementation, and formal timing variants remain later-lecture material. Lecturer pacing/emphasis review remains open; status stays `review`.

Closing challenge updated: the final activity extends the problem instead of repeating the answered timeout case. Timing is 57–58 recap and 58–60 design discussion, preserving the hour.
