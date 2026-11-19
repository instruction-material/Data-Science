# Compare Trip Rates by Route and Week

Open the starter in the course IDE or run `python main.py` from this folder. Use
`--csv` to compare a CSV with the same four columns. Each synthetic row describes
one route and week. The trips column counts trips observed over the number of
covered days. A blank trip value or zero covered days cannot contribute to a
measured rate. Zero trips with positive coverage is a measured zero.

Complete `summarize` so it groups the measured reports, adds trips and covered
days separately, and then divides. Return rows sorted by group name. Keep the
same function usable for route and week. The default case contains six measured
rows. North has 77 trips over nine covered days, or 8.56 trips per day. Week W2
has 45 trips over nine covered route-days, or 5.00 trips per route-day. A day with
coverage on two routes contributes two route-days to the weekly total.

For a second check, use a CSV whose only trip count is blank. The expected
output is `No measured reports`. Record how changing coverage can affect the
interpretation of a ranking. These fixtures describe fictional observations.
