import argparse
import csv
from pathlib import Path

FIXTURE = Path(__file__).parent / "data" / "sample.csv"


def load_reports(path):
    reports = []
    keys = set()
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["route", "week", "trips", "days"]:
            raise ValueError("Expected the route,week,trips,days header")
        for line, row in enumerate(reader, 2):
            if len(row) != 4 or any(value is None for value in row.values()):
                raise ValueError(f"Malformed report on line {line}")
            route = row["route"].strip()
            week = row["week"].strip()
            key = (route, week)
            if not route or not week or key in keys:
                raise ValueError(f"Missing or repeated route-week on line {line}")
            keys.add(key)
            days = int(row["days"])
            trips = None if not row["trips"].strip() else int(row["trips"])
            if days < 0 or (trips is not None and trips < 0):
                raise ValueError(f"Negative observation on line {line}")
            if trips is not None and days > 0:
                reports.append({"route": route, "week": week, "trips": trips, "days": days})
    return reports



def compare_coverage(reports, minimum_days):
    """Return each route's (eligible reports before, eligible reports after, rate before, rate after)."""
    # TODO: Compare all measured reports with reports meeting minimum_days.
    # Use None when a filtered group has no coverage.
    return None


def display_rate(value):
    return "unavailable" if value is None else f"{value:.2f}"


def main():
    parser = argparse.ArgumentParser(description="Compare results under a coverage cutoff")
    parser.add_argument("--csv", type=Path, default=FIXTURE)
    parser.add_argument("--minimum-days", type=int, default=3)
    args = parser.parse_args()
    if args.minimum_days < 1:
        parser.error("minimum days must be positive")
    try:
        reports = load_reports(args.csv)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    comparison = compare_coverage(reports, args.minimum_days)
    if comparison is None:
        print("TODO: compare rates across coverage rules")
        return
    print(f"Minimum covered days per report: {args.minimum_days}")
    for route, (before_count, after_count, before, after) in comparison.items():
        print(
            f"{route}: {before_count} -> {after_count} reports, "
            f"{display_rate(before)} -> {display_rate(after)} trips/day"
        )


if __name__ == "__main__":
    main()
