import argparse
import itertools
from functools import cache
from pprint import pprint

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
    return sections[0]


NUMERIC_KEYPAD = dict(
    [
        ("7", (0, 0)),
        ("8", (0, 1)),
        ("9", (0, 2)),
        ("4", (1, 0)),
        ("5", (1, 1)),
        ("6", (1, 2)),
        ("1", (2, 0)),
        ("2", (2, 1)),
        ("3", (2, 2)),
        ("0", (3, 1)),
        ("A", (3, 2)),
    ]
)


def nkft2dkseqs(nkft):
    """Convert a from-to pair on the numeric keypad to candidate sequences of preses on
    the controlling directional keypad.  Each sequence consists of a (possibly empty)
    sequence of moves then an 'A' to press the 'to' key.
    """
    f, t = nkft
    frc = NUMERIC_KEYPAD[f]
    trc = NUMERIC_KEYPAD[t]
    vm = trc[0] - frc[0]
    if vm == 0:
        vseq = ""
    if vm > 0:
        vseq = "v" * vm
    if vm < 0:
        vseq = "^" * abs(vm)
    hm = trc[1] - frc[1]
    if hm == 0:
        hseq = ""
    if hm > 0:
        hseq = ">" * hm
    if hm < 0:
        hseq = "<" * abs(hm)

    # Assume it always makes sense to group together same-direction moves, so there are
    # either one or two candidate sequences to return
    if frc[1] == 0 and trc[0] == 3:
        return [hseq + vseq + "A"]
    if frc[0] == 3 and trc[1] == 0:
        return [vseq + hseq + "A"]
    if not vseq or not hseq:
        return [vseq + hseq + "A"]

    return [
        vseq + hseq + "A",
        hseq + vseq + "A",
    ]


def nkseq2dkseqs(nkseq):
    """Convert a sequence of buttons on the numeric keypad to candidate sequences of
    button presses on the controlling directional keypad.  The sequences are taken by
    concatenating directional sequences for each pair of successive buttons in nkseq.
    """
    dkftseqs = [nkft2dkseqs(nkft) for nkft in helpers.subsequences(nkseq, 2)]
    dkseqs = ["".join(s) for s in list(itertools.product(*dkftseqs))]
    return dkseqs


#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
DIRECTIONAL_KEYPAD = dict(
    [
        ("^", (0, 1)),
        ("A", (0, 2)),
        ("<", (1, 0)),
        ("v", (1, 1)),
        (">", (1, 2)),
    ]
)


def dkft2nextdkseqs(dkft):
    """Convert a from-to pair on a directional keypad to candidate sequences of presses on
    a controlling directional keypad at the next level.  Each sequence consists of a
    (possibly empty) sequence of moves then an 'A' to press the 'to' key.
    """

    f, t = dkft
    frc = DIRECTIONAL_KEYPAD[f]
    trc = DIRECTIONAL_KEYPAD[t]
    vm = trc[0] - frc[0]
    if vm == 0:
        vseq = ""
    if vm > 0:
        vseq = "v" * vm
    if vm < 0:
        vseq = "^" * abs(vm)
    hm = trc[1] - frc[1]
    if hm == 0:
        hseq = ""
    if hm > 0:
        hseq = ">" * hm
    if hm < 0:
        hseq = "<" * abs(hm)

    # Same assumptions as for the numeric keypad
    if frc[1] == 0 and trc[0] == 0:
        return [hseq + vseq + "A"]
    if frc[0] == 0 and trc[1] == 0:
        return [vseq + hseq + "A"]
    if not vseq or not hseq:
        return [vseq + hseq + "A"]
    return [
        vseq + hseq + "A",
        hseq + vseq + "A",
    ]


@cache
def dkft_cost(dkft, level):
    if level == 1:
        return 1
    return min(dkseq_cost(nextdkseq, level - 1) for nextdkseq in dkft2nextdkseqs(dkft))


@cache
def dkseq_cost(dkseq, level):
    return sum(dkft_cost(dkft, level) for dkft in helpers.subsequences("A" + dkseq, 2))


def run_cases(cases, n_levels):
    return sum(
        int(case[:-1])
        * min(dkseq_cost(dkseq, n_levels - 1) for dkseq in nkseq2dkseqs("A" + case))
        for case in cases
    )


def run_part1(cases):
    return run_cases(cases, n_levels=4)


def run_part2(cases):
    return run_cases(cases, n_levels=27)


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    processed_input = process_sections(sections)
    pprint(processed_input)
    if part == 1:
        return run_part1(processed_input)
    else:
        return run_part2(processed_input)
