import math

from collections import Counter
from dataclasses import dataclass

import aoc.helpers as helpers


@dataclass
class Robot:
    p: tuple[int]
    v: tuple[int]

    @staticmethod
    def from_str(s: str):
        def str2tup(ss):
            return tuple(map(int, ss.split("=")[1].split(",")))

        p_part, v_part = s.split()
        return Robot(
            p=str2tup(p_part),
            v=str2tup(v_part),
        )


def process_sections(sections):
    return [Robot.from_str(line) for line in sections[0]]


def quad(p, grid_size):
    def sect(n, size):
        if 0 <= n < size // 2:
            return "first"
        elif 2 * n + 1 == size:
            return None
        else:
            return "second"

    sect0 = sect(p[0], grid_size[0])
    sect1 = sect(p[1], grid_size[1])

    if sect0 is None or sect1 is None:
        return None

    return (sect0, sect1)


def positions_after(robots, grid_size, t):
    return [
        ((r.p[0] + t * r.v[0]) % grid_size[0], (r.p[1] + t * r.v[1]) % grid_size[1])
        for r in robots
    ]


def calculate_safety_factor(positions, grid_size):
    counts = Counter(
        q for position in positions if (q := quad(position, grid_size)) is not None
    )
    return math.prod(counts.values())


def run_part1(robots, grid_size):
    positions = positions_after(robots, grid_size, t=100)
    return calculate_safety_factor(positions, grid_size)


@dataclass
class Stats:
    t: int
    max_column_count: int
    max_row_count: int
    safety_factor: int


def calculate_stats(robots, grid_size, t):
    positions = positions_after(robots, grid_size, t=t)

    # originally implemented entropy too but max is enough given the distributions
    #
    # safety factor also works (the tree configuration has the minimum safety factor and
    # is an outlier) but it would also have been natural for the tree configuration to be
    # highly symmetric and so have maximum safety factor

    # columns are lines of constant x, so column counts use index [0] while row counts use
    # index [1]
    def max_count(ind):
        return max(Counter(position[ind] for position in positions).values())

    return Stats(
        t=t,
        max_column_count=max_count(0),
        max_row_count=max_count(1),
        safety_factor=calculate_safety_factor(positions, grid_size),
    )


def show_distribution(values):
    min_value = min(values)
    max_value = max(values)
    value_counts = Counter(values)
    max_value_count = max(value_counts.values())
    for i in range(min_value, max_value + 1):
        num_chars = value_counts[i] * 80 // max_value_count
        print(f"{i:>4}: {value_counts[i]:>6}: {'.'*num_chars}")


def show_positions(positions, grid_size):
    """Show the robot positions by printing out an x-y grid"""
    for y in range(grid_size[1]):
        print(
            "".join(("x" if (x, y) in positions else " ") for x in range(grid_size[0]))
        )


def run_part2(robots, grid_size):
    # This puzzle, sigh. Thought: trees have vertical bits so expect column occupancy to
    # be concentrated when the tree configuration is reached.  Try the same for rows too.

    # given the periodicity you could reduced the running time to O(rows+columns) rather
    # than O(rows*columns) but it runs quickly at the given size anyhow.
    stats = [
        calculate_stats(robots, grid_size, t=t) for t in range(math.prod(grid_size))
    ]
    max_column_counts = [s.max_column_count for s in stats]
    max_max_column_counts = max(max_column_counts)
    show_distribution(max_column_counts)

    max_row_counts = [s.max_row_count for s in stats]
    max_max_row_counts = max(max_row_counts)
    show_distribution(max_row_counts)

    hits = []
    for s in stats:
        if (
            s.max_column_count == max_max_column_counts
            and s.max_row_count == max_max_row_counts
        ):
            hits.append(s.t)
            positions = positions_after(robots, grid_size, t=s.t)
            show_positions(positions=positions, grid_size=grid_size)
    assert len(hits) == 1
    return hits[0]


def run(input_file, part, grid_size):
    sections = helpers.read_input_sections(input_file)
    robots = process_sections(sections)
    if part == 1:
        return run_part1(robots, grid_size)
    else:
        return run_part2(robots, grid_size)
