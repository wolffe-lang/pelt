# Rebase and renewed gates

Base: `ed5963c56d45cdea64fa02a0bee6d3ece4003ceb`. This replaces PR #123,
whose head was `554a18a5d13e9b3c17707eddaa136e500e8516d1`.

## Prediction

The rebase changes none of this change's patches. `git range-diff` matches
all nineteen commits with `=` and there were no conflicts. The new base adds
only the hangup witness's platform-aware signal-sender expectations and its
notes; this pass's implementation, prompt/refusal witnesses, docs and rig
files are otherwise identical to the old head. Original notes and commit
references remain a historical account, not evidence for this new head.

The old head's full local record was green: 45 steps, worst=0, sha256
`3e0a0e3f2f62812e50c357d0e6c5603ae66ddf7db881c9682ca2ff1ce674c034`.
It does not gate this rebased head. Retake the full both-tier Linux gauntlet
with standalone preflight first, and the focused macOS prompt and refusal
witnesses on both compiler tiers. A fresh one-file, one-hunk plant on this
head must still fail `prompt-vcs-backoff-third` by counted probe starts.

No feature decision or bound changes on rebase. The synchronous 50 ms budget,
two-miss back-off, directory-change re-arm and friendly-only refusal hints
remain as documented in `notes/sh39-the-prompt-backs-off.md`.

## Evidence index

- Rebased patch series before this delivery note: `2b5c96e`.
- `notes/sh39/rig/gauntlet.manifest`: full 45-step local take.
- `notes/sh39b/mac.manifest`: focused prompt and refusal checks, native and
  release, after builds from the same committed head.
- New records and the replacement plant are indexed in the replacement PR.
  A running or partial record is not a green verdict.

## Done-when

- [x] All nineteen patches rebase unchanged, with no conflict.
- [ ] Fresh final-head Linux gauntlet green and verified.
- [ ] Focused final-head macOS record green.
- [ ] New plant red by name and recorder verified.
- [ ] Hosted Linux and macOS runs green. Prompt and terminal changes require
  both, even with green local records. A failure of `c_hist_fc_edit` must be
  read and investigated; the existing report in #126 is not a reason to
  dismiss a new red without inspecting it.

No PAX runtime test or deployment is claimed. Pin the replacement PR's final
head only after all required gates are green. PR #123 is left open for its
owner to close; this change closes no PR or issue itself.
