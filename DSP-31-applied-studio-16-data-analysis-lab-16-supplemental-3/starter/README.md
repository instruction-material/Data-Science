# Filtered Summary Export

This starter uses six generated synthetic `site,trips` records. A row is one nonnegative whole trip count. North has count 2, total 6 and mean 3; south has count 1, total 8 and mean 8; west has count 3, total 18 and mean 6. The all-data total is 32 across six rows.

Run `python main.py` with the Python standard library. The bundled input resolves beside the script even from another working directory. `--input PATH` selects another CSV with the same columns. Notebook cells use this role directory or receive an explicit CSV path; kernel arguments are excluded from the script parser.

Write the selected summary and filter metadata to the documented UTF-8 CSV schema.

Keep observed zeros and leave the measured mean absent when no records remain. Preserve original input rows. A one-record comparison retains its count and limitation. These synthetic records establish no real-world or causal ranking.

For west with minimum 5, run `python main.py --site west --minimum 5 --output selected.csv`: count 2, total 18, mean 9.00. The default output is `filtered-summary.csv`. The header order is `site_filter,minimum_trips,records,total_trips,mean_trips_per_record,state`. A missing selection is `all`; an absent minimum and unmeasured mean are empty fields. Standard CSV line endings are retained.
