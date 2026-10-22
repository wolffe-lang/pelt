#!/usr/bin/env python3
"""sh24: isolate jobs' own keep from equal-length input/parse storage.
Linux RssAnon avoids sh20's file-mapping noise. Inside ctr.sh only.
"""
import os
import subprocess
import sys
import tempfile

for shell in sys.argv[1:]:
    for turn in range(1, 4):
        rows = {}
        with tempfile.TemporaryDirectory(prefix="sh24-anon.") as d:
            for body in ("true", "jobs"):
                vals = []
                for n in (10000, 20000):
                    script = os.path.join(d, "s")
                    with open(script, "w") as f:
                        f.write((body + "\n") * n)
                        f.write("while read k v u; do case $k in RssAnon:) echo $v;; esac; done </proc/self/status\n")
                    r = subprocess.run([shell, script], capture_output=True, text=True)
                    if r.returncode or r.stderr or not r.stdout.strip().isdigit():
                        raise SystemExit(f"wrong answer: {r}")
                    vals.append(int(r.stdout.strip()))
                rows[body] = vals
        own = ((rows["jobs"][1] - rows["jobs"][0]) -
               (rows["true"][1] - rows["true"][0])) * 1024 // 10000
        print(f"{shell} pass={turn} RssAnon_KB={rows} own={own} B/call", flush=True)
