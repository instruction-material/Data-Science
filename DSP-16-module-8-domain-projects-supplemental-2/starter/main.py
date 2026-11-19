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


def audit_reports(rows):
    """Return (accepted route-week keys, reason-to-count mapping)."""
    # TODO: Classify each row once using the rule order in the README.
    return None


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
