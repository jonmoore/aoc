import itertools
from collections import defaultdict
import aoc.helpers as helpers
from aoc.helpers import RectGrid


def group_antennas_by_id(grid: RectGrid) -> dict:
    """Parse the grid to find and group antennas by their identifiers."""
    antenna_dict = defaultdict(list)
    for (i, j), value in grid.items():
        if value != ".":
            antenna_dict[value].append((i, j))
    return dict(antenna_dict)


def calculate_new_position(i1: int, j1: int, i2: int, j2: int, steps: int) -> tuple:
    """Calculate new grid position based on steps along the line connecting two points."""
    return i1 + steps * (i2 - i1), j1 + steps * (j2 - j1)


def generate_fundamental_antinodes(
    grid: RectGrid, i1: int, j1: int, i2: int, j2: int
) -> iter:
    """Yield antinodes that exist at fundamental steps relative to the two points."""
    assert (i1, j1) < (i2, j2)
    for steps in [-1, 2]:
        pos = calculate_new_position(i1, j1, i2, j2, steps)
        if pos in grid:
            yield pos


def generate_resonant_antinodes(
    grid: RectGrid, i1: int, j1: int, i2: int, j2: int
) -> iter:
    """Yield antinodes that exist at a range of resonant steps for the two points."""
    assert (i1, j1) < (i2, j2)
    for step_range in [itertools.count(), itertools.count(-1, -1)]:
        for steps in step_range:
            pos = calculate_new_position(i1, j1, i2, j2, steps)
            if pos in grid:
                yield pos
            else:
                break


def generate_antinodes_for_pairs(
    *, grid: RectGrid, antenna_dict: dict, antinode_gen: callable
) -> dict:
    """Generate antinodes for all pairs of antennas using a specified generator."""
    antinode_dict = defaultdict(list)
    for letter, positions in antenna_dict.items():
        for i1, j1 in positions:
            for i2, j2 in positions:
                if (i1, j1) < (i2, j2):
                    antinode_dict[letter].extend(antinode_gen(grid, i1, j1, i2, j2))
    return dict(antinode_dict)


def calculate_antinodes_for_mode(*, grid: RectGrid, mode: str) -> None:
    """Run the calculation of antinodes for the specified mode."""
    antinode_gen = {
        "fundamental": generate_fundamental_antinodes,
        "resonant": generate_resonant_antinodes,
    }[mode]
    antenna_dict = group_antennas_by_id(grid)
    antinode_dict = generate_antinodes_for_pairs(
        grid=grid, antenna_dict=antenna_dict, antinode_gen=antinode_gen
    )
    unique_antinodes = {pos for posns in antinode_dict.values() for pos in posns}
    return len(unique_antinodes)


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    grid = RectGrid(sections[0])
    if part == 1:
        return calculate_antinodes_for_mode(grid=grid, mode="fundamental")
    else:
        return calculate_antinodes_for_mode(grid=grid, mode="resonant")
