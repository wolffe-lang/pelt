#!/usr/bin/env python3
"""sh24: re-derive sh20/sh22's no-wait loop neighbors with R-sh24-2's
Linux RssAnon instrument; do not compare these directly to archived peaks.
"""
import os
import runpy
import sys
import tempfile

root = sys.argv[1]
run = runpy.run_path(os.path.join(root, "tools/shape-rss"))["run_file"]
for shell in sys.argv[2:]:
    for body in ("true &", "env true &"):
        with tempfile.TemporaryDirectory(prefix="sh24-neighbor.") as d:
            vals = []
            for n in (5000, 10000):
                kb, ok, why = run(shell, "monitor", body, n, d)
                if not ok:
                    raise SystemExit(why)
                vals.append(kb)
        print(f"{shell} [{body}] RssAnon_KB={vals} own={(vals[1]-vals[0])*1024//5000} B/job", flush=True)
