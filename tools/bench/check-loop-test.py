#!/usr/bin/env python3
"""Total-CPU guard contracts, including coarse user/system clock splits."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("loop_guard", HERE / "check-loop.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class LoopGuard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="counted-loop-", dir=os.environ.get("TMPDIR"))
        self.root = Path(self.temp.name)
        (self.root / "meta.json").write_text(json.dumps({"uname": ["Linux"]}))
        self.rows = []
        for count, reference in ((1000, 861.0), (100000, 70000.0)):
            for name, ratio in (("reference", 1), ("reference-again", 1.01), ("pelt", 3.40 if count == 1000 else 2.75), ("baseline", 4.35)):
                for rep in range(31):
                    total = reference * ratio
                    self.rows.append({"variant": "counted", "count": count, "participant": name, "repetition": rep,
                                      "exit": 0, "stdout": "", "stderr": "", "cpu_us": total,
                                      "user_us": total if rep % 2 else 0.0,
                                      "system_us": 0.0 if rep % 2 else total})

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        (self.root / "runs.json").write_text(json.dumps(self.rows))

    def check(self, counts=(1000, 100000)):
        self.save()
        output = []
        result = guard.check(self.root, counts, output.append)
        return result, output

    def test_zero_component_ticks_preserve_total_cpu(self):
        ok, output = self.check()
        self.assertTrue(ok)
        self.assertTrue(any("PASS loop-counted-long" in x for x in output))

    def test_short_bound_is_seen_red(self):
        for row in self.rows:
            if row["participant"] == "pelt" and row["count"] == 1000:
                row.update(user_us=3136.0, system_us=0.0, cpu_us=3136.0)
        ok, output = self.check()
        self.assertFalse(ok)
        self.assertTrue(any(x.startswith("FAIL loop-counted-cpu ") for x in output))

    def test_long_bound_is_seen_red(self):
        for row in self.rows:
            if row["participant"] == "pelt" and row["count"] == 100000:
                row.update(user_us=70000 * 3.20, system_us=0, cpu_us=70000 * 3.20)
        ok, output = self.check()
        self.assertFalse(ok)
        self.assertTrue(any(x.startswith("FAIL loop-counted-long ") and "reason=cpu-bound" in x for x in output))

    def test_long_requires_five_percent_improvement(self):
        for row in self.rows:
            if row["participant"] == "baseline":
                row.update(user_us=70000 * 2.85, system_us=0, cpu_us=70000 * 2.85)
        ok, output = self.check()
        self.assertFalse(ok)
        self.assertTrue(any("reason=baseline-improvement" in x for x in output))

    def test_long_requires_interleaved_baseline(self):
        self.rows = [r for r in self.rows if r["participant"] != "baseline"]
        with self.assertRaisesRegex(ValueError, "baseline"):
            self.check()

    def test_baseline_repetitions_must_be_unique_and_paired(self):
        old = [r for r in self.rows if r["participant"] == "baseline" and r["count"] == 100000]
        old[0]["repetition"] = old[1]["repetition"]
        with self.assertRaisesRegex(ValueError, "baseline"):
            self.check()

    def test_paired_reduction_not_ratio_of_medians(self):
        for row in self.rows:
            if row["count"] == 100000 and row["participant"] in ("pelt", "baseline"):
                k = row["repetition"] % 5
                ratio = (1 if k < 2 else 10) if row["participant"] == "baseline" else (1 if k < 2 else 10 if k == 2 else 0.5)
                row.update(user_us=70000 * ratio, system_us=0, cpu_us=70000 * ratio)
        ok, output = self.check()
        self.assertFalse(ok)
        self.assertTrue(any("reason=baseline-improvement" in x for x in output))

    def test_long_bound_is_inclusive(self):
        for row in self.rows:
            if row["count"] == 100000 and row["participant"] == "pelt":
                row.update(user_us=70000 * 3.00, system_us=0, cpu_us=70000 * 3.00)
        self.assertTrue(self.check()[0])

    def test_total_not_user_time_decides(self):
        for row in self.rows:
            if row["participant"] == "pelt":
                row.update(user_us=0.0, system_us=row["cpu_us"])
        self.assertTrue(self.check()[0])

    def test_missing_long_row_is_not_a_complete_take(self):
        self.rows = [r for r in self.rows if r["count"] == 1000]
        self.save()
        with self.assertRaises(ValueError):
            guard.check(self.root, emit=lambda x: None)
        self.assertTrue(guard.check(self.root, (1000,), lambda x: None))

    def test_small_long_reference_is_refused(self):
        for row in self.rows:
            if row["count"] == 100000:
                for key in ("user_us", "system_us", "cpu_us"):
                    row[key] /= 100
        ok, output = self.check()
        self.assertFalse(ok)
        self.assertTrue(any("reference-below-timer-floor" in x for x in output))

    def test_noisy_reference_is_refused(self):
        for row in self.rows:
            if row["participant"] == "reference-again":
                for key in ("user_us", "system_us", "cpu_us"):
                    row[key] *= 2
        self.assertFalse(self.check()[0])

    def test_non_linux_record_is_refused(self):
        (self.root / "meta.json").write_text(json.dumps({"uname": ["Darwin"]}))
        with self.assertRaises(ValueError):
            self.check()

    def test_failed_child_is_refused(self):
        self.rows[0]["exit"] = 2
        with self.assertRaises(ValueError):
            self.check()

    def test_unexpected_output_is_refused(self):
        self.rows[0]["stdout"] = "wrong result"
        with self.assertRaises(ValueError):
            self.check()

    def test_inconsistent_total_is_refused(self):
        self.rows[0]["cpu_us"] += 1
        with self.assertRaises(ValueError):
            self.check()

    def test_nonfinite_cpu_is_refused(self):
        self.rows[0].update(cpu_us=float("nan"), user_us=float("nan"))
        with self.assertRaises(ValueError):
            self.check()

    def test_duplicate_repetition_is_refused(self):
        self.rows[1]["repetition"] = self.rows[0]["repetition"]
        with self.assertRaises(ValueError):
            self.check()

    def cli(self, *flags, hosted=False):
        self.save()
        env = dict(os.environ, HOME=str(self.root), SHELL="/bin/sh")
        env.pop("GITHUB_ACTIONS", None)
        if hosted:
            env["GITHUB_ACTIONS"] = "true"
        return subprocess.run([sys.executable, "-I", str(HERE / "check-loop.py"), "--results", str(self.root), *flags],
                              env=env, capture_output=True, text=True)

    def make_ratios_fail(self):
        for row in self.rows:
            if row["participant"] == "pelt":
                row.update(user_us=row["cpu_us"] * 2, system_us=0.0, cpu_us=row["cpu_us"] * 2)

    def test_cli_propagates_named_failure(self):
        self.make_ratios_fail()
        result = self.cli("--pool-gate")
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL loop-counted-cpu", result.stdout)
        self.assertIn("FAIL loop-counted-long", result.stdout)

    def test_cli_default_reports_without_ratio_gating(self):
        self.make_ratios_fail()
        result = self.cli()
        self.assertEqual(result.returncode, 0)
        self.assertIn("REPORT loop-counted-long", result.stdout)
        self.assertIn("would-fail", result.stdout)
        self.assertNotIn("FAIL loop-counted-long", result.stdout)

    def test_hosted_ci_never_gates_ratio_even_with_pool_flag(self):
        self.make_ratios_fail()
        result = self.cli("--pool-gate", hosted=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("policy=report", result.stdout)
        self.assertIn("REPORT loop-counted-long", result.stdout)

    def test_report_mode_keeps_noise_and_floor_visible(self):
        for row in self.rows:
            if row["participant"] == "reference-again":
                for key in ("user_us", "system_us", "cpu_us"):
                    row[key] *= 2
        result = self.cli(hosted=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("reason=reference-noise", result.stdout)
        self.assertIn("would-fail", result.stdout)

    def test_report_mode_does_not_hide_broken_record(self):
        self.rows[0]["exit"] = 2
        result = self.cli(hosted=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL loop-counted-record", result.stdout)


if __name__ == "__main__":
    unittest.main()
