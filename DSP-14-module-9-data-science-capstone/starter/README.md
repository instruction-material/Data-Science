# Capstone: Compare Laptop Loan Rates

Run `python main.py` in the course IDE or from this folder. The program
uses the synthetic `data/sample.csv` and writes `report.md` in the project.
Use `--csv` to rerun with another file of the same shape and `--output` to
write the report to a different Markdown file.

Each row is one reporting week in the Before or After phase. Loans are
counted over recorded open hours. Exclude rows with missing loans or zero
hours from a rate, and include measured zeros with positive hours. Report
how many rows were excluded for each phase. Divide the total measured
loans by the total measured hours for that phase.

Before has 42 loans in 14 measured hours (3.00 per hour) and one excluded
observation. After has 60 in 15 (4.00 per hour). Verify one rate by hand.
Check a file where one phase has no observations with positive coverage.
The report states an observed difference and explains why the comparison
alone cannot identify the effect of the pilot.
