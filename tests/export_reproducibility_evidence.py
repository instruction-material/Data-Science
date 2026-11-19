"""Retain original native entrypoint output and CSV bytes for independent review."""
from pathlib import Path
import base64
import datetime
import hashlib
import json
import os
import platform
import signal
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
folders = ['DSP-09-module-2-notebook-workflow-and-reproducibility', 'DSP-05-module-2-notebook-workflow-and-reproducibility-supplemental-2', 'DSP-06-module-2-notebook-workflow-and-reproducibility-supplemental-3']
results = []
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
for index, folder in enumerate(folders):
    for role in ['starter', 'solution']:
        source = ROOT / folder / role
        with tempfile.TemporaryDirectory(prefix='dashboard-native-') as temporary:
            output = Path(temporary) / 'summary.json'
            command = [sys.executable, '-I', '-B', str(source / 'main.py')]
            if index == 2: command += ['--output', str(output)]
            row = dict(parentTask='data-science-foundations-reproducibility-source', parentPid=os.getpid(),
                       folder=folder, role=role, command=command, cwd=temporary,
                       startTime=stamp(), timeoutSeconds=15)
            child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, start_new_session=True, text=True)
            row['pid'] = child.pid
            try:
                stdout, stderr = child.communicate('', timeout=15)
                row.update(stdout=stdout, stderr=stderr, exitCode=child.returncode,
                           childProcessGroupCleanup='not needed')
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGTERM)
                try: child.communicate(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL); child.communicate()
                row.update(exitCode=124, childProcessGroupCleanup='terminated child process group')
                raise
            finally:
                row['endTime'] = stamp()
            assert child.returncode == 0 and stderr == '', row
            row['sourceFiles'] = {p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
            if output.exists():
                data = output.read_bytes()
                row['report'] = dict(base64=base64.b64encode(data).decode(), sha256=hashlib.sha256(data).hexdigest(),
                                  bytes=len(data), text=data.decode())
                report = json.loads(data)
                expected = dict(input_filename='sample.csv', input_sha256=hashlib.sha256((source/'data/sample.csv').read_bytes()).hexdigest(), unit='trips per record', records=6, total_trips=32, mean_trips_per_record=32/6)
                assert report == expected
            assert ('TODO: complete' in stdout) == (role == 'starter')
            if role == 'solution': assert stdout.startswith('Records: 6\nTotal trips: 32\nMean trips per record: 5.33\n')
            results.append(row)
proof = dict(at=stamp(), pythonVersion=platform.python_version(),
             sourceCommit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
             complete=True, actualEntrypoints=len(results), results=results,
             sourceQualificationOnly=True, applicationAccepted=False, wholeCourseAccepted=False)
destination = ROOT / 'evidence/foundations-reproducibility-native.json'
destination.parent.mkdir(exist_ok=True)
destination.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(dict(complete=True, actualEntrypoints=len(results), pythonVersion=platform.python_version())))
