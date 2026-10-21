#!/usr/bin/env python3
"""sh23: a reference shell typed at on a pseudo-terminal by pelt's own
session runner (tools/lib_session.py, loaded from the pelt tree): the
transcript it records (standard output, whether anything but the prompt
reached standard error, the prompt) for KEYS under each ARGV.
usage: ptyrun.py PELT_TREE KEYS 'argv…' ['argv…' …]"""
import os
import sys
sys.path.insert(0, os.path.join(sys.argv[1], "tools"))
import lib_session as ls  # noqa: E402

keys = sys.argv[2]
for spec in sys.argv[3:]:
    argv = spec.split()
    print("### " + spec)
    for line in ls.run(argv, keys, {"env": "PS1=$\\s"}):
        print(line)
