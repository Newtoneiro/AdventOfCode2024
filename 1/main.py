import os
import numpy as np

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_arrays():
    arr1, arr2 = [], []
    with open(filename) as f:
        for line in f.readlines():
            x1, x2 = line.split()
            arr1.append(int(x1))
            arr2.append(int(x2))
    return arr1, arr2


def main_one():
    arr1, arr2 = get_arrays()
    arr1.sort()
    arr2.sort()

    return sum(abs(x - y) for x, y in zip(arr1, arr2))


def main_two():
    sum = 0
    arr1, arr2 = get_arrays()
    for elem in arr1:
        count = arr2.count(elem)
        sum += elem * count

    return sum


if __name__ == "__main__":
    print(main_one())
    print(main_two())
