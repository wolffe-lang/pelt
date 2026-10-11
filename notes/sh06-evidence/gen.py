#!/usr/bin/env python3
"""gen — lane-local: turn the census source (*.census) into case files
under tests/diff/ and the clause table tests/census/clauses.tsv.

Source format:
  @ID | KIND | statement          KIND: T corpus, S session, U untestable
  > area/name area/name           existing or new cases that cover it
  ! text                          note (why untestable, what decides)
  --- area/name [key=value ...]   a new case; lines up to the next marker
  script
"""
import os, sys, glob

ROOT = sys.argv[1]
DIFF = os.path.join(ROOT, "tests", "diff")
rows = []
new = {}
cur = None
case = None
for path in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "*.census"))):
    for raw in open(path, encoding="utf-8").read().split("\n"):
        if raw.startswith("@"):
            parts = [p.strip() for p in raw[1:].split("|", 2)]
            cur = {"id": parts[0], "kind": parts[1], "text": parts[2], "cases": [], "note": ""}
            if any(r["id"] == cur["id"] for r in rows):
                sys.exit(f"duplicate id {cur['id']}")
            rows.append(cur)
            case = None
        elif raw.startswith("> ") and case is None:
            cur["cases"] += raw[2:].split()
        elif raw.startswith("! ") and case is None:
            cur["note"] = (cur["note"] + " " + raw[2:]).strip()
        elif raw.startswith("--- "):
            bits = raw[4:].split(" ")
            name = bits[0]
            meta = dict(b.split("=", 1) for b in bits[1:] if "=" in b)
            if name in new:
                sys.exit(f"duplicate case {name}")
            case = {"meta": meta, "lines": []}
            new[name] = case
            cur["cases"].append(name)
        elif case is not None:
            case["lines"].append(raw)
        elif raw.strip() and not raw.startswith("#"):
            sys.exit(f"{path}: stray line {raw!r}")

for name, c in new.items():
    area, n = name.split("/")
    d = os.path.join(DIFF, area)
    os.makedirs(d, exist_ok=True)
    while c["lines"] and c["lines"][-1] == "":
        c["lines"].pop()
    body = "\n".join(c["lines"]) + "\n"
    p = os.path.join(d, n + ".sh")
    if os.path.exists(p) and open(p).read() != body and "--force" not in sys.argv:
        sys.exit(f"{name}: exists with other content")
    open(p, "w").write(body)
    mp = os.path.join(d, n + ".meta")
    old = {}
    if os.path.exists(mp):
        for line in open(mp):
            k, _, v = line.rstrip("\n").partition("=")
            old[k] = v
    for k, v in c["meta"].items():
        old[k] = v.replace("\\s", " ")
    with open(mp, "w") as fh:
        for k in old:
            fh.write(f"{k}={old[k]}\n")

for r in rows:
    for cn in r["cases"]:
        if cn.startswith("session:"):
            continue
        a, n = cn.split("/")
        if not os.path.exists(os.path.join(DIFF, a, n + ".sh")):
            sys.exit(f"{r['id']}: no case {cn}")
    if r["kind"] == "T" and not r["cases"]:
        sys.exit(f"{r['id']}: T with no case")

os.makedirs(os.path.join(ROOT, "tests", "census"), exist_ok=True)
with open(os.path.join(ROOT, "tests", "census", "clauses.tsv"), "w") as fh:
    fh.write("id\tkind\tstatement\tcases\tnote\n")
    for r in rows:
        fh.write("\t".join([r["id"], r["kind"], r["text"], " ".join(r["cases"]), r["note"]]) + "\n")
print(f"{len(rows)} statements, {len(new)} new cases")
