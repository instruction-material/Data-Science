# Capstone extension: Stress-Test Coverage

Run `python main.py` in the course IDE or from this folder. Compare the
default baseline rule of at least one open hour with the rule set by
`--minimum-hours`, initially seven. Missing loan counts never contribute
to a rate. Report the number of eligible rows and their measured hours
beside each rate, and write a conclusion about how the rule matters.

Before retains one of two measured rows and its rate stays at 3.00.
After retains one of three measured rows and its rate changes from 4.00
to 4.86. At nine hours neither phase supports a rate. Explain why a
stricter rule can increase a reported rate while reducing the evidence
available to support it. Keep the input and both rule values with the result.
