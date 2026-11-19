"""Reproduce a descriptive trip summary from an explicitly identified input."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DEFAULT_INPUT = BASE / "data" / "sample.csv"


def read_values(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        if not fields or len(fields) != len(set(fields)) or not {"site", "trips"}.issubset(fields):
            raise ValueError("CSV needs unique site and trips columns")
        values = []
        for record, row in enumerate(reader, 2):
            if None in row or not str(row.get("site") or "").strip():
                raise ValueError(f"Record {record}: a nonblank site is required")
            count = str(row.get("trips") or "").strip()
            if re.fullmatch(r"[0-9]+", count) is None:
                raise ValueError(f"Record {record}: trips must be a nonnegative whole number")
            values.append(int(count))
        return values


def summarize(values):
    raise NotImplementedError('TODO: complete summarize')


def format_summary(summary):
    mean = summary["mean_trips_per_record"]
    displayed = "undefined" if mean is None else f"{mean:.2f}"
    return (f"Records: {summary['records']}\n"
            f"Total trips: {summary['total_trips']}\n"
            f"Mean trips per record: {displayed}")


def main(argv=()):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args(list(argv))
    try:
        summary = summarize(read_values(args.input))
        print(format_summary(summary))
    except NotImplementedError as error:
        print(error)


if __name__ == "__main__":
    main(sys.argv[1:] if "__file__" in globals() and "ipykernel" not in sys.modules else ())
