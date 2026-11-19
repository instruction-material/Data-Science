# %%
"""Reproducible report from a bundled synthetic weekly-count dataset."""
import csv
import hashlib
from pathlib import Path
import platform
import sys

PROJECT_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_FILE = PROJECT_DIR / "data" / "sample.csv"
QUESTION = "What is the average recorded weekly trip count in this CSV?"
LIMITATION = "These synthetic practice weeks illustrate reporting; they describe no real traveler or population."


def load_rows(path=DATA_FILE):
    """Load nonnegative whole trip counts while retaining the week labels."""
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not {"week", "trips"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV requires week and trips columns")
        rows, seen = [], set()
        for record, row in enumerate(reader, start=2):
            week = row.get("week")
            if not isinstance(week, str) or not week.strip():
                raise ValueError(f"Record {record}: week is missing")
            if week in seen:
                raise ValueError(f"Record {record}: duplicate week")
            try:
                trips = int(row.get("trips"))
            except (TypeError, ValueError) as error:
                raise ValueError(f"Record {record}: trips must be a whole number") from error
            if trips < 0:
                raise ValueError(f"Record {record}: trips must be nonnegative")
            seen.add(week)
            rows.append({"week": week, "trips": trips})
        return rows


def analyze(rows, *, source="data/sample.csv"):
    """Keep the computed result separate from its Markdown representation."""
    count = len(rows)
    total = sum(row["trips"] for row in rows)
    return {"question": QUESTION, "source": source, "rows": [dict(row) for row in rows],
            "count": count, "total": total, "average": total / count if count else None,
            "limitation": LIMITATION}


def render_table(rows):
    lines = ["| Recorded week | Trips |", "| --- | ---: |"]
    for row in rows:
        week = row["week"].replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").replace("\r", " ")
        lines.append(f"| {week} | {row['trips']} |")
    return "\n".join(lines)


def reproducibility_appendix(path=DATA_FILE):
    """Describe the exact input bytes and the current interpreter."""
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    source = "data/sample.csv" if Path(path).resolve() == DATA_FILE.resolve() else str(Path(path))
    return ("## Reproducibility appendix\n"
            f"Input: {source} (UTF-8 CSV; week and trips columns).\n"
            f"Input SHA-256: {digest}\n"
            f"Python: {platform.python_version()}; dependencies: standard library only.\n"
            "Run from the role folder: python3 main.py\n"
            "A fresh process reloads the input; notebook cells run from the role folder "
            "or receive an explicit CSV path.")


def build_report(rows, *, include_appendix=False, input_path=DATA_FILE):
    """Return seven named report sections and optionally the exact-input appendix.

    Use analyze(rows) and render_table(rows). The Results section includes
    count, total, mean and its units. An empty mean stays undefined.
    Preserve the synthetic-data limitation and make the next question explicit.
    """
    raise NotImplementedError("TODO: build the reproducible mini report")


def main():
    try:
        text = build_report(load_rows(), include_appendix="--appendix" in sys.argv[1:])
        print(text)
    except NotImplementedError as error:
        print(str(error))


if __name__ == "__main__":
    main()
