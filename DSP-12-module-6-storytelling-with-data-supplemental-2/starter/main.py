"""Tell the same booking story to two audiences."""

import argparse
import csv
import json
from fractions import Fraction
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


PERIODS = ("early", "late")


def load(path):
    rows = []
    for index, (period, booked, seats) in records(path, ["period", "booked", "seats"]):
        try:
            booked, seats = int(booked), int(seats)
        except ValueError:
            raise ValueError(f"Record {index} needs whole booked and seat counts") from None
        if period not in PERIODS or not 0 <= booked <= seats:
            raise ValueError(f"Record {index} needs a period and 0 <= booked <= seats")
        rows.append((period, booked, seats))
    return rows


def evidence(rows):
    """Total numerators and denominators before calculating each rate."""
    totals = {name: [0, 0] for name in PERIODS}
    for period, booked, seats in rows:
        totals[period][0] += booked
        totals[period][1] += seats
    return [
        {"period": name, "booked": booked, "seats": seats,
         "rate": Fraction(booked, seats) if seats else None}
        for name, (booked, seats) in totals.items()
    ]


def line(row):
    numerator = row["booked"]
    denominator = row["seats"]
    rate = row["rate"]
    share = "undefined booking share" if rate is None else f"{float(rate):.1%} booked"
    return f"{row['period']}: {numerator} of {denominator} seats booked ({share})"


def percentage_change(early, late):
    if early["rate"] is None or late["rate"] is None:
        return None
    return round(float(100 * (late["rate"] - early["rate"])), 2)


def captions(comparison):
    """Write two captions with the same numbers and different uses."""
    raise NotImplementedError("Complete captions before comparing results.")


def analyze(rows):
    return captions(evidence(rows))


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
