# Pending differential cases

Every case here has its expectation recorded from dash like any other,
RUNS on every `tools/difftest` pass, and is reported as `PEND-ok` or
`PEND-fail`; it does not decide the exit status. `tools/difftest` fails
any case marked `pending=` in its `.meta` that is not named below, so
nothing is skipped silently. A case leaves this list in the commit that
makes it pass.

| primitive pelt waits on | where it comes from | cases |
|---|---|---|
| **signal number** — `128+N` for a child killed by signal N | wolf-lang#534 (`os_wait`'s `signal` row carries no number: pelt answers 128); s219's `os_wait_status` (wolf-lang PR #636, unreleased) answers `-N` | `pending/signal_status` |
| **env unset** — removing a variable from the environment a child receives | wolf-lang#534 (no environment unset or clear: `unset HOME` still reaches `/usr/bin/env`) | `pending/unset_env` |
| **getpid** — `$$` on every host | wolf-lang#141 (pelt reads `/proc/self/stat` on linux; macOS has no `/proc`) | `pending/pid` |

**No case, named:** `$!` is pelt's job number, not a process id: the
handle `os_spawn_fds` answers is a table index (wolf-lang#141 covers the
process's own pid, not a child's), so `wait $!` works and `kill $!`
would signal the wrong process. s219's `os_proc_pid` (wolf-lang PR #636,
unreleased) is the way to a real one; reaping a background child
without waiting for it needs its CHILD meaning and poll. And with no
fork, a pipeline stage pelt runs itself runs to the end before the next
starts, so an endless in-process producer (`while :; do echo y; done |
head -1`) does not end as it does under dash.
| **user database** — `~login` | no `getpwnam` surface in wolf 0.2.26; not filed until a lane needs it beyond this case | `tilde/user` |

**Cleared by sh03 (H2, wolf 0.2.26):** the fifteen cases that waited on
s215's descriptor builtins — `pipe/pipeline_status`, `control/pipeline`,
`redir/redirect_out`, `redir/redirect_err`, `redir/heredoc`,
`builtin/dot`, `builtin/times`, `func/unset_f`, `tilde/middle`,
`cmdsub/external`, `control/async_list`, `jobs/background`,
`builtin/cd`, `cd/cd_subshell`, `simple/child_stdin` (the ones that
were under `pending/` moved to their subjects' areas).
