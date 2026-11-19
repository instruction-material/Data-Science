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


def summarize(observations):
    """Return (phase, loans, hours, excluded rows, hourly rate) rows."""
    # TODO: Accumulate loans and hours only for measured rows, and count exclusions.
    return


def render_report(rows, source_name):
    lines = [
        "# Laptop loans before and after the pilot",
        "",
        f"Input: {source_name}. Each observation covers one reported phase-week.",
        "",
        "| Phase | Measured loans | Measured hours | Excluded rows | Loans per hour |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for phase, loans, hours, excluded, rate in rows:
        observed = "unavailable" if loans is None else loans
        lines.append(f"| {phase} | {observed} | {hours} | {excluded} | {format_rate(rate)} |")
    before = rows[0][-1]
    after = rows[1][-1]
    lines.append("")
    if before is None or after is None:
        lines.append("There is insufficient measured coverage for a phase comparison.")
    else:
        lines.append(f"After minus Before: {after - before:+.2f} observed loans per open hour.")
    lines.extend(("", "This observational comparison cannot establish what caused the change."))
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Create a reproducible laptop-loan report")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    parser.add_argument("--output", type=Path, default=Path("report.md"))
    args = parser.parse_args()
    try:
        rows = summarize(load_observations(args.csv))
        if rows is None:
            print("TODO: summarize both phases using the measured-hours denominator")
            return
        if args.csv.resolve() == args.output.resolve():
            raise ValueError("Choose an output path different from the input")
        report = render_report(rows, args.csv.name)
        args.output.write_text(report, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(report, end="")


if __name__ == "__main__":
    main()
