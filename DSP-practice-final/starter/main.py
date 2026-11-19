import argparse
import csv
from pathlib import Path

SAMPLE = Path(__file__).parent / "data" / "sample.csv"


def load_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['route', 'week', 'trips', 'days']:
            raise ValueError("Expected this header: route,week,trips,days")
        rows = list(reader)
        if any(None in row or None in row.values() for row in rows):
            raise ValueError("A row has a different field count than the header")
        return rows


def build_views(rows):
    """Return route summaries and weekly coverage rows for the same observations."""
    # TODO: Build both views from the same validated rows and track measured days.
    return


def main():
    parser = argparse.ArgumentParser(description="Report transit rates and their coverage")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    args = parser.parse_args()
    try:
        views = build_views(load_rows(args.csv))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if views is None:
        print("TODO: create route rates and an independent coverage view")
        return
    summaries, coverage = views
    print("Observed rate by route")
    print("Route | Observed trips | Measured days | Trips per measured day")
    for route, trips, days, rate in summaries:
        count = "unavailable" if trips is None else str(trips)
        display_rate = "unavailable" if rate is None else f"{rate:.2f}"
        print(f"{route} | {count} | {days} | {display_rate}")
    print("\nCoverage by route and week")
    print("Route | Week | Reported days | Trip measurement")
    for route, week, days, status in coverage:
        print(f"{route} | {week} | {days} | {status}")


if __name__ == "__main__":
    main()
