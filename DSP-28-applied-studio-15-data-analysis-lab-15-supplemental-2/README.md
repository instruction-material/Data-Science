# Script and Markdown conversion

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

The supplied `analyze` function separates calculation from presentation.
Complete `render_markdown(result)` to preserve the same seven report sections,
values, units and limits as the core mini report without modifying `result`.
The script prints the report. An explicit output path also saves its UTF-8
Markdown, for example `python3 main.py report.md`; the provided writer ends
it with exactly one newline. Compare the printed and saved Results sections
with a fresh core run. A saved report describes that run's input, and must be
regenerated when the input changes.
