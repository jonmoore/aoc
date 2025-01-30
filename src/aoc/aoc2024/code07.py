import aoc.helpers as helpers
from dataclasses import dataclass
from functools import reduce


@dataclass
class Case:
    target: int
    operands: list[int]


def parse_case(line):
    parts = line.split(":")
    return Case(
        target=int(parts[0]),
        operands=[int(el) for el in parts[1].strip().split()],
    )


_POW10 = [10**p for p in range(20)]


def cat(a, b):
    digits = 1
    lb, ub = 1, 10
    while True:
        if lb <= b < ub:
            break
        digits += 1
        lb, ub = ub, 10 * ub
    return a * _POW10[digits] + b


def possibles(operands, *, max_value, num_ops=2):
    assert operands
    assert isinstance(max_value, int)
    assert num_ops in (2, 3)

    values = {operands[0]}

    for operand in operands[1:]:
        new_values = set()
        for v in values:
            if num_ops == 2:
                els = v + operand, v * operand
            else:
                els = v + operand, v * operand, cat(v, operand)
            for el in els:
                if el <= max_value:
                    new_values.add(el)
        values = new_values
    return values


def run_part(*, cases, num_ops):
    total, max_len = reduce(
        lambda a, b: (a[0] + b[0], max(a[1], b[1])),
        (
            (case.target, len(v))
            for case in cases
            if case.target
            in (v := possibles(case.operands, max_value=case.target, num_ops=num_ops))
        ),
    )
    return total, max_len


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    cases = [parse_case(line) for line in sections[0]]

    total, max_len = run_part(cases=cases, num_ops=2)
    if part == 1:
        return total
    if part == 2:
        total, max_len = run_part(cases=cases, num_ops=3)
        return total
