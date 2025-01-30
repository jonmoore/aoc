from collections import defaultdict

import aoc.helpers as helpers
from aoc.helpers import RectGrid


def process_sections(sections):
    width, height, to_read = map(int, sections[0][0].split())

    xys = [tuple(map(int, row.split(","))) for row in sections[1]]
    return width, height, to_read, xys


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

        assert best not in green and best in yellow
        green[best] = yellow[best]
        del yellow[best]
        assert best not in yellow and best in green
    return dict(green)


def run_part1(width, height, to_read, xys):
    grid = RectGrid(["." * width for _ in range(height)])

    for x, y in xys[:to_read]:
        grid[y, x] = "#"

    dists = dijkstra(grid, 0, 0)
    print(f"{dists[(height-1, width-1)]=}")
    return dists[(height - 1, width - 1)]


def run_part2(width, height, to_read, xys):
    def has_path(to_read):
        grid = RectGrid(["." * width for _ in range(height)])
        for x, y in xys[:to_read]:
            grid[y, x] = "#"
        dists = dijkstra(grid, 0, 0)
        retval = (height - 1, width - 1) in dists
        print(f"{(to_read,retval)=}")
        return retval

    import bisect

    index = bisect.bisect_left(range(len(xys)), True, key=lambda i: not has_path(i))

    print(f"{index=}")
    print(f"{xys[index-1]=}")
    return xys[index - 1]


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    processed_input = process_sections(sections)
    if part == 1:
        return run_part1(*processed_input)
    else:
        return run_part2(*processed_input)
