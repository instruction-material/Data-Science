import argparse
import csv
from pathlib import Path

FIXTURE = Path(__file__).parent / "data" / "sample.csv"
REASONS = ("invalid", "missing trips", "no coverage", "duplicate")


def load_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["route", "week", "trips", "days"]:
            raise ValueError("Expected the route,week,trips,days header")
        return list(reader)


def rejection_reason(row, accepted_keys):
    if len(row) != 4 or any(value is None for value in row.values()):
        return "invalid"
    route = row["route"].strip()
    week = row["week"].strip()
    try:
        days = int(row["days"])
        trips = int(row["trips"]) if row["trips"].strip() else None
    except ValueError:
        return "invalid"
    if not route or not week or days < 0 or (trips is not None and trips < 0):
        return "invalid"
    if trips is None:
        return "missing trips"
    if days == 0:
        return "no coverage"
    if (route, week) in accepted_keys:
        return "duplicate"
    return None


def audit_reports(rows):
    accepted = []
    accepted_keys = set()
    rejected = dict.fromkeys(REASONS, 0)
    for row in rows:
        reason = rejection_reason(row, accepted_keys)
        if reason is not None:
            rejected[reason] += 1
        else:
            key = (row["route"].strip(), row["week"].strip())
            accepted.append(key)
            accepted_keys.add(key)
    return accepted, rejected


def main():
    parser = argparse.ArgumentParser(description="Account for every route-week CSV row")
    parser.add_argument("--csv", type=Path, default=FIXTURE)
    args = parser.parse_args()
    try:
        rows = load_rows(args.csv)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    outcome = audit_reports(rows)
    if outcome is None:
        print("TODO: audit route-week rows")
        return
    accepted, rejected = outcome
    print(f"Input: {len(rows)}")
    print(f"Accepted: {len(accepted)}")
    for reason in REASONS:
        print(f"{reason}: {rejected[reason]}")


if __name__ == "__main__":
    main()
