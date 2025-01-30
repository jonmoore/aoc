import argparse
import dataclasses
import re
from dataclasses import dataclass

import aoc.helpers as helpers
from aoc.helpers import PuzzleSize


def parse_args() -> PuzzleSize:
    parser = argparse.ArgumentParser(description="Process input types.")

    parser.add_argument(
        "--input-type",
        "-i",
        required=True,
        choices=[input_type.value for input_type in PuzzleSize],
        help="Specify the input type (example or full).",
    )

    args = parser.parse_args()

    return PuzzleSize(args.input_type)


@dataclass
class Machine:
    a: tuple
    b: tuple
    prize: tuple


def process_sections(sections):
    number_pattern = re.compile(r"X[+=](\d+), Y[+=](\d+)")

    def extract_ints(s: str) -> tuple[int]:
        match = number_pattern.search(s)
        assert match
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            return (x, y)

    return [
        Machine(
            a=extract_ints(section[0]),
            b=extract_ints(section[1]),
            prize=extract_ints(section[2]),
        )
        for section in sections
    ]


def cost_analysis(machine: Machine) -> tuple[bool, int]:
    a = machine.a[0]
    b = machine.b[0]
    c = machine.a[1]
    d = machine.b[1]

    det = a * d - b * c
    assert det != 0

    """
    a b  d -b  = det 0
    c d  -c a    0 det
    """

    p0 = machine.prize[0]
    p1 = machine.prize[1]

    ma = (d * p0 - b * p1) / det
    mb = (-c * p0 + a * p1) / det

    rma = round(ma)
    rmb = round(mb)

    has_soln = all(
        [
            abs(rma - ma) < 0.001,
            0 <= rma,
            abs(rmb - mb) < 0.001,
            0 <= rmb,
        ]
    )

    if not has_soln:
        return False, 0

    cost_a = 3
    cost_b = 1

    return True, rma * cost_a + rmb * cost_b


def full_cost_analysis(machines, offset):
    count_solns = 0
    total_cost = 0
    for machine in machines:
        machine2 = dataclasses.replace(
            machine,
            prize=(
                machine.prize[0] + offset[0],
                machine.prize[1] + offset[1],
            ),
        )
        has_soln, cost = cost_analysis(machine2)
        # pprint(f"{machine2=}, {has_soln=}, {cost=}")
        count_solns += has_soln
        total_cost += cost

    print(f"{count_solns=}, {total_cost=}")
    return total_cost


def run_part1(machines):
    offset = (0, 0)
    return full_cost_analysis(machines, offset)


def run_part2(machines):
    offset = (10000000000000, 10000000000000)
    return full_cost_analysis(machines, offset)


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    machines = process_sections(sections)
    if part == 1:
        return run_part1(machines)
    else:
        return run_part2(machines)
