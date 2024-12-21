import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")

KEYPAD = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['', '0', 'A'],
]
KEYPAD_DICT = {
    key: [x, y] for y, row in enumerate(KEYPAD)
    for x, key in enumerate(row)
}
INIT_KEYPAD_POS = [2, 3]

CONTROLLER = [
    ['', '^', 'A'],
    ['<', 'v', '>'],
]
CONTROLLER_DICT = {
    key: [x, y] for y, row in enumerate(CONTROLLER)
    for x, key in enumerate(row)
}
INIT_CONTROLLER_POS = [2, 0]


def get_codes():
    codes = []
    with open(filename) as f:
        for line in f.readlines():
            codes.append([c for c in line.strip()])
    return codes


def get_movements(board_dict, initial_pos, sequence):
    out = []
    pos = initial_pos
    gap = board_dict['']
    for ch in sequence:
        next_out = []
        next_pos = board_dict[ch]

        swap = False
        if next_pos[1] != pos[1]:
            y_movement_key = "v" if next_pos[1] > pos[1] else "^"
            for i in range(abs(next_pos[1] - pos[1])):
                next_out.append(y_movement_key)
                dir = 1 if y_movement_key == "v" else -1
                if pos[1] + dir * (i+1) == gap[1]:
                    swap = True
        if next_pos[0] != pos[0]:
            x_movement_key = ">" if next_pos[0] > pos[0] else "<"
            for i in range(abs(next_pos[0] - pos[0])):
                if not swap:
                    next_out.append(x_movement_key)
                else:
                    next_out.insert(0, x_movement_key)
        next_out.append("A")

        pos = next_pos
        out += next_out
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
        first_robot = get_movements(KEYPAD_DICT, INIT_KEYPAD_POS, code)
        second_robot = get_movements(CONTROLLER_DICT, INIT_CONTROLLER_POS, first_robot)
        my_input = get_movements(CONTROLLER_DICT, INIT_CONTROLLER_POS, second_robot)
        total += len(my_input) * cast_to_int(code)
    return total


def main_two():
    total = 0
    codes = get_codes()
    for code in codes:
        first_robot = get_movements(KEYPAD_DICT, INIT_KEYPAD_POS, code)
        for i in range(25):
            second_robot = get_movements(CONTROLLER_DICT, INIT_CONTROLLER_POS, first_robot)
            first_robot = second_robot
        my_input = get_movements(CONTROLLER_DICT, INIT_CONTROLLER_POS, second_robot)
        total += len(my_input) * cast_to_int(code)
    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
