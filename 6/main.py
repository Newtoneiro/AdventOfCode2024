import os
from pprint import pprint

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
            break
        if board[next_pos[1]][next_pos[0]] == "#":
            cur_direction += 1
            cur_direction = cur_direction % 4
            pivot_points.append(cur_pos)
        else:
            cur_pos = next_pos

    total = 0
    for row in board:
        total += sum(el == "X" for el in row)

    return pivot_points, total


def main_two(pivot_points):
    total = 0

    print(pivot_points)
    for start, end in zip(pivot_points[:-1], pivot_points[1:]):
        print(start, end)

    return total


if __name__ == "__main__":
    pivot_points, total_one = main_one()
    print(total_one)
    print(main_two(pivot_points))
