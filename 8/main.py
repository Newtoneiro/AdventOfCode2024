import os
from itertools import combinations
from collections import defaultdict

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_map():
    map = []
    with open(filename) as f:
        for line in f.readlines():
            map.append([ch for ch in line.strip()])
    return map


def main_one():
    antinodes = set()
    groups = defaultdict(list)

    map = get_map()
    for i, row in enumerate(map):
        for j, col in enumerate(row):
            if col != ".":
                groups[col].append((j, i))

    def reflect_point(point, center):
        x, y = point
        cx, cy = center
        x_reflected = 2 * cx - x
        y_reflected = 2 * cy - y
        return x_reflected, y_reflected

    for group in groups.values():
        for a, b in combinations(group, 2):
            for antinode in [reflect_point(a, b), reflect_point(b, a)]:
                if antinode[0] >= 0 and antinode[0] < len(map[0]) and antinode[1] >= 0 and antinode[1] < len(map):
                    antinodes.add(antinode)

    return len(antinodes)


def main_two():
    antinodes = set()
    groups = defaultdict(list)

    map = get_map()
    for i, row in enumerate(map):
        for j, col in enumerate(row):
            if col != ".":
                groups[col].append((j, i))

    def reflect_point(point, center):
        x, y = point
        cx, cy = center
        x_reflected = 2 * cx - x
        y_reflected = 2 * cy - y
        return x_reflected, y_reflected

    for group in groups.values():
        for a, b in combinations(group, 2):
            antinodes.add(a)
            antinodes.add(b)
            for point, center in [(a, b), (b, a)]:
                antinode = reflect_point(point, center)
                while antinode[0] >= 0 and antinode[0] < len(map[0]) and antinode[1] >= 0 and antinode[1] < len(map):
                    antinodes.add(antinode)
                    point = center
                    center = antinode
                    antinode = reflect_point(point, center)

    return len(antinodes)


if __name__ == "__main__":
    print(main_one())
    print(main_two())
