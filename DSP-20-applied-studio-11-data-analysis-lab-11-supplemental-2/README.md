# Median and mode comparison

Complete `median` and `modes` in the starter, then run `summarize_distribution`.
The supplied count/total/mean helper and CSV loader are already complete.
Use a sorted copy for median so the original row order remains available.
For an even sample, average the two middle values. An empty median is `None`.
Return every tied mode in first-appearance order; an empty sample has `[]` modes.
When every value appears once, every value is tied for highest frequency.

Hand checks:

| Values | Mean | Median | Modes |
| --- | ---: | ---: | --- |
| 4, 8, 11, 17 | 10 | 9.5 | 4, 8, 11, 17 |
| 1, 2, 2, 3, 100 | 21.6 | 2 | 2 |
| 3, 1, 3, 1 | 2 | 2 | 3, 1 |

Explain why the extreme value changes mean more than median. Neither statistic
alone establishes whether the extreme row is an error.
The CSV is synthetic and its `value` column contains finite numbers.
Run `python3 main.py` in a role folder, or run its full path from elsewhere.
`load_values(path)` accepts another CSV with a `value` header.
