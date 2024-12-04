import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_board():
    out = []
    with open(filename) as f:
        for line in f.readlines():
            out.append([ch for ch in line.strip()])
    return out


def check_for_xmas(col, row, board):
    matches = 0
    directions = [
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]

    for d in directions:
        text = "X"
        cur_col, cur_row = col, row
        while len(text) != 4:
            cur_col += d[0]
            cur_row += d[1]
            if cur_col < 0 or cur_row < 0:
                break
            try:
                text += board[cur_col][cur_row]
            except IndexError:
                break

        if text == "XMAS":
            matches += 1
    return matches


def check_for_x_mas(col, row, board):
    matches = 0

    first = f"{board[col - 1][row - 1]}A{board[col + 1][row + 1]}"
    second = f"{board[col + 1][row - 1]}A{board[col - 1][row + 1]}"
    if first in ["MAS", "SAM"] and second in ["MAS", "SAM"]:
        matches += 1

    return matches


def main_one():
    total = 0

    board = get_board()
    for col in range(len(board)):
        for row in range(len(board[0])):
            if board[col][row] == "X":
                total += check_for_xmas(col, row, board)

    return total


def main_two():
    total = 0

    board = get_board()
    for col in range(1, len(board) - 1):
        for row in range(1, len(board[0]) - 1):
            if board[col][row] == "A":
                total += check_for_x_mas(col, row, board)

    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
