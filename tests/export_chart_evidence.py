"""Retain native figures and numeric observations for independent source review."""
import importlib.util
import json
from pathlib import Path
import platform

import matplotlib
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence"
OUT.mkdir(exist_ok=True)
observations = []
for folder, metric in [("DSP-04-data-analysis-lab-14", "mean"),
                       ("DSP-04-data-analysis-lab-14", "total"),
                       ("DSP-26-applied-studio-14-data-analysis-lab-14-supplemental-2", "mean")]:
    spec = importlib.util.spec_from_file_location("chart", ROOT / folder / "solution" / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    summary = module.summarize(module.load_rows())
    fig = module.make_chart(summary, metric)
    name = ("redesign" if "supplemental" in folder else "core") + "-" + metric
    for extension in ["svg", "png"]:
        fig.savefig(OUT / (name + "." + extension), bbox_inches="tight")
    ax = fig.axes[0]
    observations.append(dict(name=name, source=folder, summary=summary,
        heights=[p.get_height() for p in ax.patches], baseline=ax.get_ylim()[0],
        title=ax.get_title(), xlabel=ax.get_xlabel(), ylabel=ax.get_ylabel(),
        annotations=[t.get_text() for t in ax.texts]))
    if "supplemental" in folder:
        weak = module.make_weak_chart(summary)
        for extension in ["svg", "png"]:
            weak.savefig(OUT / ("deliberately-weak." + extension), bbox_inches="tight")
    plt.close("all")
(OUT / "chart-observations.json").write_text(json.dumps(dict(
    python=platform.python_version(), matplotlib=matplotlib.__version__,
    observations=observations), indent=2) + "\n", encoding="utf-8")
