#!/usr/bin/env python3
"""sh16: write the completion session cases (keys, meta, files) into
tests/session/. Transcripts come after: `tools/session-record` for the
cases recorded from bash, pelt's own run checked by eye for the ones
marked tr_by=hand (notes/sh16-the-completion.md §4)."""
import os
import sys

SESS = os.path.join(sys.argv[1], "tests", "session")
ECHO = "#!/bin/sh\necho \"zq:$*\"\n"

BASH = "PS1=$\\s"
CASES = {}


def case(name, keys, why, files=None, hand=False, extra=None):
    meta = {"env": BASH, "compare": "stdout"}
    if not hand:
        meta["oracle"] = "bash"
        # session-record's second opinion: dash completes nothing
        # (logs/record3.log: "bash differs" names the other shell)
        meta["dash"] = "differs"
    else:
        meta["tr_by"] = "hand"
    meta["why"] = why
    meta.update(extra or {})
    CASES[name] = (keys, meta, files or {})


ZQ = {"home/bin/zqcmd": (0o755, ECHO), "home/bin/zqxa1": (0o755, ECHO),
      "home/bin/zqxa2": (0o755, ECHO), "home/bin/zqxbb": (0o755, ECHO)}
P = "PATH=$HOME/bin:$PATH"

# --- recorded from bash --posix -i (pelt's standard output must equal it)
case("c_ed_complete_names", [P, "f_mine() { echo \"fn:$*\"; }",
     "\\k zqcm\\tX\\r", "\\k f_mi\\tX\\r", "\\k umas\\tX\\x01echo \\r", "\\k whil\\tX\\x01echo \\r"],
     "Tab completes a command in PATH, a function, a built-in and a reserved word, each with a space after it", ZQ)
case("c_ed_complete_after_ops", [P, "\\k echo hi | zqcm\\tX\\r", "\\k true; zqcm\\tX\\r",
     "\\k true && zqcm\\tX\\r", "\\k echo $(zqcm\\tX)\\r", "\\k (zqcm\\tX)\\r"],
     "a command name after |, ;, &&, $( and ( is completed as a command", ZQ)
case("c_ed_complete_lcp", [P, "\\k zq\\ta1\\tX\\r", "\\k zqxa\\t\\t2\\tY\\r"],
     "several matches: the longest common prefix, then typing on, and a second Tab (a list) changes nothing in the line",
     {k: v for k, v in ZQ.items() if "zqx" in k})
case("c_ed_complete_slash_cmd", ["\\k ./scr\\tX\\r", "\\k ./scd\\tx\\tY\\x01echo \\r"],
     "a command word with a slash completes files: an executable, a directory", 
     {"w/script.sh": (0o755, ECHO), "w/scfile": (0o644, "x\n"), "w/scdir/xfile": (0o644, "x\n")})
case("c_ed_complete_dirs", ["\\k echo su\\t\\t\\tX\\r"],
     "a directory completes with a slash and no space; Tab again goes on inside it",
     {"w/sub/dir/afile": (0o644, "x\n")})
case("c_ed_complete_quoting", ["touch 'my file' 'dol$b' \"q'uote\" 'zd\"q' 'amp&b;c(d)' 'st*ar'",
     "\\k echo my\\tX\\r", "\\k echo do\\tX\\r", "\\k echo q\\tX\\r", "\\k echo zd\\tX\\r",
     "\\k echo am\\tX\\r", "\\k echo st\\tX\\r"],
     "a name with a blank, $, quotes, &;() or * is inserted quoted so it reads back as itself")
case("c_ed_complete_newline", ["touch \"$(printf 'nl\\nname')\"", "\\k echo nl\\tX\\r"],
     "a name with a newline reads back as itself (bash quotes the whole word, pelt the newline alone: the same standard output)")
case("c_ed_complete_in_quotes", ["touch 'my file'", "\\k echo \"my\\tX\\r", "\\k echo 'my\\tX\\r",
     "\\k echo my\\\\ \\tX\\r"],
     "inside a quote the word opened, the name is completed inside it and the quote closed")
case("c_ed_complete_mid_word", ["touch unique_file_name", "\\k echo uniqZZ\\e[D\\e[D\\t\\r",
     "\\k echo uniq \\e[D\\tX\\r"],
     "only the text before the cursor is completed; no space is added when text follows")
case("c_ed_complete_tilde", ["\\k cat ~/do\\tn\\t\\r"],
     "~/ completes from HOME and keeps the tilde in the line",
     {"home/docs/note": (0o644, "note-text\n")})
case("c_ed_complete_abs", ["\\k echo /us\\tX\\r", "\\k echo /usr/bi\\tX\\r"],
     "an absolute path completes from /")
case("c_ed_complete_redirect", ["echo content > unique_file_name", "\\k cat <uniq\\t\\r",
     "\\k echo hi >uniq\\t\\r", "cat unique_file_name", "\\k FOO=uniq\\t\\x01echo \\r"],
     "a file name after < and >, and the value of an assignment, are completed as files")
case("c_ed_complete_var", ["ZQV_ONE=1 ZQV_TWO=2", "\\k echo $ZQV_O\\tX\\r", "\\k echo ${ZQV_O\\tX\\r",
     "\\k echo \"$ZQV_O\\tX\\r", "\\k echo $ZQV\\t\\tO\\tX\\r"],
     "a variable's name after $, ${ (closed with }) and \"$ (the quote closed)")
case("c_ed_complete_nomatch", ["\\k echo qqqzz\\tX\\r", "\\k qqqzz\\t\\x15echo done\\r"],
     "no match: the bell, and the line as it was")

# --- written by hand: pelt chose otherwise than both references
case("c_vi_complete", ["set -o vi", "touch unique_file_name", "\\k echo uniq\\tX\\r"],
     "vi insert mode: Tab completes (the contract; mksh's vi-tabcomplete; bash --posix inserts a tab). Written by hand", hand=True)
case("c_ed_complete_after_assign", [P, "\\k FOO=1 zqcm\\tX\\r", "\\k if zqcm\\tX; then :; fi\\r",
     "\\k ! zqcm\\tX\\r", "\\k echo `zqcm\\tX`\\r"],
     "after an assignment, after if or !, and inside a backquote the word is a command name (XCU 2.9.1, 2.6.3): completed as a command; neither bash nor mksh does (bash does after $( but not in a backquote). Written by hand", ZQ, hand=True)
case("c_ed_complete_var_in_word", ["ZQV_ONE=1", "\\k echo a$ZQV_O\\tX\\r"],
     "a $name inside a word is completed too (bash only at a word's start, mksh never). Written by hand", hand=True)
case("c_ed_complete_hidden", ["touch .hid1 vis", "\\k echo \\tX\\r", "\\k echo .h\\tX\\r"],
     "names starting with . only when the typed part does (pathname expansion's rule, as mksh; bash offers them). Written by hand", hand=True)
case("c_ed_complete_tilde_alone", ["\\k ls ~\\t\\r"],
     "a lone ~ completes to ~/ (bash offers login names, mksh expands it). Written by hand",
     {"home/docs/note": (0o644, "x\n")}, hand=True)

# --- screens written by hand (40 columns)
COLS = {"cols": "40"}
FS = {f"w/f{n}": (0o644, "") for n in ["a", "bb", "ccc", "dddd", "eeeee", "ffffff", "g", "hh", "iii",
                                       "jjjj", "kkkkk", "llllllllllll", "m", "nn"]}
FS["w/fdir/x"] = (0o644, "")
case("c_ed_complete_list", ["\\k echo f\\t", "\\k \\t", "\\k \\t", "\\k \\x15echo done\\r"],
     "the first Tab rings, the second lists the names below the line in columns down then across (the widest plus 2 cells, as many as fit in 39), a directory with /; then the prompt and the line again. Screens and transcript written by hand",
     FS, hand=True, extra=dict(COLS, screen="2-3", screen_by="hand"))
case("c_ed_complete_list_vars", ["ZQV_ONE=1 ZQV_TWO=2", "\\k echo $ZQV\\t", "\\k \\t", "\\k \\x15echo done\\r"],
     "a list of variables shows each with its $. Screens and transcript written by hand",
     hand=True, extra=dict(COLS, screen="2-3", screen_by="hand"))
case("c_ed_complete_list_wide", ["touch été 日本", "\\k echo \\t\\t", "\\k \\x15echo done\\r"],
     "columns are counted in cells: a wide character takes two. Screens and transcript written by hand",
     hand=True, extra=dict(COLS, screen="2-2", screen_by="hand"))
case("c_ed_complete_list_prompt", ["PS1=\"$(printf 'top\\n> ')\"", "touch aa1 aa2", "\\k echo xyz aa\\t\\t",
     "\\k \\x15echo done\\r"],
     "after a list the whole prompt (two lines here) and the line are drawn again. The harness reads standard error through a pipe, where the prompt's newline does not return the carriage, so its first drawing is shifted; the editor's redraw goes to the terminal. Screens and transcript written by hand",
     hand=True, extra=dict(COLS, screen="3-3", screen_by="hand"))
case("c_ed_complete_query", ["i=0; while [ $i -lt 80 ]; do : > q$i; i=$((i+1)); done", "\\k echo q\\t\\t",
     "\\k n", "\\k \\t\\t", "\\k y", "\\k \\x15echo done\\r"],
     "a list taller than the window less a row is asked about first: n draws the line again, y lists; the answer ends the row of Tabs, so asking again takes two. Screens and transcript written by hand",
     hand=True, extra=dict(COLS, rows="10", screen="2-5", screen_by="hand"))

for name, (keys, meta, files) in CASES.items():
    with open(os.path.join(SESS, name + ".keys"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(keys) + "\nexit\n")
    order = ["args", "env", "oracle", "compare", "dash", "tr_by", "why"]
    with open(os.path.join(SESS, name + ".meta"), "w", encoding="utf-8") as fh:
        for k in order + sorted(k for k in meta if k not in order):
            if k in meta:
                fh.write(f"{k}={meta[k]}\n")
    for path, (mode, body) in files.items():
        p = os.path.join(SESS, name + ".files", path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body)
        os.chmod(p, mode)
print(len(CASES), "cases")
