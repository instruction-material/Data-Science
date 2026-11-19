# Tiny Capstone Prototype

This solution uses six generated synthetic `site,trips` records. A row is one nonnegative whole trip count. North has count 2, total 6 and mean 3; south has count 1, total 8 and mean 8; west has count 3, total 18 and mean 6. The all-data total is 32 across six rows.

Run `python main.py` with the Python standard library. The bundled input resolves beside the script even from another working directory. `--input PATH` selects another CSV with the same columns. Notebook cells use this role directory or receive an explicit CSV path; kernel arguments are excluded from the script parser.

Build sorted group evidence and identify every site tied for the largest recorded mean.

Keep observed zeros and leave the measured mean absent when no records remain. Preserve original input rows. A one-record comparison retains its count and limitation. These synthetic records establish no real-world or causal ranking.

`analyze(rows)` returns `groups` and `maximum_mean_sites`. Sorted group evidence retains count, total and mean; the maximum comparison uses exact cross multiplication before display rounding. The bundled maximum is south; an empty input has no winner and an exact tie retains all winning labels in sorted order.
