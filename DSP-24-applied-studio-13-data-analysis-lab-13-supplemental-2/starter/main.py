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
    """Group finite numeric values without changing any input dictionary.

    Labels stay exact by default. Optional normalization strips padding and
    uses casefold only when the source says those labels identify one group.
    Missing/blank categories and nonnumeric/nonfinite values raise ValueError
    with the CSV record number. Negative values are valid in this example.
    """
    buckets = {}
    for record, row in enumerate(rows, start=2):
        label = row.get("category")
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"Record {record}: category is missing")
        original_value = row.get("value")
        try:
            value = float(original_value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Record {record}: value is not numeric") from error
        if not math.isfinite(value):
            raise ValueError(f"Record {record}: value is not finite")
        key = label.strip().casefold() if normalize_labels else label
        buckets.setdefault(key, []).append(value)
    summaries = {}
    for label in sorted(buckets):
        values = buckets[label]
        total = sum(values)
        summaries[label] = {"count": len(values), "total": total,
                            "average": total / len(values)}
    return summaries


def render_table(summaries):
    """Return Markdown Category/Count/Total/Mean; retain headers when empty.

    Use two decimals for total/mean and escape label backslashes/pipes.
    """
    raise NotImplementedError("TODO: display the grouped summary table")


def interpretation(summaries):
    """Expose the denominator and retain the synthetic-data interpretation limit."""
    count = sum(summary["count"] for summary in summaries.values())
    small = sum(summary["count"] < 2 for summary in summaries.values())
    return (f"{count} rows across {len(summaries)} groups; {small} groups have fewer than two rows. "
            "These synthetic measurements illustrate grouping and do not establish a population difference.")


def main():
    try:
        summary = summarize_groups(load_rows(), normalize_labels=True)
        print(render_table(summary))
        print(interpretation(summary))
    except NotImplementedError as error:
        print(str(error))


if __name__ == "__main__":
    main()
