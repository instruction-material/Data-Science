import argparse
import csv
import hashlib
import io
from pathlib import Path

SAMPLE = Path(__file__).parent / "data" / "sample.csv"
PHASES = ("Before", "After")


def load_observations(raw):
    with io.StringIO(raw.decode("utf-8"), newline="") as stream:
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


def changes(previous, revised):
    """Return human-readable field and row changes in phase-week order."""
    result = []
    for phase, week in sorted(previous.keys() | revised.keys()):
        key = phase, week
        if key not in previous:
            result.append(f"{phase} {week}: row added")
        elif key not in revised:
            result.append(f"{phase} {week}: row removed")
        else:
            for field, old, new in zip(("loans", "open hours"), previous[key], revised[key], strict=True):
                if old != new:
                    left = "unavailable" if old is None else old
                    right = "unavailable" if new is None else new
                    result.append(f"{phase} {week}: {field} {left} -> {right}")
    return result


def phase_rate(observations, phase):
    covered = [
        (loans, hours) for (row_phase, _), (loans, hours) in observations.items()
        if row_phase == phase and loans is not None and hours > 0
    ]
    if not covered:
        return None
    return sum(loans for loans, _ in covered) / sum(hours for _, hours in covered)


def main():
    parser = argparse.ArgumentParser(description="Trace a revision to the reported capstone result")
    parser.add_argument("--previous", type=Path, default=SAMPLE)
    parser.add_argument("--revised", type=Path, default=SAMPLE.with_name("corrected.csv"))
    args = parser.parse_args()
    try:
        snapshots = [(path, path.read_bytes()) for path in (args.previous, args.revised)]
        previous, revised = (load_observations(raw) for _, raw in snapshots)
        result = changes(previous, revised)
        if result is None:
            print("TODO: report the data changes by phase, week and field")
            return
        for path, raw in snapshots:
            print(f"{path.name} SHA-256: {hashlib.sha256(raw).hexdigest()}")
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(*(result or ["No record changes"]), sep="\n")
    for phase in PHASES:
        start = format_rate(phase_rate(previous, phase))
        end = format_rate(phase_rate(revised, phase))
        print(f"{phase}: {start} -> {end} loans/hour")


if __name__ == "__main__":
    main()
