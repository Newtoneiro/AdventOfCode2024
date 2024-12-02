import os
from copy import copy

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def is_safe(line: list):
    if all(line[i] < line[i+1] for i in range(len(line) - 1)):
        return all(line[i+1] - line[i] <= 3 for i in range(len(line) - 1))
    elif all(line[i] > line[i+1] for i in range(len(line) - 1)):
        return all(line[i] - line[i+1] <= 3 for i in range(len(line) - 1))
    return False


def main_one():
    total_lines = 0
    with open(filename) as f:
        for line in f.readlines():
            if is_safe([int(elem) for elem in line.strip().split()]):
                total_lines += 1
    return total_lines


def main_two():
    total_lines = 0
    with open(filename) as f:
        for line in f.readlines():
            line = [int(elem) for elem in line.strip().split()]
            for i in range(len(line)):
                line_without_i = copy(line)
                del line_without_i[i]
                if is_safe(line_without_i):
                    total_lines += 1
                    break
    return total_lines


if __name__ == "__main__":
    print(main_one())
    print(main_two())
