import os
import re

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def eval_mul(match):
    total = 0
    mul_reg = re.compile(r'mul\(\d+,\d+\)')
    for found_mul_exp in re.findall(mul_reg, match):
        x, y = [int(num) for num in found_mul_exp.strip('mul(').strip(')').split(',')]
        total += x * y
    return total


def main_one():
    sum = 0
    with open(filename) as f:
        lines = f.read()
        sum += eval_mul(lines)
    return sum


def main_two():
    sum = 0
    mul_reg = r'mul\(\d+,\d+\)'
    do_reg = r'do\(\)'
    dont_reg = r'don\'t\(\)'
    all_regex = f"({mul_reg}|{do_reg}|{dont_reg})"
    with open(filename) as f:
        lines = f.read()
        enabled = True
        for match in re.findall(all_regex, lines):
            if match == "do()":
                enabled = True
            elif match == "don't()":
                enabled = False
            elif enabled:
                sum += eval_mul(match)

    return sum


if __name__ == "__main__":
    print(main_one())
    print(main_two())
