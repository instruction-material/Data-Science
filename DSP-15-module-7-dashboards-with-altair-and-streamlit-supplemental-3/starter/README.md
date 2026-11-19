# Keep a Common Scale for Day Comparisons

Complete `comparable_panels` to select each day separately and compute the
upper scale limit from the full file. The two bar charts start at 0 and end
at 12 for the default data. In the IDE, run the default command. Then run
`python main.py --first Tuesday --second Wednesday`. Both charts still use
a 0 to 12 scale although Studio's Wednesday value is 4.

Change both selectors in the native dashboard and compare the bar heights
against the labeled values. Where a room has no recorded observation, show
the existing rows only. Submit the two filtered tables, chart views and a
sentence on why paired displays use a common scale.

## Run the project

Run `python main.py` from the course IDE to inspect the calculation. Select
`data/sample.csv` to inspect the fictional observations. Use `--csv` with a
file using the same header to test another case.

To open the dashboard locally, create a virtual environment with Python 3.14,
install the course repository's locked dependencies with
`python -m pip install --require-hashes -r /path/to/Data-Science/requirements.txt`,
then run `python -m streamlit run dashboard.py --server.address 127.0.0.1`
from this project folder. The Altair chart, table and text use the same data.
