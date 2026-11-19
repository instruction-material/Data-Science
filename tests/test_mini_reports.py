"""Hand-checked report semantics, exact source evidence and fresh-process use."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ['DSP-05-data-analysis-lab-15', 'DSP-28-applied-studio-15-data-analysis-lab-15-supplemental-2']


def load(index=0, role='solution'):
    spec = importlib.util.spec_from_file_location('report_' + str(index) + role, ROOT / FOLDERS[index] / role / 'main.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MiniReportTests(unittest.TestCase):
    def test_exact_four_week_hand_case_and_seven_sections(self):
        m = load(); rows = m.load_rows(); result = m.analyze(rows)
        self.assertEqual((result['count'], result['total'], result['average']), (4, 28, 7))
        text = m.build_report(rows)
        sections = [line[3:] for line in text.splitlines() if line.startswith('## ')]
        self.assertEqual(sections, ['Question', 'Data source', 'Method', 'Results', 'Interpretation', 'Limitation', 'Next question'])
        for literal in ['| week-1 | 4 |', '| week-2 | 7 |', '| week-3 | 7 |', '| week-4 | 10 |', 'Recorded weeks: 4; total trips: 28; mean: 7.00 trips per recorded week.', 'synthetic', 'no real traveler or population']:
            self.assertIn(literal, text)

    def test_conversion_preserves_the_complete_core_report_and_input(self):
        core, conversion = load(), load(1)
        rows = conversion.load_rows(); before_rows = copy.deepcopy(rows)
        result = conversion.analyze(rows); before_result = copy.deepcopy(result)
        self.assertEqual(conversion.render_markdown(result), core.build_report(rows))
        self.assertEqual(rows, before_rows); self.assertEqual(result, before_result)

    def test_empty_and_zero_are_distinct(self):
        for index in range(2):
            m = load(index)
            empty = m.render_markdown(m.analyze([]))
            self.assertIn('Recorded weeks: 0; total trips: 0; mean: undefined (no recorded weeks).', empty)
            self.assertIn('| Recorded week | Trips |\n| --- | ---: |', empty)
            zero = m.render_markdown(m.analyze([dict(week='week-0', trips=0)]))
            self.assertIn('Recorded weeks: 1; total trips: 0; mean: 0.00 trips per recorded week.', zero)

    def test_record_validation_and_required_columns(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'case.csv'
            cases = [('week,trips\nw1,1\nw1,2\n', 'Record 3: duplicate week'),
                     ('week,trips\nw1,1\n ,2\n', 'Record 3: week is missing'),
                     ('week,trips\nw1,1\nw2,-1\n', 'Record 3: trips must be nonnegative'),
                     *[('week,trips\nw1,1\nw2,' + value + '\n', 'Record 3: trips must be a whole number') for value in ['2.5', '', 'NaN', 'inf', 'word']]]
            for index in range(2):
                m = load(index)
                for text, message in cases:
                    path.write_text(text)
                    with self.subTest(index=index, text=text), self.assertRaisesRegex(ValueError, message): m.load_rows(path)
                path.write_text('label,value\nw1,1\n')
                with self.assertRaisesRegex(ValueError, 'week and trips'): m.load_rows(path)
                path.write_text('week,trips\n')
                self.assertEqual(m.load_rows(path), [])

    def test_appendix_hashes_actual_bytes_and_records_current_runtime(self):
        m = load()
        appendix = m.reproducibility_appendix()
        self.assertIn(hashlib.sha256(m.DATA_FILE.read_bytes()).hexdigest(), appendix)
        self.assertIn('Python: ' + m.platform.python_version(), appendix)
        self.assertIn('dependencies: standard library only', appendix)
        self.assertIn('python3 main.py', appendix)
        self.assertEqual(m.build_report(m.load_rows(), include_appendix=True), m.build_report(m.load_rows()) + '\n\n' + appendix)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'other.csv'; path.write_bytes(b'week,trips\nw1,0\n')
            before = m.reproducibility_appendix(path)
            self.assertIn(hashlib.sha256(path.read_bytes()).hexdigest(), before)
            self.assertIn('Input: ' + str(path), before)
            self.assertIn('Synthetic CSV: ' + str(path), m.build_report(m.load_rows(path), input_path=path))
            path.write_bytes(b'week,trips\nw1,1\n')
            self.assertNotEqual(before, m.reproducibility_appendix(path))

    def test_saved_markdown_matches_the_printed_result(self):
        m = load(1); report = m.render_markdown(m.analyze(m.load_rows()))
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'report.md'
            m.write_report(path, report + '\n\n')
            self.assertEqual(path.read_bytes(), (report + '\n').encode('utf-8'))
            actual = subprocess.run([sys.executable, '-I', '-B', str(ROOT / FOLDERS[1] / 'solution/main.py'), str(path)], cwd=temporary, capture_output=True, text=True, timeout=10)
            self.assertEqual((actual.returncode, actual.stderr), (0, ''))
            self.assertEqual(actual.stdout.encode(), path.read_bytes())
            self.assertEqual(actual.stdout, report + '\n')

    def test_actual_four_entrypoints_rerun_outside_the_project(self):
        with tempfile.TemporaryDirectory() as temporary:
            for folder in FOLDERS:
                for role in ['starter', 'solution']:
                    args = [sys.executable, '-I', '-B', str(ROOT / folder / role / 'main.py')]
                    runs = [subprocess.run(args, cwd=temporary, capture_output=True, text=True, timeout=10) for _ in range(2)]
                    self.assertTrue(all(r.returncode == 0 and not r.stderr for r in runs))
                    self.assertEqual(runs[0].stdout, runs[1].stdout)
                    self.assertIn('TODO:' if role == 'starter' else 'mean: 7.00 trips per recorded week.', runs[0].stdout)

    def test_notebook_cells_without_file_global_load_bundled_rows(self):
        for folder in FOLDERS:
            for role in ['starter', 'solution']:
                directory = ROOT / folder / role
                code = "from pathlib import Path; scope={'__name__':'report_notebook'}; exec(compile(Path('main.py').read_text(), '<cell>', 'exec'), scope); print(scope['analyze'](scope['load_rows']())['average'])"
                actual = subprocess.run([sys.executable, '-I', '-B', '-c', code], cwd=directory, capture_output=True, text=True, timeout=10)
                self.assertEqual((actual.returncode, actual.stdout, actual.stderr), (0, '7.0\n', ''))


if __name__ == '__main__': unittest.main()
