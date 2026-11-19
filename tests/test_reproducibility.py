"""Semantic contracts for fresh runs, explicit inputs and traceable reports."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import runpy
import signal
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ['DSP-09-module-2-notebook-workflow-and-reproducibility',
           'DSP-05-module-2-notebook-workflow-and-reproducibility-supplemental-2',
           'DSP-06-module-2-notebook-workflow-and-reproducibility-supplemental-3']
CSV = b'site,trips\nnorth,2\nnorth,4\nsouth,8\nwest,0\nwest,6\nwest,12\n'
EXPECTED = 'Records: 6\nTotal trips: 32\nMean trips per record: 5.33\n'


def execute(command, cwd):
    stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    row = dict(parentTask='data-science-reproducibility-source', parentPid=os.getpid(),
               cwd=str(cwd), command=command, startTime=stamp(), timeoutSeconds=15)
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
    row['pid'] = child.pid
    try:
        stdout, stderr = child.communicate(timeout=15)
        row.update(stdout=stdout.decode(), stderr=stderr.decode(), exitCode=child.returncode,
                   childProcessGroupCleanup='not needed')
    except BaseException:
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.communicate(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.communicate()
        row.update(exitCode=child.returncode, childProcessGroupCleanup='terminated child process group')
        raise
    finally:
        row['endTime'] = stamp()
        destination = ROOT / 'evidence' / 'foundations-processes.jsonl'
        destination.parent.mkdir(exist_ok=True)
        with destination.open('a') as handle:
            handle.write(json.dumps(row) + '\n')
    return row


class ReproducibilityContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = [runpy.run_path(str(ROOT / folder / 'solution/main.py')) for folder in FOLDERS]

    def run_program(self, index, role, args=()):
        with tempfile.TemporaryDirectory(prefix='foundation-contract-') as cwd:
            result = execute([sys.executable, '-I', '-B', str(ROOT / FOLDERS[index] / role / 'main.py'), *args], cwd)
            report = Path(cwd) / 'outputs/report.json'
            if report.exists():
                result['report'] = json.loads(report.read_text())
        return result

    def test_six_real_entrypoints_run_from_another_working_directory(self):
        for index in range(3):
            for role in ['starter', 'solution']:
                with self.subTest(index=index, role=role):
                    row = self.run_program(index, role)
                    self.assertEqual(row['exitCode'], 0)
                    self.assertEqual(row['stderr'], '')
                    if role == 'starter':
                        self.assertIn('TODO: complete', row['stdout'])
                    else:
                        self.assertEqual(row['stdout'], EXPECTED + ('Saved outputs/report.json\n' if index == 2 else ''))

    def test_changed_input_is_explicit_and_does_not_replace_the_default(self):
        with tempfile.TemporaryDirectory() as temporary:
            changed = Path(temporary) / 'changed.csv'
            changed.write_bytes(CSV.replace(b'west,12', b'west,18'))
            for index in range(3):
                row = self.run_program(index, 'solution', ['--input', str(changed)])
                self.assertEqual(row['exitCode'], 0)
                self.assertTrue(row['stdout'].startswith('Records: 6\nTotal trips: 38\nMean trips per record: 6.33\n'))
                self.assertEqual((ROOT / FOLDERS[index] / 'solution/data/sample.csv').read_bytes(), CSV)

    def test_empty_and_zero_records_have_different_means(self):
        for data, expected in [(b'site,trips\n', 'Records: 0\nTotal trips: 0\nMean trips per record: undefined\n'),
                               (b'site,trips\nwest,0\n', 'Records: 1\nTotal trips: 0\nMean trips per record: 0.00\n')]:
            with tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / 'edge.csv'; path.write_bytes(data)
                for index in range(3):
                    row = self.run_program(index, 'solution', ['--input', str(path)])
                    self.assertEqual(row['exitCode'], 0)
                    self.assertEqual(row['stderr'], '')
                    self.assertTrue(row['stdout'].startswith(expected))

    def test_bad_columns_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'bad.csv'
            for data in [b'', b'value\n3\n', b'site,trips,trips\nwest,2,4\n']:
                path.write_bytes(data)
                for module in self.modules:
                    with self.assertRaisesRegex(ValueError, 'unique site and trips'):
                        module['read_values'](path)

    def test_invalid_observations_name_the_record(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'bad.csv'
            for row in ['west,-1', 'west,1.5', 'west,NaN', 'west,', ',3', 'west,1,extra']:
                path.write_text('site,trips\n' + row + '\n')
                for module in self.modules:
                    with self.assertRaisesRegex(ValueError, 'Record 2:'):
                        module['read_values'](path)

    def test_bom_and_crlf_inputs_keep_the_recorded_zero(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'windows.csv'; path.write_bytes(b'\xef\xbb\xbfsite,trips\r\nwest,0\r\nwest,6\r\n')
            for module in self.modules:
                self.assertEqual(module['read_values'](path), [0, 6])

    def test_summary_preserves_input_and_accepts_an_iterator(self):
        for module in self.modules:
            values = [2, 4, 8, 0, 6, 12]
            before = values.copy()
            observed = module['summarize'](values)
            self.assertEqual(values, before)
            self.assertEqual(observed, {'records': 6, 'total_trips': 32, 'mean_trips_per_record': 32 / 6})
            self.assertEqual(module['summarize'](iter(values)), observed)

    def test_counts_reject_boolean_fraction_and_negative_values(self):
        for module in self.modules:
            for invalid in [[True], [2.5], [-1], ['3']]:
                with self.assertRaisesRegex(ValueError, 'nonnegative integers'):
                    module['summarize'](invalid)

    def test_numeric_overflow_is_an_explicit_input_limitation(self):
        for module in self.modules:
            with self.assertRaisesRegex(ValueError, 'numeric range'):
                module['summarize']([2 ** 2000])

    def test_report_identifies_exact_input_and_repeats_identically(self):
        writer = self.modules[2]['write_report']
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'sample.csv'; source.write_bytes(CSV)
            summary = self.modules[2]['summarize']([2, 4, 8, 0, 6, 12])
            first, second = Path(temporary) / 'a.json', Path(temporary) / 'nested/b.json'
            writer(first, summary, source); writer(second, summary, source)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            data = json.loads(first.read_text())
            self.assertEqual(data, {'input_filename': 'sample.csv', 'input_sha256': hashlib.sha256(CSV).hexdigest(),
                                    'unit': 'trips per record', **summary})
            self.assertEqual(source.read_bytes(), CSV)

    def test_report_preserves_null_and_measured_zero(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'input.csv'; output = Path(temporary) / 'report.json'
            for values, raw, mean in [([], b'site,trips\n', None), ([0], b'site,trips\nwest,0\n', 0.0)]:
                path.write_bytes(raw)
                self.modules[2]['write_report'](output, self.modules[2]['summarize'](values), path)
                self.assertEqual(json.loads(output.read_text())['mean_trips_per_record'], mean)

    def test_report_cannot_overwrite_its_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'input.csv'; source.write_bytes(CSV)
            with self.assertRaisesRegex(ValueError, 'differ from'):
                self.modules[2]['write_report'](source, self.modules[2]['summarize']([2]), source)
            self.assertEqual(source.read_bytes(), CSV)

    def test_notebook_kernel_arguments_are_not_parsed_as_script_flags(self):
        code = 'import runpy,sys,types;sys.modules["ipykernel"]=types.ModuleType("ipykernel");sys.argv=["kernel","-f","connection.json"];runpy.run_path({path},run_name="__main__")'
        for index in range(3):
            with tempfile.TemporaryDirectory() as temporary:
                row = execute([sys.executable, '-I', '-B', '-c', code.format(path=repr(str(ROOT / FOLDERS[index] / 'solution/main.py')))], temporary)
                self.assertEqual(row['exitCode'], 0, row)
                self.assertTrue(row['stdout'].startswith(EXPECTED))

    def test_missing_input_is_reported_without_falling_back(self):
        for index in range(3):
            row = self.run_program(index, 'solution', ['--input', 'absent.csv'])
            self.assertNotEqual(row['exitCode'], 0)
            self.assertIn('FileNotFoundError', row['stderr'])
            self.assertNotIn('Records: 6', row['stdout'])


if __name__ == '__main__':
    unittest.main()
