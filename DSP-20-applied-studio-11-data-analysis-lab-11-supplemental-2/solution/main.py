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


def median(values: list[Number]) -> Number | None:
    """Find the middle of a sorted copy, averaging an even middle pair."""
    if not values:
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def modes(values: list[Number]) -> list[Number]:
    """Return every most-frequent value, in first-appearance order."""
    counts: dict[Number, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    highest = max(counts.values(), default=0)
    return [value for value, count in counts.items() if count == highest]


def summarize_distribution(values: list[Number]) -> dict[str, object]:
    """Keep mean, median and all tied modes visible together."""
    return {**summarize(values), "median": median(values), "modes": modes(values)}


if __name__ == "__main__":
    try:
        print(summarize_distribution(load_values()))
    except NotImplementedError as error:
        print(error)
