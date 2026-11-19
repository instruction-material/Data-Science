# Filtered Dashboard Build

This starter uses six generated synthetic `site,trips` records. A row is one nonnegative whole trip count. North has count 2, total 6 and mean 3; south has count 1, total 8 and mean 8; west has count 3, total 18 and mean 6. The all-data total is 32 across six rows.

Run `python main.py` with the Python standard library. The bundled input resolves beside the script even from another working directory. `--input PATH` selects another CSV with the same columns. Notebook cells use this role directory or receive an explicit CSV path; kernel arguments are excluded from the script parser.

Select records for the current site; extend with an inclusive minimum in the optional activity.

Keep observed zeros and leave the measured mean absent when no records remain. Preserve original input rows. A one-record comparison retains its count and limitation. These synthetic records establish no real-world or causal ranking.

The repeated menu accepts `all`, an exact site label or `quit`; an absent label yields no matches. Each selection starts from the original rows. The optional second-filter task adds a minimum control to this saved project. `select_rows(rows, site, minimum)` uses an inclusive nonnegative whole threshold and AND when both controls are present.
