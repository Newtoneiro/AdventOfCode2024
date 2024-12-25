import os
from pprint import pprint

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_input():
    input = []
    with open(filename) as f:
        cur = []
        for line in f.readlines():
            if line == "\n":
                input.append(cur)
                cur = []
                continue
            cur.append([x for x in line.strip()])
        input.append(cur)
            
    return input


def get_locks_and_keys(data):
    locks = []
    keys = []
    for scheme in data:
        isKey = scheme[0][0] == "."
        heights = []
        for x in range(len(scheme[0])):
            h = -1
            if isKey:
                for y in range(len(scheme) - 1, -1, -1):
                    if scheme[y][x] == "#":
                        h += 1
            else:
                for y in range(0, len(scheme)):
                    if scheme[y][x] == "#":
                        h += 1
            heights.append(h)
        if isKey:
            keys.append(heights)
        else:
            locks.append(heights)
    return locks, keys


def fit(key, lock):
    for h_k, h_l in zip(key, lock):
        if h_k + h_l > 5:
            return False
    return True


def main_one():
    data = get_input()
    locks, keys = get_locks_and_keys(data)
    
    total = 0
    for lock in locks:
        for key in keys:
            if fit(key, lock):
                total += 1
                
    return total


def main_two():
    pass


if __name__ == "__main__":
    print(main_one())
    print(main_two())
