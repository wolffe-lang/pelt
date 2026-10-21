#!/usr/bin/env python3
"""sh23: write a hand transcript (`tr_by=hand`) for an autocd session from
pelt TRUNK's own answers to the explicit session: the case's keys with each
line the option would turn into `cd -- WORD...` typed as that `cd`
(`handtr/<case>.explicit`), and `set -o autocd`, which trunk refuses, as
`:`. This is the prediction of §3.2 made exact: the option is the explicit
`cd`. The transcript is trunk pelt's, typed by pelt's own session runner
(tools/lib_session.py from the pelt tree), with each step's typed line put
back to the case's own. Written before the first change under src/.
usage: handtr.py PELT_TREE PELT_BIN CASE..."""
import json
import os
import sys

tree, pelt = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(tree, "tools"))
import lib_session as ls  # noqa: E402

here = os.path.dirname(os.path.abspath(__file__))
for case in sys.argv[3:]:
    keys = os.path.join(tree, "tests", "session", case + ".keys")
    explicit = os.path.join(here, "handtr", case + ".explicit")
    mine = open(keys, encoding="utf-8").read().split("\n")[:-1]
    theirs = open(explicit, encoding="utf-8").read().split("\n")[:-1]
    assert len(mine) == len(theirs), case
    meta = ls.read_meta(keys[:-5] + ".meta") if os.path.exists(keys[:-5] + ".meta") else {}
    lines = ls.run(ls.argv_for(pelt, meta, True), explicit, meta)
    # a second run: the transcript must not depend on timing
    again = ls.run(ls.argv_for(pelt, meta, True), explicit, meta)
    if lines != again:
        print(f"UNSTABLE {case}")
        sys.exit(1)
    out = []
    i = 0
    for ln in lines:
        if ln.startswith("step ") and ln != "step 0":
            i += 1
            ln = f"step {i} {json.dumps(mine[i - 1])}"
        out.append(ln)
    with open(os.path.join(here, "handtr", case + ".tr"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"wrote {case}: {len(out)} lines")
