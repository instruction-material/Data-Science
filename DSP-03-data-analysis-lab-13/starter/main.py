# %%
"""Synthetic grouped-summary practice; Python standard library only."""
import csv
import math
from pathlib import Path
from statistics import median

DATA_FILE = Path(__file__).resolve().parent / "data" / "sample.csv"


def load_rows(path=DATA_FILE):
    """Read the required columns as original text; parsing happens in grouping."""
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not {"category", "value"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV requires category and value columns")
        return list(reader)


def summarize_groups(rows, *, normalize_labels=False):
    """Return sorted category -> count, total, average; preserve the original rows.

    First implement exact labels. The extension optionally uses strip/casefold.
    Reject blank categories and nonnumeric/nonfinite values with a row number.
    Return an empty dictionary for no rows; negative finite values are valid.
    """
    raise NotImplementedError("TODO: summarize values by category")


def main():
    try:
        print(summarize_groups(load_rows()))
    except NotImplementedError as error:
        print(str(error))


if __name__ == "__main__":
    main()
