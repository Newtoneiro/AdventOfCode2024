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
            if nx < 0 or\
                    nx >= len(grid[0]) or\
                    ny < 0 or\
                    ny >= len(grid):
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
                if nx < 0 or\
                        nx >= len(grid[0]) or\
                        ny < 0 or\
                        ny >= len(grid):
                    continue
                if grid[ny][nx] != "#":
                    if (nx, ny) not in visited:
                        out_cost = abs(nx - pos_x) + abs(ny - pos_y)
                        out.add(((nx, ny), out_cost, ((pos_x, pos_y), (nx, ny))))
                else:
                    stack.append(((nx, ny), cur_cost + 1))

    return out


def main_two(min_saved_time):
    grid, start, end = get_grid()

    def djikstra(grid, start, end, max_cost=float('inf')):
        pq = [(0, start)]  # Priority queue: (total_cost, current_pos)
        visited = {}
        previous = {}  # To store the path

        while pq:
            total_cost, current_pos = heapq.heappop(pq)

            if total_cost > max_cost:
                return float('inf'), []  # Return infinity and empty path if cost exceeds max_cost

            if current_pos == end:
                # Reconstruct the path
                path = []
                while current_pos:
                    path.append(current_pos)
                    current_pos = previous.get(current_pos)
                return total_cost, path[::-1]  # Reverse the path to start -> end

            if current_pos in visited and visited[current_pos] < total_cost:
                continue

            visited[current_pos] = total_cost

            for new_pos, move_cost in get_moves(grid, current_pos):
                if new_pos not in visited or visited[new_pos] > total_cost + move_cost:
                    heapq.heappush(pq, (total_cost + move_cost, new_pos))
                    previous[new_pos] = current_pos  # Track the path

        return float('inf'), []  # If no path exists

    cost_without_cheats, path = djikstra(grid, start, end)
    costs = defaultdict(set)
    checked_cheats = set()
    for i, node_a in enumerate(path):
        print(f"{i} / {len(path)}")
        for out_a, cheat_dist, cheat in get_moves_two(grid, node_a, True):
            if cheat in checked_cheats:
                continue
            dist, _ = djikstra(grid, out_a, end)
            if dist == float('inf'):
                continue
            new_cost = i + cheat_dist + dist
            if new_cost < cost_without_cheats and cost_without_cheats - new_cost >= min_saved_time:
                costs[new_cost].add(cheat)
            checked_cheats.add(cheat)


        # print(f"{i} / {len(path)}")
        # for j, node_b in enumerate(path):
        #     if start != end:
        #         distance = get_distance(node_a, node_b)
        #         if distance <= CHEAT_PS and is_valid_cheat(node_a, node_b):
        #             new_cost = i + distance + (cost_without_cheats - j)
        #             if new_cost < cost_without_cheats and cost_without_cheats - new_cost >= min_saved_time:
        #                 costs[new_cost].add((node_a, node_b))

    total = 0
    for c, items in sorted(costs.items(), key=lambda item: item[0]):
        total += len(items)
        print(f"{cost_without_cheats - c}: {len(items)}")
    return total


if __name__ == "__main__":
    # print(main_one(100))
    print(main_two(50))
