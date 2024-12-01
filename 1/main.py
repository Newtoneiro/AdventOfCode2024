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
    sum = 0
    arr1, arr2 = get_arrays()
    while len(arr1) > 0:
        idx1 = np.argmin(arr1)
        idx2 = np.argmin(arr2)
        sum += abs(arr1[idx1] - arr2[idx2])
        del arr1[idx1]
        del arr2[idx2]

    return sum


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
