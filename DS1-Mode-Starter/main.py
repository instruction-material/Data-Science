"""Use a frequency table to report all tied most frequent values."""

data1 = [-21, -15, -60, -60, -45, -34, -20, -21, -10, -30]
data2 = [54, 54, 56, 56, 56, 51, 57, 57, 57, 58, 51, 54]
data3 = [32, 43, 87, 56, 34, 21, 21, 90, 76, 72, 63]

def mode(values):
    """Return all maximum-frequency values in first-seen order."""
    # Count observations, find the maximum frequency and retain every tie.
    raise NotImplementedError("Complete mode before comparing results.")


def main():
    try:
        for name, values in (("Negative", data1), ("Repeated", data2), ("Mixed", data3)):
            print(f"{name}: {mode(values)}")
    except NotImplementedError as error:
        print(error)


if __name__ == "__main__":
    main()
