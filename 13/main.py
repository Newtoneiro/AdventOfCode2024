import os
import re
from sympy import symbols, Eq, solve
from sympy.core.numbers import Integer


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


TOKEN_COSTS = [3, 1]
BONUS_COST = 10000000000000


def get_claws(p2=False):
    def chunks(iterable, n):
        for i in range(0, len(iterable), n):
            yield iterable[i:i+n]

    button_re = re.compile(r'Button .: X\+(\d+), Y\+(\d+)\n')
    prize_re = re.compile(r'Prize: X=(\d+), Y=(\d+)')
    out = []
    with open(filename) as f:
        for lines in chunks(f.readlines(), 4):
            button1 = button_re.search(lines[0])
            button1 = [int(x) for x in button1.groups()]
            button2 = button_re.search(lines[1])
            button2 = [int(x) for x in button2.groups()]
            prize = prize_re.search(lines[2])
            prize = [int(x) for x in prize.groups()]
            if p2:
                prize[0] += BONUS_COST
                prize[1] += BONUS_COST
            out.append((button1, button2, prize))
    return out


def main_one():
    claws = get_claws()
    total = 0
    for (b1, b2, prize) in claws:
        x, y = symbols('x y')

        eq1 = Eq(b1[0] * x + b2[0] * y, prize[0])
        eq2 = Eq(b1[1] * x + b2[1] * y, prize[1])

        solution = solve((eq1, eq2), (x, y))

        if isinstance(solution[x], Integer) and isinstance(solution[y], Integer):
            total += solution[x] * TOKEN_COSTS[0] + solution[y] * TOKEN_COSTS[1]
    return total


def main_two():
    claws = get_claws(True)
    total = 0
    for (b1, b2, prize) in claws:
        x, y = symbols('x y')

        eq1 = Eq(b1[0] * x + b2[0] * y, prize[0])
        eq2 = Eq(b1[1] * x + b2[1] * y, prize[1])

        solution = solve((eq1, eq2), (x, y))

        if isinstance(solution[x], Integer) and isinstance(solution[y], Integer):
            total += solution[x] * TOKEN_COSTS[0] + solution[y] * TOKEN_COSTS[1]

    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
