import csv
from pathlib import Path


def load_values() -> list[int]:
	with Path("data/sample.csv").open() as handle:
		reader = csv.DictReader(handle)
		return [int(row["value"]) for row in reader]


def summarize(values: list[int]) -> dict[str, float]:
	# TODO: compute count, total, and average.
	return {"count": 0, "total": 0, "average": 0.0}


def main() -> None:
	print(summarize(load_values()))


if __name__ == "__main__":
	main()
