"""Compare pooled and within-session correlation."""

import argparse
import csv
import json
from math import isfinite
from statistics import correlation
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DEFAULT = BASE / "data" / "sample.csv"


def records(path, expected_columns):
    with open(path, encoding="utf-8-sig", newline="") as stream:
        rows = csv.reader(stream)
        if next(rows, []) != expected_columns:
            raise ValueError("Expected CSV fields: " + ", ".join(expected_columns))
        for index, row in enumerate(rows, 1):
            if len(row) != len(expected_columns):
                raise ValueError(f"Record {index} has an unexpected number of fields")
            yield index, row


def load(path):
    rows = []
    for index, (session, temperature, visits) in records(
        path, ["session", "temperature_c", "visits"]
    ):
        try:
            point = (session, float(temperature), int(visits))
        except ValueError:
            raise ValueError(f"Record {index} needs numeric temperature and whole visits") from None
        if not session or not isfinite(point[1]) or point[2] < 0:
            raise ValueError(f"Record {index} has an invalid session, temperature or visit count")
        rows.append(point)
    return rows


def measure(points):
    """Return the count and rounded Pearson r or an undefined r."""
    if len(points) < 2:
        return {"pairs": len(points), "r": None}
    xs, ys = zip(*points)
    if min(xs) == max(xs) or min(ys) == max(ys):
        return {"pairs": len(points), "r": None}
    return {"pairs": len(points), "r": round(correlation(xs, ys), 3)}


def split_sessions(rows):
    """Measure the pooled rows and each distinct session separately."""
    raise NotImplementedError("Complete split_sessions before comparing results.")


def analyze(rows):
    return split_sessions(rows)


def main(argv=()):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT)
    args = parser.parse_args(list(argv))
    try:
        report = analyze(load(args.input))
    except NotImplementedError as error:
        print(error)
        return
    print(json.dumps(report, allow_nan=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:] if "__file__" in globals() and "ipykernel" not in sys.modules else ())
