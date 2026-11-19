# Simple Sort and Ranking Warm-up

Run `python main.py` from this folder or open it in the course IDE. Each
example tuple contains a route, observed trips, and positive covered days.
Complete `rank_routes` by starting with a copy, choosing the next highest
trips-per-day result, and moving that entry into the output. Resolve equal
rates by route name. `Fraction` can represent a rate exactly.

North with 12 trips in 3 days and South with 8 in 2 both have a rate of 4.
The example should print North, South, then East. Verify that an empty list
returns an empty ranking and that the input list is unchanged.
