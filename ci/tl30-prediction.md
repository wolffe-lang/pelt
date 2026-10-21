# tl30 — the macOS cap: the prediction, before the first change

Written before any tl30 change to this repository is committed, against
trunk `01fec4d`. Contract: `sprints/tooling/tl30-footprints-and-the-macos-cap.md`
(planning repo `wolffe-lang/wolf`, trunk `809e40f`), under `sprints/RULES.md`.
The org-wide census (every repository's macOS jobs, the last 60 runs each
ran one, every red macOS job against its Linux counterpart) is wolf-lang's
`ci/tl30.md`; this is pelt's slice.

**Why.** Since the Team plan (2026-10-20) the Linux pool is 60 slots and the
macOS pool is still 5: tl29 measured all five macOS slots busy 55 % of the
time after the switch, a median macOS wait of 17.6 minutes. pelt's merge
gate (`tier full`: the `full-matrix` label, and again on the trunk push)
holds two macOS slots, the gauntlet's native leg (18.5 to 25.5 minutes)
and its release leg (18.4 to 23.4).

**What the macOS legs caught.** The last 60 runs with a macOS job
(38275349105 .. 39504135828, 2026-10-12 to 10-20): 11 red macOS jobs; in
five the ubuntu gauntlet of the same attempt was green:

| run | lane | what macOS alone saw | what it was |
|---|---|---|---|
| 38745068019, 38747594660 | sh15 | four Ctrl-V session cases | macOS's `od -c` pads its columns: the test's bytes (`198cb96`) |
| 39029075072 | sh17 | `quote/ds_contexts` | BSD `od`: the test's bytes (`06fe9fe`) |
| 39157796715, 39157808792 | sh18 | the `c_jc_*` job-control sessions | **a defect of pelt's**: a job's notice raced the host (macOS reaps a killed job before the next prompt's look), fixed in `src/sh/jobs.lu` (`04f1fc3`); beside it two host rules the tests now take (`71fa22c`, `d726186`) |

So the macOS gauntlet has caught a red no Linux job caught, in the session
corpus (the terminal and job control: macOS-shaped), on the **native**
compiler tier: in those runs one macOS job ran both tiers, and its step
"the session corpus, native tier" went red (8.7 minutes, job 117764578826)
while "the session corpus, release tier" was skipped after it, so the
record names the native leg alone. That leg stays at the merge whole. The macOS **release** leg (pelt#40's
split, eight runs since, none red) caught nothing a Linux leg did not and
leaves the merge for the nightly: the same steps, the release compiler,
on macOS.

## The shape

| tier | when | the gauntlet's legs |
|---|---|---|
| `all` (new) | the nightly; `workflow_dispatch -f tier=all` | linux x86-64, macOS arm64, linux aarch64, each native and release (6) |
| `full` | the `full-matrix` label (the merge gate); a trunk push; a dispatch (the default); a path no rule names | linux x86-64 native and release, **macOS native**, linux aarch64 native and release (5) |
| `pr` | any other pull-request run; `-f tier=pr` | linux x86-64 native and release |
| `noop` | prose alone; another label | — |

The nightly is `tier all`, every leg as `tier full` was before tl30; its red
still opens the `nightly-red` issue (`ci/nightly-red.sh`, unchanged).
`lane-audit.sh` accepts a green `tier all` as the superset of `tier full`
(tl29); the merge rule is unchanged.

## Prediction

Before (the six labelled and trunk-push `tier full` runs 39357537780 ..
39504135828): **38.6 macOS-minutes a run** (median; native 19.2, release
19.7), two macOS slots, 66.4 job-minutes, 43 minutes of wall.

1. `tier full` (the label and every trunk push): **18 to 26 macOS-minutes
   and one macOS slot a run** (falsified above 30), about **46 job-minutes**
   (falsified above 55); wall the macOS native leg's, 20 to 30 minutes with
   a free runner. About **−20 macOS-minutes a run, −39 a merge** (the
   label's run and the trunk push's).
2. `tier all` (the nightly, `-f tier=all`): unchanged, six legs, 63 to 78
   job-minutes, 37 to 49 of them macOS.
3. `tier pr`: unchanged (linux x86-64, both tiers).
4. The planted break (`full_leg` answering every leg, the merge's shape
   before tl30) reds `ci/tiers-test.py` in the plan job of a dispatch
   `-f tier=pr` on its own branch; nothing else runs; under 2 job-minutes.
5. This pull request touches `ci/` and `.github/`, so its pull-request run
   is `tier pr`; the labelled run at the final head is the first `tier
   full` of the new shape and is the measurement (its macOS leg is read
   when it ends; the orchestrator watches the run, RULES §6).
