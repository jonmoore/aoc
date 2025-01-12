import itertools

import aoc.helpers as helpers
from aoc.helpers import RectGrid


def process_sections(sections):
    def widen_row(row):
        return "".join(
            {
                "#": "##",
                "O": "[]",
                ".": "..",
                "@": "@.",
            }[char]
            for char in row
        )

    def widen_section(section):
        return [widen_row(row) for row in section]

    return [
        (
            RectGrid(sections[2 * i]),
            RectGrid(widen_section(sections[2 * i])),
            "".join(sections[2 * i + 1]),
        )
        for i in range(len(sections) // 2)
    ]


def make_move(grid, pos, move):
    assert grid[pos] == "@"

    inc = {
        "<": (0, -1),
        ">": (0, 1),
        "^": (-1, 0),
        "v": (1, 0),
    }[move]

    def step(pos, n):
        return (pos[0] + n * inc[0], pos[1] + n * inc[1])

    for n in itertools.count(1):
        assert n < 1000
        pos2 = step(pos, n)
        if grid[pos2] in ".#":
            break

    if grid[pos2] == "#":
        return grid, pos

    assert grid[pos2] == "."
    pos_new = step(pos, 1)
    grid[pos2] = grid[step(pos2, -1)]
    grid[pos_new] = "@"
    grid[pos] = "."
    return grid, pos_new


def run_part1(processed_input):
    ret = []
    for grid, _, moves in processed_input:
        for pos in grid:
            if grid[pos] == "@":
                break

        for move in moves:
            grid, pos = make_move(grid, pos, move)

        gps_score = sum(100 * r + c for r, c in grid if grid[r, c] == "O")
        ret.append(gps_score)
    return ret


def make_move2(grid, pos, move):
    assert grid[pos] == "@"

    inc = {
        "<": (0, -1),
        ">": (0, 1),
        "^": (-1, 0),
        "v": (1, 0),
    }[move]

    def step(pos, n):
        return (pos[0] + n * inc[0], pos[1] + n * inc[1])

    def fringe(pre_fringe, move):
        match move:
            case "<":
                assert len(pre_fringe) == 1
                return [(pre_fringe[0][0], pre_fringe[0][1] - 1)]
            case ">":
                assert len(pre_fringe) == 1
                return [(pre_fringe[-1][0], pre_fringe[-1][1] + 1)]
            case "^":
                assert max(pos[0] for pos in pre_fringe) == min(
                    pos[0] for pos in pre_fringe
                )
                return [(pos[0] - 1, pos[1]) for pos in pre_fringe]
            case "v":
                assert max(pos[0] for pos in pre_fringe) == min(
                    pos[0] for pos in pre_fringe
                )
                return [(pos[0] + 1, pos[1]) for pos in pre_fringe]
        breakpoint()
        assert False

    def blocked(to_move, move):
        return any(grid[pos] == "#" for pos in fringe(to_move[-1], move))

    def free(to_move, move):
        return all(grid[pos] == "." for pos in fringe(to_move[-1], move))

    def complete_box(pos):
        assert grid[pos] in "[]"
        if grid[pos] == "[":
            return pos, (pos[0], pos[1] + 1)
        if grid[pos] == "]":
            return pos, (pos[0], pos[1] - 1)

    def fringe2to_move(posns):
        new_posns = []
        for pos in posns:
            if grid[pos] == ".":
                continue
            new_posns.extend(complete_box(pos))
        return sorted(set(new_posns))

    def expand(to_move, move):
        fr = fringe(to_move[-1], move)
        assert move in "<>^v"
        match move:
            case "<":
                return to_move + [fr]
            case ">":
                return to_move + [fr]
            case "^":
                return to_move + [fringe2to_move(fr)]
            case "v":
                return to_move + [fringe2to_move(fr)]

    to_move = [[pos]]
    for n in itertools.count(1):
        assert n < 1000
        if blocked(to_move, move):
            return grid, pos
        if free(to_move, move):
            break
        to_move = expand(to_move, move)

    for tm in to_move[::-1]:
        for sq_move in tm:
            match move:
                case "<":
                    sq_to = (sq_move[0], sq_move[1] - 1)
                case ">":
                    sq_to = (sq_move[0], sq_move[1] + 1)
                case "^":
                    sq_to = (sq_move[0] - 1, sq_move[1])
                case "v":
                    sq_to = (sq_move[0] + 1, sq_move[1])
            grid[sq_to], grid[sq_move] = grid[sq_move], "."
            if sq_move == pos:
                pos = sq_to

    return grid, pos


def run_part2(processed_input):
    ret = []
    for _, grid, moves in processed_input:
        for pos in grid:
            if grid[pos] == "@":
                break

        for move in moves:
            grid, pos = make_move2(grid, pos, move)

        gps_score = sum(100 * r + c for r, c in grid if grid[r, c] in "[O")
        ret.append(gps_score)
    return ret


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    processed_input = process_sections(sections)
    if part == 1:
        return run_part1(processed_input)
    else:
        return run_part2(processed_input)
