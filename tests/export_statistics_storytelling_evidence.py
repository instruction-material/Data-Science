"""Retain the original outputs and every downloadable project file hash."""
import hashlib
import json
import runpy
import sys

from test_statistics_storytelling import FOLDERS, ROOT, program, stdout


def capture(directory, loaded):
    return {
        "stdout": stdout(loaded),
        "files": {
            path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(directory.rglob("*")) if path.is_file()
        },
    }


def main():
    groups = {}
    for folder in FOLDERS:
        groups[folder] = {
            role: capture(ROOT / folder / role, program(folder, role))
            for role in ("starter", "solution")
        }
    for title, starter, reference in (
        ("simple-stats", "DS1-Simple-Stats-Starter", "DS1-Simple-Stats"),
        ("mode-finder", "DS1-Mode-Starter", "DS1-Mode"),
    ):
        groups[title] = {}
        for role, folder in (("starter", starter), ("solution", reference)):
            directory = ROOT / folder
            groups[title][role] = capture(directory, runpy.run_path(str(directory / "main.py")))
    evidence = ROOT / "evidence" / "statistics-storytelling-native.json"
    evidence.parent.mkdir(exist_ok=True)
    evidence.write_text(json.dumps({"python": sys.version.split()[0], "groups": groups}, indent=2) + "\n")


if __name__ == "__main__":
    main()
