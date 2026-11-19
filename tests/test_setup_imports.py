"""Check the setup practice files and starter/reference defaults."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSFER = ROOT / "DSP-01-dsp0-setup-and-tooling-supplemental-2"
EXTENSION = ROOT / "DSP-02-dsp0-setup-and-tooling-supplemental-3"


def run(project, role, *args):
    work = project / role
    return subprocess.run(
        [sys.executable, "-I", "-B", "main.py", *args],
        cwd=work, check=True, capture_output=True, text=True, timeout=10,
    ).stdout


class SetupImportTests(unittest.TestCase):
    def test_transfer_preserves_baseline_and_loads_the_new_values(self):
        baseline = "Records: 6\nTotal trips: 32\nMean trips per record: 5.33\n"
        expected = "Records: 4\nTotal trips: 16\nMean trips per record: 4.00\n"
        self.assertEqual(run(TRANSFER, "starter"), baseline)
        self.assertEqual(run(TRANSFER, "starter", "--csv", "data/practice.csv"), expected)
        self.assertEqual(run(TRANSFER, "solution"), expected)
        self.assertEqual(run(TRANSFER, "starter"), baseline)

    def test_extension_reports_both_denominators(self):
        expected = (
            "empty\nRecords: 0\nTotal trips: 0\nMean trips per record: undefined\n"
            "zero\nRecords: 1\nTotal trips: 0\nMean trips per record: 0.00\n"
        )
        self.assertIn("Records: 6", run(EXTENSION, "starter"))
        self.assertEqual(
            run(EXTENSION, "starter", "--csv", "data/empty.csv", "data/zero.csv"), expected,
        )
        self.assertEqual(run(EXTENSION, "solution"), expected)


if __name__ == "__main__":
    unittest.main()
