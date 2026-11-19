"""Independent hand cases for grouped summaries, display and second metrics."""
import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ["DSP-03-data-analysis-lab-13",
           "DSP-24-applied-studio-13-data-analysis-lab-13-supplemental-2",
           "DSP-25-applied-studio-13-data-analysis-lab-13-supplemental-3"]


def load(index=0, role="solution"):
    spec = importlib.util.spec_from_file_location(
        "grouped_" + str(index) + "_" + role, ROOT / FOLDERS[index] / role / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GroupedSummariesTests(unittest.TestCase):
    def test_raw_and_normalized_sample_with_exact_denominators(self):
        m = load()
        rows = m.load_rows()
        raw = m.summarize_groups(rows)
        self.assertEqual(list(raw), ["NORTH", "North", "north", "south", "west"])
        self.assertEqual([raw[label]["average"] for label in list(raw)[:3]], [12, 8, 4])
        actual = m.summarize_groups(rows, normalize_labels=True)
        self.assertEqual(actual, {
            "north": dict(count=3, total=24, average=8),
            "south": dict(count=2, total=24, average=12),
            "west": dict(count=3, total=102, average=34)})
        self.assertEqual(sum(x["total"] for x in actual.values()) / len(rows), 18.75)
        self.assertEqual(sum(x["count"] for x in raw.values()), len(rows))

    def test_normalization_preserves_all_original_evidence(self):
        rows = [dict(category=" North ", value=" -2.5 "),
                dict(category="NORTH", value="2.5"), dict(category="south", value="0")]
        before = copy.deepcopy(rows)
        for index in range(3):
            m = load(index)
            raw = m.summarize_groups(rows)
            self.assertEqual(len(raw), 3)
            result = m.summarize_groups(rows, normalize_labels=True)
            self.assertEqual(list(result), ["north", "south"])
            self.assertEqual(result["north"]["count"], 2)
            self.assertEqual(result["north"]["total"], 0)
            self.assertEqual(rows, before)

    def test_empty_singleton_fraction_and_finite_negatives(self):
        for index in range(3):
            m = load(index)
            self.assertEqual(m.summarize_groups([]), {})
            result = m.summarize_groups([dict(category="one", value="-1.5")])["one"]
            self.assertEqual((result["count"], result["total"], result["average"]), (1, -1.5, -1.5))
            if index == 2:
                self.assertEqual((result["median"], result["maximum"]), (-1.5, -1.5))

    def test_invalid_rows_report_the_record_and_originals_stay_intact(self):
        for index in range(3):
            m = load(index)
            for row, error in [(dict(category=" ", value="1"), "category is missing"),
                (dict(value="1"), "category is missing"),
                (dict(category="x", value="apple"), "value is not numeric"),
                (dict(category="x"), "value is not numeric"),
                *[(dict(category="x", value=v), "value is not finite") for v in ["NaN", "inf", "-Infinity"]]]:
                rows = [dict(category="first", value="1"), row]
                before = copy.deepcopy(rows)
                with self.subTest(index=index, row=row):
                    with self.assertRaisesRegex(ValueError, "Record 3: " + error):
                        m.summarize_groups(rows, normalize_labels=True)
                    self.assertEqual(rows, before)

    def test_markdown_and_interpretation_display_the_same_grouped_result(self):
        m = load(1)
        summary = m.summarize_groups(m.load_rows(), normalize_labels=True)
        self.assertEqual(m.render_table(summary),
            "| Category | Count | Total | Mean |\n| --- | ---: | ---: | ---: |\n"
            "| north | 3 | 24.00 | 8.00 |\n| south | 2 | 24.00 | 12.00 |\n| west | 3 | 102.00 | 34.00 |")
        self.assertEqual(m.interpretation(summary),
            "8 rows across 3 groups; 0 groups have fewer than two rows. "
            "These synthetic measurements illustrate grouping and do not establish a population difference.")
        self.assertEqual(len(m.render_table({}).splitlines()), 2)
        self.assertIn("0 rows across 0 groups", m.interpretation({}))
        self.assertIn("1 groups have fewer than two rows", m.interpretation({"x": dict(count=1)}))
        self.assertIn("a\\|b", m.render_table({"a|b": dict(count=1, total=2, average=2)}))

    def test_second_metric_exposes_skew_and_even_unsorted_median(self):
        m = load(2)
        west = m.summarize_groups(m.load_rows(), normalize_labels=True)["west"]
        self.assertEqual(west, dict(count=3, total=102, average=34, median=1, maximum=100))
        rows = [dict(category="x", value=str(x)) for x in [10, 0, 4, 2]]
        before = copy.deepcopy(rows)
        result = m.summarize_groups(rows)["x"]
        self.assertEqual(result, dict(count=4, total=16, average=4, median=3, maximum=10))
        self.assertEqual(rows, before)

    def test_loaders_check_columns_and_accept_a_quoted_category(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "case.csv"
            for index in range(3):
                m = load(index)
                path.write_text('category,value\n"a,b",2.5\n', encoding="utf-8")
                self.assertEqual(m.load_rows(path), [dict(category="a,b", value="2.5")])
                path.write_text("label,value\nx,1\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "category and value"):
                    m.load_rows(path)

    def test_all_six_actual_entrypoints_from_an_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            for index, folder in enumerate(FOLDERS):
                for role in ["starter", "solution"]:
                    run = subprocess.run([sys.executable, "-I", "-B", str(ROOT / folder / role / "main.py")],
                        cwd=temporary, capture_output=True, text=True, timeout=10)
                    self.assertEqual(run.returncode, 0, run.stderr)
                    self.assertEqual(run.stderr, "")
                    self.assertIn("TODO:" if role == "starter" else
                        ["'south': {'count': 2", "| west | 3 | 102.00 | 34.00 |", "'median': 1.0, 'maximum': 100.0"][index], run.stdout)


if __name__ == "__main__":
    unittest.main()
