#!/usr/bin/env python3
"""Check recorded counted-loop runs using total child CPU, never user alone.

The short row is bounded against the pinned reference. The long row reports
100,000 turns separately because removing startup changes the ratio; its
reference must exceed 10 ms CPU so timer grain cannot dominate the result.
"""
import argparse
import json
import math
from pathlib import Path
import statistics
import sys

SHORT_BOUND = 3.46
MIN_RUNS = 31
PARTICIPANTS = ("reference", "pelt", "reference-again")


def totals(rows):
    result = []
    for row in rows:
        if row["exit"] != 0 or row["stdout"] or row["stderr"]:
            raise ValueError("unsuccessful measured child")
        user, system = float(row["user_us"]), float(row["system_us"])
        if not all(math.isfinite(x) and x >= 0 for x in (user, system)):
            raise ValueError("invalid CPU component")
        cpu = user + system
        if cpu <= 0 or not math.isclose(cpu, float(row["cpu_us"]), abs_tol=1e-6):
            raise ValueError("invalid total CPU")
        result.append(cpu)
    return result


def check(directory, counts=(1000, 100000), emit=print):
    directory = Path(directory)
    meta = json.loads((directory / "meta.json").read_text())
    if meta["uname"][0] != "Linux":
        raise ValueError("the deciding measurements must be from Linux")
    runs = json.loads((directory / "runs.json").read_text())
    failed = False
    for count in counts:
        row_name = "loop-counted-cpu" if count == 1000 else "loop-counted-long"
        groups = {}
        for name in PARTICIPANTS:
            subset = [r for r in runs if r["variant"] == "counted" and r["count"] == count and r["participant"] == name]
            if len(subset) < MIN_RUNS or len({r["repetition"] for r in subset}) != len(subset):
                raise ValueError(f"{count} turns: insufficient or duplicate {name} runs")
            groups[name] = totals(subset)
        med = {name: statistics.median(values) for name, values in groups.items()}
        ratio = med["pelt"] / med["reference"]
        aa = med["reference-again"] / med["reference"]
        if not 0.90 <= aa <= 1.10:
            emit(f"FAIL {row_name} turns={count} reason=reference-noise cpu_aa={aa:.6f}")
            failed = True
        elif count == 100000 and med["reference"] < 10000:
            emit(f"FAIL {row_name} turns={count} reason=reference-below-timer-floor")
            failed = True
        elif count == 1000 and ratio > SHORT_BOUND:
            emit(f"FAIL {row_name} turns={count} cpu_ratio={ratio:.6f} bound={SHORT_BOUND:.2f}")
            failed = True
        else:
            emit(f"PASS {row_name} turns={count} cpu_ratio={ratio:.6f} cpu_aa={aa:.6f}")
        emit(f"MEASURE turns={count} reference_cpu_us={med['reference']:.3f} pelt_cpu_us={med['pelt']:.3f}")
        old = [r for r in runs if r["variant"] == "counted" and r["count"] == count and r["participant"] == "baseline"]
        if old:
            if len(old) < MIN_RUNS:
                raise ValueError("insufficient baseline runs")
            previous = statistics.median(totals(old))
            emit(f"COMPARE turns={count} baseline_cpu_ratio={previous / med['reference']:.6f} candidate_over_baseline={med['pelt'] / previous:.6f}")
    return not failed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", required=True)
    parser.add_argument("--short-only", action="store_true", help="score an earlier short-only measurement; not a complete take")
    args = parser.parse_args()
    try:
        return 0 if check(args.results, (1000,) if args.short_only else (1000, 100000)) else 1
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"FAIL loop-counted-record {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
