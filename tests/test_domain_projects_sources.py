"""Verify the distinct Domain Projects starter and reference roles."""

from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = "DSP-domain-trip-coverage"
WARMUP = "DM7-Simple-Sort"
TRANSFER = "DSP-16-module-8-domain-projects-supplemental-2"
EXTENSION = "DSP-17-module-8-domain-projects-supplemental-3"


def execute(folder, role, *arguments):
    source = ROOT / folder / role
    return subprocess.run(
        [sys.executable, "-I", "-B", str(source / "main.py"), *arguments],
        cwd=source,
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    ).stdout.strip()


def implementation(folder):
    return runpy.run_path(str(ROOT / folder / "solution" / "main.py"))


class DomainProjectsSourceTests(unittest.TestCase):
    def test_each_starter_has_its_own_entrypoint(self):
        messages = {
            CORE: "TODO: summarize measured reports by route and by week",
            WARMUP: "TODO: rank measured routes",
            TRANSFER: "TODO: audit route-week rows",
            EXTENSION: "TODO: compare rates across coverage rules",
        }
        for folder, message in messages.items():
            with self.subTest(folder=folder):
                self.assertEqual(execute(folder, "starter"), message)
                starter = ROOT / folder / "starter"
                solution = ROOT / folder / "solution"
                self.assertEqual((starter / "README.md").read_bytes(),
                                 (solution / "README.md").read_bytes())
                if folder != WARMUP:
                    self.assertEqual((starter / "data" / "sample.csv").read_bytes(),
                                     (solution / "data" / "sample.csv").read_bytes())

    def test_core_provides_distinct_route_and_week_denominators(self):
        self.assertEqual(
            execute(CORE, "solution").splitlines(),
            [
                "Routes",
                "East: 0 trips / 2 days = 0.00 trips/day",
                "North: 77 trips / 9 days = 8.56 trips/day",
                "South: 39 trips / 6 days = 6.50 trips/day",
                "Weeks",
                "W1: 38 trips / 5 route-days = 7.60 trips/route-day",
                "W2: 45 trips / 9 route-days = 5.00 trips/route-day",
                "W3: 33 trips / 3 route-days = 11.00 trips/route-day",
            ],
        )

    def test_core_handles_a_file_without_measurements(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "empty.csv"
            source.write_text("route,week,trips,days\nNorth,W1,,4\n", encoding="utf-8")
            self.assertEqual(execute(CORE, "solution", "--csv", str(source)),
                             "No measured reports")

    def test_ranking_preserves_input_and_resolves_exact_ties(self):
        rank = implementation(WARMUP)["rank_routes"]
        input_records = [("South", 10, 6), ("East", 8, 5), ("North", 5, 3)]
        snapshot = input_records.copy()
        self.assertEqual(rank(input_records), [snapshot[2], snapshot[0], snapshot[1]])
        self.assertEqual(input_records, snapshot)
        self.assertEqual(rank([]), [])
        self.assertEqual(
            execute(WARMUP, "solution").splitlines(),
            ["North: 4.00 trips/day", "South: 4.00 trips/day", "East: 2.00 trips/day"],
        )

    def test_transfer_reconciles_every_row_once(self):
        self.assertEqual(
            execute(TRANSFER, "solution").splitlines(),
            ["Input: 10", "Accepted: 6", "invalid: 1", "missing trips: 1",
             "no coverage: 1", "duplicate: 1"],
        )

    def test_missing_row_does_not_reserve_a_valid_route_week(self):
        audit = implementation(TRANSFER)["audit_reports"]
        missing = {"route": "North", "week": "W1", "trips": "", "days": "2"}
        valid = dict(missing, trips="0")
        records = [missing, valid, valid.copy()]
        snapshot = [row.copy() for row in records]
        accepted, reasons = audit(records)
        self.assertEqual(accepted, [("North", "W1")])
        self.assertEqual(reasons, {"invalid": 0, "missing trips": 1,
                                   "no coverage": 0, "duplicate": 1})
        self.assertEqual(records, snapshot)

    def test_extension_distinguishes_unavailable_from_measured_zero(self):
        self.assertEqual(
            execute(EXTENSION, "solution").splitlines(),
            [
                "Minimum covered days per report: 3",
                "East: 1 -> 0 reports, 0.00 -> unavailable trips/day",
                "North: 3 -> 2 reports, 8.56 -> 8.14 trips/day",
                "South: 2 -> 2 reports, 6.50 -> 6.50 trips/day",
            ],
        )

    def test_extension_with_minimum_one_keeps_all_measurements(self):
        text = execute(EXTENSION, "solution", "--minimum-days", "1")
        self.assertIn("North: 3 -> 3 reports, 8.56 -> 8.56", text)
        self.assertIn("East: 1 -> 1 reports, 0.00 -> 0.00", text)


if __name__ == "__main__":
    unittest.main()
