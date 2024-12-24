import os
from collections import deque

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_data():
    inputs = {}
    operations = []
    with open(filename) as f:
        lines = (line for line in f.readlines())
        line = next(lines)
        while line != "\n":
            name, val = line.strip().split(": ")
            inputs[name] = int(val)
            line = next(lines)
            
        line = next(lines)
        try:
            while line:
                name1, operation, name2, _, out = line.strip().split(" ")
                operations.append((name1, name2, operation, out))
                line = next(lines)
        except StopIteration:
            pass
            
    return inputs, operations


def main_one():
    inputs, operations = get_data()
    operations = deque(operations)
    while len(operations) > 0:
        name1, name2, operation, out = operations.pop()
        if name1 not in inputs or name2 not in inputs:
            operations.appendleft((name1, name2, operation, out))
            continue

        if operation == "AND":
            inputs[out] = int(inputs[name1] and inputs[name2])
        elif operation == "OR":
            inputs[out] = int(inputs[name1] or inputs[name2])
        elif operation == "XOR":
            inputs[out] = int(inputs[name1] ^ inputs[name2])
    
    bits = [str(val) for key, val in sorted(filter(lambda item: item[0].startswith("z"), inputs.items()), key= lambda item: int(item[0][1:]), reverse=True)]
    val = int("".join(bits), 2)
    return val


def main_two():
    pass


if __name__ == "__main__":
    print(main_one())
    print(main_two())
