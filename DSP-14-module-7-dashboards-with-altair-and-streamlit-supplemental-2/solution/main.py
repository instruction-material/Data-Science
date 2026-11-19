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


def filter_observations(rows, day, room):
    """Return rows satisfying both selections. All rooms disables the room filter."""
    return [
        row for row in rows if row["day"] == day
        and (room == "All rooms" or row["room"] == room)
    ]


def main():
    parser = argparse.ArgumentParser(description="Filter room observations by day and room")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    parser.add_argument("--day", default="Monday")
    parser.add_argument("--room", default="All rooms")
    args = parser.parse_args()
    try:
        selected = filter_observations(load_observations(args.csv), args.day, args.room)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if selected is None:
        print("TODO: apply the day and room filters together")
        return
    if not selected:
        print(f"No observation for {args.room} on {args.day}.")
        return
    print(f"{args.day}: {sum(row['checkins'] for row in selected)} observed check-ins")
    for row in selected:
        print(f"{row['room']}: {row['checkins']} check-ins")


if __name__ == "__main__":
    main()
