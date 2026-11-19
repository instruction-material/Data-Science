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
