"""A pytest test module that tests the functions in the package aoc.aoc2024.  Each test is
parameterized as follows:
- puzzle: an integer in the range 1..25 inclusive
- input_type: either "example" or "full"
- part: either 1 or 2

puzzle is used to determine a module to load, e.g. aoc.aoc2024.code03 when puzzle is 3.

each such module has a function run that takes puzzle, input_type and part as arguments
and returns a value.

each parameterized test should call run with the appropriate arguments and check the
return values against the expected results for the given puzzle, input_type and part.
These are defined in a data structure for all tests stored in the testing code.

"""

import pytest
from pathlib import Path

INPUT_FILES_DIR = Path(__file__).parent / "data"
HEAVY_PUZZLES = {6, 24}
KWARGS = {
    # (puzzle, part, input_type) -> kwargs
    (14, 1, "example"): dict(grid_size=(11, 7)),
    (14, 2, "example"): dict(grid_size=(11, 7)),
    (14, 1, "full"): dict(grid_size=(101, 103)),
    (14, 2, "full"): dict(grid_size=(101, 103)),
    # the example input is different enough from the full input that trying to run the
    # same calculation on it doesn't make sense
    (24, 2, "example"): dict(skip=True),
}

EXPECTED_RESULTS = {
    1: {
        1: {"example": 11, "full": 1941353},
        2: {"example": 31, "full": 22539317},
    },
    2: {
        1: {"example": 2, "full": 598},
        2: {"example": 4, "full": 634},
    },
    3: {
        1: {"example": 161, "full": 188116424},
        2: {"example": 48, "full": 104245808},
    },
    4: {
        1: {"example": 18, "full": 2458},
        2: {"example": 9, "full": 1945},
    },
    5: {
        1: {"example": 143, "full": 5762},
        2: {"example": 123, "full": 4130},
    },
    6: {
        1: {"example": 41, "full": 4433},
        2: {"example": 6, "full": 1516},
    },
    7: {
        1: {"example": 3749, "full": 1153997401072},
        2: {"example": 11387, "full": 97902809384118},
    },
    8: {
        1: {"example": 14, "full": 261},
        2: {"example": 34, "full": 898},
    },
    9: {
        1: {"example": 1928, "full": 6200294120911},
        2: {"example": 2858, "full": 6227018762750},
    },
    10: {
        1: {"example": 36, "full": 811},
        2: {"example": 81, "full": 1794},
    },
    11: {
        1: {"example": 55312, "full": 186175},
        2: {"example": None, "full": 220566831337810},
    },
    12: {
        1: {"example": 1930, "full": 1421958},
        2: {"example": 1206, "full": 885394},
    },
    13: {
        1: {"example": 480, "full": 31589},
        2: {"example": None, "full": 98080815200063},
    },
    14: {
        1: {"example": 12, "full": 218619324},
        2: {"example": None, "full": 6446},
    },
    15: {
        1: {"example": [10092, 2028, 908], "full": [1451928]},
        2: {"example": None, "full": [1462788]},
    },
    16: {
        1: {"example": [7036, 11048], "full": [108504]},
        2: {"example": [45, 64], "full": [538]},
    },
    17: {
        1: {"example": "4,6,3,5,6,3,5,2,1,0", "full": "7,5,4,3,4,5,3,4,6"},
        2: {"example": 117440, "full": 164278899142333},
    },
    18: {
        1: {"example": 22, "full": 438},
        2: {"example": (6, 1), "full": (26, 22)},
    },
    19: {
        1: {"example": 6, "full": 358},
        2: {"example": 16, "full": 600639829400603},
    },
    20: {
        1: {"example": 0, "full": 1323},
        2: {"example": 0, "full": 983905},
    },
    21: {
        1: {"example": 126384, "full": 237342},
        2: {"example": None, "full": 294585598101704},
    },
    22: {
        1: {"example": 37327623, "full": 18317943467},
        2: {"example": None, "full": 2018},
    },
    23: {
        1: {"example": 7, "full": 1599},
        2: {"example": "co,de,ka,ta", "full": "av,ax,dg,di,dw,fa,ge,kh,ki,ot,qw,vz,yw"},
    },
    24: {
        1: {"example": 2024, "full": 38869984335432},
        2: {"example": None, "full": "drg,gvw,jbp,jgc,qjb,z15,z22,z35"},
    },
    25: {
        1: {"example": 3, "full": 3284},
        2: {"example": None, "full": None},
    },
}


@pytest.mark.parametrize("input_type", ["example", "full"])
@pytest.mark.parametrize("part", [1, 2], ids=lambda part: f"part{part}")
@pytest.mark.parametrize(
    "puzzle",
    [
        pytest.param(
            puzzle, marks=([pytest.mark.heavy] if puzzle in HEAVY_PUZZLES else [])
        )
        for puzzle in EXPECTED_RESULTS
    ],
    ids=lambda puzzle: f"puzzle{puzzle:02d}",
)
def test_puzzle(puzzle, part, input_type):
    module_name = f"aoc.aoc2024.code{puzzle:02d}"
    code_module = __import__(module_name, fromlist=[""])

    file_name = f"{input_type}{puzzle:02d}.txt"
    file_path = Path(INPUT_FILES_DIR) / file_name

    with open(file_path, "r") as input_file:
        try:
            kwargs = KWARGS[(puzzle, part, input_type)]
        except KeyError:
            kwargs = dict()
        result = code_module.run(input_file, part, **kwargs)

    expected_result = EXPECTED_RESULTS[puzzle][part][input_type]

    if expected_result is not None:
        assert (
            result == expected_result
        ), f"Failed for puzzle {puzzle}, part {part}, input_type {input_type}"
