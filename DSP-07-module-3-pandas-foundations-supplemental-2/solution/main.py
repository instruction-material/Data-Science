"""Filter and sort trip records."""

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


COLUMNS = ["trip_id", "site", "trips", "hours"]
BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DEFAULT_INPUT = BASE / "data" / "sample.csv"


def load_frame(path):
    """Read the four-column, complete dataset used in this module."""
    types = {"trip_id": "string", "site": "string", "trips": "Int64", "hours": "Int64"}
    frame = pd.read_csv(path, dtype=types)
    if not isinstance(frame.index, pd.RangeIndex):
        raise ValueError("A CSV record has more fields than the header")
    if frame.columns.tolist() != COLUMNS:
        raise ValueError("Expected columns trip_id, site, trips, hours in that order")
    if frame.isna().any().any() or frame["trip_id"].duplicated().any():
        raise ValueError("Expected complete rows and unique trip IDs")
    if (frame[["trips", "hours"]] < 0).any().any():
        raise ValueError("Expected nonnegative trips and hours")
    return frame


def select_trips(frame, minimum):
    """Keep inclusive matches and sort highest trips first, then by ID."""
    columns = ["trip_id", "site", "trips"]
    return frame.loc[frame["trips"].ge(minimum), columns].sort_values(
        ["trips", "trip_id"], ascending=[False, True]
    )



def analyze(frame):
    selected = select_trips(frame, minimum=6)
    return {"minimum": 6, "rows": selected.to_dict(orient="records")}


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
