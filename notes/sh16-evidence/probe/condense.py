#!/usr/bin/env python3
"""condense a probe log: per step the keys, stdout, BELs and raw bytes
with runs of backspaces and blanks shortened."""
import re, sys, ast
for ln in open(sys.argv[1], encoding="utf-8"):
    ln = ln.rstrip("\n")
    if ln.startswith("====="):
        print(ln)
    elif ln.startswith("  step ") or ln.startswith("  out ") or ln.startswith("  exit") or ln.startswith("  alive"):
        print(ln)
    elif ln.startswith("      bel "):
        m = re.match(r"      bel (\d+) raw (b.*)$", ln)
        raw = ast.literal_eval(m.group(2))
        s = raw.decode("utf-8", "replace")
        s = re.sub(r"\x08{3,}", lambda m: f"<BS*{len(m.group(0))}>", s)
        s = re.sub(r" {6,}", lambda m: f"<SP*{len(m.group(0))}>", s)
        s = s.replace("\x1b[?2004h", "").replace("\x1b[?2004l", "")
        print(f"        bel={m.group(1)} {s!r}")
