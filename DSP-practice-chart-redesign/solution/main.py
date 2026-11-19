import argparse
import csv
from pathlib import Path

SAMPLE = Path(__file__).parent / "data" / "sample.csv"


def load_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['service', 'observed_trips']:
            raise ValueError("Expected this header: service,observed_trips")
        rows = list(reader)
        if any(None in row or None in row.values() for row in rows):
            raise ValueError("A row has a different field count than the header")
        return rows


def draw_bars(observations, width=49):
    """Return (service, count, bar) tuples with a zero baseline and shared scale."""
    maximum = max(count for _, count in observations)
    return [
        (service, count, "#" * round(count * width / maximum) if maximum else "")
        for service, count in observations
    ]


def main():
    parser = argparse.ArgumentParser(description="Redesign a two-service trip chart")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    parser.add_argument("--draft-baseline", type=int, default=40)
    args = parser.parse_args()
    try:
        observations = [
            (row["service"].strip(), int(row["observed_trips"]))
            for row in load_rows(args.csv)
        ]
        if len(observations) != 2 or len({name for name, _ in observations}) != 2:
            raise ValueError("Supply observations for two different services")
        if any(not name or count < 0 for name, count in observations):
            raise ValueError("Supply non-empty service names and non-negative trip counts")
        if args.draft_baseline < 0:
            raise ValueError("The baseline must be non-negative")
        bars = draw_bars(observations)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if bars is None:
        print("TODO: draw both bars from a common zero baseline")
        return
    print(f"Draft lengths from {args.draft_baseline} trips (clipped at zero)")
    for service, count in observations:
        print(f"{service}: {max(0, count - args.draft_baseline)} trips above baseline")
    print("\nObserved trips by service (baseline: 0)")
    for service, count, bar in bars:
        print(f"{service} |{bar} {count} trips")
    first, second = bars
    print(f"Text summary: {first[0]} has {first[1]} trips; {second[0]} has {second[1]}. "
          f"The difference is {abs(first[1] - second[1])} trips.")


if __name__ == "__main__":
    main()
