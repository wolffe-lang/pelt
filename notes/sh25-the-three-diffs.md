# sh25 — the three diffs a local model wrote, and the two reds pelt owed (pelt#62)

**Lane sh25, GPT-6.1-Sol, crawl 54, 2026-10-23. Merged at trunk `9cf5ee31`.** This note is the PR body as the lane handed it back, written into `notes/` by the orchestrator at merge (the lane's wrapper refuses to write notes). The raw evidence is under `notes/sh25-evidence/`.

This adopts **wollf-v7sf3 (wl66's window run)**'s three diffs by name: **`pwd -x`** (retain rejection, preserve `--`, grouped flags and operand boundaries), **`cd -P -e`** (retain acceptance, implement unresolved-cwd failure rather than ignore it), and **`printf %d 12x`** (retain numeric-prefix conversion, extend it to signed/octal/hexadecimal and whitespace inputs). It also repairs notice5's malformed here-documents and applies the measured RSS slack approved for pelt#60.

Footprint: cross-cutting

## 1. Forbidden, absolutely

Clean-room: no shell, libc or kernel source read. Dash and bash were black-box oracles. No pin, nominal RSS allowance or iteration count changed; only the explicitly approved per-row slack changed. No build on nomad-1, package installed, merge, tag, issue filed or issue closure. No attribution trailers. Required builds, corpus, sessions and measurements ran in sh25's private rootless containers on kasumi, core limit0. R-sh25-2 is taken: **no host fork readings**. Source checkouts were isolated; no shared branch was switched or committed.

A Mac worktree-local signing-setting mistake was reported; the orchestrator restored the shared repository setting. No further Mac git configuration was changed.

## 2. Inputs, verified

- Trunk `9d4f56cb`; final head **9cf5ee319de16699cc32e6ac37c99e448c843e9a**. Source/tool head `63104f9`; later changes are docs, README and raw evidence only. All final source/tool/case hashes match `notes/sh25-evidence/logs/tested-inputs.sha256`.
- Wolf0.2.34 `9da7bdcf`, lupin0.1.55 `e642f26`, std `e036bec` unchanged. Tags/objects and release digests read twice; fetched archives pass the pinned hash checks. `notes/sh25-evidence/inputs.txt` records the identities and archive digests.
- Original wl66 patches and check logs read; native-only checks there did not stand in for this lane's release tier or gauntlet. Original diffs and SHA256 manifest are preserved under `notes/sh25-evidence/patches/`.
- pelt#16/#59/#60, sh22/sh24's memory method, PR58's headings and px61's Linux/PAX recordings were read. GitHub's same-head native readings were independently verified in raw logs: PR39841894702 **124**, trunk39847135493 attempt1 **213**, attempt2 **135 B/turn**.
- Baseline corpus995/0/28 and sessions290/0/2. **519/548 statements**, not the contract's517: each independent wl66 patch measured516→517; all three together retire three pending statements. Full generated current table is in CENSUS section5; the original sh06 prose remains explicitly historical.

## 3. Prediction

Committed before implementation in `cb8ad1f`, `notes/sh25-evidence/prediction.txt`. All three reviewer predictions held; the added controls fail all three original model patches, not just trunk. Notice5 changes only rows9/10. The prediction that not every #60 reading would stay below110 B/turn also held.

| diff | as wollf-v7sf3 wrote it | as adopted |
|---|---|---|
| pwd | reject every multi-character argument beginning `-` | keep status2/`diag`; accept grouped L/P, stop at `--` or the first operand |
| cd | empty `-e` arm, claiming resolution already checks it | track `-e`; with `-P`, unresolved physical cwd answers1; avoid shortcutting that check |
| printf | scan sign and decimal digits, then `parse_const(prefix) else 0` | retain scan/fallback and bad status; scan the C constant's octal/hex base and whitespace too |

All three original PENDING rows and meta markers are removed, and no unrelated pending is retired. Dash supports the pwd controls and the printf prefixes; **dash does not support `cd -e`**, so the existing POSIX.1-2024 case retains bash `--posix` as its oracle.

### #60: the required trunk readings

Unchanged trunk binaries and trunk instrument, N10000→20000. All legs inside the container and confined by outer taskset12–15; “bare” omits only the inner taskset. Commands, affinity and uptime are in `logs/baseline-assigned.status`.

| pass | native inner taskset | native bare | release inner taskset | release bare |
|---|---:|---:|---:|---:|
| 1 |92|76|83|112|
| 2 |108|129|99|99|
| 3 |125|81|108|93|

B/turn; native76–129, median100; release83–112, median99. All12 pass the old bound. Earlier exploratory container controls (bare unpinned, taskset12–15) supplied the ruling's original table, preserved rather than replaced:

| pass | native taskset | native bare | release taskset | release bare |
|---|---:|---:|---:|---:|
| 1 |137|87|96|96|
| 2 |75|83|81|80|
| 3 |117|70|101|76|

Diagnostic retained RssAnon, not substituted for the peak gate: native91/91/91, release91/92/91, dash−1/−1/0 B/turn. The shape has a real local keep around91 B/turn; no new retaining object was established. These diagnostics do not prove GitHub's unobserved RssAnon was identical.

**R-sh25-1(a), taken by the maintainer:** retain100 B/turn and N10000, add256 KiB to this row's allocator/runner slack,1024→1280 KiB. Exact effective gate2000→2256 KiB (204.8→231.0144 B/turn). GitHub's failed2088 KiB peak was88 KiB beyond the old gate. This is a runner-spread allowance, **not a claimed leak fix**. The dedicated commit includes the original readings table in its message body.

### #59: notice5 before/after

| row | old recording | corrected recording |
|---|---|---|
|9 stdout|`doc\|E; echo "st=0"`|`doc\|st=0`|
|10 stdout|empty|`st=0`|
|10 file|`doc\|E; echo "st=0"\|`|`doc\|`|

The other18 rows are byte-identical under dash. The checker rejects the old recording and accepts the corrected one. Baseline/head comparisons on each pelt tier independently prove the same18 rows unchanged and exact corrected9/10 bytes.

The initial final driver compared pelt's row15 diagnostic text with dash's and failed both notice-check legs. Those reds remain in `logs/final.status`; `notice-domain.txt` explains the correction. `retake-notice.sh` compares the same shell before/after, with **the unchanged checker**, all six commands green. The validator explicitly requires the original row15 diagnosis and the six retake results; it does not silently ignore a red. No binary, corpus assertion or RSS result changed.

px61's old Linux and PAX recordings contain the same malformed delimiter payload. PAX should replay the repaired fixture after taking this commit; **no corrected PAX execution is claimed**, and no pax repository was touched.

## 4. Evidence index

All local paths below are under `notes/sh25-evidence/`.

- `f5426ed`: pwd adoption and option controls.
- `7bfcc26`: cd adoption and removed-cwd failure; `80957a7` documents its statuses.
- `52478e1`: printf adoption and numeric-prefix controls.
- `eb22cb9`: newline-delimited notice5 status and corrected dash recording.
- `63104f9`: the ruled per-row256 KiB slack, unchanged nominal100/N10000, readings in the commit body.
- `c257b0a`: regenerated CENSUS; `1efc62a`: Unreleased; `ab8e9f1` and `9132261`: README counts and fixture extension.
- `0b21457`, `3d88f32`, `96cb2fe`: baseline/model/assigned-core measurements and CI plant evidence.
- `f0698fc`: complete final evidence and explicit same-shell notice retake; `9cf5ee3`: pruning record.

**Reds:** `logs/plant-three.log`: strict trunk cases29/3/4. `logs/model-original-strengthened.log`: original model patches29/3/4. `logs/plant-notice5.log`: old malformed recording rejected. Fixed targeted cases32/0/4 on both tiers in `logs/review.launch.log`.

**Cross-cutting CI plant:** run **39882857944**, branchsh25-plant at `c49c4f2`, smallest tier-pr dispatch. A deliberately retained growing string in this row's body exceeds even the new slack: native**15577**, release**15595 B/turn**, exactly one shape failure per tier. Jobs120184160532/native and120184160531/release; tier-pr120189962703 red. First verdict read once; full log and JSON retained in `logs/ci-plant-*`. This branch never merges.

**Final local evidence:** `logs/final.status`, `logs/notice-retake.status` and `logs/validator-green.txt`: all required outcomes validated, no SKIP. Corpus**998/0/25 x4**, sessions**290/0/2 x4**, checked unit1 passed/0 rejected/0 unsupported, compiled self-checks on both tiers, fmt, width, all witnesses/selftests and oracle-check**0 drift**. Three complete52-row shape passes/tier, bare and inner-taskset, **624 passing assertions**. `gauntlet.sh`, `retake-notice.sh` and `validate.py` reproduce and strictly validate the evidence.

Final background-subshell readings (B/turn), not a claim of retention improvement:

| pass | native bare | native taskset | release bare | release taskset |
|---|---:|---:|---:|---:|
|1|107|81|116|117|
|2|78|135|90|111|
|3|60|138|114|60|

All final legs inherit CPUs12–15/core0. At launch those cores were99.2–99.6% idle despite high system load from other affinity-pinned work. Uptime and the idle series are recorded; global load later reached53.67 during sessions, not an sh25 RSS measurement. The orchestrator identified r40/s259 work on other cores and the GPU RPC service; t06's dist build was not visible at the initial check. No run was restarted to manufacture a quieter value. At most two RSS workers ran together.

## 5. Done-when

- [x] Prediction committed before implementation; three model diffs reviewed, credited and adopted in separate commits.
- [x] New controls fail trunk and the original model patches; fixed native/release controls pass.
- [x] Notice5 rows9/10 re-recorded; other18 unchanged; PAX replay handoff explicit.
- [x] Trunk readings, diagnostic split, taken rulings and effective bounds recorded.
- [x] Final local gauntlet complete, strict validator green,624 RSS assertions; initial notice-domain failures preserved with explicit correction.
- [x] CENSUS/Unreleased updated; README read and refreshed (counts and `.sh` fixture extension), build/install paragraphs current.
- [x] Build artifacts pruned: target/.wolf-bin/cache/base-bin/tmp removed;56M clone/source/evidence remain on kasumi. Plant worktree removed; plant branch/run evidence retained.
- [ ] Final-head CI green before merge: the orchestrator watches; this lane reads the first PR-tier status once and hands back.

Final-head CI/audit, read without waiting:

- PR-tier **39889770327**: first verdict read once, **in progress**, tier job not completed.
- Full-matrix **39889847247**, labelled at the unchanged final head; **not awaited**.
- Required `bash wolf/tools/lane-audit.sh pelt sh25 62`: exit1, last line **`AUDIT FAIL (footprint: cross-cutting)`**. Only final-head CI/tier completion is missing; fast-forward, footprint, shas, five sections, label and other static checks pass. Do not merge before green at this head.
- [pelt#16 comment](https://github.com/wolffe-lang/pelt/issues/16#issuecomment-6355941688) records the three cases and leaves its other corners open.

The CI watch and merge belong to the orchestrator. The orchestrator writes `notes/sh25-the-three-diffs.md` from this complete record at merge; no standalone Markdown report was written by this lane.

On merge, close pelt#59 and pelt#60 manually. pelt#16 is already commented with these three cases; its other corners remain open. No new issue to file. No issue was filed or closed here.

