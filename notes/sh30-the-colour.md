# sh30 — the colour (pelt#81, merged at `be80068d`; notes at `a274d13`)

This note is the PR body of pelt#81, materialised at the merge by the orchestrator (the lane's wrapper could not write Markdown). The measurements and logs are under `notes/sh30/`.

Footprint: cross-cutting

Final regression ran at `9338727`; the rebase added only `887ce12` (notes/sh29-the-shadow.md), with source, tools, tests and CI inputs unchanged.

## Forbidden

No shell or line-editor implementation source read. Fish was measured only
through owned ptys. No Mac build, git config, PAX build, label, merge, tag,
release or issue filing. Hasu uses block B, CPUs 6–11 under its flock, with
rootless containers limited to 12 GB. The five sections here are the lane
note; evidence and the sh31 draft live under `notes/sh30/`.

## Inputs verified

- Source base `b942504d`, sh29's owned display layer; final head `be80068`.
- Unchanged wolf 0.2.35 / lupin 0.1.56 / std `2386522e`; release digest
  fields and downloaded archive hashes read twice, whole archives staged.
- Fish 4.9.3-1 has exactly sh29's binary SHA. Rebuilt upstream Arch has
  dash 0.5.13.4-1 / bash 5.3.20-1, not CachyOS's -1.1/-2 package rebuilds.
  No expectation was re-recorded against those different packages.
- All 1,038 corpus cases and 443 original session expectations unchanged;
  45 new sessions make 488. The final regression explicitly checks this.
- px70's palette/cell evidence read; no PAX rendering result claimed.
  Exact framebuffer/serial inputs remain pending a px-owned harness slot.

## Prediction

`d96bc4e` recorded predictions before measurement. The classifier is 258
lines, inside the guessed 250–350; palette/rendering work exceeded its
150–200-line guess. Added 45 sessions, not 60. Release highlighting met
both predicted and required per-key bounds. Several guessed fish colours
were wrong: comments are red, arguments cyan, variables bright cyan,
separators green, and unresolved commands bright red. Fish echoes and
repaints asynchronously; pelt's synchronous span redraw bytes differ.

Recommendations, implemented but not maintainer rulings:
- **R-sh30-1 A:** unresolved names bright red immediately, before a separator.
- **R-sh30-2 A:** use fish's measured deterministic 16-colour defaults on linux.
- **R-sh30-3 A:** pager rows keep their own plain styles, not syntax colours.
- **R-sh30-4 A:** resolved commands use the measured default foreground, not
  the campaign's guessed green. `PELT_COLORS=command=green` is available.

Fish's Enter diagnostic/caret was uncoloured. Existing pelt printed only
its ordinary message, contrary to the brief's caret premise. The coloured
source span and caret added here are explicitly pelt behavior.

## Evidence index

Implementation chunks (pre-rebase hashes):
- `1f2990b`: pure classifier and per-kind/parser-state checks.
- `5014a77`: shared renderer, atomic PELT_COLORS, independent option bit
  1048576, direct buffer/history/undo/kill-ring invariants.
- `82a7e02`: parser error span/caret and raw typed reset-boundary witness.
- `0354a7c`: 45 typed cases and CI gate; budget test observed red before green.
- `09e452e`: continuation-prompt quote context without storing styles.
- `e58e394`, `661d516`: user docs, PAX pending inputs and README refresh.
- `9338727`: final regression asserts legacy expectations remain unchanged.

Final whole regression on hasu B at `9338727`, 07:46:56–08:21:50Z:
- [x] Native/release builds, warnings denied; canonical formatting.
- [x] Checked tests and both compiled selfchecks; zero unsupported tests.
- [x] CI planner, including colour gate and session-budget assertions.
- [x] Whole corpus on each tier: 1,023 pass / 0 fail / 15 named pending,
  all 1,038 cases run.
- [x] All 488 typed sessions on each tier: 488 pass / 0 fail / 0 pending.
- [x] Raw colours, reset-before-motion/erase, error caret, theme fallback,
  script/pipe/POSIX/tty/dumb gates, shadow, pager, resize and history laws.
- [x] Direct editor storage checks, command census and PS2 quote context.
- [x] Shadow, terminal restoration and history witnesses on both tiers.
- [x] Strict release cost and child-THP-disabled idle checks.
- [x] Legacy expectations unchanged; tracked inputs identical before/after.
- [x] Every final step exit 0; `FINAL: 0 failed`, process exit 0.

Durable final log: `/home/mfwolffe/lanes/sh30/final-job.log`, SHA256
`c1be0f2a8cc5afba03dfefe026f281a8cfa89a3e373cd2192127bb70018baa41`.
Per-step evidence is in `/home/mfwolffe/lanes/sh30/pelt/notes/sh30/logs/`;
Mac copy `/Users/mfwolffe/lanes/sh30/final-evidence/`. Input-manifest SHA256,
both before and after:
`89578438901c720d306515671dca9e98d9d318a7e19926b24186c9fcead49cdc`.
The final log was re-hashed after copying. No source change after its run.

The initial baseline's three failures were one missing container dependency:
`cmp` in exec/exec_pid on both tiers and in the input comparison. Installing
container diffutils made both full corpus reruns and input comparison pass;
no application or fixture fix. Original reds and reruns remain retained.

Final 80-column line cost, 100 keys after warmup, live owned-pty responses:

| tier / run | median ms | p99 ms | idle 10 seconds |
|---|---:|---:|---|
| native | 0.157638 | 0.462189 | zero context switches; RSS 10536 → 10536 kB |
| release | 0.103542 | 0.302383 | zero context switches; RSS 7776 → 7776 kB |
| release strict repeat | 0.108042 | 0.309086 | zero context switches; RSS 7824 → 7824 kB |

CPU/fault/anonymous-memory counters are also unchanged. THP is disabled in
only the fixture's child. The strict local release gate requires median and
p99 below 1 ms; CI allows scheduling noise while enforcing exact raw bytes.
Prompt initialization made 2,316 filesystem calls; 80 typed characters plus
200 editing keys afterward made zero. Explicit paths are statted once per
distinct spelling per prompt. No display-time expansion, execution or fork.

Plants, fixes committed first at `09e452e`; orchestrator verified intended
CI failures and closed all three drafts unmerged:
- #78 `08ce0c5`, run **40173879512**: `tools/colour-witness`, argument colour
  row fails on both tiers (magenta planted where cyan is required).
- #79 `9b21d69`, run **40173884134**: storage-invariant selfchecks, five
  failures; the planted escape reaches buffer/undo/history/kill state.
- #80 `7100921`, run **40173887873**: `colour-resize-narrow` rejects missing
  clearing of old coloured display rows.

## Done-when

Implementation, both-tier whole regression, named-red plants, measurements,
docs and sh31 draft are complete. README read and refreshed. This is not
merge approval: final-head PR CI and the orchestrator's labelled full tier
are still required. The lane adds no label and does not wait on CI.

`notes/sh30/follow-on.txt` drafts F3: abbr persistence, described completion
pager and interactive opt-in `!!`/`!$`. `issues-to-file.txt` names reproducible
oracle packaging, the existing argv[0] re-pin, a PAX session slot and bounded
semantic-highlighting follow-ons. No issue filed or closed. Substitution
bodies are one variable span; aliases are recognized by name, not expanded
for display; cached external changes need a fresh prompt. These limits are
documented rather than hidden background work.

`notes/sh30/prune-list.txt` lists only this lane's paths. Preserve final
logs and raw measurements until review. Mac source/plant worktrees are
clean and pushed; cleanup and audit status follow in the handoff.

