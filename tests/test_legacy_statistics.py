"""Known-answer checks for the original statistics reference programs."""
import contextlib
import io
from pathlib import Path
import runpy
import statistics
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LegacyStatisticsContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.programs = {}
        for folder in ("DS1-Mode", "DS1-Simple-Stats"):
            with contextlib.redirect_stdout(io.StringIO()):
                cls.programs[folder] = runpy.run_path(str(ROOT / folder / "main.py"))

    def test_original_samples_match_their_downloadable_starters(self):
        pairs = {"DS1-Simple-Stats": "DS1-Simple-Stats-Starter", "DS1-Mode": "DS1-Mode-Starter"}
        for reference, student in pairs.items():
            starter = runpy.run_path(str(ROOT / student / "main.py"))
            solution = self.programs[reference]
            for key in ("data1", "data2", "data3"):
                self.assertEqual(starter[key], solution[key], (reference, key))
            self.assertEqual(len(solution["data3"]), 11)
            self.assertEqual(solution["my_sum"](solution["data3"]), 595)
            self.assertEqual(solution["median"](solution["data3"]), 56)

    def test_medians_for_unsorted_odd_even_negative_and_repeated_values(self):
        for folder, program in self.programs.items():
            for values in ([3, 1, 2], [4, 1, 3, 2], [-5, -1, -9],
                           [8], [2, 2, 7, 2], [3.5, 1.5], []):
                with self.subTest(folder=folder, values=values):
                    expected = statistics.median(values) if values else None
                    self.assertEqual(program["median"](values), expected)

    def test_median_preserves_the_callers_original_order(self):
        for folder, program in self.programs.items():
            values = [9, 1, 4, 2]
            with self.subTest(folder=folder):
                program["median"](values)
                self.assertEqual(values, [9, 1, 4, 2])

    def test_ranges_include_empty_singleton_and_negative_inputs(self):
        for folder, program in self.programs.items():
            for values, expected in (([], None), ([7], 0),
                                     ([-9, -2, -5], 7), ([3, 1, 8], 7)):
                with self.subTest(folder=folder, values=values):
                    self.assertEqual(program["my_range"](values), expected)

    def test_mode_reports_all_ties_and_handles_an_empty_input(self):
        mode = self.programs["DS1-Mode"]["mode"]
        self.assertEqual(mode([2, 1, 2, 1, 3]), [2, 1])
        self.assertEqual(mode([4, 4, 2]), [4])
        self.assertEqual(mode([]), [])


if __name__ == "__main__":
    unittest.main()
