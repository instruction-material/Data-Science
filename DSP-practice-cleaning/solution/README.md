# Audit a Messy Station CSV

Open the project in the course IDE or run `python main.py` from this folder.
The default run reads `data/sample.csv`. Supply `--csv PATH` to use a file with the same columns.

Leave the supplied synthetic CSV unchanged. Preserve the quoted station name
`North, Annex` and keep the first valid observation per record ID. A measured
zero is a valid count. The default result has four accepted rows totaling 25
riders and four rejected rows. The report includes two CSV sections. Save
each as a separate file and reconcile their record counts to the original.

Add a malformed count before a valid row with the same ID and run again.
Verify that rejecting the malformed row leaves the later row eligible.
