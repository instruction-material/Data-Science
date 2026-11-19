# Chart Integrity Build: solution

Build a labeled, zero-baseline chart of mean recorded trips per site.

Each row of the bundled synthetic CSV is one recorded trip count at a named collection site. North has two records (2 and 4), south one (8), and west three (0, 6 and 12). The means are 3, 8 and 6 trips per record. Counts 2, 1 and 3 remain visible. These practice values support no claim about a real location or population.

For native Python 3.14, create a virtual environment, activate it, and install `python -m pip install --require-hashes -r requirements.txt`. Run `python main.py` from this folder. The program also locates its CSV when invoked from another folder. Open the saved `chart.svg` in a browser. The site IDE supplies Matplotlib and displays the figure with its normal chart output; installing the native requirements there is unnecessary.

make_chart returns the Matplotlib Figure for inspection or reuse. A categorical comparison uses bar lengths starting at zero, a descriptive title, labeled axes and units, and a value and record count on every bar. Empty input has no bars and says `No records`.

The optional second question is total recorded trips: `python main.py --metric total --output totals.svg`. Its heights are 6, 8 and 18, while the original mean chart is unchanged. Unequal row counts explain why these questions produce different rankings. A line through unrelated sites would imply an order the dataset does not supply.

Use `--input path/to/file.csv` for another UTF-8 CSV with `site,trips` columns, and `--output path/to/chart.svg` to select a destination. Site labels retain their spelling. Trips must be nonnegative whole numbers. Missing labels, malformed counts and negative values report their record number. Empty files with the required header are valid; their empty mean is not plotted as zero. In a notebook, run the cells with this role folder as the current directory or pass an explicit CSV path to load_rows.
