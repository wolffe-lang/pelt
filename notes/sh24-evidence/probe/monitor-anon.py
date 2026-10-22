#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile

for shell in sys.argv[1:]:
    vals = []
    with tempfile.TemporaryDirectory(prefix="sh24-monitor.") as d:
        for n in (3000, 6000):
            script = os.path.join(d, "s")
            with open(script, "w") as f:
                f.write("exec 2>/dev/null\nset -m\ni=0\n")
                f.write(f"while [ $i -lt {n} ]; do env true & wait $!; i=$((i+1)); done; ")
                f.write("while read k v u; do case $k in RssAnon:|RssFile:|VmHWM:) echo $k $v;; esac; done </proc/self/status; exec true\n")
            r = subprocess.run([shell, script], capture_output=True, text=True)
            if r.returncode or r.stderr:
                raise SystemExit(str(r))
            vals.append(r.stdout.strip())
    print(shell, vals, flush=True)
