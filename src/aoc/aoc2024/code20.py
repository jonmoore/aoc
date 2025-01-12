import argparse
from collections import defaultdict, Counter

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


def process_sections(sections):
    return RectGrid(sections[0])


def dijkstra(grid, r0, c0):
    HUGE_DIST = 2**20
    green = defaultdict(lambda: HUGE_DIST)
    yellow = defaultdict(lambda: HUGE_DIST)
    yellow[(r0, c0)] = 0

    while yellow:
        best, best_dist = min(
            ((cand, dist) for cand, dist in yellow.items()), key=lambda cd: cd[1]
        )

        neighbors = [
            pos for pos in grid.neighbors(best) if grid[pos] == "." and pos not in green
        ]

        for n in neighbors:
            yellow[n] = min(yellow[n], best_dist + 1)

        # print(best, best_dist)
        # print("neighbors", neighbors)
        assert best not in green and best in yellow
        green[best] = yellow[best]
        del yellow[best]
        assert best not in yellow and best in green
    count_open = sum(1 for pos in grid if grid[pos] != "#")
    assert count_open == len(green)
    return dict(green)


def run_part1(grid):
    starts = [pos for pos in grid if grid[pos] == "S"]
    assert len(starts) == 1
    ends = [pos for pos in grid if grid[pos] == "E"]
    assert len(ends) == 1
    start, end = starts[0], ends[0]
    grid[start] = "."
    grid[end] = "."

    d_start = dijkstra(grid, start[0], start[1])
    d_end = dijkstra(grid, end[0], end[1])
    assert d_start[start] == 0
    assert d_end[end] == 0
    assert d_end[start] == d_start[end]
    for pos in d_start:
        assert d_start[pos] + d_end[pos] == d_start[end]
    baseline = d_start[end]
    print("baseline", baseline)

    cheats = []
    for cheat1 in grid:
        if grid[cheat1] == ".":
            # wlog there's at least one blocked square being used
            continue
        for cheat2 in grid.neighbors(cheat1):
            # ok if cheat2 is clear
            for n1 in grid.neighbors(cheat1):
                if n1 != cheat2 and n1 in d_start:
                    if cheat2 in d_end:
                        cheat_dist = d_start[n1] + 2 + d_end[cheat2]
                        if cheat_dist < baseline:
                            cheats.append((n1, cheat1, cheat2, baseline - cheat_dist))
    counts = Counter(cheat[3] for cheat in cheats)
    saves_100 = sum(count for savings, count in counts.items() if savings >= 100)
    return saves_100


def run_part2(grid):
    starts = [pos for pos in grid if grid[pos] == "S"]
    assert len(starts) == 1
    ends = [pos for pos in grid if grid[pos] == "E"]
    assert len(ends) == 1
    start, end = starts[0], ends[0]
    grid[start] = "."
    grid[end] = "."

    d_start = dijkstra(grid, start[0], start[1])
    d_end = dijkstra(grid, end[0], end[1])
    assert d_start[start] == 0
    assert d_end[end] == 0
    assert d_end[start] == d_start[end]
    for pos in d_start:
        assert d_start[pos] + d_end[pos] == d_start[end]
    baseline = d_start[end]
    print("baseline", baseline)

    cheats = []
    radius = 20

    threshold = 50
    for cheat0 in grid:
        if grid[cheat0] != "." or cheat0 not in d_start:
            # start the cheat at a reachable open square
            continue
        for c1r in range(
            max(0, cheat0[0] - radius), min(grid.nrows, cheat0[0] + radius + 1)
        ):
            radius2 = radius - abs(c1r - cheat0[0])
            for c1c in range(
                max(0, cheat0[1] - radius2), min(grid.ncols, cheat0[1] + radius2 + 1)
            ):
                cheat1 = (c1r, c1c)
                if grid[cheat1] != "." or cheat1 not in d_end:
                    continue
                cheat_dist = (
                    d_start[cheat0]
                    + abs(cheat0[0] - cheat1[0])
                    + abs(cheat0[1] - cheat1[1])
                    + d_end[cheat1]
                )
                if baseline - cheat_dist >= threshold:
                    cheats.append((cheat0, cheat1, baseline - cheat_dist))
    counts = Counter(cheat[2] for cheat in cheats)
    saves_100 = sum(count for savings, count in counts.items() if savings >= 100)
    return saves_100


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    grid = process_sections(sections)
    if part == 1:
        return run_part1(grid)
    else:
        return run_part2(grid)
