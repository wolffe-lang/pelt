#!/usr/bin/env python3
"""race.py WITNESS PELT TABLE N ROW[,ROW...] OUT

Boot each ROW N times, interleaved, through WITNESS's own rows and run_row
(tools/hangup-witness, loaded as a module) against PELT, and compare each
line with TABLE's line for the row. Every line goes to OUT (with the raw
line when the witness reports one, and the probes' log lines), and a tally
per row is printed at the end: how many of N hold the table's line, and
each distinct line seen with its count. Run from the checkout whose
witness it is; TMPDIR holds the work directory."""
import collections
import importlib.machinery
import importlib.util
import os
import shutil
import sys
import tempfile

w, pelt, table, n, rows, out = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3], int(sys.argv[4]), \
    sys.argv[5].split(","), sys.argv[6]
loader = importlib.machinery.SourceFileLoader("hw", w)
spec = importlib.util.spec_from_loader("hw", loader)
hw = importlib.util.module_from_spec(spec)
loader.exec_module(hw)
want, _ = hw.read_table(table)
work = tempfile.mkdtemp(prefix="race-", dir=os.environ.get("TMPDIR") or None)
probe = hw.compile_probe(work)[0]
argv_i, argv_s, argv0, is_pelt = hw.shell_argvs("pelt", pelt)
defs = {row[0]: row for row in hw.rows()}
tally = {x: collections.Counter() for x in rows}
raws = {x: collections.Counter() for x in rows}
print(f"race: {w} {pelt} {table} N={n} rows={','.join(rows)}", flush=True)
with open(out, "w") as fh:
    for i in range(n):
        wk = os.path.join(work, f"b{i}")
        os.makedirs(wk)
        for x in rows:
            res = hw.run_row(defs[x], argv_i, argv_s, argv0, wk, os.path.dirname(probe), is_pelt)
            line, note = res[0], res[1]
            raw = res[2] if len(res) > 2 else line
            ok = line == want.get(x) and not note
            tally[x][line + (f"  # NOTE {note}" if note else "")] += 1
            raws[x][raw] += 1
            fh.write(f"{i} {'ok' if ok else 'FAIL'} {line}\n")
            if raw != line:
                fh.write(f"  raw {raw}\n")
            try:
                with open(os.path.join(wk, x, "probe.log"), errors="replace") as lg:
                    for ln in lg.read().splitlines():
                        fh.write(f"  log {ln}\n")
            except OSError:
                pass
            fh.flush()
        shutil.rmtree(wk, ignore_errors=True)
        if (i + 1) % 25 == 0:
            print(f"race: {i + 1} of {n} boots", flush=True)
for x in rows:
    held = tally[x].get(want.get(x), 0)
    print(f"race: {x}: {held} of {n} hold the table's line")
    for ln, c in tally[x].most_common():
        print(f"  {c:5d}  {ln}")
    if raws[x] != tally[x]:
        print("  raw:")
        for ln, c in raws[x].most_common():
            print(f"  {c:5d}  {ln}")
shutil.rmtree(work, ignore_errors=True)
