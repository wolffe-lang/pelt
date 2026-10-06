# Pending differential cases

Every case here has its expectation recorded from dash like any other,
RUNS on every `tools/difftest` pass, and is reported as `PEND-ok` or
`PEND-fail`; it does not decide the exit status. `tools/difftest` fails
any case marked `pending=` in its `.meta` that is not named below, so
nothing is skipped silently. A case leaves this list in the commit that
makes it pass.

| primitive pelt waits on | where it comes from | cases |
|---|---|---|
| **pipe** — a pipe between two children, and a child's descriptors mapped onto it | wolf-lang s215 (`os_pipe`, spawn with a descriptor map), pelt H2 | `control/pipeline`, `pending/pipeline_status` |
| **redirection** — a child (or pelt itself) with descriptor 0/1/2 or any other mapped to a file | wolf-lang s215 (spawn with a descriptor map), pelt H2 | `pending/redirect_out`, `pending/redirect_err`, `pending/heredoc`, `builtin/dot`, `builtin/times`, `func/unset_f`, `tilde/middle` |
| **capture** — reading what a child writes, for a command substitution that runs another program | wolf-lang s215 (`os_pipe`), pelt H2 | `cmdsub/external` |
| **background jobs** — `&`, `$!`, `wait` on a real child | a spawn that does not wait (exists) plus `$!` from a pid (wolf-lang#141), pelt H2 | `control/async_list`, `pending/background` |
| **chdir** — changing the working directory | wolf-lang s215 (`os_chdir`) | `builtin/cd`, `pending/cd_subshell` |
| **child stdin** — a child reading the shell's own standard input | wolf-lang s215; today `[os.proc.spawn]` wires a child's descriptor 0 to the null device | `pending/child_stdin` |
| **signal number** — `128+N` for a child killed by signal N | wolf-lang#534 (`os_wait`'s `signal` row carries no number) | `pending/signal_status` |
| **env unset** — removing a variable from the environment a child receives | wolf-lang#534 (no environment unset or clear) | `pending/unset_env` |
| **getpid** — `$$` on every host | wolf-lang#141 (pelt reads `/proc/self/stat` on linux; macOS has no `/proc`) | `pending/pid` |
| **user database** — `~login` | no `getpwnam` surface in wolf 0.2.24; not filed until a lane needs it beyond this case | `tilde/user` |
