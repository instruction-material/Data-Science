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
    values = []
    rejected = []
    repaired = 0
    for row_number, row in enumerate(rows, start=2):
        original = row.get("value")
        reason = None
        number = None
        text = "" if original is None else original
        stripped = text.strip()
        if not stripped:
            reason = "missing"
        elif text != stripped and not repair_whitespace:
            reason = "surrounding whitespace"
        else:
            try:
                number = float(stripped)
            except ValueError:
                reason = "not numeric"
            else:
                if not math.isfinite(number):
                    reason = "not finite"
                elif number < 0:
                    reason = "negative"
        if reason is not None:
            rejected.append({"row": row_number, "label": row.get("label"),
                             "value": original, "reason": reason})
        else:
            values.append(number)
            if text != stripped:
                repaired += 1
    return {
        "values": values,
        "report": {"rows_loaded": len(rows), "rows_accepted": len(values),
                   "rows_rejected": len(rejected), "rows_repaired": repaired},
        "rejected_rows": rejected,
    }


if __name__ == "__main__":
    try:
        print(clean_rows(load_rows()))
    except NotImplementedError as error:
        print(error)
