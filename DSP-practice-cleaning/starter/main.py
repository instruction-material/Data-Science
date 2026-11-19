import argparse
import csv
import sys
from pathlib import Path

SAMPLE = Path(__file__).parent / "data" / "sample.csv"


def load_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['record_id', 'station', 'riders']:
            raise ValueError("Expected this header: record_id,station,riders")
        return [(reader.line_num, row) for row in reader]


def classify(rows):
    """Return accepted tuples and (line number, ID, reason) rejected tuples."""
    # TODO: Assign each input row exactly one outcome.
    return


def print_csv(headers, rows):
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Classify station observations")
    parser.add_argument("--csv", type=Path, default=SAMPLE)
    args = parser.parse_args()
    try:
        rows = load_rows(args.csv)
        result = classify(rows)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if result is None:
        print("TODO: classify every station row")
        return
    accepted, rejected = result
    print(f"{len(accepted)} accepted + {len(rejected)} rejected = {len(rows)} input rows")
    print(f"Accepted riders: {sum(row[2] for row in accepted)}")
    print("\nClean CSV")
    print_csv(["record_id", "station", "riders"], accepted)
    print("\nRejection log CSV")
    print_csv(["line", "record_id", "reason"], rejected)


if __name__ == "__main__":
    main()
