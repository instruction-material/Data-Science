"""Independent expected cases for correlation and statistical storytelling."""
import io
import json
import runpy
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORRELATION = "DSP-11-module-5-visualization-and-statistics-in-context-supplemental-3"
CLAIM = "DSP-12-module-6-storytelling-with-data"
CAPTIONS = "DSP-12-module-6-storytelling-with-data-supplemental-2"
LIMITS = "DSP-13-module-6-storytelling-with-data-supplemental-3"
FOLDERS = (CORRELATION, CLAIM, CAPTIONS, LIMITS)
EARLY = "early: 18 of 24 seats booked (75.0% booked)"
LATE = "late: 24 of 40 seats booked (60.0% booked)"


def program(folder, role="solution"):
    return runpy.run_path(str(ROOT / folder / role / "main.py"))


def stdout(loaded, args=()):
    with redirect_stdout(io.StringIO()) as run:
        loaded["main"](args)
    return run.getvalue()


class StatisticsStorytellingTests(unittest.TestCase):
    def test_pooled_and_separate_correlations_have_opposite_signs(self):
        result = json.loads(stdout(program(CORRELATION)))
        self.assertEqual(result["pooled"], {"pairs": 6, "r": 0.888})
        self.assertEqual(result["sessions"], {
            "A": {"pairs": 3, "r": -1.0},
            "B": {"pairs": 3, "r": -1.0},
        })

    def test_constant_or_unobserved_series_has_no_measured_correlation(self):
        measure = program(CORRELATION)["measure"]
        for points in ([], [(1, 5)], [(1, 5), (1, 6)], [(1, 5), (2, 5)]):
            self.assertEqual(measure(points), {"pairs": len(points), "r": None})

    def test_claim_distinguishes_more_bookings_from_higher_rate(self):
        result = json.loads(stdout(program(CLAIM)))
        self.assertEqual(result, {
            "comparison": [EARLY, LATE],
            "booking_change": 6,
            "booking_share_change_percentage_points": -15.0,
        })

    def test_captions_share_both_denominators_and_differ_in_purpose(self):
        result = json.loads(stdout(program(CAPTIONS)))
        for caption in result.values():
            self.assertIn(EARLY, caption)
            self.assertIn(LATE, caption)
        self.assertNotIn("attendance", result["club_update"])
        self.assertIn("attendance and turnaways", result["planning_note"])

    def test_extension_distinguishes_no_capacity_from_a_measured_zero(self):
        loaded = program(LIMITS)
        result = json.loads(stdout(loaded))
        self.assertEqual(result["booking_share_change_percentage_points"], None)
        self.assertEqual(result["status"], "insufficient denominator")
        self.assertEqual(result["comparison"], [
            "early: 0 of 0 seats booked (undefined booking share)", LATE,
        ])
        with tempfile.TemporaryDirectory() as scratch:
            changed = Path(scratch) / "measured-zero.csv"
            changed.write_text("period,booked,seats\nearly,0,10\nlate,24,40\n")
            measured = json.loads(stdout(loaded, ["--input", str(changed)]))
        self.assertEqual(measured["booking_share_change_percentage_points"], 60.0)
        self.assertEqual(measured["status"], "descriptive comparison")

    def test_csv_rejects_impossible_bookings_and_unpaired_fields(self):
        with tempfile.TemporaryDirectory() as scratch:
            damaged = Path(scratch) / "bad.csv"
            damaged.write_text("period,booked,seats\nearly,7,4\n")
            with self.assertRaisesRegex(ValueError, "0 <= booked <= seats"):
                program(CLAIM)["load"](damaged)
            damaged.write_text("session,temperature_c,visits\nA,10\n")
            with self.assertRaisesRegex(ValueError, "unexpected number of fields"):
                program(CORRELATION)["load"](damaged)

    def test_roles_share_inputs_and_starter_identifies_its_missing_function(self):
        for folder in FOLDERS:
            with self.subTest(folder=folder):
                student, reference = program(folder, "starter"), program(folder)
                self.assertEqual(student["DEFAULT"].read_bytes(), reference["DEFAULT"].read_bytes())
                self.assertRegex(stdout(student), r"^Complete \w+ before comparing results\.\n$")
                self.assertIsInstance(json.loads(stdout(reference)), dict)


if __name__ == "__main__":
    unittest.main()
