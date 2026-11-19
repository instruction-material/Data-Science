# Readable summary report

Complete `format_report(filename, values)` in the starter. The loader and
count/total/mean calculation are supplied. Return the following five lines
for the bundled synthetic CSV, rather than printing a Python dictionary:

```text
Source: sample.csv
Rows: 4
Total: 40
Mean: 10
Caution: This describes the loaded rows; it does not establish a cause.
```

Keep source identity and row count alongside the result. For an empty dataset,
print `Rows: 0`, `Total: 0` and `Mean: undefined (no rows)`. Check another file
name and `[-2, 2, 6]`; its count is 3, total 6 and mean 2. Preserve input order.
The provided CSV has a `value` header and finite numbers. Run `python3 main.py`
inside a role folder, or invoke its full path from another working directory.
The completed reference implements exactly this output contract.
