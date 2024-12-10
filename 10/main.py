import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_map():
    content = []

    with open(filename) as f:
        for line in f.readlines():
            content.append([int(x) if x != "." else -1 for x in line.strip()])

    return content


def main_one():
    map = get_map()
    starting_positions = []

    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if col == 0:
                starting_positions.append((x, y))

    def get_neighbors(pos):
        neighbors = []
        if pos[0] > 0:
            neighbors.append((pos[0] - 1, pos[1]))
        if pos[0] < len(map[pos[1]]) - 1:
            neighbors.append((pos[0] + 1, pos[1]))
        if pos[1] > 0:
            neighbors.append((pos[0], pos[1] - 1))
        if pos[1] < len(map) - 1:
            neighbors.append((pos[0], pos[1] + 1))
        neighbors = [n for n in filter(lambda n: map[n[1]][n[0]] == map[pos[1]][pos[0]] + 1, neighbors)]
        return neighbors

    def get_peaks(trail):
        last_step = trail[-1]
        if map[last_step[1]][last_step[0]] == 9:
            return set([last_step])

        neighbors = get_neighbors(last_step)
        if len(neighbors) == 0:
            return set([None])

        peaks = set()
        for n in neighbors:
            neighbour_peaks = get_peaks([*trail, n])
            for peak in neighbour_peaks:
                if peak:
                    peaks.add(peak)

        return peaks

    total = 0

    for pos in starting_positions:
        total += len(get_peaks([pos]))

    return total


def main_two():
    total = 0

    map = get_map()
    starting_positions = []

    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if col == 0:
                starting_positions.append((x, y))

    def get_neighbors(pos):
        neighbors = []
        if pos[0] > 0:
            neighbors.append((pos[0] - 1, pos[1]))
        if pos[0] < len(map[pos[1]]) - 1:
            neighbors.append((pos[0] + 1, pos[1]))
        if pos[1] > 0:
            neighbors.append((pos[0], pos[1] - 1))
        if pos[1] < len(map) - 1:
            neighbors.append((pos[0], pos[1] + 1))
        neighbors = [n for n in filter(lambda n: map[n[1]][n[0]] == map[pos[1]][pos[0]] + 1, neighbors)]
        return neighbors

    def get_score(trail):
        last_step = trail[-1]
        if map[last_step[1]][last_step[0]] == 9:
            return 1

        neighbors = get_neighbors(last_step)
        if len(neighbors) == 0:
            return 0

        total = 0
        for n in neighbors:
            total += get_score([*trail, n])

        return total

    for pos in starting_positions:
        total += get_score([pos])

    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
