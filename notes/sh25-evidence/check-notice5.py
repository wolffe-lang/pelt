#!/usr/bin/env python3
"""Check the two repaired here-documents and preserve all other rows."""
import re
import sys
from pathlib import Path

def rows(path):
    text = Path(path).read_text()
    return {int(m.group(1)): m.group(0) for m in re.finditer(
        r"^(\d\d) .*?(?=^\d\d |\Z)", text, re.M | re.S)}

old, new = map(rows, sys.argv[1:])
assert sorted(old) == sorted(new) == list(range(1, 21))
for n in old:
    if n not in (9, 10):
        assert old[n] == new[n], f"unexpected changed row {n}"
assert "   out: doc|st=0\n" in new[9], new[9]
assert "   out: st=0\n" in new[10], new[10]
assert "   file: doc|\n" in new[10], new[10]
print("notice5: rows 9/10 correct; other 18 rows byte-identical")
