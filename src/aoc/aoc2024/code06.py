import aoc.helpers as helpers
from enum import Enum
import copy

POS_MARKERS = "<>^v"


class Direction(Enum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"


def find_guard_position(grid):
    guard_positions = [(i, j) for (i, j), value in grid.items() if value in POS_MARKERS]
    assert len(guard_positions) == 1
    return guard_positions[0]


def find_guard_direction(grid):
    return Direction(grid[find_guard_position(grid)]).value


_incs = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}
_rotations = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",
}


def gen_move(grid, guard_position, guard_direction, nrows, ncols):
    """Generate a move for the guard in the grid.

    Returns:

    If the guard moves off the grid returns (None, None).  If the guard moves to a new
    position on the grid, returns the guard's new position and direction.

    Raises:

    ValueError if no valid new position can be found.
    """
    for i in range(4):
        inc0, inc1 = _incs[guard_direction]
        new_position0 = guard_position[0] + inc0
        new_position1 = guard_position[1] + inc1
        if 0 <= new_position0 < nrows and 0 <= new_position1 < ncols:
            if grid[new_position0, new_position1] != "#":
                return (new_position0, new_position1), guard_direction
        else:
            return None, None
        guard_direction = _rotations[guard_direction]
    raise ValueError("Cannot find a valid move for the guard!")


def part1(grid):
    grid = copy.deepcopy(grid)
    start_guard_position = find_guard_position(grid)
    start_guard_direction = find_guard_direction(grid)

    guard_position = start_guard_position
    guard_direction = start_guard_direction
    while True:
        grid[guard_position] = "X"
        guard_position, guard_direction = gen_move(
            grid, guard_position, guard_direction, grid.nrows, grid.ncols
        )
        if guard_position is None:
            # indicates the guard moved out of the grid, so we're done
            break
    return [ij for ij, c in grid.items() if c == "X"]


def obstructs(grid, i, j, guard_position, guard_direction):
    visited = set()
    nrows, ncols = grid.nrows, grid.ncols
    while True:
        visited.add((guard_position, guard_direction))
        guard_position, guard_direction = gen_move(
            grid, guard_position, guard_direction, nrows, ncols
        )
        if guard_position is None:
            return False
        if (guard_position, guard_direction) in visited:
            return True


def generate_obstructions(grid, candidates):
    """This takes about 13 seconds brute force, can probably be optimized with a
    least-common-ancestor algorithm.
    """

    skip_values = POS_MARKERS + "#"
    start_guard_position = find_guard_position(grid)
    start_guard_direction = Direction(grid[start_guard_position]).value
    candidates = set(candidates)

    for i, j in candidates:
        value = grid[i, j]
        if value in skip_values:
            continue
        grid[i, j] = "#"
        if obstructs(grid, i, j, start_guard_position, start_guard_direction):
            yield (i, j)
        grid[i, j] = value


def run(input_file, part):
    sections: list[list[str]] = helpers.read_input_sections(input_file)

    start_text = sections[0]
    start_grid = helpers.RectGrid(start_text)
    xs = part1(start_grid)

    if part == 1:
        return len(xs)
    else:
        obstructions = list(generate_obstructions(start_grid, candidates=xs))
        return len(obstructions)
