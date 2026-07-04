import csv
from pathlib import Path

#################
#   CONSTANTS   #
#################

DATA_FILE = Path("data/sample.csv")
VALUE_FIELD = "value"
COUNT_FIELD = "count"
TOTAL_FIELD = "total"
AVERAGE_FIELD = "average"
EMPTY_AVERAGE = 0.0


#################
#   FUNCTIONS   #
#################

def load_values() -> list[int]:
	"""Load integer values from the sample CSV file"""
	# Read the named value column from each CSV row
	with DATA_FILE.open(newline="") as handle:
		reader = csv.DictReader(handle)
		return [int(row[VALUE_FIELD]) for row in reader]


def summarize(values: list[int]) -> dict[str, float]:
	"""Summarize the count total and average for the provided values"""
	total = sum(values)
	count = len(values)

	# Avoid division by zero when a dataset has no rows
	average = total / count if count else EMPTY_AVERAGE

	return {
		COUNT_FIELD: count,
		TOTAL_FIELD: total,
		AVERAGE_FIELD: average,
	}


def main() -> None:
	"""Print the summary for the sample dataset"""
	print(summarize(load_values()))


if __name__ == "__main__":
	main()
