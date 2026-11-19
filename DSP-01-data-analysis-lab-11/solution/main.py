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


def extended_summary(values: list[Number]) -> dict[str, Number | None]:
    """Optional minimum/maximum/range comparison; preserve the input."""
    minimum = min(values) if values else None
    maximum = max(values) if values else None
    return {**summarize(values), "minimum": minimum, "maximum": maximum,
            "range": maximum - minimum if values else None}


if __name__ == "__main__":
    try:
        print(summarize(load_values()))
    except NotImplementedError as error:
        print(error)
