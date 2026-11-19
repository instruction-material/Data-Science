"""Verify standalone Project Practice Guide starters and references."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_project(name, role="solution", *arguments):
    folder = ROOT / f"DSP-practice-{name}" / role
    return subprocess.run(
        [sys.executable, "-I", "-B", "main.py", *arguments],
        cwd=folder,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout


def run_with_csv(name, csv):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "custom.csv"
        path.write_text(csv, encoding="utf-8")
        return run_project(name, "solution", "--csv", str(path))


class PracticeProjectTests(unittest.TestCase):
    def test_starters_run_and_share_inputs_with_their_references(self):
        names = ("public-dataset", "cleaning", "chart-redesign", "trend", "final")
        messages = set()
        for name in names:
            with self.subTest(name=name):
                starter = ROOT / f"DSP-practice-{name}" / "starter"
                solution = starter.with_name("solution")
                for asset in ("README.md", "data/sample.csv"):
                    self.assertEqual((starter / asset).read_bytes(),
                                     (solution / asset).read_bytes())
                message = run_project(name, "starter")
                self.assertTrue(message.startswith("TODO: "))
                messages.add(message)
        self.assertEqual(len(messages), len(names))

    def test_public_report_compares_complete_observations_using_original_units(self):
        text = run_project("public-dataset")
        self.assertIn("Canada | 81.8 | 82.2 | +0.4", text)
        self.assertIn("Japan | 83.5 | 83.7 | +0.2", text)
        self.assertIn("2015 gap between highest and lowest: 1.5 years", text)
        self.assertEqual(
            run_project("public-dataset", "solution", "--year", "2020").strip(),
            "No countries have observations in both 2013 and 2020.",
        )

    def test_cleaning_counts_rows_and_preserves_the_quoted_station_and_zero(self):
        text = run_project("cleaning")
        self.assertIn("4 accepted + 4 rejected = 8 input rows\nAccepted riders: 25", text)
        self.assertIn('N2,"North, Annex",0', text)
        self.assertIn("5,S1,duplicate ID", text)
        self.assertIn("6,N3,missing count", text)
        self.assertIn("7,S2,invalid count", text)
        self.assertIn("8,S3,invalid count", text)

    def test_invalid_first_occurrence_does_not_reserve_an_id(self):
        text = run_with_csv("cleaning", "record_id,station,riders\nX,North,bad\nX,North,0\n")
        self.assertIn("1 accepted + 1 rejected = 2 input rows\nAccepted riders: 0", text)
        self.assertIn("X,North,0", text)
        self.assertIn("2,X,invalid count", text)

    def test_redesign_compares_the_same_counts_from_zero(self):
        text = run_project("chart-redesign")
        self.assertIn("A: 2 trips above baseline\nB: 9 trips above baseline", text)
        self.assertIn(f"A |{'#' * 42} 42 trips", text)
        self.assertIn(f"B |{'#' * 49} 49 trips", text)
        self.assertIn("The difference is 7 trips.", text)
        for count in (0, 20):
            with self.subTest(count=count):
                tied = run_with_csv("chart-redesign", f"service,observed_trips\nA,{count}\nB,{count}\n")
                a, b = [line[2:] for line in tied.splitlines() if line.startswith(("A |", "B |"))]
                self.assertEqual(a, b)
                self.assertIn("The difference is 0 trips.", tied)

    def test_trend_distinguishes_unavailable_period_from_measured_zero(self):
        text = run_project("trend")
        for row in ("Week 1 | 20 | 2 | 10.00", "Week 2 | 30 | 3 | 10.00",
                    "Week 3 | unavailable | 0 | unavailable", "Week 4 | 36 | 4 | 9.00"):
            self.assertIn(row, text)
        zero = run_with_csv("trend", "week,trips,covered_days\nWeek 1,0,3\nWeek 2,,3\n")
        self.assertIn("Week 1 | 0 | 3 | 0.00", zero)
        self.assertIn("Week 2 | unavailable | 3 | unavailable", zero)

    def test_final_story_reconciles_coverage_and_both_rate_boundaries(self):
        rates, coverage = run_project("final").split("\nCoverage by route and week\n")
        self.assertIn("North | 77 | 9 | 8.56", rates)
        self.assertIn("East | 0 | 2 | 0.00", rates)
        self.assertIn("West | unavailable | 0 | unavailable", rates)
        self.assertIn("South | W3 | 2 | unavailable", coverage)
        self.assertIn("West | W1 | 0 | unavailable", coverage)


if __name__ == "__main__":
    unittest.main()
