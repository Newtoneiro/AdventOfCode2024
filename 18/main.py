import os
import heapq
from copy import copy


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")

MAP_SIZE = 71
NEIGHBOURS = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0)
]
data_size = 1024


def get_data(size=None):
    coords = []
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            if size and i >= size:
                break
            parsed_coords = tuple(int(x) for x in line.strip().split(","))
            coords.append(parsed_coords)
    return coords


def astar(grid):
    def heuristic(a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def is_valid(node):
        r, c = node
        return 0 <= r < MAP_SIZE and 0 <= c < MAP_SIZE and grid[r][c] == "."

    start = (0, 0)
    end = (MAP_SIZE - 1, MAP_SIZE - 1)

    g_cost = {start: 0}
    came_from = {}

    open_set = []
    heapq.heappush(open_set, (0, start))

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return len(path)

        for dr, dc in NEIGHBOURS:
            neighbor = (current[0] + dr, current[1] + dc)
            if is_valid(neighbor):
                tentative_g_cost = g_cost[current] + 1  # Distance between nodes is 1
                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_cost, neighbor))
                    came_from[neighbor] = current

    return None


def main_one():
    grid = []
    coords = get_data(data_size)
    for i in range(MAP_SIZE):
        grid.append([])
        for _ in range(MAP_SIZE):
            grid[i].append(".")

    for coord in coords:
        grid[coord[1]][coord[0]] = "#"

    return astar(grid)


def main_two():
    grid = []
    coords = get_data()
    for i in range(MAP_SIZE):
        grid.append([])
        for _ in range(MAP_SIZE):
            grid[i].append(".")

    for coord in coords[:data_size]:
        grid[coord[1]][coord[0]] = "#"

    low = data_size
    high = len(coords) - 1

    while abs(low - high) > 1:
        grid_cp = [copy(row) for row in grid]
        middle = int((high + low) / 2)
        for x, y in coords[:middle + 1]:
            grid_cp[y][x] = "#"
        if not astar(grid_cp):
            high = middle
        else:
            low = middle

    return coords[high]


if __name__ == "__main__":
    print(main_one())
    print(main_two())
