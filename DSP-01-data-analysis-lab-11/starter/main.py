import csv
from pathlib import Path

Number = int | float
DATA_FILE = Path(__file__).resolve().parent / "data" / "sample.csv"


def load_values(path: str | Path = DATA_FILE) -> list[float]:
    """Read the named numeric column from a well-formed CSV."""
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [float(row["value"]) for row in csv.DictReader(handle)]


def summarize(values: list[Number]) -> dict[str, Number | None]:
    # Empty input has count 0, total 0 and average None.
    raise NotImplementedError("TODO: compute count, total, and mean.")


def extended_summary(values: list[Number]) -> dict[str, Number | None]:
    # Optional extension: add minimum, maximum and range without changing values.
    raise NotImplementedError("TODO: add the optional minimum, maximum, and range.")


if __name__ == "__main__":
    try:
        print(summarize(load_values()))
    except NotImplementedError as error:
        print(error)
