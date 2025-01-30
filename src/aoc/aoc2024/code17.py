import itertools


import aoc.helpers as helpers


def process_sections(sections):
    registers = dict()
    for line in sections[0]:
        name_part, value_part = line.split(":")
        name = name_part.split()[1]
        value = int(value_part)
        registers[name] = value

    program = list(map(int, sections[1][0].split(":")[1].split(",")))

    return registers, program


def process_opcode(opcode, operand, registers):
    def combo(i):
        assert isinstance(i, int)
        if 0 <= i <= 3:
            return i
        return registers["ABC"[i - 4]]

    jump_to = None
    output = None

    match opcode:
        case 0:  # adv
            registers["A"] = registers["A"] // 2 ** combo(operand)
        case 1:  # bxl
            registers["B"] = registers["B"] ^ operand
        case 2:  # bst
            registers["B"] = combo(operand) % 8
        case 3:  # jnz
            if registers["A"] != 0:
                return operand, None
        case 4:  # bxc
            registers["B"] = registers["B"] ^ registers["C"]
        case 5:  # out
            output = combo(operand) % 8
        case 6:  # bdv
            registers["B"] = registers["A"] // 2 ** combo(operand)
        case 7:  # cdv
            registers["C"] = registers["A"] // 2 ** combo(operand)
        case _:
            breakpoint()
            assert False
    return jump_to, output


def run_program(*, registers, program):
    instruction_pointer = 0
    output_buffer = []

    while 0 <= instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        jump_to, output = process_opcode(opcode, operand, registers)

        if jump_to is not None:
            instruction_pointer = jump_to
        else:
            instruction_pointer += 2
        if output is not None:
            output_buffer.append(output)
    return output_buffer


def disassemble(program):
    return list(itertools.batched(program, n=2, strict=True))


def opcode_name(opcode):
    return [
        "adv",
        "bxl",
        "bst",
        "jnz",
        "bxc",
        "out",
        "bdv",
        "cdv",
    ][opcode]


def pprint_program(program):
    print()
    for opcode, operand in disassemble(program):
        print(f"{opcode_name(opcode)}: {operand}")


def run_part1(registers, program):
    output_buffer = run_program(registers=registers, program=program)
    return ",".join(map(str, output_buffer))


def run_part2(registers, program):
    # This is specialized to the programs provided.  The full one is harder, and is as
    # below.

    # bst: 4 : b = a % 8
    # bxl: 1 : b = b ^ 1
    # cdv: 5 : c = a >> b
    # bxl: 5 : b = b ^ 5
    # bxc: 3 : b = b ^ c
    # out: 5 : out b % 8
    # adv: 3 : a = a >> 3
    # jnz: 0

    len_program = len(program)

    def dfs(root, depth):
        """Run a depth-first search, offset by root.  The key things here are that the
        program operates as a loop, and that in each iteration 1) a is shifted right by
        three digits until it is zero, 2) one character is output 3) the output depends
        only on the value of a at the start of the iteration.

        We do a depth-first search on A by octal digits. It's easier to do this most
        significant octal digit first.  That's because the last n outputs depend only on
        the n most significant octal digits.

        Working from least significant octal digits is also possible but the first n
        outputs in general depend on higher order octal digits than just the n least
        significant ones, so the search needs to "look ahead".  It's possible in
        reasonable time with the example program as only a few extra octal digits are
        influential in each iteration.

        root contains depth most-significant octal digits.  Except when depth == 0, it
        will be an octal number with len(program) octal digits.  Its children have zero or
        more less-significant octal digits set.

        depth is the depth of the search, which is 1 when visiting the most significant
        octal digit, 2 visiting the next-most, and so on.

        """
        target_output = program
        output = run_program(program=program, registers=registers | {"A": root})
        if output == target_output:
            return root

        # at a given depth we need the last depth outputs to be correct
        if output[len_program - depth :] != target_output[len_program - depth :]:
            return None
        child_unit = 1 << (3 * (len_program - 1 - depth))
        children = [root + child_unit * i for i in range(8)]
        for child in children:
            if (child_result := dfs(child, depth + 1)) is not None:
                return child_result
        return None

    return dfs(root=0, depth=0)


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    if part == 1:
        registers, program = process_sections(sections[:2])
        return run_part1(registers, program)
    else:
        registers, program = process_sections(sections[2:4])
        return run_part2(registers, program)
