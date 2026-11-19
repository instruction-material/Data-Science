"""Hand cases and real figure/export checks for the chart integrity assignments."""
import copy
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ["DSP-04-data-analysis-lab-14",
           "DSP-26-applied-studio-14-data-analysis-lab-14-supplemental-2"]
HAS_MATPLOTLIB = importlib.util.find_spec("matplotlib") is not None


def load(index=0, role="solution"):
    spec = importlib.util.spec_from_file_location(
        f"chart_{index}_{role}", ROOT / FOLDERS[index] / role / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ChartDataTests(unittest.TestCase):
    def test_hand_case_preserves_each_denominator_and_original_rows(self):
        expected = {"north": dict(count=2, total=6, mean=3),
                    "south": dict(count=1, total=8, mean=8),
                    "west": dict(count=3, total=18, mean=6)}
        for index in range(2):
            for role in ["starter", "solution"]:
                m = load(index, role)
                rows = m.load_rows()
                before = copy.deepcopy(rows)
                self.assertEqual(m.summarize(rows), expected)
                self.assertEqual(m.summarize(list(reversed(rows))), expected)
                self.assertEqual(rows, before)

    def test_empty_zero_case_and_distinct_spelling(self):
        m = load()
        self.assertEqual(m.summarize([]), {})
        self.assertEqual(m.summarize([dict(site="x", trips=0)]),
                         {"x": dict(count=1, total=0, mean=0)})
        self.assertEqual(list(m.summarize([dict(site="north", trips=1),
                                         dict(site="North", trips=2)])), ["North", "north"])

    def test_loader_reports_missing_or_invalid_records(self):
        for index in range(2):
            m = load(index)
            for text, message in [
                ("value\n1\n", "requires site and trips"),
                ("site,trips\n,1\n", "Record 2: site is missing"),
                ("site,trips\nx,no\n", "Record 2: trips must be a whole number"),
                ("site,trips\nx,1.5\n", "Record 2: trips must be a whole number"),
                ("site,trips\nx,-1\n", "Record 2: trips must be nonnegative")]:
                with self.subTest(index=index, text=text), tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "input.csv"
                    path.write_text(text, encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, message): m.load_rows(path)

    def test_direct_inputs_cannot_smuggle_invalid_counts_or_mutate_rows(self):
        for value in [True, -1, 1.5, "3", float("nan"), float("inf"), None]:
            rows = [dict(site="a", trips=2), dict(site="b", trips=value)]
            before = repr(rows)
            with self.assertRaisesRegex(ValueError, "Record 3: trips must"):
                load().summarize(rows)
            self.assertEqual(repr(rows), before)

    def test_table_exposes_units_counts_and_question(self):
        m = load()
        summary = m.summarize(m.load_rows())
        mean = m.describe(summary)
        total = m.describe(summary, "total")
        self.assertIn("north | 2 | 6 | 3.00", mean)
        self.assertIn("west | 3 | 18 | 6.00", mean)
        self.assertIn("mean trip count", mean)
        self.assertIn("total trips", total)
        self.assertIn(m.LIMITATION, total)
        with self.assertRaises(ValueError): m.describe(summary, "median")

    def test_starter_identifies_the_unfinished_chart(self):
        for index in range(2):
            with self.assertRaisesRegex(NotImplementedError, "TODO: make the labeled"):
                load(index, "starter").make_chart({})

    def test_native_lock_is_present_in_every_downloadable_role(self):
        def hashed_pins(contents):
            blocks = re.split(r"(?m)(?=^[a-z][a-z0-9_-]*==)", contents)
            return {
                block.split()[0]: set(re.findall(r"--hash=sha256:([a-f0-9]{64})", block))
                for block in blocks if block and not block.startswith("#")
            }

        chart_lock = ROOT / FOLDERS[0] / "starter" / "requirements.txt"
        locked = chart_lock.read_bytes()
        chart_pins = hashed_pins(chart_lock.read_text())
        course_pins = hashed_pins((ROOT / "requirements.txt").read_text())
        self.assertIn("matplotlib==3.11.2", chart_pins)
        self.assertNotIn("pandas", {pin.split("==")[0] for pin in chart_pins})
        for pin, hashes in chart_pins.items():
            with self.subTest(pin=pin):
                self.assertTrue(hashes)
                self.assertLessEqual(hashes, course_pins[pin])
        for folder in FOLDERS:
            for role in ["starter", "solution"]:
                self.assertEqual((ROOT / folder / role / "requirements.txt").read_bytes(), locked)

    def test_notebook_cells_resolve_data_without_a_file_global(self):
        for folder in FOLDERS:
            for role in ["starter", "solution"]:
                path = ROOT / folder / role / "main.py"
                code = "import os; os.chdir(" + repr(str(path.parent)) + "); ns={'__name__':'notebook'}; exec(" + repr(path.read_text()) + ",ns); assert len(ns['load_rows']())==6; assert ns['summarize'](ns['load_rows']())['west']['mean']==6"
                result = subprocess.run([sys.executable, "-B", "-c", code],
                                        cwd=tempfile.gettempdir(), capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)


@unittest.skipUnless(HAS_MATPLOTLIB, "Native Matplotlib required; hosted qualification installs the locked graph.")
class ChartFigureTests(unittest.TestCase):
    def tearDown(self):
        import matplotlib.pyplot as plt
        plt.close("all")

    def test_mean_chart_has_real_heights_units_zero_baseline_and_counts(self):
        for index in range(2):
            m = load(index)
            summary = m.summarize(m.load_rows())
            before = copy.deepcopy(summary)
            fig = m.make_chart(summary)
            ax = fig.axes[0]
            self.assertEqual([p.get_height() for p in ax.patches], [3, 8, 6])
            self.assertEqual(ax.get_ylim()[0], 0)
            self.assertEqual(ax.get_ylabel(), "Mean trips per record")
            self.assertEqual(ax.get_xlabel(), "Synthetic collection site")
            self.assertEqual(ax.get_title(), "Mean recorded trips by site")
            self.assertEqual([t.get_text() for t in ax.texts], ["3 (n=2)", "8 (n=1)", "6 (n=3)"])
            self.assertEqual(summary, before)

    def test_second_question_changes_metric_and_units(self):
        m = load()
        summary = m.summarize(m.load_rows())
        mean, total = m.make_chart(summary), m.make_chart(summary, "total")
        self.assertEqual([p.get_height() for p in mean.axes[0].patches], [3, 8, 6])
        self.assertEqual([p.get_height() for p in total.axes[0].patches], [6, 8, 18])
        self.assertEqual(total.axes[0].get_ylabel(), "Total recorded trips")
        self.assertEqual(total.axes[0].get_ylim()[0], 0)
        with self.assertRaises(ValueError): m.make_chart(summary, "median")

    def test_empty_chart_is_distinct_from_a_real_zero_measurement(self):
        m = load()
        empty = m.make_chart({}).axes[0]
        self.assertEqual(len(empty.patches), 0)
        self.assertIn("No records", [t.get_text() for t in empty.texts])
        zero = m.make_chart(m.summarize([dict(site="z", trips=0)])).axes[0]
        self.assertEqual(len(zero.patches), 1)
        self.assertEqual(zero.patches[0].get_height(), 0)
        self.assertIn("0 (n=1)", [t.get_text() for t in zero.texts])

    def test_redesign_keeps_values_while_correcting_encoding(self):
        m = load(1)
        summary = m.summarize(m.load_rows())
        before = copy.deepcopy(summary)
        weak, repaired = m.make_weak_chart(summary).axes[0], m.make_chart(summary).axes[0]
        self.assertEqual([p.get_height() for p in weak.patches], [p.get_height() for p in repaired.patches])
        self.assertEqual(weak.get_ylim(), (5, 9))
        self.assertEqual(repaired.get_ylim()[0], 0)
        self.assertEqual(weak.get_ylabel(), "")
        self.assertEqual(repaired.get_ylabel(), "Mean trips per record")
        self.assertEqual(summary, before)

    def test_real_entrypoints_save_inspectable_svg_outside_the_source_tree(self):
        for index, folder in enumerate(FOLDERS):
            for role in ["starter", "solution"]:
                with self.subTest(folder=folder, role=role), tempfile.TemporaryDirectory() as tmp:
                    output = Path(tmp) / "actual.svg"
                    result = subprocess.run([sys.executable, "-B", str(ROOT / folder / role / "main.py"),
                        "--output", str(output)], cwd=tmp, capture_output=True, text=True,
                        env={**os.environ, "MPLBACKEND": "Agg"}, timeout=40)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("west | 3 | 18 | 6.00", result.stdout)
                    self.assertEqual(output.exists(), role == "solution")
                    if role == "solution":
                        self.assertEqual(ET.fromstring(output.read_bytes()).tag, "{http://www.w3.org/2000/svg}svg")
                        self.assertGreater(output.stat().st_size, 10000)
                    else:
                        self.assertIn("TODO: make the labeled", result.stdout)
                    self.assertEqual(output.with_name("actual-weak.svg").exists(), index == 1)

    def test_real_notebook_entrypoint_ignores_kernel_cli_arguments(self):
        for index, folder in enumerate(FOLDERS):
            for role in ["starter", "solution"]:
                with self.subTest(folder=folder, role=role), tempfile.TemporaryDirectory() as tmp:
                    source = ROOT / folder / role
                    data = Path(tmp) / "data"
                    data.mkdir()
                    (data / "sample.csv").write_bytes((source / "data" / "sample.csv").read_bytes())
                    code = "import sys; sys.argv=['ipykernel_launcher','-f','kernel.json']; ns={'__name__':'__main__'}; exec(" + repr((source / "main.py").read_text()) + ",ns); assert len(ns['load_rows']())==6"
                    result = subprocess.run([sys.executable, "-B", "-c", code], cwd=tmp,
                        capture_output=True, text=True, env={**os.environ, "MPLBACKEND": "Agg"}, timeout=40)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("west | 3 | 18 | 6.00", result.stdout)
                    self.assertEqual((Path(tmp) / "chart.svg").exists(), role == "solution")
                    self.assertFalse((Path(tmp) / "-f").exists())


if __name__ == "__main__": unittest.main()
