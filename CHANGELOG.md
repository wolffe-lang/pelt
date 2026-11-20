# Changelog

## 0.1.0 — 2026-11-20

- First 0.1.0 release of the POSIX shell, with the documented compatibility boundaries and named pending cases preserved. See docs/CENSUS.md and docs/CHANGELOG.md for the behavior ledger and development history.
- Add `pelt --version` and align it with the package manifest.
- Require the complete all-tier gate, including both macOS compiler tiers, before staging checksummed archives as a draft.
- History is appended before each interactive command runs and synced once, when the shell ends by `exit`, end of input or a hangup. Nothing on the interactive path waits for the disk. With `HISTSIZE` unset the history keeps 1000 entries.
- Variables such as `$HOME/` and `${HOME}/` name completion paths; the typed text stays intact and nothing is executed.
- Editor test controllers wait for the editor's readiness, and idle samples start only after the editor has answered a key.
- Linux runners are pinned to ubuntu-24.04, and the release gate is regenerated from that CI.
