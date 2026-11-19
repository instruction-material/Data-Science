"""Independent cases for the actual cleaning assignment and safe extension."""
import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "DSP-02-data-analysis-lab-12"


def load(role="solution"):
    spec = importlib.util.spec_from_file_location(
        "cleaning_" + role, FOLDER / role / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CleaningReportTests(unittest.TestCase):
    def test_supplied_rows_and_exact_rejection_evidence(self):
        module = load()
        result = module.clean_rows(module.load_rows())
        self.assertEqual(result["values"], [4, 8, 17])
        self.assertEqual(result["report"], dict(
            rows_loaded=8, rows_accepted=3, rows_rejected=5, rows_repaired=0))
        self.assertEqual(result["rejected_rows"], [
            dict(row=3, label="beta", value="", reason="missing"),
            dict(row=4, label="gamma", value="apple", reason="not numeric"),
            dict(row=5, label="delta", value="-6", reason="negative"),
            dict(row=7, label="zeta", value="NaN", reason="not finite"),
            dict(row=8, label="eta", value=" 11 ", reason="surrounding whitespace"),
        ])

    def test_safe_repair_preserves_order_originals_and_accounting(self):
        module = load()
        rows = module.load_rows()
        original = copy.deepcopy(rows)
        for policy, values, rejected, repaired in [
            (False, [4, 8, 17], 5, 0),
            (True, [4, 8, 11, 17], 4, 1),
        ]:
            result = module.clean_rows(rows, repair_whitespace=policy)
            self.assertEqual(result["values"], values)
            report = result["report"]
            self.assertEqual(report["rows_rejected"], rejected)
            self.assertEqual(report["rows_repaired"], repaired)
            self.assertEqual(report["rows_accepted"] + report["rows_rejected"],
                             report["rows_loaded"])
            self.assertEqual(rows, original)

    def test_zero_fraction_empty_and_all_rejected(self):
        module = load()
        for rows, expected in [([], []),
            ([dict(label="zero", value="0"), dict(label="fraction", value="0.5")], [0, 0.5]),
            ([dict(label="empty", value=None), dict(label="bad", value="x")], [])]:
            with self.subTest(rows=rows):
                result = module.clean_rows(rows)
                self.assertEqual(result["values"], expected)
                self.assertEqual(result["report"]["rows_loaded"], len(rows))
                self.assertEqual(result["report"]["rows_rejected"], len(rows) - len(expected))

    def test_nonfinite_and_invalid_cells_stay_rejected_after_repair(self):
        module = load()
        rows = [dict(label=str(i), value=text) for i, text in enumerate(
            [" NaN ", "inf", "-Infinity", " -3 ", "apple", "   "])]
        result = module.clean_rows(rows, repair_whitespace=True)
        self.assertEqual(result["values"], [])
        self.assertEqual(result["report"], dict(
            rows_loaded=6, rows_accepted=0, rows_rejected=6, rows_repaired=0))
        self.assertEqual([row["reason"] for row in result["rejected_rows"]],
                         ["not finite", "not finite", "not finite", "negative", "not numeric", "missing"])

    def test_custom_csv_header_and_original_cells(self):
        module = load()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "custom.csv"
            path.write_text('label,value\n"two, words", 2.5 \n', encoding="utf-8")
            rows = module.load_rows(path)
            self.assertEqual(rows, [dict(label="two, words", value=" 2.5 ")])
            self.assertEqual(module.clean_rows(rows, repair_whitespace=True)["values"], [2.5])
            path.write_text("label,other\nx,1\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "label and value"):
                module.load_rows(path)

    def test_both_actual_entrypoints_from_independent_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            for role, expected in [("starter", "TODO: clean the rows"),
                                   ("solution", "'rows_rejected': 5")]:
                result = subprocess.run([sys.executable, "-I", "-B", str(FOLDER / role / "main.py")],
                    cwd=temporary, capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertIn(expected, result.stdout)


if __name__ == "__main__":
    unittest.main()
