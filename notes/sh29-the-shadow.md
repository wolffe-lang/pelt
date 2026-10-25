# sh29 — the shadow: autosuggestions, fish's history UI, the friendly Ctrl-R (F1)

pelt#77, merged 2026-10-25 at `b942504d` (run 40163399596 green 8/8, AUDIT CLEAN). The lane's wrapper could not write this file, so the orchestrator materialised it from the PR body at merge; the text below is the PR body as merged. The sh30 draft is `notes/sh29/follow-on.txt`; the prune list `notes/sh29/prune-list.txt`.

Footprint: cross-cutting

## Forbidden

No shell or line-editor source read. Fish was measured as a program through
owned ptys in the Arch oracle container. No Mac build/test, Mac git config,
PAX build, label, merge, tag, release or issue filing. Kasumi uses CPUs 4–7
under its flock; no other lane's directory or process is touched.

Report-file restriction: these five sections are the lane note. Evidence,
the sh30 draft, issues and pruning paths are under `notes/sh29/`.

## Inputs verified

- Rebased onto `f3b2160` (sh26); option bits 131072/262144/524288 are distinct.
- Unchanged pin: wolf 0.2.35 / lupin 0.1.56 / std `2386522e`; release asset
  digests and downloaded archive hashes read twice (`digests.txt`).
- Black boxes: dash 0.5.13.4-1.1, bash 5.3.20-2, fish 4.9.3-1; image id
  `3ed18d5c7b242c675807f875e43eabf11bdf87f9eebd875fce9e9b1d1bf7297f`.
- No differential fixture and no pre-existing session expectation changed.
  sh26's baseline is 1,038 differential cases, 380 sessions; this pass adds
  63 typed sessions (443 total), not changes to the old 998-case baseline.
- px70's final SGR/palette evidence was read. No PAX session claimed; two
  exact-byte framebuffer/serial targets remain pending a px-owned slot.

## Prediction

`e10ac2e` committed the prediction before measurement or implementation.
Predicted 65 sessions; added 63. The guessed prefix-of-a-word fallback was
refuted: fish showed none for the measured same-command/different-command
cases. R-sh29-1 B is exact-prefix only. R-sh29-2 A is Ctrl-R Enter accepting
into the line, not running. The contract's default-grey guess was wrong:
fish emits SGR 90 without dim, including with truecolour advertised. That
is pelt's default; no shadow on TERM=dumb. Indexed/RGB PELT_COLORS are F2.

Alt-F accepts one word; Ctrl-Right accepts a blank-delimited token. For
alpha-beta/gamma they stop after alpha and gamma respectively. Fish chooses
the first sorted file candidate even when several match; pelt follows it.
Fish can suggest history after literal `!`; pelt does too, but never treats
leading `!`/`!!` as a command-completion source. No history expansion added.

Pager Ctrl-C deliberately restores the original draft instead of fish's
clear-draft behavior. Fish's narrow shadow truncated with an ellipsis; no
wrap bug was reproduced. Pelt reserves the final cell and truncates without
an ellipsis. New options default off at this pin, preserving old sessions;
the argv[0] re-pin turns them on with friendly under the ruled default.

## Evidence index

**macOS session-budget follow-up (`b942504`).** Full run 40160785846 at
`a0a9873` exhausted the macOS native session step's old 15-minute cap while
still reporting passing `sh29_history_*` cases (about 408 sessions done).
No session failed. The measured new typed-session cost is about 4 seconds
per case on that runner; a conservative 443-case estimate is about 30
minutes. The session step now allows 45 minutes on macOS, retaining 15
on Linux and the existing 45-minute whole-job ceiling. This adds headroom
without skipping or filtering any case. A CI-planner regression test failed
on the old cap and passes with the new host-specific expression (kasumi,
`session-budget-red.log` / `session-budget-green.log` under the lane).
No shell source, fixtures or test expectations changed in this follow-up.
The prior PR-tier run 40160637579 is green; the new head still needs CI.

Implementation chunks:
- `d5e8c11`: independent opt-in options and restoration bits.
- `a0bf90b`: separate display-only shadow, explicit acceptance, prefix history,
  cursor-restoring pager, exact-prefix/unit invariants.
- `c2e48ed`: 63 independently specified output cases and pelt-owned screens.
- `005d82f`: raw bytes, 32,767-entry latency and zero-idle CI gate.
- `b415863`, `8494351`: user docs, exact PAX pending rows and README refresh.
- `00a253c`: live bindings and self-contained reusable fixture helpers.
- `a3241be`, `a0a9873`: retained evidence and durable final-regression script.

Post-rebase checks at the same implementation source:
- [x] Native/release builds, warnings denied.
- [x] Both compiled selfchecks; checked tests: 1 passed, 0 unsupported.
- [x] Canonical Wolf formatting and CI planner tests.
- [x] All 63 new typed sessions on native and release: 63/0 each.
- [x] Raw drawn-never-typed, EL clearing and filtered-history witnesses.
- [x] 32,767-entry oldest-history hit and THP-disabled idle witnesses.
- [x] Full local regression on both tiers: corpus 1,023 pass / 0 fail /
  15 pending; all 443 sessions pass. Every phase returned 0; tracked inputs
  unchanged. Final job ended 0.
- [x] Three named-red plants confirmed by the orchestrator; #74/#75/#76
  closed unmerged.
- [ ] Final-head PR/full CI and lane audit merge gate.

Kasumi cost, 100 responses after warmup, oldest matching entry of 32,767:

| tier | median ms | p99 ms | bytes per measured key | idle 10s |
|---|---:|---:|---:|---|
| native | 0.210697 | 1.638452 | 26 | 0 context switches; RSS unchanged |
| release | 0.126489 | 1.734955 | 26 | 0 context switches; RSS unchanged |

These are end-to-end pty responses, not leaf-function timings. Both are
under 5.5ms; they do not claim a bound for arbitrary cold PATH enumeration.
`logs/post-rebase-cost.log` has CPU/fault/RSS/THP counters. Raw UI uses SGR90,
SGR39, EL and explicit cursor restoration; unaccepted text never enters
Enter, undo or the kill ring. The session screen file's `| ` empty-row
marker is intentional harness syntax, not prose whitespace to trim.

Plants (fix committed first; drafts, never merge):
- #74 `ce4db64`, run 40159960460, first state in_progress: Enter leak;
  `sh29_never_typed` / raw drawn-never-typed must fail.
- #75 `15b9dc8`, run 40159965478, first state queued: missing EL;
  the explicit raw EL assertion must fail.
- #76 `96f3e15`, run 40159969642, first state in_progress: unfiltered Up;
  `sh29_history_twice` / raw histsearch must fail.

## Done-when

The implementation, full local regression, named-red plants, docs, cost
rows and PAX pending rows are done. This is a Codex handoff, not merge
approval: no CI wait or label by the lane. The timeout-only follow-up must
receive green final-head CI before merging.

Final local job paths on kasumi:
`/home/mfwolffe/lanes/sh29/final-job.pid`, `final-job.log`, `final-job.exit`;
per-target results in `pelt/notes/sh29/logs/final.status`, with head and
tracked-input hashes before/after. The complete pair finished with every phase 0 and GAUNTLET: 0 failed;
its exit marker is 0. The timeout-only follow-up does not change its shell
source or fixture inputs.

`notes/sh29/follow-on.txt` drafts sh30: pure syntax classification, a shared
coloured renderer, PELT_COLORS, reset/resize/pager/shadow interaction tests,
<1ms highlighting and zero idle wakeups. `issues-to-file.txt` names existing
pin/terminal/oracle/PAX follow-ons and a PATH-source latency measurement;
no issue was filed or closed. `prune-list.txt` lists only this lane's paths.
README read and refreshed. Audit result follows in the handoff/comment.


