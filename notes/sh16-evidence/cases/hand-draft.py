#!/usr/bin/env python3
"""sh16: draft a tr_by=hand case's transcript (and screen_by=hand
screens) by typing it into a pelt, for a person to check line by line
against the design (notes/sh16-the-completion.md §3.1) before it is
committed. usage: hand-draft.py PELT case ..."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools"))
import lib_session as ls  # noqa: E402

pelt = sys.argv[1]
for name in sys.argv[2:]:
    keys = os.path.join(ls.SESS, name + ".keys")
    meta = ls.read_meta(keys[:-5] + ".meta")
    assert meta.get("tr_by") == "hand", name
    tr = ls.run([pelt, "-i"], keys, meta)
    with open(keys[:-5] + ".tr", "w", encoding="utf-8") as fh:
        fh.write("\n".join(tr) + "\n")
    if meta.get("screen_by") == "hand":
        ls.write_screen(keys[:-5] + ".screen", ls.last_screens, meta["screen"])
    print(f"drafted {name}: {tr[-1]}")
