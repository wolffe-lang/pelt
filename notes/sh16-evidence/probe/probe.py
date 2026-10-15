#!/usr/bin/env python3
"""sh16 probe: how the reference shells complete at Tab, black-box.

Runs each probe below as a session case (tools/lib_session.py: a fresh
pty, PATH=/usr/bin:/bin, HOME and the working directory in scratch,
LC_ALL=C) under each shell named on the command line, and prints the
transcript, the screen after every step, and the BEL bytes the step
sent to the terminal. Run inside the throwaway reference container
(Debian trixie: bash 5.2.37, mksh 59c, dash 0.5.12); no shell's source
is read, only its binary is run.

usage: probe.py PELT_TREE [shell ...]   (shells: bash mksh dash pelt=PATH)
"""
import os
import sys
import tempfile

TREE = sys.argv[1]
sys.path.insert(0, os.path.join(TREE, "tools"))
import lib_session as ls  # noqa: E402

SHELLS = {
    "bash": ["bash", "--posix", "-i", "+m"],
    # mksh edits only when its standard error is the terminal (observed:
    # with stderr on a pipe it reads lines through the tty's own editing)
    "mksh": ["dash", "-c", "exec mksh -i +m 2>&0"],
    "dash": ["dash", "-i", "+m"],
}

EXE = 0o755
F = 0o644
# name: (files {path: (mode, text)}, keys, meta)
PROBES = [
    ("cmd_unique", {}, ["\\k unam\\tX\\x01echo \\r"], {}),
    ("cmd_lcp_list", {"home/bin/zqxa1": EXE, "home/bin/zqxa2": EXE, "home/bin/zqxbb": EXE},
     ["PATH=$HOME/bin:$PATH", "\\k zq\\t", "\\k \\t", "\\k \\t", "\\k \\x15echo done\\r"], {}),
    ("cmd_at_lcp", {"home/bin/zqxa1": EXE, "home/bin/zqxa2": EXE},
     ["PATH=$HOME/bin:$PATH", "\\k zqxa\\t", "\\k \\t", "\\k 1\\x01echo \\r"], {}),
    ("cmd_empty_tab", {}, ["\\k \\t", "\\k \\t", "\\k n", "\\k \\x15echo done\\r"], {}),
    ("cmd_many", {}, ["\\k b\\t", "\\k \\t", "\\k n", "\\k \\x15echo done\\r"], {}),
    ("cmd_nomatch", {}, ["\\k qqqzz\\t", "\\k \\t", "\\k \\x15echo done\\r"], {}),
    ("cmd_builtin_fn_alias", {},
     ["f_mine() { :; }", "alias al_mine=true", "\\k f_mi\\tX\\x01echo \\r", "\\k al_mi\\tX\\x01echo \\r",
      "\\k alia\\tX\\x01echo \\r", "\\k whil\\tX\\x01echo \\r", "\\k getop\\tX\\x01echo \\r"], {}),
    ("cmd_after_ops", {},
     ["\\k echo hi | unam\\tX\\x01echo \\r", "\\k true; unam\\tX\\x01echo \\r", "\\k true && unam\\tX\\x01echo \\r",
      "\\k echo $(unam\\tX\\x01echo \\r", "\\k FOO=1 unam\\tX\\x01echo \\r", "\\k if unam\\tX\\x01echo \\r"], {}),
    ("cmd_slash", {"w/script.sh": EXE, "w/scfile": F, "w/scdir/x": F},
     ["\\k ./scr\\tX\\x01echo \\r", "\\k ./sc\\t", "\\k \\t", "\\k \\x15echo done\\r"], {}),
    ("file_unique", {"w/unique_file_name": F}, ["\\k echo uniq\\tX\\r"], {}),
    ("file_dirs", {"w/sub/dir/afile": F}, ["\\k echo su\\t", "\\k \\t", "\\k \\t", "\\k X\\r"], {}),
    ("file_list_cols", {**{f"w/f{n}": F for n in ["a", "bb", "ccc", "dddd", "eeeee", "ffffff", "g", "hh", "iii", "jjjj", "kkkkk", "llllllllllll", "m", "nn"]}, "w/fdir/x": F},
     ["\\k echo f\\t", "\\k \\t", "\\k \\x15echo done\\r"], {"cols": "40"}),
    ("file_space", {"w/my file": F}, ["\\k echo my\\tX\\r"], {}),
    ("file_space_lcp", {"w/my file a": F, "w/my file b": F}, ["\\k echo my\\t", "\\k \\t", "\\k a\\r"], {}),
    ("file_dollar", {"w/a$b": F}, ["\\k echo a\\tX\\r"], {}),
    ("file_squote", {"w/q'uote": F}, ["\\k echo q\\tX\\r"], {}),
    ("file_dquote", {"w/d\"q": F}, ["\\k echo d\\tX\\r"], {}),
    ("file_star", {"w/st*ar": F, "w/stz": F}, ["\\k echo st*\\t", "\\k \\x15echo done\\r", "\\k echo st\\\\*\\tX\\r"], {}),
    ("file_newline", {"w/nl\nname": F}, ["\\k echo nl\\tX\\r"], {}),
    ("file_amp_semi", {"w/a&b;c(d)": F}, ["\\k echo a\\tX\\r"], {}),
    ("file_quoted_typed", {"w/my file": F}, ["\\k echo \"my\\tX\\r", "\\k echo 'my\\tX\\r", "\\k echo my\\\\ \\tX\\r"], {}),
    ("file_tilde", {"home/docs/note": F, "home/.hidden": F},
     ["\\k echo ~/do\\tX\\r", "\\k echo ~/\\t", "\\k \\t", "\\k \\x15echo done\\r", "\\k echo ~\\t", "\\k \\x15echo done\\r"], {}),
    ("file_abs", {}, ["\\k echo /us\\tX\\r", "\\k echo /usr/bi\\tX\\r"], {}),
    ("file_hidden", {"w/.hid1": F, "w/vis": F},
     ["\\k echo \\t", "\\k \\t", "\\k \\x15echo done\\r", "\\k echo .h\\tX\\r"], {}),
    ("file_mid_word", {"w/unique_file_name": F}, ["\\k echo uniqZZ\\e[D\\e[D\\t\\r"], {}),
    ("file_redir", {"w/unique_file_name": F}, ["\\k cat <uniq\\tX\\r", "\\k echo hi >uniq\\tX\\r", "\\k FOO=uniq\\tX\\x01echo \\r"], {}),
    ("var", {}, ["\\k echo $HO\\tX\\r", "\\k echo ${HO\\tX\\r", "\\k echo \"$HO\\tX\\r", "\\k echo a$HO\\tX\\r"], {}),
    ("var_lcp", {}, ["ZQV_ONE=1 ZQV_TWO=2", "\\k echo $ZQV\\t", "\\k \\t", "\\k \\t", "\\k \\x15echo done\\r", "\\k echo $ZQV_O\\tX\\r"], {}),
    ("vi_insert_tab", {"w/unique_file_name": F}, ["set -o vi", "\\k echo uniq\\tX\\r"], {}),
    ("vi_cmd_expand", {"w/fa1": F, "w/fa2": F},
     ["set -o vi", "\\k echo fa\\e\\\\", "\\k X\\r", "\\k echo fa\\e*", "\\k \\r", "\\k echo fa\\e=", "\\k \\x03"], {}),
    ("tab_literal", {}, ["\\k echo \"a\\x16\\tb\" | od -c\\r"], {}),
    ("list_redraw", {"w/aa1": F, "w/aa2": F}, ["PS1='my-long-prompt> '", "\\k echo xyz aa\\t\\t", "\\k \\r"], {}),
    ("var_forms", {},
     ["ZQV_ONE=1 ZQV_TWO=2", "\\k echo ${ZQV_O\\tX\\r", "\\k echo \"$ZQV_O\\tX\\r", "\\k echo a$ZQV_O\\tX\\r",
      "\\k echo ${ZQV\\t\\t", "\\k \\x15echo done\\r", "\\k echo $\\t\\t", "\\k n\\x15echo done\\r",
      "\\k echo $ZQV_ONE\\tX\\r", "\\k echo ${ZQV_ONE}\\tX\\r"], {}),
    ("list_tall", {f"w/t{n:02d}": F for n in range(60)},
     ["\\k echo t\\t\\t", "\\k  ", "\\k  ", "\\k q", "\\k \\x15echo done\\r"], {"cols": "40", "rows": "10"}),
    ("list_query_files", {f"w/q{n:03d}": F for n in range(120)},
     ["\\k echo q\\t\\t", "\\k y", "\\k  ", "\\k q", "\\k \\x15echo done\\r"], {}),
    ("dash_vi", {}, ["set -o vi; echo st=$?", "set -o | grep -E 'vi|emacs'"], {}),
    ("tab_after_space", {"w/unique_file_name": F}, ["\\k echo uniq \\e[D\\tX\\r", "\\k echo uniq\\tX\\tY\\r"], {}),
    ("cmd_dir_in_path_word", {"w/subd/x": F}, ["\\k subd\\t", "\\k \\x15echo done\\r", "\\k cd sub\\tX\\x01echo \\r"], {}),
    ("lcp_then_type", {"home/bin/zqxa1": EXE, "home/bin/zqxa2": EXE, "home/bin/zqxbb": EXE},
     ["PATH=$HOME/bin:$PATH", "\\k zq\\t", "\\k a1", "\\k \\t", "\\k X\\x01echo \\r", "\\k zq\\ta1\\tX\\x01echo \\r"], {}),
    ("wide_names", {"w/\u00e9t\u00e9": F, "w/\u65e5\u672c": F}, ["\\k echo \\xc3\\xa9\\tX\\r", "\\k echo \\t\\t", "\\k \\x15echo done\\r"], {}),
]


class Spy:
    raw = b""


_feed = ls.Screen.feed
_snap = ls.Screen.snapshot


def feed(self, data):
    Spy.raw += data
    _feed(self, data)


def snapshot(self, start):
    rows = _snap(self, start)
    bels = Spy.raw.count(b"\x07")
    rows.append(f"bel {bels} raw {Spy.raw!r}")
    Spy.raw = b""
    return rows


ls.Screen.feed = feed
ls.Screen.snapshot = snapshot


def write_case(d, name, files, keys, meta):
    for path, mode in files.items():
        p = os.path.join(d, name + ".files", path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\n" if mode == EXE else "x\n")
        os.chmod(p, mode)
    with open(os.path.join(d, name + ".keys"), "w") as fh:
        fh.write("\n".join(keys) + "\nexit\n")
    return os.path.join(d, name + ".keys")


def main():
    want = sys.argv[2:] or ["bash", "mksh", "dash"]
    only = os.environ.get("PROBES")
    d = tempfile.mkdtemp(prefix="sh16-probe.")
    for name, files, keys, meta in PROBES:
        if only and name not in only.split(","):
            continue
        kp = write_case(d, name, files, keys, meta)
        meta = dict(meta)
        meta["env"] = "PS1=$\\s"
        for sh in want:
            if sh.startswith("pelt="):
                argv = [sh[5:], "-i"]
            else:
                argv = SHELLS[sh]
            Spy.raw = b""
            tr = ls.run(argv, kp, meta)
            print(f"===== {name} [{sh}]")
            si = 0
            for ln in tr:
                print("  " + ln)
                if ln.startswith("prompt ") and si < len(ls.last_screens):
                    for r in ls.last_screens[si]:
                        print("      " + r)
                    si += 1
            sys.stdout.flush()


main()
