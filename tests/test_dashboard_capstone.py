"""Hand cases and real native entrypoints for filters, CSV exports and scope evidence."""
import copy
import csv
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ['DSP-06-data-analysis-lab-16',
           'DSP-31-applied-studio-16-data-analysis-lab-16-supplemental-3',
           'DSP-07-data-analysis-lab-17']


def load(index=0, role='solution'):
    spec = importlib.util.spec_from_file_location('dashboard_' + str(index) + role,
                                                 ROOT / FOLDERS[index] / role / 'main.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DashboardCapstoneTests(unittest.TestCase):
    def test_all_default_rows_and_group_denominators(self):
        for index in range(3):
            m = load(index)
            self.assertEqual(m.summarize(m.load_rows()), dict(count=6, total=32, mean=32/6))
        self.assertEqual(load().summarize(load().select_rows(load().load_rows(), 'west')),
                         dict(count=3, total=18, mean=6))

    def test_filters_combine_and_restore_the_original_input(self):
        for index in [0, 1]:
            m = load(index); rows = m.load_rows(); before = copy.deepcopy(rows)
            self.assertEqual([r['trips'] for r in m.select_rows(rows, 'west', 5)], [6, 12])
            self.assertEqual([r['trips'] for r in m.select_rows(rows, 'west', 0)], [0, 6, 12])
            self.assertEqual(m.select_rows(rows, 'west', 13), [])
            self.assertEqual(m.select_rows(rows), before)
            selected = m.select_rows(rows, 'west'); selected[0]['trips'] = 99
            self.assertEqual(rows, before)
            self.assertEqual(m.select_rows(rows, 'West'), [])

    def test_empty_observed_zero_and_one_record_keep_distinct_states(self):
        m = load()
        self.assertEqual(m.summarize([]), dict(count=0, total=0, mean=None))
        self.assertIn('No matching records; no measured mean.', m.render_summary([], 'missing'))
        zero = m.render_summary([dict(site='west', trips=0)], 'west')
        self.assertIn('Mean trips per record: 0.00', zero)
        self.assertIn('Records: 1', zero)
        self.assertIn('One record only', zero)
        self.assertIn(m.LIMITATION, zero)

    def test_invalid_controls_do_not_silently_change_the_selection(self):
        for index in [0, 1]:
            m = load(index)
            for minimum in [-1, 1.5, '5', True, float('nan')]:
                with self.subTest(minimum=minimum), self.assertRaisesRegex(ValueError, 'minimum'):
                    m.select_rows(m.load_rows(), minimum=minimum)
            for site in ['', ' ', 1, True]:
                with self.subTest(site=site), self.assertRaisesRegex(ValueError, 'site'):
                    m.select_rows(m.load_rows(), site=site)

    def test_loader_reports_record_and_schema_errors_in_all_six_roles(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'input.csv'
            cases = [('label,value\nx,1\n', 'site and trips'),
                     ('site,trips\nx,1\n,2\n', 'Record 3: site'),
                     *[('site,trips\nx,1\ny,' + value + '\n', 'Record 3: trips')
                       for value in ['-1', '1.5', '', 'NaN', 'word']]]
            for index in range(3):
                for role in ['starter', 'solution']:
                    m = load(index, role)
                    for text, message in cases:
                        path.write_text(text)
                        with self.subTest(index=index, role=role, text=text), self.assertRaisesRegex(ValueError, message):
                            m.load_rows(path)

    def test_direct_counts_are_validated_before_any_summary(self):
        for index in range(3):
            m = load(index)
            for value in [True, -1, 1.5, '3', None, float('inf')]:
                rows = [dict(site='x', trips=value)]
                with self.assertRaisesRegex(ValueError, 'Record 2: trips'): m.summarize(rows)

    def test_csv_export_records_selection_schema_and_exact_repeatable_bytes(self):
        m = load(1); rows = m.load_rows(); before = copy.deepcopy(rows)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'report.csv'
            record = m.write_summary(rows, path, 'west', 5)
            self.assertEqual(record, dict(site_filter='west', minimum_trips=5, records=2,
                                         total_trips=18, mean_trips_per_record='9.00', state='ready'))
            expected = (b'site_filter,minimum_trips,records,total_trips,mean_trips_per_record,state\r\n'
                        b'west,5,2,18,9.00,ready\r\n')
            self.assertEqual(path.read_bytes(), expected)
            m.write_summary(rows, path, 'west', 5)
            self.assertEqual(path.read_bytes(), expected)
            self.assertEqual(rows, before)

    def test_csv_empty_zero_unicode_and_changed_selection_round_trip(self):
        m = load(1)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'report.csv'
            for rows, site, expected in [([], 'missing', ('0', '0', '', 'no matching records')),
                                         ([dict(site='café,港', trips=0)], 'café,港', ('1', '0', '0.00', 'one record only')),
                                         (m.load_rows(), 'south', ('1', '8', '8.00', 'one record only'))]:
                m.write_summary(rows, path, site)
                with path.open(newline='', encoding='utf-8') as handle:
                    reader = csv.DictReader(handle); actual = next(reader)
                    self.assertEqual(reader.fieldnames, m.EXPORT_FIELDS)
                    self.assertIsNone(next(reader, None))
                self.assertEqual(actual['site_filter'], site)
                self.assertEqual(tuple(actual[k] for k in ['records', 'total_trips', 'mean_trips_per_record', 'state']), expected)

    def test_capstone_retains_group_evidence_and_original_rows(self):
        m = load(2); rows = m.load_rows(); before = copy.deepcopy(rows)
        expected = dict(north=dict(count=2, total=6, mean=3),
                        south=dict(count=1, total=8, mean=8), west=dict(count=3, total=18, mean=6))
        self.assertEqual(m.analyze(rows), dict(groups=expected, maximum_mean_sites=['south']))
        self.assertEqual(m.analyze(list(reversed(rows))), m.analyze(rows))
        self.assertEqual(rows, before)

    def test_capstone_empty_zero_and_exact_ties(self):
        m = load(2)
        self.assertEqual(m.analyze([]), dict(groups={}, maximum_mean_sites=[]))
        self.assertEqual(m.analyze([dict(site='a', trips=0)])['maximum_mean_sites'], ['a'])
        self.assertEqual(m.analyze([dict(site='b', trips=3), dict(site='a', trips=2),
                                   dict(site='a', trips=4)])['maximum_mean_sites'], ['a', 'b'])

    def test_capstone_uses_exact_ratios_before_rounded_display(self):
        m = load(2)
        # Both display as 1.00, but 1001/1000 is greater than 1.
        rows = [dict(site='a', trips=1)] * 1000 + [dict(site='b', trips=1)] * 999 + [dict(site='b', trips=2)]
        self.assertEqual(m.analyze(rows)['maximum_mean_sites'], ['b'])
        # Float conversion loses this one-unit distinction; the winner remains exact.
        rows = [dict(site='a', trips=2**53), dict(site='b', trips=2**53+1)]
        self.assertEqual(m.analyze(rows)['maximum_mean_sites'], ['b'])

    def test_starters_expose_their_distinct_unfinished_functions(self):
        for index, function, args in [(0, 'select_rows', ([],)), (1, 'write_summary', ([], 'unused.csv')), (2, 'analyze', ([],))]:
            m = load(index, 'starter')
            with self.assertRaisesRegex(NotImplementedError, 'TODO: complete ' + function): getattr(m, function)(*args)

    def test_actual_six_entrypoints_run_outside_the_project(self):
        with tempfile.TemporaryDirectory() as temporary:
            for index, folder in enumerate(FOLDERS):
                for role in ['starter', 'solution']:
                    args = [sys.executable, '-I', '-B', str(ROOT / folder / role / 'main.py')]
                    if index == 1: args += ['--output', str(Path(temporary) / 'result.csv')]
                    actual = subprocess.run(args, input='west\nmissing\nall\nquit\n', cwd=temporary,
                                            capture_output=True, text=True, timeout=15)
                    self.assertEqual((actual.returncode, actual.stderr), (0, ''), actual.stderr)
                    if role == 'starter': self.assertIn('TODO: complete', actual.stdout)
                    elif index == 0:
                        self.assertGreaterEqual(actual.stdout.count('Records: 6'), 2)
                        self.assertIn('Records: 3\nTotal trips: 18\nMean trips per record: 6.00', actual.stdout)
                        self.assertIn('No matching records', actual.stdout)
                    elif index == 1:
                        self.assertIn('Saved result.csv', actual.stdout)
                        self.assertTrue((Path(temporary) / 'result.csv').is_file())
                    else: self.assertIn('Recorded maximum mean sites: south', actual.stdout)

    def test_notebook_cells_ignore_kernel_arguments_for_all_six_roles(self):
        with tempfile.TemporaryDirectory() as temporary:
            for index, folder in enumerate(FOLDERS):
                for role in ['starter', 'solution']:
                    original = ROOT / folder / role
                    path = Path(temporary) / (str(index) + role); (path / 'data').mkdir(parents=True)
                    (path / 'data/sample.csv').write_bytes((original / 'data/sample.csv').read_bytes())
                    code = original.joinpath('main.py').read_text()
                    script = "import sys; sys.argv=['kernel','-f','connection.json']; ns={'__name__':'__main__'}; exec(" + repr(code) + ",ns)"
                    actual = subprocess.run([sys.executable, '-I', '-B', '-c', script], input='quit\n', cwd=path,
                                            capture_output=True, text=True, timeout=15)
                    self.assertEqual((actual.returncode, actual.stderr), (0, ''), actual.stderr)


if __name__ == '__main__': unittest.main()
