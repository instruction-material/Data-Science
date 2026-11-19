import csv
import math
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "sample.csv"


def load_rows(path: str | Path = DATA_FILE) -> list[dict[str, str | None]]:
    """Load rows without silently changing their original cell text."""
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not {"label", "value"} <= set(reader.fieldnames):
            raise ValueError("CSV requires label and value columns.")
        return list(reader)


def clean_rows(rows: list[dict[str, str | None]], *,
               repair_whitespace: bool = False) -> dict[str, object]:
    """Validate synthetic nonnegative measurements and retain rejection evidence.

    Each rejected row receives its first applicable reason. Optional whitespace
    repair affects numeric cells only and counts successfully accepted rows.
    The caller's row dictionaries and original cell text remain unchanged.
    """
    # Classify missing, whitespace, nonnumeric, nonfinite and negative values.
    # Keep original row numbers and cell text in the rejection evidence.
    # Complete the default policy before adding optional whitespace repair.
    raise NotImplementedError("TODO: clean the rows and explain each rejection.")


if __name__ == "__main__":
    try:
        print(clean_rows(load_rows()))
    except NotImplementedError as error:
        print(error)
