#!/usr/bin/env python3
"""Validate sh24's collected evidence; never infer success from silence."""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent / "logs"
text = (root / "final.status").read_text()
assert text.rstrip().endswith("done"), "gauntlet has not ended"
pairs = re.findall(r"^([a-z][-a-z0-9]*)=(\d+)$", text, re.M)
codes = dict(pairs)
assert all(v == "0" for _, v in pairs), [(k, v) for k, v in pairs if v != "0"]
required = {"fmt", "build", "test", "clause", "width", "diff-selftest", "sess-selftest", "oracle-check"}
for tier in ("native", "release"):
    required |= {f"{k}-{tier}" for k in ("diff", "sess", "self", "glob-rss", "loop-rss", "exec-witness", "edit-witness", "hist-witness", "signal-witness", "reap")}
    required |= {f"diff-{tier}-taskset", f"sess-{tier}-taskset", f"edit-{tier}-control", f"signal-{tier}-control"}
    for mode in ("", "-taskset"):
        for pass_ in (1, 2, 3):
            name = f"shape-{tier}-{pass_}{mode}"
            required.add(name)
            log = (root / "gauntlet" / f"final-{name}.log").read_text()
            assert len(re.findall(r"^shape-rss: ok\s+\S+\s+\S+\s+\d+", log, re.M)) == 52, name
            assert "shape-rss: FAIL" not in log, name
            status = (root / "gauntlet" / f"final-{name}.status").read_text()
            assert "load average:" in status and "affinity mask: f00" in status, name
            assert "exit=0" in status, name
    for suffix in ("", "-taskset"):
        diff = (root / "gauntlet" / f"final-diff-{tier}{suffix}.log").read_text()
        sess = (root / "gauntlet" / f"final-sess-{tier}{suffix}.log").read_text()
        assert re.search(r"difftest: total\s+994\s+0\s+28", diff), tier + suffix
        assert "session: pass 290  fail 0  pending 2" in sess, tier + suffix
required |= {"neighbors-2-four", "neighbors-3-bare", "neighbors-3-four", "release-driver", "rss-worker-0", "rss-worker-1"}
assert required <= codes.keys(), sorted(required - codes.keys())
assert len(codes) == 54, len(codes)
print(f"sh24 evidence: {len(codes)} exits zero; corpus 994/0/28 x4; sessions 290/0/2 x4; 52 shapes x12; affinity/load recorded")
