import os


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_data(size=None):
    available_towels = None
    designs = []
    with open(filename) as f:
        lines = f.readlines()
        available_towels = [x for x in lines[0].strip().split(', ')]
        for line in lines[2:]:
            designs.append(line.strip())

    return available_towels, designs


def main_one():
    available_towels, designs = get_data()

    def check_design(design, design_towels):
        design_arr = [False] * (len(design) + 1)
        design_arr[0] = True  # Empty prefix is composable

        for i in range(len(design)):
            if design_arr[i]:
                for towel in design_towels:
                    if design[i:i + len(towel)] == towel:
                        design_arr[i + len(towel)] = True

        return design_arr[len(design)]

    total = 0
    for design in designs:
        design_towels = set()
        for towel in available_towels:
            if towel in design:
                design_towels.add(towel)
        if check_design(design, design_towels):
            total += 1

    return total


def main_two():
    available_towels, designs = get_data()

    def check_design(design, design_towels):
        design_arr = [0] * (len(design) + 1)
        design_arr[0] = 1  # Empty prefix can be made in 1 way

        for i in range(len(design)):
            if design_arr[i] > 0:
                for towel in design_towels:
                    if design[i:i + len(towel)] == towel:
                        design_arr[i + len(towel)] += design_arr[i]

        return design_arr[len(design)]

    total = 0
    for design in designs:
        design_towels = set()
        for towel in available_towels:
            if towel in design:
                design_towels.add(towel)
        total += check_design(design, design_towels)

    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
