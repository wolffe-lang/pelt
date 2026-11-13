# A prompt that backs off, and a refused file that names itself

## Prediction

Keep the synchronous 50 ms collection deadline for `den status --porcelain`.
Two consecutive deadline misses in the same directory suppress further probes
until a different working directory is observed at a primary prompt. A timely
completion resets the consecutive-miss count. A rejected answer retains only
the last same-directory value, dimmed; without one, draw nothing. No background
child, elapsed-time retry, prompt-count retry or idle refresh is added. Retrying
only on directory change is recommended: an expensive directory should not
periodically charge another 50 ms for an answer already known to be unusable.

Before the implementation, `tools/prompt-witness` will gain named rows checking
the stand-in den's own call log: two slow probes, no third or later probe,
re-arming on directory change, uninterrupted fast probes, and a timely answer
resetting the miss count. The rows will fail before the fix. Existing stale
value, invalid UTF-8 and no-per-key-probe rows must stay green. A separate
planted reversal will make the no-third-probe row fail by name.

For #122, rows will run a non-executable regular file, a directory and, when
a container permits a noexec mount, an executable file on it. Compare status
with dash (126), require `pelt: PATH: permission denied`, and require exactly
one actionable hint only in friendly interactive mode. The pre-fix rows must
fail the missing path. The recommendation is a quoted `chmod +x FILE` hint for
a regular file lacking executable mode bits, a quoted `sh FILE` hint for an
executable regular file rejected by execution, and no misleading hint for a
directory. POSIX mode and scripts must have no hint.

The kept corners need no implementation change: inherited ignored SIGHUP stays
ignored; a trapped SIGHUP at a prompt runs its action and continues; a refused
exit with stopped jobs sets status 0. Confirm their existing witness/session
rows and add plain documentation of each difference from bash where missing.

Measure direct den status and 15 prompt turns with and without den, across the
same repository sizes as the earlier measurement. Compare before and after on
the same host; record the first two slow prompts separately from later turns.

## How the prediction held

`prompt-vcs-backoff-third` was red at the base: the stand-in logged three
starts. It is green after the change, with two starts. The witness also holds
`prompt-vcs-backoff-first`, `-second`, `-stays`, `-fast`, `-cd`, `-reset` and
`-stale`; its rows wait for the actual next prompt, not a fixed sleep. The
clock-controlled unit rows distinguish a deadline miss from a timely rejected
answer. Only the former counts toward back-off; either a successful or a
rejected timely completion clears the consecutive-miss count.

The #122 prediction needed one correction: the base already named the path
and returned 126 on Linux and macOS. The reported pathless diagnostic was not
reproduced there. The new exact prompt format and missing friendly hint were
red before the change and are green afterward. The regular-file, quoted-name,
directory and actual noexec-mount rows all return dash's 126. Non-interactive
plain, `command` and `exec` forms retain their diagnostic location and get no
hint. Kernel execution decides permissions; no mode-bit precheck replaces it.
The mode bits choose only which hint to display after a refusal.

A provisional extra PATH-search case was removed rather than inventing an
unrequested rule: the installed dash returned 127 for it in the Linux
container and 126 on macOS. This change concerns explicitly found paths.
No PATH-search status was changed.

The three kept corners already have their rows at the base:

- `ignored` in `tests/hangup/expected`: an ignored inherited SIGHUP stays ignored.
- `trap` and `trap-fg`: the HUP action runs and the shell continues.
- `exit-stopped` and `exit-stopped-bg`: the second exit uses status 0 after the
  first was refused; `c_jc_ctrl_z` and `c_jc_exit_stopped` also remain in the
  typed-session corpus. Both typed sessions passed in the preparatory run.

README and CHANGELOG now call these pelt's rules and explicitly name bash's
different answers: override the inherited ignore, leave after the prompt's
HUP action, and status 1 after a refused exit, respectively. No signal or
job-control implementation was changed.

## Prompt cost before and after

`notes/sh39/prompt-cost.py` makes the same repository shapes as the previous
measurement: N committed files in directories of 200, then up to 60 changed.
The full table, including maxima and both no-den baselines, is
`notes/sh39/prompt-cost.csv`. Linux, one bounded container on two CPUs, with
the execution and timing locks held. den is the release build at `a749692d`;
pelt is native, before at `45c4de11` and after at `73a58f8`. Later changes only
adjust the rig and this evidence; the measured prompt implementation is the
final one. Every row ran, none skipped. Each steady-state column is the median
of 15 turns; the first two prompts are excluded and reported separately.

All times below are milliseconds. The baseline column is the after binary
without den on PATH.

| files | direct status, median / max | prompt before, median / max | first two after | prompt after, median / max | baseline |
|---:|---:|---:|---:|---:|---:|
| 10 | 0.77 / 0.94 | 4.87 / 5.20 | 2.41 / 4.98 | 4.80 / 5.16 | 3.52 |
| 100 | 2.17 / 2.44 | 7.27 / 7.48 | 5.21 / 7.83 | 7.20 / 7.58 | 3.71 |
| 400 | 5.91 / 6.19 | 19.94 / 20.76 | 17.59 / 20.70 | 20.21 / 22.34 | 3.62 |
| 2,000 | 28.17 / 30.06 | 59.61 / 61.35 | 56.74 / 59.53 | 3.77 / 4.58 | 3.73 |
| 3,000 | 42.23 / 46.74 | 59.83 / 61.07 | 56.91 / 60.05 | 3.50 / 4.48 | 3.50 |
| 5,000 | 71.13 / 72.98 | 59.89 / 60.48 | 57.06 / 59.96 | 3.76 / 4.59 | 3.76 |
| 10,000 | 143.06 / 151.99 | 58.76 / 59.09 | 55.62 / 59.40 | 3.79 / 4.59 | 3.51 |
| 20,000 | 303.20 / 317.42 | 56.45 / 56.80 | 53.90 / 56.72 | 3.65 / 4.28 | 3.77 |

At 10, 100 and 400 files all 15 steady-state prompts show a fresh segment,
before and after. At every larger size neither binary shows a segment in any
of the 15 turns: before, every turn still pays the deadline; afterward, only
the first two prompts pay it. Direct status cost is not the probe's entire
cost: here the probe misses already at 2,000 files even though direct status
is under 50 ms. This is a same-machine comparison, not a comparison with the
earlier machine's timings or a measurement on PAX.

## Forbidden

No other shell's source. Reference shells are black boxes only. No background
probe or idle refresh. No toolchain, CI or instruction-file changes. No
attribution trailers, labels, merges, tags or issue state changes.

## Inputs verified

Base: `45c4de11a52a3c670acf3a48b5f8fdd0cf387d66`. README,
`docs/FRIENDLY.md`, the previous hangup note, prompt witness, session harness,
and the local-gate tests were read before this prediction.

The unchanged pin is wolf 0.2.36, lupin 0.1.58 and std `78b9d3cb`.
`tools/fetch-toolchain` checked the release archive digests on Linux and macOS;
every build checked the compiler/interpreter identities and the std revision.
The Linux images are `localhost/r41-toolchain:1` (`77fdad6b841a`, Ubuntu 24.04,
dash 0.5.12) and `localhost/sh38-oracle:1` (`717765173fa0`, Unicode 16.0.0 for
the width-table check). The measured den was rebuilt from `a749692d` rather
than using an installed binary with older command support.

## Evidence index

- `c1f48f7`: prediction committed before the tests or implementation.
- `e6155f8`: counted-start back-off rows, red at the base; `6a9b3bb`: back-off
  implementation and deterministic-clock unit rows; `b5ac60a`: actual-prompt
  pacing rather than a fixed wait in the new witness.
- `17554f1`: refusal rows before the fix; `3f78b3c`: named prompt diagnostics
  and hints; `c59a0ab`: leave permission decisions to the kernel.
- `69fe6b2`: friendly limits and explicit bash differences; `6e637ac`: README
  only, read and refreshed. `e0be158` corrects its inherited corpus count to
  the measured 1,051 cases. This pass adds no differential or typed-session cases.
- The corrected Linux preparatory run at `73a58f8`: build, full raw prompt
  witness, refusal witness (including the real noexec mount), format check,
  self-check, differential corpus and both kept job-control sessions, all
  green. The differential corpus reports 1,036 passing and 15 pending; no
  pending case is represented as a pass.
- macOS native smoke at `73a58f8`: build, refusal witness, counted back-off,
  format and self-check, all green. The noexec row was explicitly skipped
  there; it ran on Linux.
- `notes/sh39/prompt-cost.py` and `notes/sh39/prompt-cost.csv`: repeatable rig
  and all eight before/after measurement rows. The full private run log has
  sha256 `9caba6ba92b471f9ec3cfd0a0514caf1bef7405fde977aa3a5a77058902c8f30`.
- `notes/sh39/rig/`: committed, preflighted steps for both tiers' full gauntlet,
  the plant, and a recorder parser-shape fixture. The full gauntlet and its
  separate one-hunk plant are indexed in the PR, not replaced by these smoke
  checks. The full take's completion remains a delivery gate.

Preparatory rig corrections are retained, not called product flakes: the first
measurement attempt used an older installed den without configuration writes;
a corpus attempt ran as root and failed the three permission-sensitive rows;
and an unprivileged attempt found its noexec fixture directory unwritable.
The rig now preflights the unprivileged identity, writable noexec fixture and
Unicode image. Clean-environment fixtures have their container fallback
storage mapped into the run directory, not the host's temporary directory.
No heavy job ran in a light slot.

## Done-when

- [x] Back-off rows red before the implementation and green afterward.
- [x] Refused execution rows compare against dash, with friendly-only hints.
- [x] Three kept corners have rows and explicit documentation.
- [x] Prompt costs measured before and after.
- [ ] Delivery evidence in the PR: separate one-hunk plant red by name,
  final-head full gauntlet and one audit. The commit to pin on PAX is the
  final PR head after that gate is green; no PAX runtime test was run here.
