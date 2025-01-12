import re
from functools import cache


import aoc.helpers as helpers


def process_sections(sections):
    towels = sections[0][0].split(", ")
    designs = sections[1]
    return towels, designs


def run_part1(towels, designs):
    pattern = "(" + "|".join(towels) + ")*"
    return sum(bool(re.fullmatch(pattern, design)) for design in designs)


@cache
def count_matches(towels, design):
    return sum(
        1 if design == towel else count_matches(towels, design[len(towel) :])
        for towel in towels
        if design.startswith(towel)
    )


def run_part2(towels, designs):
    towels = tuple(towels)
    designs = tuple(designs)
    return sum(count_matches(towels, design) for design in designs)


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    processed_input = process_sections(sections)
    #    pprint(processed_input)
    if part == 1:
        return run_part1(*processed_input)
    else:
        return run_part2(*processed_input)
