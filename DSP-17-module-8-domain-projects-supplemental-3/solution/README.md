# Check Sensitivity to Coverage

Run `python main.py` or open the starter in the course IDE. The sample has
fictional route-week reports. Complete `compare_coverage` to calculate a
rate for each route with all measured reports and with a minimum number
of covered days per report. Divide total trips by the total covered days
for each group. Keep the report counts alongside the rates.

Run again with `--minimum-days 1` to confirm both columns agree. With the
default of three days, North changes from 8.56 to 8.14 trips per day, South
stays at 6.50, and East changes from a measured 0.00 to unavailable. The
comparison shows how a data inclusion rule changes the reported estimate.
It does not establish a change in travel behavior.
