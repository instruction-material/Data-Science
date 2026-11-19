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


def analyze(rows):
    """Return inspectable group evidence and all exact maximum-mean ties."""
    validate_rows(rows)
    groups = {}
    for row in rows:
        group = groups.setdefault(row["site"], {"count": 0, "total": 0})
        group["count"] += 1
        group["total"] += row["trips"]
    groups = {site: {**groups[site], "mean": groups[site]["total"] / groups[site]["count"]}
              for site in sorted(groups)}
    winners = []
    for site, group in groups.items():
        if not winners:
            winners = [site]
            continue
        best = groups[winners[0]]
        # Cross multiplication compares exact ratios before display rounding.
        left, right = group["total"] * best["count"], best["total"] * group["count"]
        if left > right:
            winners = [site]
        elif left == right:
            winners.append(site)
    return {"groups": groups, "maximum_mean_sites": winners}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Prove a narrow synthetic CSV-to-evidence capstone path.")
    parser.add_argument("--input", type=Path, default=DATA_FILE)
    args = parser.parse_args(argv)
    try:
        evidence = analyze(load_rows(args.input))
    except NotImplementedError as error:
        print(str(error))
        return
    print("Question: Which site's recorded rows have the largest mean trip count?")
    print("site | records | total trips | mean trips per record")
    for site, group in evidence["groups"].items():
        print(f"{site} | {group['count']} | {group['total']} | {group['mean']:.2f}")
    if evidence["maximum_mean_sites"]:
        print("Recorded maximum mean sites: " + ", ".join(evidence["maximum_mean_sites"]))
    else:
        print("No records; no measured mean or winning site.")
    print(LIMITATION)


if __name__ == "__main__":
    main(None if "__file__" in globals() else [])
