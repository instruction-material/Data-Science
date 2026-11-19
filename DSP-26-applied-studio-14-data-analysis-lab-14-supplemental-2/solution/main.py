# %%
"""Compare recorded trips at three synthetic collection sites."""
import argparse
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_FILE = PROJECT_DIR / "data" / "sample.csv"
LIMITATION = "Synthetic practice records; unequal record counts describe no real site or population."


def load_rows(path=DATA_FILE):
    """Read site labels and nonnegative whole trip counts; preserve label spelling."""
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not {"site", "trips"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV requires site and trips columns")
        rows = []
        for record, row in enumerate(reader, start=2):
            site = row.get("site")
            if not isinstance(site, str) or not site.strip():
                raise ValueError(f"Record {record}: site is missing")
            try:
                trips = int(row.get("trips"))
            except (TypeError, ValueError) as error:
                raise ValueError(f"Record {record}: trips must be a whole number") from error
            if trips < 0:
                raise ValueError(f"Record {record}: trips must be nonnegative")
            rows.append({"site": site, "trips": trips})
        return rows


def summarize(rows):
    """Return sorted groups with their actual denominator; leave input rows intact."""
    groups = {}
    for record, row in enumerate(rows, start=2):
        site, trips = row.get("site"), row.get("trips")
        if not isinstance(site, str) or not site.strip():
            raise ValueError(f"Record {record}: site is missing")
        if isinstance(trips, bool) or not isinstance(trips, int) or trips < 0:
            raise ValueError(f"Record {record}: trips must be a nonnegative whole number")
        group = groups.setdefault(site, {"count": 0, "total": 0})
        group["count"] += 1
        group["total"] += trips
    return {site: {**groups[site], "mean": groups[site]["total"] / groups[site]["count"]}
            for site in sorted(groups)}


def describe(summary, metric="mean"):
    if metric not in {"mean", "total"}:
        raise ValueError("metric must be mean or total")
    lines = ["Synthetic recorded trips by site", "site | records | total trips | mean trips per record"]
    lines.extend(f"{site} | {g['count']} | {g['total']} | {g['mean']:.2f}" for site, g in summary.items())
    lines.append("Question: " + ("What mean trip count was recorded at each site?" if metric == "mean" else "How many total trips were recorded at each site?"))
    lines.append(LIMITATION)
    return "\n".join(lines)


def make_weak_chart(summary):
    """A deliberately weak comparison for critique; the input numbers stay intact."""
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")
    ax.bar(list(summary), [group["mean"] for group in summary.values()], color="#868686")
    ax.set_title("Deliberately weak comparison")
    ax.set_ylim(5, 9)
    return fig


def make_chart(summary, metric="mean"):
    """Use a zero-baseline bar chart with units and visible group denominators."""
    if metric not in {"mean", "total"}:
        raise ValueError("metric must be mean or total")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")
    sites = list(summary)
    heights = [summary[site][metric] for site in sites]
    bars = ax.bar(sites, heights, color="#316879")
    ax.set_title("Mean recorded trips by site" if metric == "mean" else "Total recorded trips by site")
    ax.set_xlabel("Synthetic collection site")
    ax.set_ylabel("Mean trips per record" if metric == "mean" else "Total recorded trips")
    ax.set_ylim(bottom=0, top=max(heights, default=0) * 1.25 or 1)
    if sites:
        ax.bar_label(bars, labels=[f"{height:g} (n={summary[site]['count']})" for site, height in zip(sites, heights)], padding=4)
    else:
        ax.text(0.5, 0.5, "No records", transform=ax.transAxes, ha="center")
    fig.text(0.02, -0.025, "Synthetic practice data; n = recorded rows at each site.", fontsize=9)
    return fig


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chart synthetic trip records without changing their data.")
    parser.add_argument("--input", type=Path, default=DATA_FILE)
    parser.add_argument("--output", type=Path, default=PROJECT_DIR / "chart.svg")
    parser.add_argument("--metric", choices=["mean"], default="mean")
    args = parser.parse_args(argv)
    summary = summarize(load_rows(args.input))
    print(describe(summary, args.metric))
    weak = make_weak_chart(summary)
    weak_path = args.output.with_name(args.output.stem + "-weak.svg")
    weak.savefig(weak_path, format="svg", bbox_inches="tight")
    print("Weak comparison saved as " + str(weak_path))
    try:
        fig = make_chart(summary, args.metric)
    except NotImplementedError as error:
        print(str(error))
        return None
    fig.savefig(args.output, format="svg", bbox_inches="tight")
    print("Chart saved as " + str(args.output))
    return fig


if __name__ == "__main__":
    main(None if "__file__" in globals() else [])
