# Classify and account for dirty records (starter)

Complete `validation_reasons`. Classify ID, site, trips and hours in order. Distinguish missing, malformed and out-of-range values. Allow trips from 0 to 1000 and hours from 0 to 24.

Run main.py in the course IDE with the bundled input. For native Python 3.14, install pandas with `python -m pip install pandas==3.1.1` and run `python main.py`. Use `--input PATH` to try a separate CSV. A notebook can call `main(["--input", "PATH"])` from the project folder. Keep the original CSV unchanged.

Expect 10 loaded and 5 accepted, including the recorded zero. One duplicate and four invalid records are excluded. Two accepted labels are repaired. The accepted total is 24 trips.
