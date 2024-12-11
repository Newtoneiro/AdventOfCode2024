import os
from collections import deque
from functools import lru_cache


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_rocks():
    rocks = deque()

    with open(filename) as f:
        unparsed = f.read()
        for rock in unparsed.strip().split():
            rocks.append(int(rock))

    return rocks


def blink(rocks: deque):
    new_rocks = deque()
    while len(rocks) > 0:
        rock = rocks.popleft()
        if rock == 0:
            new_rocks.append(1)
        elif len(str(rock)) % 2 == 0:
            first_half, second_half = str(rock)[:len(str(rock)) // 2], str(rock)[len(str(rock)) // 2:]
            new_rocks.append(int(first_half))
            new_rocks.append(int(second_half))
        else:
            new_rocks.append(rock * 2024)
    return new_rocks


def main_one():
    rocks = get_rocks()

    for _ in range(25):
        rocks = blink(rocks)

    return len(rocks)


@lru_cache(maxsize=None)
def blink_two(rock, total, blinks_left):
    if blinks_left == 0:
        return total

    if rock == 0:
        return blink_two(1, total, blinks_left - 1)
    elif len(str(rock)) % 2 == 0:
        first_half, second_half = str(rock)[:len(str(rock)) // 2], str(rock)[len(str(rock)) // 2:]
        return blink_two(int(first_half), total, blinks_left - 1) + blink_two(int(second_half), total, blinks_left - 1)
    else:
        return blink_two(rock * 2024, total, blinks_left - 1)


def main_two():
    rocks = get_rocks()
    total = 0

    for rock in rocks:
        total += blink_two(rock, 1, 75)

    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
