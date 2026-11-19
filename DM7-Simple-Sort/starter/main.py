EXAMPLE = [("South", 8, 2), ("East", 6, 3), ("North", 12, 3)]


def rank_routes(records):
    """Return (route, trips, days) rows in descending rate order."""
    # TODO: Repeatedly choose the highest rate. Order ties by route name.
    # Keep the supplied list unchanged.
    return None


def main():
    rows = rank_routes(EXAMPLE)
    if rows is None:
        print("TODO: rank measured routes")
        return
    for route, trips, days in rows:
        print(f"{route}: {trips / days:.2f} trips/day")


if __name__ == "__main__":
    main()
