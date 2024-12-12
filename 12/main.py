import os
from collections import defaultdict, deque
from copy import copy

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
    corners = 0  # neat trick, the figure has as many corners as it has sides.

    for (c_x, c_y) in coordinates:
        c_neighbors = set()
        for dx, dy in NEIGHBOURS:
            if (c_x + dx, c_y + dy) in coordinates:
                c_neighbors.add((c_x + dx, c_y + dy))

        if len(c_neighbors) == 0:  # Single, left alone block -> + 4 sides
            corners += 4
        elif len(c_neighbors) == 1:  # A pimple in a figure -> + 2 corners
            corners += 2
        else:  # For every other combination -> L shapes, T shapes and + shapes
            if ((c_x - 1, c_y) in c_neighbors and (c_x, c_y - 1) in c_neighbors):
                if len(c_neighbors) == 2:  # If is L shaped (count the sharp corner)
                    corners += 1
                if (c_x - 1, c_y - 1) not in coordinates:  # Check for the inner corner
                    corners += 1
            if ((c_x, c_y - 1) in c_neighbors and (c_x + 1, c_y) in c_neighbors):
                if len(c_neighbors) == 2:
                    corners += 1
                if (c_x + 1, c_y - 1) not in coordinates:
                    corners += 1
            if ((c_x + 1, c_y) in c_neighbors and (c_x, c_y + 1) in c_neighbors):
                if len(c_neighbors) == 2:
                    corners += 1
                if (c_x + 1, c_y + 1) not in coordinates:
                    corners += 1
            if ((c_x, c_y + 1) in c_neighbors and (c_x - 1, c_y) in c_neighbors):
                if len(c_neighbors) == 2:
                    corners += 1
                if (c_x - 1, c_y + 1) not in coordinates:
                    corners += 1

    return corners


def get_value_2(squares):
    area = len(squares)
    sides = calculate_sides(squares)
    return area * sides


def main_two():
    # was really stuck on this one, done thanks to this -> https://www.reddit.com/r/adventofcode/comments/1hcf16m/2024_day_12_everyone_must_be_hating_today_so_here/
    plots = get_plots()
    total = 0

    for squares in plots.values():
        total += get_value_2(squares)

    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
