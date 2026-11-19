# Build a Reproducible Data Story

Open the project in the course IDE or run `python main.py` from this folder.
The default run reads `data/sample.csv`. Supply `--csv PATH` to use a file with the same columns.

Name a question and an audience. The synthetic fallback is the Domain
Projects route-week sample with a West row that has no coverage. The first
view compares observed trips per covered day by route. The second view checks the coverage by week within
each route. For example, North has 77 trips over nine covered days.
West has no measured rate because its only trip count is unavailable.
Keep measured zeros distinct from unavailable values.

Add a filter or use a documented dataset to answer a question of choice.
Keep a copy of the exact input, the code, two reproducible views, a
hand-checked value, one boundary check, a claim and one limitation.
