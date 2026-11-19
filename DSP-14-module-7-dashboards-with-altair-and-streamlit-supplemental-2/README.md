# Distinguish Empty Filters from Zero

Complete `filter_observations` to match the selected day and room. Preserve
Tuesday Quiet as a measured zero. Wednesday Quiet has no matching observation
and displays an explanation in place of the chart. In the IDE, run the default
case and then try `--day Tuesday --room Quiet` and `--day Wednesday --room Quiet`.

In the native dashboard, return from Wednesday Quiet to All rooms. Check that
Studio's 4 observed check-ins repopulate the chart and table. Record the
three outcomes. A missing measurement remains unavailable. A zero is an observed count.

## Run the project

Run `python main.py` from the course IDE to inspect the calculation. Select
`data/sample.csv` to inspect the fictional observations. Use `--csv` with a
file using the same header to test another case.

To open the dashboard locally, create a virtual environment with Python 3.14,
install the course repository's locked dependencies with
`python -m pip install --require-hashes -r /path/to/Data-Science/requirements.txt`,
then run `python -m streamlit run dashboard.py --server.address 127.0.0.1`
from this project folder. The Altair chart, table and text use the same data.
