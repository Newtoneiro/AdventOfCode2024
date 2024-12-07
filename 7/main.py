import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_equations():
    equations = []
    with open(filename) as f:
        for line in f.readlines():
            total, coefficients = line.strip().split(":")
            coefficients = [int(c) for c in coefficients.split()]
            equations.append((int(total), coefficients))
    return equations


def main_one():
    total = 0

    def check_equation(cumulative, left_overs, total):
        if len(left_overs) == 0:
            return cumulative == total
        else:
            return check_equation(cumulative + left_overs[0], left_overs[1:], total) or\
                    check_equation(cumulative * left_overs[0], left_overs[1:], total)

    equations = get_equations()
    for sum, coefs in equations:
        if check_equation(0, coefs, sum):
            total += sum

    return total


def main_two():
    total = 0

    def combine_numbers(one, another):
        return int(f"{one}{another}")

    def check_equation(cumulative, left_overs, total):
        if len(left_overs) == 0:
            return cumulative == total
        else:
            return check_equation(cumulative + left_overs[0], left_overs[1:], total) or\
                    check_equation(cumulative * left_overs[0], left_overs[1:], total) or\
                    check_equation(combine_numbers(cumulative, left_overs[0]), left_overs[1:], total)

    equations = get_equations()
    for sum, coefs in equations:
        if check_equation(0, coefs, sum):
            total += sum

    return total


if __name__ == "__main__":
    print(main_one())
    print(main_two())
