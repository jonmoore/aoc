import itertools
from collections import defaultdict

import aoc.helpers as helpers
from aoc.helpers import RectGrid


def process_sections(sections):
    return list(map(RectGrid, sections))


def grid_edges(grid):
    edges = defaultdict(set)
    for pos in grid:
        if grid[pos] != "#":
            for neighbor in grid.neighbors(pos):
                if grid[neighbor] != "#":
                    edges[pos].add(neighbor)
    return edges


def neighbor_costs(state, edges, sign=1):
    pos, dirn = state
    neighboring_dirns = "<>" if dirn in "^v" else "^v"

    for neighboring_dirn in neighboring_dirns:
        yield (pos, neighboring_dirn), 1000
    for neighboring_pos in edges[pos]:
        if (
            sign * (pos[0] - neighboring_pos[0]),
            sign * (pos[1] - neighboring_pos[1]),
        ) != {
            ">": (0, 1),
            "<": (0, -1),
            "^": (-1, 0),
            "v": (1, 0),
        }[dirn]:
            continue
        yield (neighboring_pos, dirn), 1


def score1(grid, start, end):
    # We want a graph of positions to positions
    # The "real" graph includes rotation but find those dynamically
    edges = grid_edges(grid)
    to_score = set(itertools.product(edges, "<>^v"))

    HUGE = 10**9

    scores = defaultdict(lambda: HUGE)
    fringe = set()

    def update_score(state, score):
        scores[state] = min(scores[state], score)
        for n_state, cost in neighbor_costs(state, edges):
            scores[n_state] = min(scores[n_state], score + cost)
            if n_state in to_score:
                fringe.add(n_state)

        to_score.remove(state)
        fringe.remove(state)

    for dirn in "<>^v":
        fringe.add((end, dirn))
        scores[(end, dirn)] = 0
        update_score((end, dirn), 0)

    while to_score:
        min_state, min_score = None, None
        for state in fringe:
            if min_state is None or scores[state] < min_score:
                min_state = state
                min_score = scores[state]
        assert min_state is not None
        update_score(min_state, min_score)

    return scores[(start, ">")], scores


def grid_match(grid, c):
    matches = [pos for pos in grid if grid[pos] == c]

    assert len(matches) == 1
    return matches[0]


def run_part1(grids):
    return [
        score1(grid, start=grid_match(grid, "S"), end=grid_match(grid, "E"))[0]
        for grid in grids
    ]


def len_optimal_states(grid, start, end):
    target, scores = score1(grid, start=start, end=end)
    edges = grid_edges(grid)

    start_states = {k for k, v in scores.items() if k[0] == start and v == target}

    optimal_states = start_states.copy()
    to_process = start_states.copy()

    while to_process:
        processing = to_process.pop()
        for n_state, cost in neighbor_costs(processing, edges, sign=-1):
            if (
                processing in optimal_states
                and scores[n_state] + cost == scores[processing]
            ):
                optimal_states.add(n_state)
                to_process.add(n_state)

    optimal_pos = {pos for pos, dirn in optimal_states}
    return len(optimal_pos)


def run_part2(grids):
    return [
        len_optimal_states(grid, start=grid_match(grid, "S"), end=grid_match(grid, "E"))
        for grid in grids
    ]


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    grids = process_sections(sections)
    if part == 1:
        return run_part1(grids)
    else:
        return run_part2(grids)
