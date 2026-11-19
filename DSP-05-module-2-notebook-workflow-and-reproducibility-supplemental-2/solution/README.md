# Empty and Zero Input Transfer: solution

Complete format_summary(summary), retaining the count and distinguishing undefined mean from 0.00.

Run `python main.py` with Python 3.14. This project uses only the standard library. The default CSV is resolved beside the saved script, including when the script is launched by its full path from another working directory. `--input PATH` selects another input explicitly. Notebook cells use the role directory for their default input or call `main(["--input", "PATH"])`.

The six synthetic trip counts are 2, 4, 8, 0, 6 and 12. The reference prints count 6, total 32 and mean 5.33 trips per record. An empty input has an undefined mean; one recorded zero has mean 0.00. A copied input ending in 18 has total 38 and mean 6.33. Invalid labels or counts raise a record-number error rather than silently dropping rows.

The transfer includes data/empty.csv and data/zero.csv. Run each using --input and preserve the original fixture.


Preserve the code, selected input, observed output and Python version. Rerun from a fresh process or restarted notebook kernel. Compare with a hand calculation. These synthetic observations establish no real-world population or causal result.
