# Pending session cases

Every case here has its transcript recorded from `dash -i +m` like any
other, is typed into pelt on every `tools/session` pass, and is reported
as `PEND-ok` or `PEND-fail`; it does not decide the exit status.
`tools/session` fails any case marked `pending=` in its `.meta` that is
not named below, so nothing is skipped silently. A case leaves this list
in the commit that makes it pass.

<!-- census:begin -->
The census cases (sh06, `c_*`; `docs/CENSUS.md`), by what they wait on.
"P03", "W03" and the like are the issue texts in the sh06 report
(`notes/sh06-the-census.md`).

| waits on | what is missing | whose work | cases |
|---|---|---|---|
<!-- census:end -->

None is pending since sh26.

**Cleared by sh26 (the corners):** `c_ignoreeof` (`set -o ignoreeof`:
the end of file refused with dash's words, R-sh26-4) and `c_mail`
(`MAIL`, `MAILPATH`, `MAILCHECK`, R-sh26-5). New with them:
`mail_path`, `mail_interval` and `jc_assign_text` (pelt#56).

**Cleared by sh20 (wolf 0.2.34, the fork):** `c_jc_mixed_pipeline`: a
stage pelt runs itself is a process that joins the job's group with
`SUSPEND` at the default, so Ctrl-Z stops the whole pipeline as one job.
New with it: `jc_subshell_stop` (a foreground `( … )` is a job Ctrl-Z
stops and `fg` continues), `jc_background_subshell` (the prompt's line
goes on while `( … ) &` runs) and `subshell_jobs` (which subshells list
the shell's jobs, as dash's).

**Cleared by sh18 (wolf 0.2.32, job control):** `c_jc_background_group`,
`c_jc_background_job`, `c_jc_bg`, `c_jc_bg_ttin`, `c_jc_ctrl_z`,
`c_jc_done_message`, `c_jc_fg`, `c_jc_fg_number`, `c_jc_foreground_group`,
`c_jc_jobs_list`, `c_jc_jobs_states`: a pipeline of programs in a group of
its own, the terminal handed over and taken back, stops reported by
`os_wait_poll`, `jobs`, `fg`, `bg`, the notices. pelt is given `+m`
in every session dash is (`tools/lib_session.py`'s `argv_for`).

**Cleared by sh16 (the completion):** `c_ed_complete_command`,
`c_ed_complete_file` (Tab completes commands, files and variables,
ruling #69 R3).

**Cleared by sh15 (wolf 0.2.30):** `c_ed_ctrl_v`, `c_ed_tab_literal`,
`c_vi_insert_ctrl_v` (lnext: the editor turns `EXTENDED` off while a
line is edited, so macOS hands it Ctrl-V too).

**Cleared by sh14 (wolf 0.2.29):** `c_jc_shell_is_leader` (`$$` is
`os_pid` on every host).

**Cleared by sh12 (the history):** `c_ed_search` (Ctrl-R),
`c_hist_fc_edit`, `c_hist_fc_list`, `c_hist_fc_s`, `c_ps1_bang`,
`c_vi_v`; and the differential case `fc/c_noninteractive`.

**Cleared by sh11 (the line editor):** `c_ed_delete_char`,
`c_ed_home_end`, `c_ed_kill_to_end`, `c_ed_left_insert`, `c_ed_up_arrow`,
`c_ed_up_down_edit`, `c_ed_utf8_erase`, `c_ed_utf8_left`,
`c_ed_word_motion`, `c_long_line`, `c_vi_basic`, `c_vi_history`,
`c_vi_motion`.

**Cleared by sh05 (wolf 0.2.27):** `ctrl_c_prompt` and `ctrl_c_child`
(an interactive pelt listens for `SIGINT`, `[os.signal.disp]`, and
polls for it after the line is read and after the child is reaped).

**Cleared by sh03 (H2, wolf 0.2.26):** `child_stdin`, `cd_root`,
`pipe`, `redirect_file`, `heredoc`, `background`.

**Gaps with no session case**, because the harness cannot type them:

- **`set -b`'s notice while a line is typed** (2.11/11) — the harness
  types when the shell is quiet and cannot place a notice between two
  keys; and dash 0.5.13.4 writes it at the next prompt anyway (sh18,
  black-box p11), where POSIX and bash write it at once, as pelt does
  (`notes/sh18-evidence/probe/keys/p24`, `p25`).
- **the history file across shells** — a session is one shell, so
  `HISTFILE` written by one shell and read by the next, two shells
  sharing one file at once, and the file cut to `HISTSIZE` are asked
  from outside by `tools/hist-witness` (sh12), in CI on both tiers.
- **a command typed right after Ctrl-C at an empty prompt** — dash
  0.5.13.4 loses that line's newline (typed `^C`, `echo after`,
  `exit`, it runs `echo afterexit`); pelt runs each line as typed. Not
  recorded as a case: it is a quirk, not a behaviour scripts rely on.

**isatty** is covered by the differential corpus, not here: the
`stdin/` cases run the shell with the script on a pipe and no operand,
and `default_interactive` types into pelt with standard error a pipe;
in both, pelt (`os_isatty(0)` and `os_isatty(2)`) and dash decide the
shell is not interactive.


## PAX friendly display rows (pending harness slot)

These are pending targets, not runnable host cases or claimed PAX passes.
A px-owned pelt-session slot is required; run each once on framebuffer and
serial (`TERM=linux`). Use the current pelt on both consoles.

| target | exact input bytes, in order | expected observation |
|---|---|---|
| `sh29_pax_framebuffer_shadow` (pending) | `set -o friendly -o suggest -o histsearch\r` then `echo shadow_tail\r` then `echo shadow` then `\r` then `echo shadow` then `\x15` | SGR 90 suffix `_tail`, cursor after typed `shadow`; Enter prints `shadow` only; EL clears after Ctrl-U |
| `sh29_pax_serial_history` (pending) | `set -o friendly -o suggest -o histsearch\r` then `echo alpha\r` then `echo beta\r` then `echo al` then `\x1b[A` then `\x1b[B` then `\x12` then `\r` then `\x03` | Up selects alpha, Down restores `echo al`; Ctrl-R list below line; Enter accepts without running; Ctrl-C leaves the editor with its normal next prompt |

The byte notation is the session harness's: `\r` is 0d, `\x15` is Ctrl-U,
`\x12` is Ctrl-R, `\x03` is Ctrl-C, `\x1b[A/B` are Up/Down. Pause at each
`then` until the screen has settled. The framebuffer's SGR basis is px70's
16-entry palette; serial rendering belongs to the host terminal.


## PAX colour rows (pending harness slot)

Run on both framebuffer and serial, with `TERM=linux`; these are pending
targets, not host passes. px70's measured 16-entry palette is the basis.

| target | exact input bytes, in order | expected observation |
|---|---|---|
| `sh30_pax_framebuffer_colour` | `set -o friendly -o suggest\r`, `echo prefix_suffix\r`, `echo prefix`, `\x0c`, `\r` | command default, typed argument cyan, shadow SGR90; redraw keeps the cursor; Enter prints only prefix; no coloured text enters history |
| `sh30_pax_serial_colour` | `set -o highlight\r`, `echo )`, `\r`, `set +o highlight\r`, `echo plain\r` | erroneous token and caret bright red, ordinary message reset; after disabling, no syntax colours; terminal modes restored |

At a px-owned resize step, narrow the first row's live edit to 16 columns
and widen to 80 before Enter. No stale wrapped row may remain. This lane
has not run either console or built PAX.
