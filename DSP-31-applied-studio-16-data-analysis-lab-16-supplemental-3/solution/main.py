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
    """Select from the original input; optional controls combine using AND."""
    validate_rows(rows)
    if site is not None and (not isinstance(site, str) or not site.strip()):
        raise ValueError("site must be a nonempty label or None")
    if minimum is not None and (isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 0):
        raise ValueError("minimum must be a nonnegative whole number or None")
    return [dict(row) for row in rows
            if (site is None or row["site"] == site)
            and (minimum is None or row["trips"] >= minimum)]


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


EXPORT_FIELDS = ["site_filter", "minimum_trips", "records", "total_trips", "mean_trips_per_record", "state"]


def write_summary(rows, output, site=None, minimum=None):
    """Save the current selection and its measured summary in UTF-8 CSV."""
    summary = summarize(select_rows(rows, site, minimum))
    record = {
        "site_filter": site if site is not None else "all",
        "minimum_trips": minimum if minimum is not None else "",
        "records": summary["count"], "total_trips": summary["total"],
        "mean_trips_per_record": f"{summary['mean']:.2f}" if summary["mean"] is not None else "",
        "state": "no matching records" if not summary["count"] else "one record only" if summary["count"] == 1 else "ready",
    }
    with Path(output).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPORT_FIELDS)
        writer.writeheader()
        writer.writerow(record)
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export the selected synthetic trip summary.")
    parser.add_argument("--input", type=Path, default=DATA_FILE)
    parser.add_argument("--site", default=None)
    parser.add_argument("--minimum", type=int, default=None)
    parser.add_argument("--output", type=Path, default=PROJECT_DIR / "filtered-summary.csv")
    args = parser.parse_args(argv)
    rows = load_rows(args.input)
    print(render_summary(rows, args.site, args.minimum))
    try:
        write_summary(rows, args.output, args.site, args.minimum)
    except NotImplementedError as error:
        print(str(error))
        return
    print("Saved " + args.output.name)


if __name__ == "__main__":
    main(None if "__file__" in globals() else [])
