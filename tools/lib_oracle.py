"""lib_oracle — who the oracle of record is, and whether this host runs it.

`tests/diff/ORACLE` names the oracle of record and the second opinion on its
first two lines, each by its package and by the sha256 of the program the
corpus runs:

  dash <version> ... /usr/bin/dash sha256 <64 hex> ...
  bash <version> ... /usr/bin/bash sha256 <64 hex> ...

`tools/oracle-record` and `tools/session-record` run `dash` and `bash` with
PATH=/usr/bin:/bin (tools/lib_cases.py's ENV, tools/lib_session.py's session
environment), so that is where the programs are looked up and hashed here.
A host runs the oracle only when `pacman -Q` answers each package EXACTLY as
ORACLE names it, and each program found there has EXACTLY the digest ORACLE
names (pelt#69). Anything else is refused: no other build, no other binary,
no host without pacman.

$PELT_ORACLE_FILE points the tools at another ORACLE (tools/oracle-test's).
"""

import hashlib
import os
import re
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEARCH = "/usr/bin:/bin"
LINE = re.compile(r"^(dash|bash) (\S+) .*?(/usr/bin/(?:dash|bash)) sha256 ([0-9a-f]{64})\b")


class Refused(Exception):
    pass


def oracle_file():
    """$PELT_ORACLE_FILE, else the ORACLE beside the corpus ($PELT_DIFF_DIR,
    as tools/lib_cases.py), else the tree's tests/diff/ORACLE."""
    if os.environ.get("PELT_ORACLE_FILE"):
        return os.environ["PELT_ORACLE_FILE"]
    diff = os.environ.get("PELT_DIFF_DIR") or os.path.join(ROOT, "tests", "diff")
    return os.path.join(diff, "ORACLE")


def identity(path=None):
    """{'dash': {'package', 'program', 'sha256'}, 'bash': {...}} from ORACLE's
    first two lines; Refused when either is missing or malformed."""
    with open(path or oracle_file(), encoding="utf-8") as fh:
        lines = fh.read().split("\n")[:2]
    found = {}
    for line in lines:
        m = LINE.match(line)
        if m:
            found[m.group(1)] = {"package": f"{m.group(1)} {m.group(2)}", "program": m.group(3),
                                 "sha256": m.group(4)}
    for name in ("dash", "bash"):
        if name not in found:
            raise Refused(f"tests/diff/ORACLE does not name {name} by package and full program digest")
    return found


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_host(names=("dash", "bash"), search=SEARCH, oracle=None):
    """Raise Refused unless this host's packages and programs are exactly the
    ones ORACLE names. Answers the identity checked."""
    want = identity(oracle)
    for name in names:
        w = want[name]
        try:
            got = subprocess.run(["pacman", "-Q", name], capture_output=True, text=True).stdout.strip()
        except FileNotFoundError:
            got = ""
        if got != w["package"]:
            raise Refused(f"this host has {got or 'no pacman ' + name}; tests/diff/ORACLE names {w['package']}")
        program = shutil.which(name, path=search)
        if program is None:
            raise Refused(f"no {name} on {search}")
        digest = sha256(os.path.realpath(program))
        if digest != w["sha256"]:
            raise Refused(f"{program} has sha256 {digest}; tests/diff/ORACLE names {w['sha256']}")
    return want


if __name__ == "__main__":
    import sys
    try:
        got = check_host()
    except Refused as exc:
        print(f"lib_oracle: REFUSED: {exc}", file=sys.stderr)
        sys.exit(2)
    for name, w in got.items():
        print(f"PASS oracle {w['package']} {w['program']} sha256 {w['sha256']}")
