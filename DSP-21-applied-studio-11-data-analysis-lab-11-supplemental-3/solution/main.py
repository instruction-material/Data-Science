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
    """Report the measured rows separately from their interpretation."""
    summary = summarize(values)
    average = summary["average"]
    mean_text = f"{average:g}" if average is not None else "undefined (no rows)"
    return (f"Source: {filename}\n"
            f"Rows: {summary['count']}\n"
            f"Total: {summary['total']:g}\n"
            f"Mean: {mean_text}\n"
            "Caution: This describes the loaded rows; it does not establish a cause.")


if __name__ == "__main__":
    try:
        print(format_report(DATA_FILE.name, load_values()))
    except NotImplementedError as error:
        print(error)
