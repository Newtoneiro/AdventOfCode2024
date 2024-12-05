import os
from collections import defaultdict

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_data():
    rules = defaultdict(set)
    records = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue

            if "|" in line:
                before, after = [int(x) for x in line.strip().split("|")]
                rules[before].add(after)
            else:
                records.append([int(x) for x in line.strip().split(",")])

    return rules, records


def set_the_record_straight(record, rules):
    out = []
    for i, elem in enumerate(record):
        if any(el in rules[elem] for el in out):
            new_i = i
            while any(el in rules[elem] for el in out[:new_i]):
                new_i -= 1
            out.insert(new_i, elem)
        else:
            out.append(elem)
    return out


def main():
    total_good = 0
    total_fixed = 0
    rules, records = get_data()
    for record in records:
        prev = set()
        counts = True
        for elem in record:
            if any(el in rules[elem] for el in prev):
                counts = False
                break
            prev.add(elem)
        if counts:
            total_good += record[len(record) // 2]
        else:
            straight_record = set_the_record_straight(record, rules)
            total_fixed += straight_record[len(straight_record) // 2]

    return total_good, total_fixed


if __name__ == "__main__":
    print(main())
