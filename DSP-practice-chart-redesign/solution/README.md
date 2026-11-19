# Redesign a Trip Comparison

Open the project in the course IDE or run `python main.py` from this folder.
The default run reads `data/sample.csv`. Supply `--csv PATH` to use a file with the same columns.

The synthetic fixture has 42 trips for A and 49 for B. Starting a bar at
40 makes its displayed lengths 2 and 9 units. The actual difference is
seven trips. Compare the reported clipped lengths with the redesign.

The console chart starts at zero. Round only bar lengths for display and
keep the actual counts in labels. Set the two counts equal and confirm the
bars and text summary show equality. Include the chart and its text summary
with the comparison.
