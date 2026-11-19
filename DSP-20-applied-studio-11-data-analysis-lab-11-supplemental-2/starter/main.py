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
    # Work from a sorted copy; average both middle values for an even count.
    raise NotImplementedError("TODO: find the median without changing the input.")


def modes(values: list[Number]) -> list[Number]:
    # Return every tied mode in first-appearance order; [] has no modes.
    raise NotImplementedError("TODO: count occurrences and return all tied modes.")


def summarize_distribution(values: list[Number]) -> dict[str, object]:
    return {**summarize(values), "median": median(values), "modes": modes(values)}


if __name__ == "__main__":
    try:
        print(summarize_distribution(load_values()))
    except NotImplementedError as error:
        print(error)
