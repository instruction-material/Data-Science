"""Retain source hashes plus both role entrypoints for the exact native run."""
import hashlib
import json
import sys

import pandas

from test_tabular_cases import PACKS, ROOT, load, output


def main():
    receipt = {"python": sys.version.split()[0], "pandas": pandas.__version__, "packs": {}}
    for folder in PACKS:
        pair = {}
        for role in ("starter", "solution"):
            directory = ROOT / folder / role
            files = ("README.md", "main.py", "data/sample.csv")
            pair[role] = {
                "files": {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in files},
                "stdout": output(load(folder, role)),
            }
        receipt["packs"][folder] = pair
    path = ROOT / "evidence" / "tabular-cases-native.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
