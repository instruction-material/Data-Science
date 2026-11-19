# Reproducible mini report

Python 3.10 or newer; standard library only. Each role owns its `main.py`
and `data/sample.csv`. From that role folder run `python3 main.py`.
The dataset path also resolves correctly when the script is run elsewhere.
Notebook cells use the role folder as their working directory or pass an
explicit path to `load_rows`. No notebook state is required.

The bundled synthetic weeks have 4, 7, 7 and 10 trips: 4 recorded weeks,
28 total trips and mean 7.00 trips per recorded week. A header-only CSV
has zero recorded weeks and an undefined mean. Whole counts can be zero;
negative counts, missing/duplicate week labels and noninteger counts are
invalid. Validation identifies the CSV record number. These data support
no claim about real people or populations.

Complete `build_report` in the starter. Its Markdown has Question, Data
source, Method, Results, Interpretation, Limitation and Next question sections.
Show the original week/count table, count, total, mean and units. Add the
supplied appendix when `include_appendix=True`; the CLI option is `--appendix`.
The appendix records the SHA-256 of the actual input bytes, interpreter,
relative input path and repeatable run command. It records provenance, not a
claim that a checksum establishes data quality. Run twice in fresh processes.
