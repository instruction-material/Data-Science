# Data Science in Python

Canonical source layout in this repo is folder-first: each project should live in
its own directory with any local assets beside it.

Generated Replit/Poetry files and old flat-layout export duplicates have been
removed. Keep starter and solution material in the project directory that owns
it; do not re-add root-level standalone copies or legacy archive folders.

- Course catalog entry: `/Users/jacobanderson/Sites/classes.jacobdanderson.net/front-end/src/stores/courses/data-science-in-python.ts`
- GitHub repo clone: `/Users/jacobanderson/Documents/Work/Juni/Data Science`
- Legacy Dropbox source: `/Users/jacobanderson/Documents/Work/Juni/Data Science in Python/dropbox-source`

The `DS1-Mode` and `DS1-Simple-Stats` references accept unsorted numeric lists.
Median sorts a copy, averages the two middle values for even counts, and leaves
the original list unchanged. Median and range return `None` for an empty list.
The CSV summary studio now has three distinct paired projects:

- `DSP-01-data-analysis-lab-11`: count, total and mean, with optional minimum,
  maximum and range. Empty samples have an undefined mean (`None`).
- `DSP-20-applied-studio-11-data-analysis-lab-11-supplemental-2`: median and all
  tied modes, including unsorted/even samples and an extreme-value comparison.
- `DSP-21-applied-studio-11-data-analysis-lab-11-supplemental-3`: a readable
  five-line report with source identity, row count and an interpretation limit.

Each uses its own bundled synthetic CSV and the Python standard library.
The loader resolves its dataset beside the source, including runs from another
working directory. The role README states the exact completion contract.
Run `bash verify-course-source.sh` to check the source layout, statistics and
CSV projects. The remaining generic packs still need curriculum alignment.

The grouped-summary studio has three distinct source pairs:

- `DSP-03-data-analysis-lab-13` groups count, total and mean. Its optional
  label policy merges `north`, `North` and `NORTH` only when their source
  meaning permits that normalization. Original row dictionaries stay intact.
- `DSP-24-applied-studio-13-data-analysis-lab-13-supplemental-2` supplies grouping
  and asks for a Markdown table plus a denominator-aware interpretation. The
  script cells also work in a notebook; the terminal prints the same table.
- `DSP-25-applied-studio-13-data-analysis-lab-13-supplemental-3` compares mean
  with median and maximum. The west sample has mean 34, median 1 and maximum
  100, making the effect of its extreme value visible.

Each bundled CSV has eight synthetic category/value rows. Normalized north
has three rows, total 24 and mean 8; south has two rows, total 24 and mean 12;
west has three rows, total 102 and mean 34. The overall mean is 18.75.
Empty input produces no groups. Invalid values, missing categories and
nonfinite values are reported with their record number; finite negatives are
valid. Counts remain visible and these examples establish no real population
or causal claim. The original label and numeric text remain recoverable.
