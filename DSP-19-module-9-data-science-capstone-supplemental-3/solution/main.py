import argparse
import csv
from pathlib import Path

SAMPLE = Path(__file__).parent / "data" / "sample.csv"
PHASES = ("Before", "After")


def load_observations(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["phase", "week", "loans", "open_hours"]:
            raise ValueError("Expected phase,week,loans,open_hours")
        observations = {}
        for row in reader:
            if None in row or None in row.values():
                raise ValueError(f"Malformed record ending at line {reader.line_num}")
            phase = row["phase"].strip()
            week = row["week"].strip()
            key = phase, week
            if phase not in PHASES or not week or key in observations:
                raise ValueError(f"Unknown phase or missing/repeated week: {key}")
            loans = int(row["loans"]) if row["loans"].strip() else None
            hours = int(row["open_hours"])
            if (loans is not None and loans < 0) or hours < 0:
                raise ValueError(f"Negative observation: {key}")
            observations[key] = loans, hours
    return observations


def format_rate(rate):
    return "unavailable" if rate is None else f"{rate:.2f}"


def coverage_summary(observations, minimum_hours):
    """Return a tuple of retained rows, measured hours and rate for each phase."""
    result = {}
    for phase in PHASES:
        retained = [
            (loans, hours) for (row_phase, _), (loans, hours) in observations.items()
            if row_phase == phase and loans is not None and hours >= minimum_hours
        ]
        total_hours = sum(hours for _, hours in retained)
        rate = sum(loans for loans, _ in retained) / total_hours if total_hours else None
        result[phase] = len(retained), total_hours, rate
    return result


def main():
    parser = argparse.ArgumentParser(description="Compare a baseline with a stricter coverage rule")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    parser.add_argument("--minimum-hours", type=int, default=7)
    args = parser.parse_args()
    if args.minimum_hours < 1:
        parser.error("Minimum open hours must be at least one")
    try:
        observations = load_observations(args.csv)
        baseline = coverage_summary(observations, 1)
        filtered = coverage_summary(observations, args.minimum_hours)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if baseline is None or filtered is None:
        print("TODO: compare rates across coverage rules and report the remaining evidence")
        return
    print(f"Minimum open hours: 1 -> {args.minimum_hours}")
    print("Phase | Retained rows | Measured hours | Loans per hour")
    for phase in PHASES:
        n1, h1, r1 = baseline[phase]
        n2, h2, r2 = filtered[phase]
        print(f"{phase} | {n1} -> {n2} | {h1} -> {h2} | {format_rate(r1)} -> {format_rate(r2)}")


if __name__ == "__main__":
    main()
