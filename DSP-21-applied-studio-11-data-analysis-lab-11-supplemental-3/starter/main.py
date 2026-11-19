import csv
from pathlib import Path

Number = int | float
DATA_FILE = Path(__file__).resolve().parent / "data" / "sample.csv"


def load_values(path: str | Path = DATA_FILE) -> list[float]:
    """Read the named numeric column from a well-formed CSV."""
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [float(row["value"]) for row in csv.DictReader(handle)]


def summarize(values: list[Number]) -> dict[str, Number | None]:
    """Describe the supplied values; an empty sample has no mean."""
    count = len(values)
    total = sum(values)
    return {"count": count, "total": total,
            "average": total / count if count else None}


def format_report(filename: str, values: list[Number]) -> str:
    # Include source, rows, total, mean and one interpretation limit.
    # An empty dataset has an undefined mean, rather than a measured zero.
    raise NotImplementedError("TODO: format a readable summary report.")


if __name__ == "__main__":
    try:
        print(format_report(DATA_FILE.name, load_values()))
    except NotImplementedError as error:
        print(error)
