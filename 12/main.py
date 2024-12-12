import os
from collections import defaultdict, deque

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


NEIGHBOURS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def get_plots():
    out = defaultdict(set)
    map = []
    points_to_visit = deque()
    with open(filename) as f:
        for i, row in enumerate(f.readlines()):
            map.append([p for p in row.strip()])
            for j, col in enumerate(row.strip()):
                points_to_visit.append((j, i))

    def dfs(points: set, last_point: tuple):
        for dx, dy in NEIGHBOURS:
            neighbour = (last_point[0] + dx, last_point[1] + dy)
            if neighbour[0] < 0 or neighbour[0] >= len(map[0]) or neighbour[1] < 0 or neighbour[1] >= len(map):
                continue

            if neighbour not in points and map[neighbour[1]][neighbour[0]] == map[last_point[1]][last_point[0]]:
                points.add(neighbour)
                points.update(dfs(points, neighbour))
        return points

    i = 0
    while len(points_to_visit) > 0:
        point_to_check = points_to_visit.pop()
        plot_coordinates = dfs(set([point_to_check]), point_to_check)
        for point in plot_coordinates:
            if point in points_to_visit:
                points_to_visit.remove(point)
        out[f"{map[point_to_check[1]][point_to_check[0]]}{i}"] = plot_coordinates
        i += 1

    return out


def calculate_perimeter(squares):
    total_perimeter = 0

    for x, y in squares:
        for dx, dy in NEIGHBOURS:
            if (x + dx, y + dy) not in squares:
                total_perimeter += 1

    return total_perimeter


def get_value_1(squares):
    area = len(squares)
    perimeter = calculate_perimeter(squares)
    return area * perimeter


def main_one():
    plots = get_plots()
    total = 0

    for squares in plots.values():
        total += get_value_1(squares)

    return total


def calculate_sides(coordinates):
    return 0


def get_value_2(squares):
    area = len(squares)
    sides = calculate_sides(squares)
    print(area, sides)
    return area * sides


def main_two():
    plots = get_plots()
    total = 0

    for name, squares in plots.items():
        print(name)
        total += get_value_2(squares)

    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
