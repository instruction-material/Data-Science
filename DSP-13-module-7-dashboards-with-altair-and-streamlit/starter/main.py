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


def summarize_day(rows, day):
    """Return rows for the day and the sum of their check-ins."""
    # TODO: Select rows for the day and calculate the total from exactly those rows.
    return


def main():
    parser = argparse.ArgumentParser(description="Summarize room check-ins by day")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    parser.add_argument("--day", default="Monday")
    args = parser.parse_args()
    try:
        result = summarize_day(load_observations(args.csv), args.day)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if result is None:
        print("TODO: select the day and calculate its total")
        return
    selected, total = result
    if not selected:
        print(f"No observations for {args.day}.")
        return
    print(f"{args.day}: {total} check-ins across {len(selected)} rooms")
    for row in selected:
        print(f"{row['room']}: {row['checkins']} check-ins")


if __name__ == "__main__":
    main()
