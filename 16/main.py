import os
import sys
import heapq
from copy import deepcopy

sys.setrecursionlimit(10**6)


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


DIRECTIONS = {
    0: (0, -1),
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0)
}


def get_grid():
    grid = []
    start = None
    end = None
    with open(filename) as f:
        for i, row in enumerate(f.readlines()):
            grid.append([])
            for j, col in enumerate(row.strip()):
                if col == "S":
                    start = (j, i)
                if col == "E":
                    end = (j, i)
                grid[i].append(col)
    return grid, start, end


def get_moves(grid, pos, pos_d):
    (pos_x, pos_y) = pos
    out = []
    for d, (dx, dy) in DIRECTIONS.items():
        if abs(d - pos_d) == 2:
            continue  # Skip for 180 deg turns

        if pos_d == d:
            if grid[pos_y + dy][pos_x + dx] != "#":
                out.append(((pos_x + dx, pos_y + dy), d, 1))
        else:
            if grid[pos_y + dy][pos_x + dx] != "#":
                out.append(((pos_x, pos_y), d, 1000))
    return out


def main_one():
    grid, start, end = get_grid()

    # Priority queue: (total_cost, (x, y), current_direction)
    pq = [(0, start, 1)]
    visited = {}

    while pq:
        total_cost, current_pos, current_dir = heapq.heappop(pq)

        if current_pos == end:
            return total_cost

        if (current_pos, current_dir) in visited and visited[(current_pos, current_dir)] < total_cost:
            continue

        visited[(current_pos, current_dir)] = total_cost

        for new_pos, new_dir, move_cost in get_moves(grid, current_pos, current_dir):
            heapq.heappush(pq, (total_cost + move_cost, new_pos, new_dir))

    return float('inf')  # If no path


def print_path(path):
    grid, start, end = get_grid()
    gridcp = deepcopy(grid)
    dir_str = ["^", ">", "v", "<"]
    color_start = "\033[92m"  # Green
    color_end = "\033[91m"    # Red
    color_path = "\033[94m"   # Blue
    color_reset = "\033[0m"   # Reset to default color

    for (x, y), d in path:
        gridcp[y][x] = color_path + dir_str[d] + color_reset

    gridcp[start[1]][start[0]] = color_start + "S" + color_reset
    gridcp[end[1]][end[0]] = color_end + "E" + color_reset

    for row in gridcp:
        print("".join(row))
    print("=================")


def print_grid(grid):
    max_width = max(len(str(cell)) for row in grid for cell in row)

    for row in grid:
        print(" | ".join(f"{str(cell):<{max_width}}" for cell in row))


def main_two():
    grid, start, end = get_grid()

    # Priority queue: (total_cost, (x, y), current_direction)
    pq = [(0, start, 1)]
    visited = {}
    best_score = 0

    while pq:
        total_cost, current_pos, current_dir = heapq.heappop(pq)

        if current_pos == end:
            visited[(current_pos, current_dir)] = total_cost
            best_score = total_cost
            break

        if (current_pos, current_dir) in visited and visited[(current_pos, current_dir)] < total_cost:
            continue

        visited[(current_pos, current_dir)] = total_cost

        for new_pos, new_dir, move_cost in get_moves(grid, current_pos, current_dir):
            heapq.heappush(pq, (total_cost + move_cost, new_pos, new_dir))

    pq = []
    seen = set()
    for end_dir in range(4):  # End going in all directions
        heapq.heappush(pq, (0, end, end_dir))
    visited_backward = {}

    while pq:
        total_cost, current_pos, current_dir = heapq.heappop(pq)
        if (current_pos, current_dir) not in visited_backward:
            visited_backward[(current_pos, current_dir)] = total_cost
        if (current_pos, current_dir) in seen:
            continue
        seen.add((current_pos, current_dir))

        # going backwards
        back_dir = (current_dir + 2) % 4
        moves = get_moves(grid, current_pos, back_dir)
        for new_pos, new_dir, move_cost in moves:
            heapq.heappush(pq, (total_cost + move_cost, new_pos, (new_dir + 2) % 4))

    good_seats = set()
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            for dir in range(4):
                if ((j, i), dir) in visited \
                        and ((j, i), dir) in visited_backward and\
                        visited[((j, i), dir)] + visited_backward[((j, i), dir)] == best_score:
                    good_seats.add((j, i))
    return len(good_seats)


if __name__ == "__main__":
    print(main_one())
    print(main_two())
