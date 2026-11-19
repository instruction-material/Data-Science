"""Implement and check mean and median on the three retained samples."""

data1 = [-21, -15, -60, -60, -45, -34, -20, -21, -10, -30]
data2 = [54, 54, 56, 56, 56, 51, 57, 57, 57, 58, 51, 54]
data3 = [32, 43, 87, 56, 34, 21, 21, 90, 76, 72, 63]

def mean(values):
    """Return the arithmetic mean or None when there are no observations."""
    raise NotImplementedError("Complete mean before comparing results.")


def median(values):
    """Return the middle of the ordered values without changing the input."""
    raise NotImplementedError("Complete median before comparing results.")


def main():
    try:
        for name, values in (("Negative", data1), ("Repeated", data2), ("Mixed", data3)):
            print(f"{name}: records={len(values)}, mean={mean(values)}, median={median(values)}")
    except NotImplementedError as error:
        print(error)


if __name__ == "__main__":
    main()
