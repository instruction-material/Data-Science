# Compare Country-Year Observations

Open the project in the course IDE or run `python main.py` from this folder.
The default run reads `data/sample.csv`. Supply `--csv PATH` to use a file with the same columns.

The six records are from the [course life expectancy dataset](https://static.classes.jacobdanderson.net/life_expectancy.csv).
Each row records a country, a year and life expectancy in years. Run with
`--year 2015` to compare with the 2013 baseline. A country with no observation
for either year lacks a measured change. Use the table to check the 2015
gap of 1.5 years, the Canada change of 0.4 and the Japan change of 0.2.

Run again with `--year 2020`. Record why this input supports no comparison.
Include the source, measurement unit and a limitation with the report.
