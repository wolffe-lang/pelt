#!/usr/bin/env python3
"""Black-box probe: type a keys file into dash -i and bash --posix -i
through lib_session and print both transcripts in full (and screens)."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/lanes/sh12/pelt/tools"))
import lib_session as ls
import json
_orig_render = ls.render
def _render(steps, exit_line):
    out = []
    for i, st in enumerate(steps):
        out.append(f"step {i} {json.dumps(st.typed)}")
        if st.out: out.append("out " + json.dumps(st.out.decode("utf-8","replace")))
        if st.err: out.append("ERR " + json.dumps(st.err.decode("utf-8","replace")))
    out.append(exit_line)
    return out
ls.render = _render

def show(name, argv, keys, meta):
    t = ls.run(argv, keys, meta)
    print(f"--- {name}: {' '.join(argv)}")
    for ln in t:
        print("   ", ln)
    if meta.get("screen"):
        for i, s in enumerate(ls.last_screens):
            print(f"    screen {i}:", s)

for keys in sys.argv[1:]:
    meta = ls.read_meta(keys[:-5] + ".meta")
    print(f"===== {os.path.basename(keys)}  meta={meta}")
    who = meta.get("who", "dash bash pelt").split()
    if "dash" in who:
        show("dash", ls.argv_for(ls.ORACLE, meta, False), keys, meta)
    if "bash" in who:
        show("bash", ls.argv_for(ls.SECOND, meta, False), keys, meta)
    pelt = os.environ.get("PELT")
    if pelt and "pelt" in who:
        show("pelt", ls.argv_for(pelt, meta, True), keys, meta)
