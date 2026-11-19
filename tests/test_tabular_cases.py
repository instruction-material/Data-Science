"""Independent expected results for the six tabular teaching packs."""
import io
import json
import runpy
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
GROUP = "DSP-10-module-3-pandas-foundations"
FILTER = "DSP-07-module-3-pandas-foundations-supplemental-2"
RATE = "DSP-08-module-3-pandas-foundations-supplemental-3"
CLEAN = "DSP-11-module-4-cleaning-and-validation"
DUPLICATES = "DSP-09-module-4-cleaning-and-validation-supplemental-2"
POLICY = "DSP-10-module-4-cleaning-and-validation-supplemental-3"
PACKS = (GROUP, FILTER, RATE, CLEAN, DUPLICATES, POLICY)


def load(folder, role="solution"):
    return runpy.run_path(str(ROOT / folder / role / "main.py"))


def output(program, args=()):
    with redirect_stdout(io.StringIO()) as captured:
        program["main"](args)
    return captured.getvalue()


class TabularCases(unittest.TestCase):
    def test_group_results_match_hand_calculation(self):
        result = json.loads(output(load(GROUP)))
        self.assertEqual(result["shape"], [6, 4])
        self.assertEqual(result["columns"], ["trip_id", "site", "trips", "hours"])
        self.assertEqual(result["sites"], [
            {"site": "north", "records": 2, "total_trips": 6, "mean_trips": 3},
            {"site": "south", "records": 1, "total_trips": 8, "mean_trips": 8},
            {"site": "west", "records": 3, "total_trips": 18, "mean_trips": 6},
        ])

    def test_filter_includes_boundary_and_uses_id_to_break_ties(self):
        program = load(FILTER)
        base = json.loads(output(program))
        self.assertEqual([row["trip_id"] for row in base["rows"]], ["R06", "R03", "R05"])
        with TemporaryDirectory() as scratch:
            changed = Path(scratch) / "changed.csv"
            changed.write_text(program["DEFAULT_INPUT"].read_text() + "R07,north,6,2\n")
            result = json.loads(output(program, ["--input", str(changed)]))
        self.assertEqual([row["trip_id"] for row in result["rows"]], ["R06", "R03", "R05", "R07"])

    def test_rate_preserves_input_and_distinguishes_zero_and_undefined(self):
        program = load(RATE)
        frame = program["load_frame"](program["DEFAULT_INPUT"])
        before = frame.copy()
        result = program["analyze"](frame)
        self.assertTrue(frame.equals(before))
        self.assertEqual([row["trips_per_hour"] for row in result["rows"]], [2, 2, 2, None, 2, 4])
        frame.loc[0, "trips"] = 0
        self.assertEqual(program["analyze"](frame)["rows"][0]["trips_per_hour"], 0)

    def test_cleaning_accounts_for_every_original_record(self):
        program = load(CLEAN)
        raw = program["load_frame"](program["DEFAULT_INPUT"])
        before = raw.copy()
        result = program["analyze"](raw)
        self.assertTrue(raw.equals(before))
        self.assertEqual(result["summary"], {
            "loaded": 10, "accepted": 5, "total_trips": 24,
            "repaired_labels": 2,
            "outcomes": {"accepted": 5, "duplicate": 1, "invalid_trips": 1,
                         "missing_site": 1, "missing_trips": 1, "range_trips": 1},
            "accepted_ids": ["R01", "R02", "R06", "R07", "R09"],
        })
        audit = result["audit"]
        self.assertEqual([row["source_record"] for row in audit], list(range(1, 11)))
        self.assertEqual([row["source_record"] for row in audit if row["label_repaired"]], [1, 10])

    def test_both_conflicting_records_are_held(self):
        result = json.loads(output(load(DUPLICATES)))
        self.assertEqual([row["source_record"] for row in result["conflicts"]], [8, 11])
        self.assertEqual([row["trip_id"] for row in result["conflicts"]], ["R07", "R07"])
        self.assertEqual(result["summary"]["outcomes"]["duplicate"], 1)
        self.assertEqual((result["summary"]["loaded"], result["summary"]["accepted"],
                          result["summary"]["total_trips"]), (11, 4, 12))

    def test_policy_reports_both_denominators_and_the_effect(self):
        result = json.loads(output(load(POLICY)))
        self.assertEqual(result["label_repair"]["accepted_ids"], ["R01", "R02", "R06", "R07", "R09"])
        self.assertEqual(result["exact_labels_only"]["accepted_ids"], ["R02", "R06", "R07"])
        self.assertEqual(result["label_repair"]["loaded"], 10)
        self.assertEqual(result["exact_labels_only"]["loaded"], 10)
        self.assertEqual((result["accepted_delta"], result["total_trips_delta"]), (2, 8))

    def test_cleaning_handles_empty_tables_and_additional_range_and_missing_cases(self):
        program = load(CLEAN)
        with TemporaryDirectory() as scratch:
            sample = Path(scratch) / "empty.csv"
            sample.write_text("trip_id,site,trips,hours\n")
            empty = json.loads(output(program, ["--input", str(sample)]))
            self.assertEqual(empty["audit"], [])
            self.assertEqual(empty["summary"]["accepted"], 0)
            sample.write_text("trip_id,site,trips,hours\nR01,west,1,25\nR02,west,1,\nR03,NA,1,21\n")
            new = json.loads(output(program, ["--input", str(sample)]))
            self.assertEqual([r["status"] for r in new["audit"]],
                             ["range_hours", "missing_hours", "invalid_site"])

    def test_wrong_columns_and_extra_field_rows_fail_clearly(self):
        for folder in (GROUP, CLEAN):
            program = load(folder)
            with TemporaryDirectory() as scratch:
                sample = Path(scratch) / "invalid.csv"
                sample.write_text("id,site,trips,hours\nR01,north,2,1\n")
                with self.assertRaisesRegex(ValueError, "Expected columns"):
                    program["load_frame"](sample)
                sample.write_text("trip_id,site,trips,hours\nextra,R01,north,2,1\n")
                with self.assertRaises(ValueError):
                    program["load_frame"](sample)

    def test_role_packs_share_inputs_but_only_solutions_complete_the_task(self):
        for folder in PACKS:
            with self.subTest(folder=folder):
                starter = load(folder, "starter")
                solution = load(folder)
                self.assertEqual(starter["DEFAULT_INPUT"].read_bytes(), solution["DEFAULT_INPUT"].read_bytes())
                self.assertRegex(output(starter), r"^Complete \w+ before comparing results\.\n$")
                self.assertIsInstance(json.loads(output(solution)), dict)


if __name__ == "__main__":
    unittest.main()
