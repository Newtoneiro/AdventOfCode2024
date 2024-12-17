import os
import re

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_data():
    registers = {}
    program_out = []
    register_re = re.compile(r'Register (.): (\d+)')
    program_re = re.compile(r'Program: ((\d+,)*\d+)')
    with open(filename) as f:
        content = f.read()
        for name, val in register_re.findall(content):
            registers[name] = int(val)
        program = program_re.findall(content)
        for instruction in program[0][0].split(","):
            program_out.append(int(instruction))

    return registers, program_out


def main_one(a_val=None, number_of_inputs=0):
    registers, program = get_data()
    if a_val is not None:
        registers["A"] = a_val
    out = []
    instruction_pointer = 0

    def perform_instruction(opcode, operand):
        combo = operand
        if operand == 4:
            combo = registers["A"]
        elif operand == 5:
            combo = registers["B"]
        elif operand == 6:
            combo = registers["C"]

        if opcode == 0:
            registers["A"] = int(registers["A"] / (2 ** combo))
        elif opcode == 1:
            registers["B"] = registers["B"] ^ operand
        elif opcode == 2:
            registers["B"] = combo % 8
        elif opcode == 3:
            if registers["A"] == 0:
                return True, 0
            return False, operand
        elif opcode == 4:
            registers["B"] = registers["B"] ^ registers["C"]
        elif opcode == 5:
            out.append(combo % 8)
        elif opcode == 6:
            registers["B"] = int(registers["A"] / (2 ** combo))
        elif opcode == 7:
            registers["C"] = int(registers["A"] / (2 ** combo))

        return True, 0

    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        increase_pointer, new_pointer = perform_instruction(opcode, operand)
        if increase_pointer:
            instruction_pointer += 2
        else:
            instruction_pointer = new_pointer

    if a_val is not None:
        return ",".join(str(el) for el in out[number_of_inputs:]) == ",".join(str(el) for el in program[number_of_inputs:])
    return ",".join(str(el) for el in out)


def main_two():
    number_of_inputs = 15
    a_val = 8**number_of_inputs
    while number_of_inputs >= 0:
        if main_one(a_val, number_of_inputs):
            number_of_inputs -= 1
            continue
        a_val += 8 ** number_of_inputs
    return a_val


if __name__ == "__main__":
    print(main_one())
    print(main_two())
