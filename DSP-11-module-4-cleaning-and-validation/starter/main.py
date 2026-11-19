"""Classify and account for dirty records."""

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


COLUMNS = ["trip_id", "site", "trips", "hours"]
BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DEFAULT_INPUT = BASE / "data" / "sample.csv"


SITES = {"east", "north", "south", "west"}


def load_frame(path):
    """Preserve raw fields so blanks and malformed strings remain distinguishable."""
    frame = pd.read_csv(path, dtype="string", keep_default_na=False)
    if not isinstance(frame.index, pd.RangeIndex):
        raise ValueError("A CSV record has more fields than the header")
    if frame.columns.tolist() != COLUMNS:
        raise ValueError("Expected columns trip_id, site, trips, hours in that order")
    return frame


def prepare_rows(raw):
    """Normalize declared labels and parse whole numbers without changing raw data."""
    rows = raw.copy()
    rows.insert(0, "source_record", range(1, len(rows) + 1))
    rows["site"] = raw["site"].str.strip().str.lower()
    for column in ("trips", "hours"):
        text = raw[column].str.strip()
        whole = text.str.fullmatch(r"-?[0-9]{1,9}")
        rows[column] = pd.to_numeric(text.where(whole), errors="coerce").astype("Int64")
    return rows


def mark_duplicates(rows, reasons):
    """Hold every conflicting valid row and retain the first identical valid row."""
    candidates = rows.loc[reasons.eq("accepted")]
    conflicts = candidates.groupby("trip_id")[["site", "trips", "hours"]].transform("nunique")
    conflicting = conflicts.gt(1).any(axis=1)
    reasons.loc[conflicting[conflicting].index] = "conflicting_id"
    comparable = candidates.loc[~conflicting]
    repeated = comparable.duplicated(subset="trip_id", keep="first")
    reasons.loc[repeated[repeated].index] = "duplicate"
    return reasons


def validation_reasons(raw, rows, *, repair_labels):
    """Assign one reason per row using the documented priority order."""
    # TODO: Classify ID, site, trips and hours in order. Distinguish missing, malformed and out-of-range values. Allow trips from 0 to 1000 and hours from 0 to 24.
    raise NotImplementedError("Complete validation_reasons before comparing results.")


def clean(raw, *, repair_labels=True):
    rows = prepare_rows(raw)
    reasons = validation_reasons(raw, rows, repair_labels=repair_labels)
    reasons = mark_duplicates(rows, reasons)
    accepted = reasons.eq("accepted")
    audit = rows[["source_record", "trip_id"]].assign(
        status=reasons,
        label_repaired=accepted & raw["site"].ne(rows["site"]),
    )
    return rows.loc[accepted, ["source_record", *COLUMNS]], audit


def describe(accepted, audit):
    return {
        "loaded": int(len(audit)),
        "accepted": int(len(accepted)),
        "total_trips": int(accepted["trips"].sum()),
        "repaired_labels": int(audit["label_repaired"].sum()),
        "outcomes": {str(reason): int(count) for reason, count in audit["status"].value_counts().sort_index().items()},
        "accepted_ids": accepted["trip_id"].tolist(),
    }


def analyze(raw):
    accepted, audit = clean(raw)
    return {"summary": describe(accepted, audit), "audit": audit.to_dict(orient="records")}


def main(argv=()):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args(list(argv))
    try:
        result = analyze(load_frame(args.input))
    except NotImplementedError as error:
        print(error)
        return
    print(json.dumps(result, allow_nan=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:] if "__file__" in globals() and "ipykernel" not in sys.modules else ())
