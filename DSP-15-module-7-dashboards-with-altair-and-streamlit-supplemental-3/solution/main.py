import argparse
import csv
from pathlib import Path

SAMPLE = Path(__file__).parent / "data" / "sample.csv"


def load_observations(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["day", "room", "checkins"]:
            raise ValueError("Expected the day,room,checkins header")
        observations = []
        seen = set()
        for row in reader:
            if None in row or None in row.values():
                raise ValueError(f"Incorrect field count at line {reader.line_num}")
            day, room = row["day"].strip(), row["room"].strip()
            checkins = int(row["checkins"])
            key = day, room
            if not day or not room or key in seen or checkins < 0:
                raise ValueError(f"Invalid or repeated day and room at line {reader.line_num}")
            seen.add(key)
            observations.append({"day": day, "room": room, "checkins": checkins})
    return observations


def comparable_panels(rows, first_day, second_day):
    """Return filtered rows for each day and the upper limit of a shared scale."""
    first = [row for row in rows if row["day"] == first_day]
    second = [row for row in rows if row["day"] == second_day]
    upper_limit = max((row["checkins"] for row in rows), default=0) or 1
    return first, second, upper_limit


def main():
    parser = argparse.ArgumentParser(description="Compare two days on a common scale")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    parser.add_argument("--first", default="Monday")
    parser.add_argument("--second", default="Tuesday")
    args = parser.parse_args()
    try:
        comparison = comparable_panels(load_observations(args.csv), args.first, args.second)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if comparison is None:
        print("TODO: prepare two day views and a shared scale")
        return
    first, second, upper_limit = comparison
    print(f"Shared check-in scale: 0 to {upper_limit}")
    for day, selected in ((args.first, first), (args.second, second)):
        print(day)
        if not selected:
            print("No observations")
        for row in selected:
            print(f"{row['room']}: {row['checkins']} check-ins")


if __name__ == "__main__":
    main()
