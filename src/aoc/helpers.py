from collections import defaultdict
import itertools
from typing import Tuple, Iterator
from dataclasses import dataclass
from enum import Enum
import time


def transpose(matrix):
    return list(zip(*matrix))


def read_input_sections(input_file) -> list[list[str]]:
    """This function reads the content of a text file, splits it into sections, with each
    section being split further into a list of strings, each representing a line within that
    section. Sections are identified by two line breaks (one empty line).

    # Example usage:
    # with open('example.txt', "r", encoding="utf-8") as input_file:
    #     sections = read_input_sections(input_file)
    #     for section in sections:
    #         print(section)
    """
    raw_sections = input_file.read().split("\n\n")
    sections = [section.splitlines() for section in raw_sections]
    return sections


def subsequences(lst: list, n: int) -> Iterator[Tuple]:
    """Generate subsequences of size n

    Example usage:

    >>> import aoc.helpers as h
    >>> from aoc.helpers import subsequences
    >>> list(subsequences(range(5), 3))
    [(0, 1, 2), (1, 2, 3), (2, 3, 4)]

    """
    iterators = itertools.tee(lst, n)

    for i, it in enumerate(iterators):
        next(itertools.islice(it, i, i), None)

    return zip(*iterators)


class DirectedGraph:
    def __init__(self, pairs: list[tuple[int, int]]) -> None:
        """Initialize directed graph with pairs.
        Args:
            pairs: A list of ordered pairs (bef, aft) defining edges.
        """
        self.succs: dict[int, list[int]] = defaultdict(list)
        self.preds: dict[int, list[int]] = defaultdict(list)
        for bef, aft in pairs:
            self.succs[bef].append(aft)
            self.preds[aft].append(bef)

    def dfwalk_subtree(
        self, root: int, to_visit: set[int], visited: dict[int, bool]
    ) -> None:
        """Depth-first traversal to visit nodes and update visited with accessible nodes.

        Args:
            root: The starting node for traversal.
            to_visit: Set of nodes that need to be explored.
            visited: Record of visited nodes.
        """
        if root not in to_visit:
            assert root in visited
            return

        if any(p in to_visit for p in self.preds[root]):
            return

        to_visit.remove(root)
        assert root not in visited
        visited[root] = True

        for succ in self.succs[root]:
            self.dfwalk_subtree(succ, to_visit, visited)


def topo_sort(nodes: set[int], pairs: list[tuple[int, int]]) -> list[int]:
    """Topological sort for graph with given nodes and edge pairs.

    Args:
        nodes: Set of nodes to sort.
        pairs: A list of directed edge pairs.
    Returns:
        list[int]: Ordered nodes based on constraints.
    Example:
        topo_sort({1, 2, 3}, [(1, 2), (2, 3)]) => [1, 2, 3]
    """
    graph = DirectedGraph(pairs)

    to_visit: set[int] = nodes.copy()
    visited: dict[int, bool] = dict()
    for root in nodes:
        if not graph.preds[root]:
            graph.dfwalk_subtree(root, to_visit, visited)
    assert not to_visit
    return list(visited)


class RectOffset:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.__check__()

    def __str__(self):
        return f"RectOffset(i={self.i}, j={self.j})"

    __repr__ = __str__

    def _tuple(self):
        return (self.i, self.j)

    def __eq__(self, other):
        if isinstance(other, RectOffset):
            return self._tuple() == other._tuple()
        return False

    def __hash__(self):
        return hash(self._tuple())

    def __add__(self, other):
        assert isinstance(other, RectOffset)
        return RectOffset(self.i + other.i, self.j + other.j)

    def __check__(self):
        assert isinstance(self.i, int)
        assert isinstance(self.j, int)


class RectCoord:
    def __init__(self, nrows, ncols, i, j):
        self.nrows = nrows
        self.ncols = ncols
        self.i = i
        self.j = j
        self.__check__()

    def __str__(self):
        return (
            f"RectCoord(nrows={self.nrows}, ncols={self.ncols}, i={self.i}, j={self.j})"
        )

    __repr__ = __str__

    def _tuple(self):
        return (self.nrows, self.ncols, self.i, self.j)

    def __eq__(self, other):
        if isinstance(other, RectCoord):
            return self._tuple() == other._tuple()
        return False

    def __hash__(self):
        return hash(self._tuple())

    def __add__(self, other):
        if isinstance(other, (tuple, list)):
            return RectCoord(
                self.nrows, self.ncols, self.i + other[0], self.j + other[1]
            )
        if isinstance(other, RectOffset):
            return RectCoord(self.nrows, self.ncols, self.i + other.i, self.j + other.j)
        if isinstance(other, RectCoord):
            assert self.nrows == other.nrows
            assert self.ncols == other.ncols
            return RectCoord(self.nrows, self.ncols, self.i + other.i, self.j + other.j)
        raise TypeError(f"Unexpected type for {other}")

    def __check__(self):
        try:
            assert 0 <= self.i < self.nrows
            assert 0 <= self.j < self.ncols
        except AssertionError as e:
            raise IndexError("index out of range") from e


class RectGrid:
    def __init__(self, text: list[str]):
        self._text = text.copy()
        self.nrows = len(self._text)
        self.ncols = len(self._text[0]) if self.nrows else 0
        self.__check__()

    def __check__(self):
        """Check invariants"""
        assert isinstance(self._text, list)
        assert all(isinstance(el, str) for el in self._text)
        if self.nrows:
            lengths = [len(row) for row in self._text]
            for i in range(1, self.nrows):
                assert lengths[i] == lengths[0]

    def __str__(self):
        return "\n".join(self._text)

    def _to_coord(self, coordinates):
        if isinstance(coordinates, (tuple, list)):
            coordinates = RectCoord(self.nrows, self.ncols, *coordinates)
        assert isinstance(coordinates, RectCoord)
        return coordinates

    def __getitem__(self, coordinates):
        i, j = coordinates
        return self._text[i][j]

    def __contains__(self, coordinates):
        i, j = coordinates
        return 0 <= i < self.nrows and 0 <= j < self.ncols

    def __setitem__(self, coordinates, value):
        coordinates = self._to_coord(coordinates)
        i, j = coordinates.i, coordinates.j
        self._text[i] = self._text[i][:j] + value + self._text[i][j + 1 :]

    def __iter__(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                yield i, j

    def coord(self, i, j):
        return RectCoord(self.nrows, self.ncols, i, j)

    def offset(self, i, j):
        return RectOffset(i, j)

    def values(self):
        for row in self._text:
            yield from row

    def items(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                yield (i, j), self._text[i][j]

    def neighbors(self, pos):
        for inc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            npos = (pos[0] + inc[0], pos[1] + inc[1])
            if 0 <= npos[0] < self.nrows:
                if 0 <= npos[1] < self.ncols:
                    yield npos


class Timer:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(f"Elapsed time: {self.elapsed_time:.4f} seconds")


class PuzzleSize(Enum):
    EXAMPLE = "example"
    FULL = "full"


@dataclass
class RunInfo:
    input_file_name: str
    part1: object
    part2: object
