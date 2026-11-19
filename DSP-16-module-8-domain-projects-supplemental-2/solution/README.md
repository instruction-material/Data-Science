# Audit a Route-Week Dataset

Run `python main.py` on the bundled fictional report or supply `--csv` with the
same header. Complete `audit_reports` so each record is accepted or rejected
once. Return accepted route-week pairs in input order and a count for each
rejection reason. Preserve the input.

Use this order. Reject an invalid row if its fields, numeric values, or
route-week identifiers are malformed. Then check for missing trips, zero
covered days, and finally a repeated previously accepted route-week. The first
valid occurrence is kept. A zero-trip row with positive coverage is valid.

The bundled input contains ten rows. Expect six accepted and one rejection
for each of the four reasons. As an additional check, put a missing row before
a valid row for the same route-week. The missing row must not block the valid
one. Record the rule used before trying a different policy for duplicates.
