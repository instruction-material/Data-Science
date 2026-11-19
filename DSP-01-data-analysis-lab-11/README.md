# CSV summaries and sanity checks

The supplied `data/sample.csv` is a synthetic four-row dataset: 4, 8, 11, 17.
Its `value` column contains finite numbers. This pack uses the standard library.

Complete `summarize(values)` in the starter. Return count, total and average.
The sample has count 4, total 40 and average 10. Empty input has count 0,
total 0 and average `None`, because no rows supplied a measured mean.
Check `[6]` and `[-2, 2, 6]` as well as the sample. Preserve the input list.

For the optional Min-Max and Outlier Extension, complete `extended_summary`.
Add minimum, maximum and range, using `None` for all three when empty.
Compare `[4, 8, 11, 17]` with `[4, 8, 11, 17, 100]`: the means are 10 and 28,
and the ranges are 13 and 96. A surprising value needs context before removal.

Run `python3 main.py` inside the chosen starter or solution folder, or pass
its path to Python from elsewhere. The bundled CSV resolves beside the source.
`load_values(path)` also accepts a custom CSV with a `value` header.
The completed reference returns the same contract as the starter assignment.
This small synthetic sample supports hand checks, not claims about a population.
