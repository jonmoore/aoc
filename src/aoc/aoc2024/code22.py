import argparse
from collections import defaultdict

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


def process_sections(sections):
    return list(map(int, sections[0]))


def mix(sn, n):
    return sn ^ n


def prune(sn):
    return sn % 2**24


def next_sn(osn):
    sn = osn
    sn = prune(mix(sn, sn * 64))
    sn = prune(mix(sn, sn // 32))
    sn = prune(mix(sn, sn * 2048))
    return sn


def advance_sn(sn, n):
    for _ in range(n):
        sn = next_sn(sn)
    return sn


assert next_sn(123) == 15887950


def run_part1(init_sns):
    return sum(advance_sn(sn, 2000) for sn in init_sns)


def run_part2(init_sns):
    total_value = defaultdict(int)
    for sn in init_sns:
        run = []
        run.append(sn)
        for _ in range(2000):
            sn = next_sn(sn)
            run.append(sn)
        local_price_info = dict()
        for i in range(1, 1998):
            seq = tuple(run[i + j] % 10 - run[i + j - 1] % 10 for j in range(4))
            value = run[i + 3] % 10
            if seq not in local_price_info:
                local_price_info[seq] = value
                total_value[seq] += value
    return max(total_value.values())


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    processed_input = process_sections(sections)
    if part == 1:
        return run_part1(processed_input)
    else:
        return run_part2(processed_input)
