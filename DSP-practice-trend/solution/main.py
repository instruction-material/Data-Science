import argparse
import csv
from pathlib import Path

SAMPLE = Path(__file__).parent / "data" / "sample.csv"


def load_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['week', 'trips', 'covered_days']:
            raise ValueError("Expected this header: week,trips,covered_days")
        rows = list(reader)
        if any(None in row or None in row.values() for row in rows):
            raise ValueError("A row has a different field count than the header")
        return rows


def compare_weeks(rows):
    """Return (week, trips, covered days, rate) with None for unavailable rates."""
    result = []
    seen = set()
    for row in rows:
        week = row["week"].strip()
        days = int(row["covered_days"])
        trips = int(row["trips"]) if row["trips"].strip() else None
        if not week or week in seen or days < 0 or (trips is not None and trips < 0):
            raise ValueError("Expected unique weeks and non-negative observations")
        seen.add(week)
        rate = trips / days if trips is not None and days else None
        result.append((week, trips, days, rate))
    return result


def main():
    parser = argparse.ArgumentParser(description="Compare trips per covered day")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    args = parser.parse_args()
    try:
        report = compare_weeks(load_rows(args.csv))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if report is None:
        print("TODO: calculate weekly rates without filling coverage gaps")
        return
    print("Week | Observed trips | Covered days | Trips per covered day")
    for week, trips, days, rate in report:
        count = "unavailable" if trips is None else str(trips)
        display_rate = "unavailable" if rate is None else f"{rate:.2f}"
        print(f"{week} | {count} | {days} | {display_rate}")


if __name__ == "__main__":
    main()
