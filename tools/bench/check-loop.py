#!/usr/bin/env python3
"""Check counted-loop records using total child CPU, never user alone.

The short row retains its reference bound. The 100,000-turn row also requires
at least five percent paired CPU improvement against interleaved baseline runs.
"""
import argparse
import json
import math
from pathlib import Path
import statistics
import sys

SHORT_BOUND = 3.46
LONG_BOUND = 4.13
BASELINE_BOUND = 0.95
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


def participant(runs, count, name):
    rows = [r for r in runs if r["variant"] == "counted" and r["count"] == count and r["participant"] == name]
    if len(rows) < MIN_RUNS or len({r["repetition"] for r in rows}) != len(rows):
        raise ValueError(f"{count} turns: insufficient or duplicate {name} runs")
    return dict(zip((r["repetition"] for r in rows), totals(rows)))


def check(directory, counts=(1000, 100000), emit=print):
    directory = Path(directory)
    meta = json.loads((directory / "meta.json").read_text())
    if meta["uname"][0] != "Linux":
        raise ValueError("the deciding measurements must be from Linux")
    runs = json.loads((directory / "runs.json").read_text())
    failed = False
    for count in counts:
        row_name = "loop-counted-cpu" if count == 1000 else "loop-counted-long"
        groups = {name: participant(runs, count, name) for name in PARTICIPANTS}
        med = {name: statistics.median(values.values()) for name, values in groups.items()}
        ratio = med["pelt"] / med["reference"]
        aa = med["reference-again"] / med["reference"]
        paired = None
        old = [r for r in runs if r["variant"] == "counted" and r["count"] == count and r["participant"] == "baseline"]
        if old or count == 100000:
            previous = participant(runs, count, "baseline")
            if previous.keys() != groups["pelt"].keys():
                raise ValueError("baseline repetitions do not match candidate repetitions")
            paired = statistics.median(groups["pelt"][rep] / cpu for rep, cpu in previous.items())
            baseline = statistics.median(previous.values())
            emit(f"COMPARE turns={count} baseline_cpu_ratio={baseline / med['reference']:.6f} candidate_over_baseline={med['pelt'] / baseline:.6f} paired_candidate_over_baseline={paired:.6f}")
        reason = ""
        if not 0.90 <= aa <= 1.10:
            reason = "reference-noise"
        elif count == 100000 and med["reference"] < 10000:
            reason = "reference-below-timer-floor"
        elif ratio > (SHORT_BOUND if count == 1000 else LONG_BOUND):
            reason = "cpu-bound"
        elif count == 100000 and paired > BASELINE_BOUND:
            reason = "baseline-improvement"
        bound = SHORT_BOUND if count == 1000 else LONG_BOUND
        emit(f"{'FAIL' if reason else 'PASS'} {row_name} turns={count} cpu_ratio={ratio:.6f} bound={bound:.2f} cpu_aa={aa:.6f}" + (f" reason={reason}" if reason else ""))
        failed |= bool(reason)
        emit(f"MEASURE turns={count} reference_cpu_us={med['reference']:.3f} pelt_cpu_us={med['pelt']:.3f}")
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
