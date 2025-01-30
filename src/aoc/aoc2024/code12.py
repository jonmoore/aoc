import itertools

import aoc.helpers as helpers
from aoc.helpers import RectGrid


def process_sections(sections) -> RectGrid:
    return RectGrid(sections[0])


def calculate_hood(grid, pos):
    hood = {pos}
    to_process = set(hood)
    while to_process:
        cur_pos = to_process.pop()
        hood.add(cur_pos)
        for neighbor in grid.neighbors(cur_pos):
            if neighbor in hood:
                continue
            if grid[neighbor] != grid[pos]:
                continue
            to_process.add(neighbor)
    return hood


def calculate_perimeter(grid, hood):
    perimeter = 0
    for cur_pos in hood:
        num_equal_neighbors = len(
            [n for n in grid.neighbors(cur_pos) if grid[n] == grid[cur_pos]]
        )
        perimeter += 4 - num_equal_neighbors
    return perimeter


def tuple_add(tuple_a, tuple_b):
    return tuple(a + b for (a, b) in zip(tuple_a, tuple_b))


def equal_neighbors(grid, pos):
    for n in grid.neighbors(pos):
        if grid[pos] == grid[n]:
            yield n


def calculate_sides(grid, hood):
    """Calculate the number of distinct sides for the neighborhood.  It might be easier to
    do this instead by grouping boundary normals of hood by direction and by row or column
    as appropriate and counting runs.
    """
    ALL_INCS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # NESW

    def d2i(d):
        return ALL_INCS[d]

    def turn_right(dirn):
        return (dirn + 1) % 4

    def turn_left(dirn):
        return (dirn - 1) % 4

    sides_checked = set()
    sides = 0
    for start_pos, start_dirn in itertools.product(hood, range(4)):
        if (start_pos, start_dirn) in sides_checked:
            continue

        # skip internal edges
        if tuple_add(start_pos, d2i(start_dirn)) in hood:
            continue

        print(f"{(start_pos, start_dirn)=}")
        pos, dirn = start_pos, start_dirn
        while True:
            pos2, dirn2 = pos, turn_right(dirn)
            while True:
                pos3 = tuple_add(pos2, d2i(dirn2))
                if pos3 not in grid:
                    break
                if grid[pos3] != grid[start_pos]:
                    break
                pos2 = pos3
                dirn2 = turn_left(dirn2)

            pos = pos2
            if dirn2 != dirn:
                sides += 1
            dirn = dirn2
            sides_checked.add((pos, dirn))

            if (pos, dirn) == (start_pos, start_dirn):
                break

    return sides


def run_part1(grid: RectGrid) -> int:
    seen = set()
    total = 0
    for pos in grid:
        if pos in seen:
            continue
        print(f"seen {len(seen)} of {grid.nrows*grid.ncols}")
        hood = calculate_hood(grid, pos)
        seen |= hood
        area = len(hood)
        perimeter = calculate_perimeter(grid, hood)
        total += area * perimeter
    return total


def run_part2(grid: RectGrid) -> int:
    seen = set()
    total = 0
    for pos in grid:
        if pos in seen:
            continue
        print(f"seen {len(seen)} of {grid.nrows*grid.ncols}")
        hood = calculate_hood(grid, pos)
        seen |= hood
        area = len(hood)
        sides = calculate_sides(grid, hood)
        print(f"{(area,sides)=}")
        total += area * sides
    return total


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    processed_input = process_sections(sections)
    if part == 1:
        return run_part1(processed_input)
    else:
        return run_part2(processed_input)
