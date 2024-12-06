import os
from copy import copy

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


DIRECTIONS = {
    0: (0, -1),
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0)
}


def get_board():
    out = []
    start = None
    with open(filename) as f:
        for y, line in enumerate(f.readlines()):
            row = []
            for x, ch in enumerate(line.strip()):
                if ch == "^":
                    start = (x, y)
                row.append(ch)
            out.append(row)

    return out, start


def main_one():
    board, cur_pos = get_board()
    cur_direction = 0
    pivot_points = []

    while True:
        board[cur_pos[1]][cur_pos[0]] = "X"
        move = DIRECTIONS[cur_direction]
        next_pos = (
            cur_pos[0] + move[0],
            cur_pos[1] + move[1]
        )
        if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= len(board[0]) or next_pos[1] >= len(board):
            end_dir = cur_direction + 1
            end_dir = end_dir % 4
            pivot_points.append(([next_pos[0], next_pos[1]], end_dir))
            break
        if board[next_pos[1]][next_pos[0]] == "#":
            cur_direction += 1
            cur_direction = cur_direction % 4
            pivot_points.append(([cur_pos[0], cur_pos[1]], cur_direction))
        else:
            cur_pos = next_pos

    total = 0
    for row in board:
        total += sum(el == "X" for el in row)

    return pivot_points, total


def main_two(pivot_points):
    potential_points = set()

    for (start, end) in zip(pivot_points[2:-1], pivot_points[3:]):
        check_pos = copy(start[0])
        while True:
            cur_dir = DIRECTIONS[start[1]]
            check_pos[0] += cur_dir[0]
            check_pos[1] += cur_dir[1]
            if check_pos == end[0]:
                break

            # check
            would_be_dir = start[1] + 1
            would_be_dir = would_be_dir % 4
            if would_be_dir in [0, 2]:  # Vertical
                candidate_x = check_pos[0]
                candidate_dir = would_be_dir + 1
                candidate_dir = candidate_dir % 4
                candidates = [x for x in filter(lambda x: x[0][0] == candidate_x and x[1] == candidate_dir, pivot_points)]
                if len(candidates) > 0:
                    potential_points.add((check_pos[0] + cur_dir[0], check_pos[1] + cur_dir[1]))
            else:  # horizontal
                candidate_y = check_pos[1]
                candidate_dir = would_be_dir + 1
                candidate_dir = candidate_dir % 4
                candidates = [x for x in filter(lambda x: x[0][1] == candidate_y and x[1] == candidate_dir, pivot_points)]
                if len(candidates) > 0:
                    potential_points.add((check_pos[0] + cur_dir[0], check_pos[1] + cur_dir[1]))

    return len(potential_points)


if __name__ == "__main__":
    pivot_points, total_one = main_one()
    print(total_one)
    print(main_two(pivot_points))
