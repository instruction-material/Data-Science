import argparse
import csv
from pathlib import Path

DATA = Path(__file__).parent / "data"
DEFAULT = [DATA / name for name in ('empty.csv', 'zero.csv')]


def describe(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["value"]:
            raise ValueError("Expected one column named value")
        values = []
        for row in reader:
            if None in row or row["value"] is None:
                raise ValueError(f"Expected one value at line {reader.line_num}")
            values.append(int(row["value"]))
    count = len(values)
    total = sum(values)
    mean = f"{total / count:.2f}" if count else "undefined"
    print(f"Records: {count}")
    print(f"Total trips: {total}")
    print(f"Mean trips per record: {mean}")


def main():
    parser = argparse.ArgumentParser(description="Checks for a reproducible setup")
    parser.add_argument("--csv", nargs="+", type=Path, default=DEFAULT)
    args = parser.parse_args()
    for path in args.csv:
        if len(args.csv) > 1:
            print(path.stem)
        try:
            describe(path)
        except (OSError, ValueError) as error:
            parser.error(str(error))


if __name__ == "__main__":
    main()
