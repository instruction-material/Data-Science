from fractions import Fraction

EXAMPLE = [("South", 8, 2), ("East", 6, 3), ("North", 12, 3)]


def rank_routes(records):
    pending = list(records)
    result = []
    while pending:
        position = min(
            range(len(pending)),
            key=lambda i: (-Fraction(pending[i][1], pending[i][2]), pending[i][0]),
        )
        result.append(pending.pop(position))
    return result


def main():
    rows = rank_routes(EXAMPLE)
    if rows is None:
        print("TODO: rank measured routes")
        return
    for route, trips, days in rows:
        print(f"{route}: {trips / days:.2f} trips/day")


if __name__ == "__main__":
    main()
