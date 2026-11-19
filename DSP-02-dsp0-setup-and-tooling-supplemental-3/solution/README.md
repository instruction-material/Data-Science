# Check Empty Input and Measured Zero

Run the starter in the course IDE. It opens the six-record setup input.
Change the default input list in `main.py` to `empty.csv` and `zero.csv`.
The first file contains a header and no measurements. The second contains
one measurement of zero. Exported projects can also run with
`python main.py --csv data/empty.csv data/zero.csv`.

Check that the empty file reports zero records and an undefined mean.
The zero file reports one record and a mean of 0.00. Keep both reports
with the original result and explain what differed in their denominators.
