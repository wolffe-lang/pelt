# tl28 — the prediction, before the first change (ruling #92)

Written before any tl28 change to this repository is committed, against
trunk `cc2fdc9`.

**Before** (the ten completed push/pull_request runs of `ci` up to
39173199730): one job, the gauntlet, on three legs (linux x86-64, macOS
arm64, linux aarch64, the last asserting both tiers refused); **47.3
job-minutes** a run (median 49.9; the green ones 47 to 61) and **32.6
minutes of wall** (median; max 68.0). macOS is the long pole (24 to 35
minutes), linux x86-64 22 to 25, aarch64 1.

**After, predicted:**

1. A pull-request push is `tier pr`: the plan (under 1 job-minute, the
   planner's test inside it), `gauntlet (ubuntu-latest, true)` (22 to 25)
   and the verdict (under 1): **23 to 27 job-minutes, about 25 minutes of
   wall**, the macOS and aarch64 legs skipped: about half the job-minutes
   of a run before, and macOS's 35-minute pole gone from a lane's wait.
2. The `full-matrix` label at the head is `tier full`: all three legs,
   **about 60 job-minutes and 35 minutes of wall**, as before.
3. A dispatch with `-f tier=pr` of a branch that adds a path no rule names
   comes out `tier full`, all three legs.
4. The planted break (an unmapped path classified pr in `ci/tiers.py`) reds
   the plan job at "the planner can say no", skips the gauntlet, and the
   verdict job, `tier unplanned`, is red: **1 to 2 job-minutes**.
5. A notes-only pull request (most of this repository's prose: notes/ is
   1,259 of 5,236 tracked paths) is `tier noop`: the plan and the verdict.
