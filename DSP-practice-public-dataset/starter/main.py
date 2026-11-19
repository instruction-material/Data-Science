import argparse
import csv
from decimal import InvalidOperation
from pathlib import Path

SAMPLE = Path(__file__).parent / "data" / "sample.csv"


def load_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['country', 'year', 'life_expectancy_years']:
            raise ValueError("Expected this header: country,year,life_expectancy_years")
        rows = list(reader)
        if any(None in row or None in row.values() for row in rows):
            raise ValueError("A row has a different field count than the header")
        return rows


def summarize(rows, start_year, end_year):
    """Return (country, baseline, comparison) for countries with both observations."""
    # TODO: Use Decimal for values and match observations from both years.
    return


def main():
    parser = argparse.ArgumentParser(description="Compare life expectancy in two years")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    parser.add_argument("--start-year", type=int, default=2013)
    parser.add_argument("--year", type=int, default=2015)
    args = parser.parse_args()
    if args.year <= args.start_year:
        parser.error("The comparison year must come after the baseline year")
    try:
        summary = summarize(load_rows(args.csv), args.start_year, args.year)
    except (OSError, ValueError, InvalidOperation) as error:
        parser.error(str(error))
    if summary is None:
        print("TODO: group complete country-year comparisons")
        return
    if not summary:
        print(f"No countries have observations in both {args.start_year} and {args.year}.")
        return
    print(f"Country | {args.start_year} | {args.year} | Change (years)")
    for country, baseline, comparison in summary:
        print(f"{country} | {baseline:.1f} | {comparison:.1f} | {comparison - baseline:+.1f}")
    if len(summary) > 1:
        values = [comparison for _, _, comparison in summary]
        print(f"{args.year} gap between highest and lowest: {max(values) - min(values):.1f} years")


if __name__ == "__main__":
    main()
