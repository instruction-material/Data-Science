"""Independent hand-calculated contracts for the three CSV studio projects."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = {
    "summary": "DSP-01-data-analysis-lab-11",
    "distribution": "DSP-20-applied-studio-11-data-analysis-lab-11-supplemental-2",
    "report": "DSP-21-applied-studio-11-data-analysis-lab-11-supplemental-3",
}


def load(kind, role="solution"):
    path = ROOT / FOLDERS[kind] / role / "main.py"
    spec = importlib.util.spec_from_file_location(f"csv_{kind}_{role}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CsvStudioTests(unittest.TestCase):
    def test_count_total_and_mean(self):
        summary = load("summary")
        cases = [
            ([], {"count": 0, "total": 0, "average": None}),
            ([6], {"count": 1, "total": 6, "average": 6}),
            ([4, 8, 11, 17], {"count": 4, "total": 40, "average": 10}),
            ([-2, 2, 6], {"count": 3, "total": 6, "average": 2}),
            ([0.5, 1.5], {"count": 2, "total": 2, "average": 1}),
        ]
        for values, expected in cases:
            with self.subTest(values=values):
                before = values.copy()
                self.assertEqual(summary.summarize(values), expected)
                self.assertEqual(values, before)

    def test_optional_range_and_outlier_comparison(self):
        summary = load("summary")
        empty = summary.extended_summary([])
        self.assertIsNone(empty["minimum"])
        self.assertIsNone(empty["maximum"])
        self.assertIsNone(empty["range"])
        for values, minimum, maximum, span, mean in [
            ([4, 8, 11, 17], 4, 17, 13, 10),
            ([4, 8, 11, 17, 100], 4, 100, 96, 28),
            ([-9, -2, -5], -9, -2, 7, -16 / 3),
            ([6], 6, 6, 0, 6),
        ]:
            with self.subTest(values=values):
                before = values.copy()
                result = summary.extended_summary(values)
                self.assertEqual((result["minimum"], result["maximum"], result["range"]),
                                 (minimum, maximum, span))
                self.assertEqual(result["average"], mean)
                self.assertEqual(values, before)

    def test_median_modes_and_extreme_value(self):
        distribution = load("distribution")
        for values, mean, median, modes in [
            ([], None, None, []),
            ([6], 6, 6, [6]),
            ([4, 8, 11, 17], 10, 9.5, [4, 8, 11, 17]),
            ([1, 2, 2, 3, 100], 21.6, 2, [2]),
            ([3, 1, 3, 1], 2, 2, [3, 1]),
            ([9, 1, 4], 14 / 3, 4, [9, 1, 4]),
            ([-4, 2, -4, 2], -1, -1, [-4, 2]),
        ]:
            with self.subTest(values=values):
                before = values.copy()
                result = distribution.summarize_distribution(values)
                self.assertEqual((result["average"], result["median"], result["modes"]),
                                 (mean, median, modes))
                self.assertEqual(values, before)

    def test_report_is_a_complete_readable_artifact(self):
        report = load("report")
        caution = "Caution: This describes the loaded rows; it does not establish a cause."
        self.assertEqual(report.format_report("sample.csv", [4, 8, 11, 17]),
                         "Source: sample.csv\nRows: 4\nTotal: 40\nMean: 10\n" + caution)
        self.assertEqual(report.format_report("empty.csv", []),
                         "Source: empty.csv\nRows: 0\nTotal: 0\nMean: undefined (no rows)\n" + caution)
        values = [-2, 2, 6]
        self.assertEqual(report.format_report("custom.csv", values),
                         "Source: custom.csv\nRows: 3\nTotal: 6\nMean: 2\n" + caution)
        self.assertEqual(values, [-2, 2, 6])

    def test_csv_inputs_and_independent_working_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            custom = folder / "custom.csv"
            custom.write_text("value,category\n-2.5,a\n3.5,b\n", encoding="utf-8")
            empty = folder / "empty.csv"
            empty.write_text("value\n", encoding="utf-8")
            for kind in FOLDERS:
                for role in ["starter", "solution"]:
                    with self.subTest(kind=kind, role=role):
                        module = load(kind, role)
                        self.assertEqual(module.load_values(), [4, 8, 11, 17])
                        self.assertEqual(module.load_values(custom), [-2.5, 3.5])
                        self.assertEqual(module.load_values(empty), [])
                        run = subprocess.run([sys.executable, "-B", str(ROOT / FOLDERS[kind] / role / "main.py")],
                                             cwd=folder, capture_output=True, text=True, timeout=10)
                        self.assertEqual(run.returncode, 0, run.stderr)
                        self.assertEqual(run.stderr, "")
                        if role == "starter":
                            self.assertIn("TODO:", run.stdout)
                        elif kind == "summary":
                            self.assertEqual(run.stdout, "{'count': 4, 'total': 40.0, 'average': 10.0}\n")
                        elif kind == "distribution":
                            self.assertEqual(run.stdout, "{'count': 4, 'total': 40.0, 'average': 10.0, 'median': 9.5, 'modes': [4.0, 8.0, 11.0, 17.0]}\n")
                        else:
                            self.assertEqual(run.stdout, "Source: sample.csv\nRows: 4\nTotal: 40\nMean: 10\nCaution: This describes the loaded rows; it does not establish a cause.\n")


if __name__ == "__main__":
    unittest.main()
