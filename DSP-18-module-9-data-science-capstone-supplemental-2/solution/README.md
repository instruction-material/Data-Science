# Capstone transfer: Verify a Data Revision

Run `python main.py` in the course IDE or from this folder. The default
command compares the original synthetic `data/sample.csv` with
`data/corrected.csv`. Use `--previous` and `--revised` to compare two other
snapshots without editing them.

Complete `changes` so it reports each added row, removed row, or changed
field with its phase and week. Compare the key and fields, independent
of file order. A blank loan count is unavailable, distinct from zero.
The default change is After W3, loans 8 to 11. The hourly rate in the
After phase then changes from 4.00 to 4.20.

Deliver both input versions, their printed fingerprints, and a note
describing which claim needs rechecking. Check that comparing a
reordered copy with identical records reports no record changes.
