"""Exercise the core capstone and its two independent review activities."""

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "DSP-14-module-9-data-science-capstone"
TRANSFER = ROOT / "DSP-18-module-9-data-science-capstone-supplemental-2"
EXTENSION = ROOT / "DSP-19-module-9-data-science-capstone-supplemental-3"


def run_project(project, *arguments, role="solution", cwd=None, check=True):
    return subprocess.run(
        [sys.executable, "-I", "-B", str(project / role / "main.py"), *arguments],
        cwd=cwd or project / role,
        capture_output=True,
        text=True,
        check=check,
        timeout=10,
    )


class CapstoneLoanTests(unittest.TestCase):
    def test_starters_run_and_keep_fixtures_identical(self):
        for project in (CORE, TRANSFER, EXTENSION):
            with self.subTest(project=project.name), tempfile.TemporaryDirectory() as tmp:
                self.assertTrue(run_project(project, role="starter", cwd=tmp).stdout.startswith("TODO:"))
                self.assertEqual(list(Path(tmp).iterdir()), [])
                for path in (project / "solution" / "data").glob("*.csv"):
                    self.assertEqual(path.read_bytes(), (project / "starter" / "data" / path.name).read_bytes())

    def test_core_report_matches_hand_calculations_and_saved_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            actual = run_project(CORE, cwd=tmp).stdout
            self.assertEqual((Path(tmp) / "report.md").read_text(), actual)
            self.assertIn("| Before | 42 | 14 | 1 | 3.00 |", actual)
            self.assertIn("| After | 60 | 15 | 0 | 4.00 |", actual)
            self.assertIn("+1.00 observed loans per open hour", actual)
            self.assertIn("cannot establish what caused the change", actual)

    def test_core_compares_measured_zero_and_unknown_without_overwriting_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "custom.csv"
            source = "phase,week,loans,open_hours\nBefore,W1,0,4\nAfter,W1,,4\n"
            path.write_text(source)
            report = run_project(CORE, "--csv", str(path), cwd=tmp).stdout
            self.assertIn("| Before | 0 | 4 | 0 | 0.00 |", report)
            self.assertIn("| After | unavailable | 0 | 1 | unavailable |", report)
            self.assertIn("insufficient measured coverage", report)
            failed = run_project(CORE, "--csv", str(path), "--output", str(path), cwd=tmp, check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertEqual(path.read_text(), source)

    def test_transfer_hashes_exact_inputs_and_finds_change_independent_of_order(self):
        actual = run_project(TRANSFER).stdout
        self.assertIn("After W3: loans 8 -> 11", actual)
        self.assertIn("After: 4.00 -> 4.20 loans/hour", actual)
        folder = TRANSFER / "solution" / "data"
        for path in (folder / "sample.csv", folder / "corrected.csv"):
            self.assertIn(f"{path.name} SHA-256: {hashlib.sha256(path.read_bytes()).hexdigest()}", actual)
        with tempfile.TemporaryDirectory() as tmp:
            reordered = Path(tmp) / "reordered.csv"
            header, *rows = (folder / "sample.csv").read_text().splitlines()
            reordered.write_text("\n".join((header, *reversed(rows))) + "\n")
            comparison = run_project(TRANSFER, "--revised", str(reordered)).stdout
            self.assertIn("No record changes", comparison)
            self.assertIn("After: 4.00 -> 4.00 loans/hour", comparison)

    def test_extension_reports_how_the_filter_changes_coverage_and_rates(self):
        actual = run_project(EXTENSION).stdout
        self.assertIn("Before | 2 -> 1 | 14 -> 8 | 3.00 -> 3.00", actual)
        self.assertIn("After | 3 -> 1 | 15 -> 7 | 4.00 -> 4.86", actual)
        empty = run_project(EXTENSION, "--minimum-hours", "9").stdout
        self.assertIn("Before | 2 -> 0 | 14 -> 0 | 3.00 -> unavailable", empty)
        self.assertIn("After | 3 -> 0 | 15 -> 0 | 4.00 -> unavailable", empty)


if __name__ == "__main__":
    unittest.main()
