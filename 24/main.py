import os
from collections import deque
from graphviz import Source

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")
graphfile = os.path.join(dirname, "graph.dot")


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
                operations.append([name1, name2, operation, out])
                line = next(lines)
        except StopIteration:
            pass
            
    return inputs, operations


def get_bits_for(inputs, val):
    bits = [str(val) for key, val in sorted(filter(lambda item: item[0].startswith(val), inputs.items()), key= lambda item: int(item[0][1:]), reverse=True)]
    val = int("".join(bits), 2)
    return val


def perform_operations(inputs, operations):
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


def main_one():
    inputs, operations = get_data()
    operations = deque(operations)

    perform_operations(inputs, operations)
    
    return get_bits_for(inputs, "z")


def main_two():
    inputs, operations = get_data()
    operations = deque(operations)
    
    # Generate .dot graph to solve by hand
    with open(graphfile, 'w') as f:
        f.write('digraph {\n')
        f.write('node [fontname="Consolas", shape=box width=.5];\n')
        f.write('splines=ortho;\nrankdir="LR";\n')

        opid = 1
        opnames = {'XOR': '^', 'AND': '&', 'OR': '|'}
        opcolors = {'XOR': 'darkgreen', 'AND': 'red', 'OR': 'blue'}
        for (a, b, op, v) in operations:
            if v.startswith('z'):
                f.write(f'{v} [color="purple" fontcolor="purple"];\n')

            f.write(f'op{opid} [label="{opnames[op]}" color="{opcolors[op]}"'
                f'fontcolor="{opcolors[op]}"];\n')
            f.write(f'{a} -> op{opid};\n')
            f.write(f'{b} -> op{opid};\n')
            f.write(f'op{opid} -> {v};\n')
            opid += 1

        f.write('}\n')

    source = Source.from_file(graphfile)
    source.view()


if __name__ == "__main__":
    print(main_one())
    print(main_two())
