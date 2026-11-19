# Compare Weekly Transit Rates

Open the project in the course IDE or run `python main.py` from this folder.
The default run reads `data/sample.csv`. Supply `--csv PATH` to use a file with the same columns.

The synthetic fixture includes weeks with different coverage. Compare the
totals with the rates. Weeks 1 and 2 each have 10 trips per covered day.
Week 3 has unavailable trips and zero covered days. Week 4 has nine
trips per covered day. Keep the original week order.

A covered week with zero trips is a measured zero. A missing period breaks
any line drawn between adjacent observed values. Extend the comparison
to a documented series with a consistent time unit.
