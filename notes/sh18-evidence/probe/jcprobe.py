#!/usr/bin/env python3
"""jcprobe — type a keys file into a shell through tools/lib_session's
pseudo-terminal (the shell is a new session's leader and the pty its
controlling terminal) and print every step's standard output and
standard error BYTES (the session harness compares only the presence of
standard error). Black-box: the reference shells are run, never read.

usage: jcprobe.py KEYS SHELL [ARG ...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.environ.get("PELT_TREE", "."), "tools"))
import lib_session as ls  # noqa: E402


def render(steps, exit_line):
    lines = []
    for i, st in enumerate(steps):
        lines.append(f"step {i} {json.dumps(st.typed)}")
        if st.out:
            lines.append("  out " + json.dumps(st.out.decode("utf-8", "replace")))
        if st.err:
            lines.append("  err " + json.dumps(st.err.decode("utf-8", "replace")))
    lines.append(f"{exit_line} at step {len(steps) - 1}")
    return lines


ls.render = render
keys, argv = sys.argv[1], sys.argv[2:]
print("$ " + " ".join(argv) + "  < " + os.path.basename(keys))
for ln in ls.run(argv, keys, {}, None):
    print(ln)
