import os
from collections import deque
from functools import lru_cache

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")

KEYPAD = (
    ('7', '8', '9'),
    ('4', '5', '6'),
    ('1', '2', '3'),
    ('', '0', 'A'),
)
INIT_KEYPAD_POS = (2, 3)

CONTROLLER = (
    ('', '^', 'A'),
    ('<', 'v', '>'),
)
INIT_CONTROLLER_POS = (2, 0)

MOVES = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

def get_codes():
    codes = []
    with open(filename) as f:
        for line in f.readlines():
            codes.append([c for c in line.strip()])
    return codes

@lru_cache(maxsize=None)
def get_move(grid, pos, ch_out):
    board_dict =  {
        key: [x, y] for y, row in enumerate(grid)
        for x, key in enumerate(row)
    }
    next_out = deque()
    gap = board_dict['']
    next_pos = board_dict[ch_out]
    if next_pos[1] != pos[1]:
        y_movement_key = "v" if next_pos[1] > pos[1] else "^"
        for i in range(abs(next_pos[1] - pos[1])):
            next_out.append(y_movement_key)
    if next_pos[0] != pos[0]:
        x_movement_key = ">" if next_pos[0] > pos[0] else "<"
        for i in range(abs(next_pos[0] - pos[0])):
            next_out.append(x_movement_key)
        
    nex_out_fixed = []
    cur_pos = pos
    while len(next_out):
        ch = next_out.popleft()
        move = MOVES[ch]
        cur_pos = [
            cur_pos[0] + move[0],
            cur_pos[1] + move[1]
        ]
        if cur_pos == gap:
            gap_avoid_ch = next_out.pop()
            gap_avoid_move = MOVES[gap_avoid_ch]
            cur_pos = [
                cur_pos[0] + gap_avoid_move[0],
                cur_pos[1] + gap_avoid_move[1]
            ]
            nex_out_fixed.append(gap_avoid_ch)
            nex_out_fixed.append(ch)
        else:
            nex_out_fixed.append(ch)
    
    nex_out_fixed.append("A")
    return nex_out_fixed, (next_pos[0], next_pos[1])

def get_movements(board, initial_pos, sequence):
    out = []
    pos = initial_pos
    for ch in sequence:
        next_out, next_pos = get_move(board, pos, ch)
        out += next_out
        pos = next_pos
    return out


def cast_to_int(code):
    out = ""
    for ch in code:
        if ch.isnumeric():
            out += ch
    return int(out)


def main_one():
    total = 0
    codes = get_codes()
    for code in codes:
        first_robot = get_movements(KEYPAD, INIT_KEYPAD_POS, code)
        second_robot = get_movements(CONTROLLER, INIT_CONTROLLER_POS, first_robot)
        my_input = get_movements(CONTROLLER, INIT_CONTROLLER_POS, second_robot)
        total += len(my_input) * cast_to_int(code)
    return total


def main_two():
    total = 0
    codes = get_codes()
    for code in codes:
        first_robot = get_movements(KEYPAD, INIT_KEYPAD_POS, code)
        for i in range(25):
            print(i)
            second_robot = get_movements(CONTROLLER, INIT_CONTROLLER_POS, first_robot)
            first_robot = second_robot
        my_input = get_movements(CONTROLLER, INIT_CONTROLLER_POS, second_robot)
        total += len(my_input) * cast_to_int(code)
    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
