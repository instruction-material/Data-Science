# Cleaning Report Builder

This synthetic dataset represents measurements whose stated domain requires
finite, nonnegative numbers. That rule belongs to this example; negative values
can be valid in other domains.

Run `python3 main.py` inside either role folder, or pass its absolute path from
another working directory. The starter reports an unfinished function until
`clean_rows` is implemented. The loader retains the original cell text.

The function returns accepted `values`, a `report` with rows loaded/accepted/
rejected/repaired, and `rejected_rows` preserving the CSV row number, label,
original value and first applicable rejection reason. The default policy checks
missing values, surrounding whitespace, numeric conversion, finiteness and
nonnegativity in that order. It changes none of the input rows.

The eight supplied rows yield values `[4.0, 8.0, 17.0]`: 8 loaded, 3 accepted,
5 rejected and 0 repaired. The rejected rows are 3 (missing), 4 (not numeric),
5 (negative), 7 (not finite) and 8 (surrounding whitespace). Accepted plus rejected
equals loaded; a repaired row is included in the accepted count.

For the optional Safe Repair Rule Extension, call
`clean_rows(load_rows(), repair_whitespace=True)`. Trimming the numeric cell
`" 11 "` accepts that row and records one repair: 8 loaded, 4 accepted, 4 rejected,
1 repaired, with values `[4.0, 8.0, 11.0, 17.0]`. Missing, nonnumeric, nonfinite and
negative cells remain rejected. Original text and row order remain intact.

Check an empty table, an all-rejected table, zero, a fraction and both policies.
Document how the rule changes the rows represented by the result. A clean table
alone does not establish that the original question can still be answered.
