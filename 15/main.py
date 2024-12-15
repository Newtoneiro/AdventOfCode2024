import os
from collections import deque


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


MOVES_DICT = {
    "<": (-1, 0),
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
}


def get_grid():
    grid = []
    moves = []
    get_moves = False
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            if line == "\n":
                get_moves = True
                continue
            if not get_moves:
                grid.append([])
                for j, ch in enumerate(line.strip()):
                    if ch == "@":
                        start = (j, i)
                    grid[i].append(ch)
            else:
                for ch in line.strip():
                    moves.append(ch)

    return grid, start, moves


def get_grid2():
    grid = []
    moves = []
    get_moves = False
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            if line == "\n":
                get_moves = True
                continue
            if not get_moves:
                grid.append([])
                for j, ch in enumerate(line.strip()):
                    if ch == "#":
                        grid[i].append('#')
                        grid[i].append('#')
                    elif ch == "O":
                        grid[i].append('[')
                        grid[i].append(']')
                    elif ch == ".":
                        grid[i].append('.')
                        grid[i].append('.')
                    elif ch == "@":
                        start = (2 * j, i)
                        grid[i].append('@')
                        grid[i].append('.')
            else:
                for ch in line.strip():
                    moves.append(ch)

    return grid, start, moves


def main_one():
    grid, cur_pos, moves = get_grid()

    for move in moves:
        stack = deque()
        m_x, m_y = MOVES_DICT[move]
        check_pos = (cur_pos[0], cur_pos[1])
        while grid[check_pos[1]][check_pos[0]] not in ["#", "."]:
            stack.append(check_pos)
            check_pos = (check_pos[0] + m_x, check_pos[1] + m_y)
        if grid[check_pos[1]][check_pos[0]] == "#":
            continue
        elif grid[check_pos[1]][check_pos[0]] == ".":
            destination = check_pos
            while len(stack) > 0:
                from_pos = stack.pop()
                grid[destination[1]][destination[0]], grid[from_pos[1]][from_pos[0]] = grid[from_pos[1]][from_pos[0]], grid[destination[1]][destination[0]]
                destination = from_pos
            cur_pos = (cur_pos[0] + m_x, cur_pos[1] + m_y)

    total = 0
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "O":
                total += 100 * i + j
    return total


def main_two():
    grid, cur_pos, moves = get_grid2()

    for i, move in enumerate(moves):
        if i == 2272:
            pass
        move_stack = deque()
        check_stack = deque([(cur_pos[0], cur_pos[1])])
        m_x, m_y = MOVES_DICT[move]
        do_move = True
        while len(check_stack) > 0:
            check_pos = check_stack.pop()
            if grid[check_pos[1]][check_pos[0]] == "#":
                do_move = False
                break

            if (check_pos, (check_pos[0] + m_x, check_pos[1] + m_y)) not in move_stack:
                move_stack.append((check_pos, (check_pos[0] + m_x, check_pos[1] + m_y)))
            if grid[check_pos[1] + m_y][check_pos[0] + m_x] != ".":
                check_stack.append((check_pos[0] + m_x, check_pos[1] + m_y))

            if move in ["^", "v"]:
                if grid[check_pos[1]][check_pos[0]] == "[":
                    if ((check_pos[0] + 1, check_pos[1]), (check_pos[0] + 1 + m_x, check_pos[1] + m_y)) not in move_stack:
                        move_stack.append(((check_pos[0] + 1, check_pos[1]), (check_pos[0] + 1 + m_x, check_pos[1] + m_y)))
                    if grid[check_pos[1] + m_y][check_pos[0] + 1 + m_x] != ".":
                        check_stack.append((check_pos[0] + 1 + m_x, check_pos[1] + m_y))
                elif grid[check_pos[1]][check_pos[0]] == "]":
                    if ((check_pos[0] - 1, check_pos[1]), (check_pos[0] - 1 + m_x, check_pos[1] + m_y)) not in move_stack:
                        move_stack.append(((check_pos[0] - 1, check_pos[1]), (check_pos[0] - 1 + m_x, check_pos[1] + m_y)))
                    if grid[check_pos[1] + m_y][check_pos[0] - 1 + m_x] != ".":
                        check_stack.append((check_pos[0] - 1 + m_x, check_pos[1] + m_y))

        # sort the moves from furthest to nearest
        move_stack_sorted = move_stack
        if move == "^":
            move_stack_sorted = deque(sorted(move_stack, key=lambda item: item[1][1], reverse=True))
        elif move == "v":
            move_stack_sorted = deque(sorted(move_stack, key=lambda item: item[1][1]))

        if do_move:
            while len(move_stack_sorted) > 0:
                from_pos, destination = move_stack_sorted.pop()
                grid[destination[1]][destination[0]], grid[from_pos[1]][from_pos[0]] = grid[from_pos[1]][from_pos[0]], grid[destination[1]][destination[0]]

            cur_pos = (cur_pos[0] + m_x, cur_pos[1] + m_y)

    total = 0
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "[":
                total += 100 * i + j
    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
