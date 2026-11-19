# Compare Room Check-ins by Day

Complete `summarize_day` and use its result for the Altair bar chart, table and
selected-day total. Monday has 6 Quiet and 12 Studio check-ins, totaling 18.
Tuesday has 0 Quiet and 9 Studio check-ins, totaling 9. Switching day changes
all three views. Keep the room names and the measurement unit visible.

Deliver a chart view for each day and a hand calculation for one selected day.
The file reports check-ins, which can include repeat visits by a person.

## Run the project

Run `python main.py` from the course IDE to inspect the calculation. Select
`data/sample.csv` to inspect the fictional observations. Use `--csv` with a
file using the same header to test another case.

To open the dashboard locally, create a virtual environment with Python 3.14,
install the course repository's locked dependencies with
`python -m pip install --require-hashes -r /path/to/Data-Science/requirements.txt`,
then run `python -m streamlit run dashboard.py --server.address 127.0.0.1`
from this project folder. The Altair chart, table and text use the same data.
