import os
import sys
import heapq
from copy import copy
from collections import deque, defaultdict

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")

sys.setrecursionlimit(10**6)

NEIGHBOURS = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0)
]
CHEAT_PS = 20


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


def get_moves(grid, pos):
    (pos_x, pos_y) = pos
    out = []
    neighbours = [(n, 1) for n in NEIGHBOURS]
    for (dx, dy), cost in neighbours:
        nx, ny = pos_x + dx, pos_y + dy
        if nx < 0 or\
                nx >= len(grid[0]) or\
                ny < 0 or\
                ny >= len(grid) or\
                grid[ny][nx] == "#":
            continue

        out.append(((nx, ny), cost))

    return out


def main_one(saved_time):
    grid, start, end = get_grid()

    def djikstra(grid, start, max_cost=float('inf')):
        pq = [(0, start)]
        visited = {}

        while pq:
            total_cost, current_pos = heapq.heappop(pq)
            if total_cost > max_cost:
                return float('inf')

            if current_pos == end:
                return total_cost

            if current_pos in visited and visited[current_pos] < total_cost:
                continue

            visited[current_pos] = total_cost

            for new_pos, move_cost in get_moves(grid, current_pos):
                heapq.heappush(pq, (total_cost + move_cost, new_pos))

        return float('inf')  # If no path

    score_without_cheating = djikstra(grid, start)
    total_cheats = 0

    for i in range(1, len(grid[0]) - 1):
        for j in range(1, len(grid)):
            print(f"{i} / {len(grid[0]) - 2}")
            if grid[j][i] == "#":
                grid_cp = [copy(row) for row in grid]
                grid_cp[j][i] = "."
                if djikstra(grid_cp, start, score_without_cheating - saved_time) != float('inf'):
                    total_cheats += 1

    return total_cheats


def get_moves_two(grid, pos, can_cheat):
    (pos_x, pos_y) = pos
    out = set()
    neighbours = [(n, 1) for n in NEIGHBOURS]
    for (dx, dy), cost in neighbours:
        nx, ny = pos_x + dx, pos_y + dy
        if nx < 0 or\
                nx >= len(grid[0]) or\
                ny < 0 or\
                ny >= len(grid) or\
                grid[ny][nx] == "#":
            continue

        out.add(((nx, ny), cost, ()))

    if can_cheat:
        stack = deque()
        visited = set([(pos_x, pos_y)])
        for dx, dy in NEIGHBOURS:
            nx, ny = pos_x + dx, pos_y + dy
            if nx < 1 or\
                    nx >= len(grid[0]) - 1 or\
                    ny < 1 or\
                    ny >= len(grid) - 1:
                continue

            if grid[ny][nx] == "#":
                stack.append(((nx, ny), 1))

        while len(stack) > 0:
            cur_pos, cur_cost = stack.pop()
            if cur_pos in visited or cur_cost >= CHEAT_PS:
                continue
            visited.add(cur_pos)
            for dx, dy in NEIGHBOURS:
                nx, ny = cur_pos[0] + dx, cur_pos[1] + dy
                if nx < 1 or\
                        nx >= len(grid[0]) - 1 or\
                        ny < 1 or\
                        ny >= len(grid) - 1:
                    continue
                if grid[ny][nx] != "#":
                    if (nx, ny) not in visited:
                        out_cost = abs(nx - pos_x) + abs(ny - pos_y)
                        out.add(((nx, ny), out_cost, ((pos_x, pos_y), (nx, ny))))
                else:
                    stack.append(((nx, ny), cur_cost + 1))

    return out


def main_two(saved_time):
    grid, start, end = get_grid()

    def djikstra(grid, start, max_cost=float('inf')):
        pq = [(0, start, ())]
        visited = {}
        cost_dict = defaultdict(set)

        while pq:
            total_cost, current_pos, cheat_path = heapq.heappop(pq)
            if total_cost > max_cost:
                return float('inf')

            if current_pos in visited and visited[current_pos] < total_cost:
                continue

            visited[current_pos] = total_cost

            if current_pos == end:
                continue

            for new_pos, move_cost, cheat_path in get_moves_two(grid, current_pos, can_cheat=cheat_path == ()):
                heapq.heappush(pq, (total_cost + move_cost, new_pos, cheat_path))

        return visited[end], cheat_path

    cost = djikstra(grid, start)

    return cost


if __name__ == "__main__":
    # print(main_one(100))
    print(main_two(76))
