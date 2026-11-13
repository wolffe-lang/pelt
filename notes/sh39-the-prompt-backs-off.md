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

## Forbidden

No other shell's source. Reference shells are black boxes only. No background
probe or idle refresh. No toolchain, CI or instruction-file changes. No
attribution trailers, labels, merges, tags or issue state changes.

## Inputs verified

Base: `45c4de11a52a3c670acf3a48b5f8fdd0cf387d66`. README,
`docs/FRIENDLY.md`, the previous hangup note, prompt witness, session harness,
and the local-gate tests were read before this prediction.

## Evidence index

Pending the red-first rows, measurements, final gauntlet and plant record.

## Done-when

- [ ] Back-off rows red before the implementation and green afterward.
- [ ] Refused execution rows compare against dash, with friendly-only hints.
- [ ] Three kept corners have rows and explicit documentation.
- [ ] Prompt costs measured before and after.
- [ ] One separate planted break is red by name.
- [ ] Final-head gauntlet, open pull request and one audit.
