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


def summarize(reports, key):
    totals = {}
    for report in reports:
        trips, days = totals.get(report[key], (0, 0))
        totals[report[key]] = (trips + report["trips"], days + report["days"])
    return [(name, trips, days, trips / days) for name, (trips, days) in sorted(totals.items())]


def main():
    parser = argparse.ArgumentParser(description="Compare transit coverage by route and week")
    parser.add_argument("--csv", type=Path, default=FIXTURE)
    args = parser.parse_args()
    try:
        reports = load_reports(args.csv)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    route_rows = summarize(reports, "route")
    week_rows = summarize(reports, "week")
    if route_rows is None or week_rows is None:
        print("TODO: summarize measured reports by route and by week")
        return
    if not reports:
        print("No measured reports")
        return
    for heading, rows, unit in (("Routes", route_rows, "day"), ("Weeks", week_rows, "route-day")):
        print(heading)
        for name, trips, days, rate in rows:
            print(f"{name}: {trips} trips / {days} {unit}s = {rate:.2f} trips/{unit}")


if __name__ == "__main__":
    main()
