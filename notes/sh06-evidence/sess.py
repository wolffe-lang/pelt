#!/usr/bin/env python3
"""sess — lane-local: write the census session cases (keys + meta)."""
import os, sys
ROOT = sys.argv[1]
S = os.path.join(ROOT, "tests", "session")
JC = {"oracle_args": "-i -m", "pelt_args": "-i -m"}
ED = {"oracle": "bash", "compare": "stdout"}
long_line = "echo " + "a" * 5000 + " | wc -c"
C = {
 "c_jc_shell_is_leader": (JC, ["[ \"$(ps -o pid= -p $$ | tr -d ' ')\" = \"$(ps -o pgid= -p $$ | tr -d ' ')\" ] && echo leader", "exit"]),
 "c_jc_foreground_group": (JC, ["sh -c 'a=$(ps -o pgid= -p $$ | tr -d \" \"); b=$(ps -o tpgid= -p $$ | tr -d \" \"); [ \"$a\" = \"$b\" ] && echo foreground; [ \"$a\" != \"$(ps -o pgid= -p $PPID | tr -d \" \")\" ] && echo own-group'", "exit"]),
 "c_jc_background_job": (JC, ["sleep 30 &", "jobs", "kill %1", "wait", "echo st=$?", "jobs", "exit"]),
 "c_jc_background_group": (JC, ["sh -c 'a=$(ps -o pgid= -p $$ | tr -d \" \"); [ \"$a\" = \"$$\" ] && echo leader > out' &", "wait", "cat out", "exit"]),
 "c_jc_terminal_back": (JC, ["sleep 0", "echo back", "sh -c 'exit 3'", "echo st=$?", "exit"]),
 "c_jc_ctrl_z": (JC, ["sleep 30", "^Z", "echo st=$?", "jobs", "kill -9 %1", "exit", "exit"]),
 "c_jc_fg": (JC, ["cat", "^Z", "fg", "typed after fg", "^D", "echo st=$?", "exit"]),
 "c_jc_bg": (JC, ["sleep 1", "^Z", "bg", "wait", "echo st=$?", "jobs", "exit"]),
 "c_jc_bg_ttin": (JC, ["cat &", "echo next", "jobs", "kill -9 %1", "exit", "exit"]),
 "c_jc_done_message": (JC, ["true &", "sleep 0.3", "echo next", "exit"]),
 "c_jc_jobs_list": (JC, ["sleep 30 &", "sleep 31 &", "jobs", "jobs -l | wc -l", "jobs -p | wc -l", "kill %1 %2", "exit"]),
 "c_jc_jobs_states": (JC, ["sleep 30 &", "sh -c 'exit 3' &", "sleep 0.3", "jobs", "kill %1", "exit"]),
 "c_jc_shell_ignores_tstp": (JC, ["^Z", "echo alive", "exit"]),
 "c_jc_fg_number": (JC, ["sleep 30 &", "sleep 1 &", "fg %2", "echo st=$?", "kill %1", "exit"]),
 "c_jc_ctrl_c_job_only": (JC, ["sleep 30", "^C", "echo st=$?", "exit"]),
 "c_ignoreeof": ({"oracle": "bash", "oracle_args": "--noediting -i +m", "env": "PS1=$"}, ["set -o ignoreeof", "^D", "echo still-here", "exit"]),
 "c_ps1_bang": ({"oracle": "bash", "oracle_args": "--noediting -i +m", "env": "PS1=!!>"}, ["echo x", "exit"]),
 "c_redirect_error": ({}, ["echo x > /nonexistent/f", "echo alive", ": < /nonexistent", "echo alive2", "exit"]),
 "c_mail": ({}, ["MAIL=$HOME/mbox MAILCHECK=0", "echo x > $HOME/mbox", "echo next", "exit"]),
 "c_alias_interactive": ({}, ["alias hi='echo hello'", "hi there", "unalias hi", "hi", "exit"]),
 "c_tty_erase": ({}, ["\\k echo abX\\x7fc\\r", "\\k echo one two\\x17three\\r", "\\k echo gone\\x15echo kept\\r", "exit"]),
 "c_paste_two_lines": ({}, ["\\k echo a\\necho b\\n", "exit"]),
 "c_long_line": (ED, ["PS1='$ '", long_line, "exit"]),
 "c_hist_fc_list": (ED, ["PS1='$ '", "echo one", "echo two", "fc -ln -2 -1", "exit"]),
 "c_hist_fc_s": (ED, ["PS1='$ '", "echo first", "fc -s first=second", "exit"]),
 "c_hist_fc_edit": (ED, ["PS1='$ '", "echo edit-me", "fc -e 'sed -i s/me/done/'", "exit"]),
 "c_vi_basic": (ED, ["PS1='$ '", "set -o vi", "\\k echo abc\\ex\\r", "exit"]),
 "c_vi_motion": (ED, ["PS1='$ '", "set -o vi", "\\k echo abcd\\e0wiX\\e\\r", "exit"]),
 "c_vi_history": (ED, ["PS1='$ '", "set -o vi", "echo first", "\\k \\ek\\r", "exit"]),
 "c_vi_insert": (ED, ["PS1='$ '", "set -o vi", "\\k echo abc \\x17xyz\\r", "exit"]),
 "c_ed_left_insert": (ED, ["PS1='$ '", "\\k echo ac\\e[Db\\r", "exit"]),
 "c_ed_home_end": (ED, ["PS1='$ '", "\\k cho x\\x01e\\x05y\\r", "exit"]),
 "c_ed_kill_to_end": (ED, ["PS1='$ '", "\\k echo keepXXX\\e[D\\e[D\\e[D\\x0b\\r", "exit"]),
 "c_ed_delete_char": (ED, ["PS1='$ '", "\\k echo abXc\\e[D\\e[D\\x04\\r", "exit"]),
 "c_ed_up_arrow": (ED, ["PS1='$ '", "echo first", "\\k \\e[A\\r", "exit"]),
 "c_ed_up_down_edit": (ED, ["PS1='$ '", "echo one", "echo two", "\\k \\e[A\\e[A\\e[B\\x7f\\x7f\\x7fTWO\\r", "exit"]),
 "c_ed_search": (ED, ["PS1='$ '", "echo findme", "echo other", "\\k \\x12find\\r", "exit"]),
 "c_ed_complete_file": (ED, ["PS1='$ '", "touch unique_file_name", "\\k echo uniq\\t\\r", "exit"]),
 "c_ed_complete_command": (ED, ["PS1='$ '", "\\k unam\\t -s >/dev/null && echo completed\\r", "exit"]),
 "c_ed_word_motion": (ED, ["PS1='$ '", "\\k echo one three\\ebtwo \\r", "exit"]),
 "c_ed_utf8_erase": ({"oracle": "bash", "compare": "stdout", "env": "LC_ALL=C.UTF-8"}, ["PS1='$ '", "\\k echo a\\xc3\\xa9\\x7fb\\r", "exit"]),
 "c_ed_utf8_left": ({"oracle": "bash", "compare": "stdout", "env": "LC_ALL=C.UTF-8"}, ["PS1='$ '", "\\k echo \\xc3\\xa9\\xe4\\xb8\\xad\\e[Dx\\r", "exit"]),
}
for name, (meta, keys) in C.items():
    open(os.path.join(S, name + ".keys"), "w").write("\n".join(keys) + "\n")
    mp = os.path.join(S, name + ".meta")
    old = {}
    if os.path.exists(mp):
        for line in open(mp):
            k, _, v = line.rstrip("\n").partition("=")
            old[k] = v
    old.update(meta)
    open(mp, "w").write("".join(f"{k}={v}\n" for k, v in old.items()))
print(len(C), "session cases")

PEND = {
 "alias": (["c_alias_interactive"], "`alias` and alias substitution", "pelt (P03)"),
 "line editor": (["c_ed_complete_command", "c_ed_complete_file", "c_ed_delete_char", "c_ed_home_end", "c_ed_kill_to_end", "c_ed_left_insert", "c_ed_search", "c_ed_up_arrow", "c_ed_up_down_edit", "c_ed_utf8_erase", "c_ed_utf8_left", "c_ed_word_motion", "c_long_line"],
   "no line editor: the terminal's own line discipline does the editing, so an arrow key, Home/End, Ctrl-A/E/K/D/R, Tab, Alt-B are typed into the command as bytes, a line stops at the terminal's 4,095 bytes, and a multi-byte character is erased a byte at a time. Recorded from `bash --posix -i` (dash has no editor of its own in this build's default mode); only standard output and the exit are compared, since each editor draws its own line",
   "pelt (sh07, sh08); wolf-lang W05 (window size, `SIGWINCH`) for a resized window; rulings R2, R3"),
 "history": (["c_hist_fc_edit", "c_hist_fc_list", "c_hist_fc_s", "c_ps1_bang"], "no command history: `fc`, the history number in `PS1`'s `!`", "pelt (sh08)"),
 "vi mode": (["c_vi_basic", "c_vi_history", "c_vi_motion"], "`set -o vi` is accepted and does nothing (XCU `sh`, Command Line Editing)", "pelt (sh09), after the editor"),
 "ignoreeof": (["c_ignoreeof"], "`set -o ignoreeof` is accepted and Ctrl-D still ends the shell", "pelt (P10)"),
 "mail": (["c_mail"], "`MAIL`, `MAILCHECK`, `MAILPATH`: no notice before the prompt", "pelt (P10); the file's time is `fs_stat`"),
 "job control": (["c_jc_background_group", "c_jc_background_job", "c_jc_bg", "c_jc_bg_ttin", "c_jc_ctrl_z", "c_jc_done_message", "c_jc_fg", "c_jc_fg_number", "c_jc_foreground_group", "c_jc_jobs_list", "c_jc_jobs_states"],
   "no job control: `set -m` is accepted and does nothing — no process group per job, no terminal handoff, Ctrl-Z stops nothing the shell can report, no `jobs`, `fg`, `bg`, no job numbers or completion notices. Recorded from `dash -i -m`",
   "wolf-lang W03 (stop reporting, `SIGCONT`, a signal to a group) and #680 (a wait that a signal or a second child can end), #141 (`kill` built in); then pelt (sh12, sh13)"),
 "getpid": (["c_jc_shell_is_leader"], "`$$` off linux (passes on linux)", "wolf-lang#141"),
}
for tag, (names, _, _) in PEND.items():
    for n in names:
        mp = os.path.join(S, n + ".meta")
        lines = [l for l in open(mp).read().split("\n") if l and not l.startswith("pending=")]
        lines.append(f"pending={tag}")
        open(mp, "w").write("\n".join(lines) + "\n")
out = ["<!-- census:begin -->", "The census cases (sh06, `c_*`; `docs/CENSUS.md`), by what they wait on.",
       "\"P03\", \"W03\" and the like are the issue texts in the sh06 report", "(`notes/sh06-the-census.md`).", "",
       "| waits on | what is missing | whose work | cases |", "|---|---|---|---|"]
for tag, (names, what, who) in PEND.items():
    out.append(f"| **{tag}** | {what} | {who} | " + ", ".join(f"`{n}`" for n in names) + " |")
out.append("<!-- census:end -->")
p = os.path.join(S, "PENDING.md")
s = open(p).read()
if "<!-- census:begin -->" in s:
    a, _, rest = s.partition("<!-- census:begin -->")
    _, _, b = rest.partition("<!-- census:end -->")
    s = a + "\n".join(out) + b
else:
    assert "No case is pending." in s
    s = s.replace("No case is pending.", "\n".join(out))
open(p, "w").write(s)
