# %%
"""Use recorded synthetic trip counts to produce inspectable evidence."""
import argparse
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_FILE = PROJECT_DIR / "data" / "sample.csv"
LIMITATION = "Synthetic practice records; these results establish no real-world or causal ranking."


def validate_rows(rows):
    for record, row in enumerate(rows, start=2):
        if not isinstance(row.get("site"), str) or not row["site"].strip():
            raise ValueError(f"Record {record}: site is missing")
        value = row.get("trips")
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"Record {record}: trips must be a nonnegative whole number")


def load_rows(path=DATA_FILE):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not {"site", "trips"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV requires site and trips columns")
        rows = []
        for record, row in enumerate(reader, start=2):
            try:
                trips = int(row.get("trips"))
            except (TypeError, ValueError) as error:
                raise ValueError(f"Record {record}: trips must be a whole number") from error
            rows.append({"site": row.get("site"), "trips": trips})
    validate_rows(rows)
    return rows


def summarize(rows):
    validate_rows(rows)
    count = len(rows)
    total = sum(row["trips"] for row in rows)
    return {"count": count, "total": total, "mean": total / count if count else None}


def select_rows(rows, site=None, minimum=None):
    """Select records for the current site; extend with an inclusive minimum in the optional activity."""
    raise NotImplementedError("TODO: complete select_rows")


def render_summary(rows, site=None, minimum=None):
    summary = summarize(select_rows(rows, site, minimum))
    lines = ["Selection: " + (site if site is not None else "all sites"),
             "Minimum trips: " + (str(minimum) if minimum is not None else "none"),
             f"Records: {summary['count']}", f"Total trips: {summary['total']}"]
    if summary["mean"] is None:
        lines.append("No matching records; no measured mean.")
    else:
        lines.append(f"Mean trips per record: {summary['mean']:.2f}")
        if summary["count"] == 1:
            lines.append("One record only; the selected evidence is limited.")
    lines.append(LIMITATION)
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect synthetic trip records with a repeated site filter.")
    parser.add_argument("--input", type=Path, default=DATA_FILE)
    args = parser.parse_args(argv)
    rows = load_rows(args.input)
    try:
        print(render_summary(rows))
    except NotImplementedError as error:
        print(str(error))
        return
    while True:
        try:
            choice = input("Site (all, a label or quit): ").strip()
        except EOFError:
            return
        if choice == "quit":
            return
        site = None if choice in {"", "all"} else choice
        print(render_summary(rows, site))


if __name__ == "__main__":
    main(None if "__file__" in globals() else [])
