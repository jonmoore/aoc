import argparse
from dataclasses import dataclass
from collections import defaultdict

import aoc.helpers as helpers
from aoc.helpers import PuzzleSize, RectGrid


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


def process_sections(sections) -> RectGrid:
    return RectGrid(sections[0])


@dataclass
class Step:
    pos1: tuple
    pos2: tuple
    height1: int
    height2: int


def height(grid, pos) -> int:
    return int(grid[pos])


def calculate_trail_heads(grid) -> set:
    return {pos for pos in grid if height(grid, pos) == 0}


def calculate_steps(grid) -> list:
    return [
        Step(pos1, pos2, height(grid, pos1), height(grid, pos2))
        for pos1 in grid
        for pos2 in grid.neighbors(pos1)
        if height(grid, pos1) + 1 == height(grid, pos2)
    ]


def run_part1(grid) -> int:
    trail_heads = calculate_trail_heads(grid)
    steps = calculate_steps(grid)

    upstream_trail_heads = defaultdict(set, {pos: {pos} for pos in trail_heads})
    for step in sorted(steps, key=lambda s: (s.height1, s.height2)):
        upstream_trail_heads[step.pos2] |= upstream_trail_heads[step.pos1]
    score = sum(
        len(trail_heads)
        for pos, trail_heads in upstream_trail_heads.items()
        if height(grid, pos) == 9
    )
    print(score)
    return score


def run_part2(grid) -> int:
    trail_heads = calculate_trail_heads(grid)
    steps = calculate_steps(grid)

    upstream_path_counts = defaultdict(int, {pos: 1 for pos in trail_heads})
    for step in sorted(steps, key=lambda s: (s.height1, s.height2)):
        upstream_path_counts[step.pos2] += upstream_path_counts[step.pos1]
    score = sum(
        path_count
        for pos, path_count in upstream_path_counts.items()
        if height(grid, pos) == 9
    )
    print(score)
    return score


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    grid = process_sections(sections)

    if part == 1:
        return run_part1(grid)
    else:
        return run_part2(grid)
