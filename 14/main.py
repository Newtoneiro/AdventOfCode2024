import os
import re
import numpy as np
from matplotlib import pyplot as plt
from dataclasses import dataclass


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


BOUNDARIES = [101, 103]
SECONDS = 100


@dataclass
class Robot:
    x: int
    y: int
    v_x: int
    v_y: int

    def tick(self):
        self.x = self.x + self.v_x
        if self.x < 0:
            self.x += BOUNDARIES[0]
        elif self.x >= BOUNDARIES[0]:
            self.x %= BOUNDARIES[0]

        self.y = self.y + self.v_y
        if self.y < 0:
            self.y += BOUNDARIES[1]
        elif self.y >= BOUNDARIES[1]:
            self.y %= BOUNDARIES[1]

    def get_quadrant(self):
        if self.x < BOUNDARIES[0] // 2 and\
                self.y < BOUNDARIES[1] // 2:
            return 1
        elif self.x < BOUNDARIES[0] // 2 and\
                self.y > BOUNDARIES[1] // 2:
            return 2
        elif self.x > BOUNDARIES[0] // 2 and\
                self.y < BOUNDARIES[1] // 2:
            return 3
        elif self.x > BOUNDARIES[0] // 2 and\
                self.y > BOUNDARIES[1] // 2:
            return 4
        return 0  # in the middle cross


def get_robots():
    robots = []
    pos_re = re.compile(r'p=(-?\d+),(-?\d+)')
    vel_re = re.compile(r'v=(-?\d+),(-?\d+)')
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            pos = pos_re.search(line)
            pos = [int(x) for x in pos.groups()]
            vel = vel_re.search(line)
            vel = [int(x) for x in vel.groups()]
            robots.append(Robot(pos[0], pos[1], vel[0], vel[1]))
    return robots


def main_one():
    robots = get_robots()

    for i in range(SECONDS):
        for robot in robots:
            robot.tick()

    quadrants = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
    }
    for robot in robots:
        quadrants[robot.get_quadrant()] += 1

    return quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4]


def display_robots(robots, time):
    grid = np.array([np.array([0 for _ in range(BOUNDARIES[0])]) for _ in range(BOUNDARIES[1])])
    for robot in robots:
        grid[robot.y][robot.x] = 1

    plt.figure(figsize=(5, 5))
    plt.imshow(grid, cmap='Greys', interpolation='none')
    plt.grid(visible=True, color='black', linewidth=0.5)
    plt.xticks(range(len(grid[0])))
    plt.yticks(range(len(grid)))
    plt.title(f"Grid at time: {time}")
    plt.show()


NEIGHBOURS = [
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0)
]


def find_largest_group(robots):
    grid = [[0 for _ in range(BOUNDARIES[0])] for _ in range(BOUNDARIES[1])]
    for robot in robots:
        grid[robot.y][robot.x] = 1

    visited = set()

    def dfs(cur):
        stack = [cur]
        size = 0

        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            size += 1

            for dx, dy in NEIGHBOURS:
                n_x, n_y = x + dx, y + dy
                if 0 <= n_x < BOUNDARIES[0] and\
                        0 <= n_y < BOUNDARIES[1] and\
                        grid[n_y][n_x] == 1 and\
                        (n_x, n_y) not in visited:
                    stack.append((n_x, n_y))

        return size

    largest_group = 0
    for robot in robots:
        if (robot.x, robot.y) not in visited:
            largest_group = max(largest_group, dfs((robot.x, robot.y)))

    return largest_group


def main_two():
    robots = get_robots()

    i = 1
    while True:
        for robot in robots:
            robot.tick()
        if find_largest_group(robots) > 150:
            display_robots(robots, i)
        i += 1


if __name__ == "__main__":
    print(main_one())
    print(main_two())
