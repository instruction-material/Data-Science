import csv
from pathlib import Path


def load_values() -> list[int]:
	with Path("data/sample.csv").open() as handle:
		reader = csv.DictReader(handle)
		return [int(row["value"]) for row in reader]


def summarize(values: list[int]) -> dict[str, float]:
	total = sum(values)
	count = len(values)
	average = total / count if count else 0.0
	return {"count": count, "total": total, "average": average}


def main() -> None:
	print(summarize(load_values()))


if __name__ == "__main__":
	main()
