import re
from collections import defaultdict
from dataclasses import dataclass
import dataclasses

import aoc.helpers as helpers


@dataclass(frozen=True)
class Constant:
    out: str
    c: int


@dataclass(frozen=True)
class BinOp:
    out: str
    a: str
    b: str


@dataclass(frozen=True)
class Xor(BinOp):
    pass


@dataclass(frozen=True)
class Or(BinOp):
    pass


@dataclass(frozen=True)
class And(BinOp):
    pass


def process_sections(sections):
    wires = []
    for line in sections[0]:
        out, c = re.fullmatch(r"(.*):.*(\d+).*", line).groups()
        assert c in "01"
        wires.append(Constant(out=out, c=int(c)))

    for line in sections[1]:
        a, op, b, arrow, out = line.split()
        assert arrow == "->"
        if op == "AND":
            wire = And(out=out, a=a, b=b)
        elif op == "OR":
            wire = Or(out=out, a=a, b=b)
        elif op == "XOR":
            wire = Xor(out=out, a=a, b=b)
        else:
            raise Exception("bad op " + op)
        wires.append(wire)
    return set(wires)


def run_part1(wires):
    def ev(wire):
        return env[wire](env)

    env = dict()
    for wire in wires:
        out = wire.out
        match wire:
            case Constant(c=c):
                env[out] = lambda env, c=c: c
            case And(a=a, b=b):
                env[out] = lambda env, a=a, b=b: ev(a) & ev(b)
            case Or(a=a, b=b):
                env[out] = lambda env, a=a, b=b: ev(a) | ev(b)
            case Xor(a=a, b=b):
                env[out] = lambda env, a=a, b=b: ev(a) ^ ev(b)
    return sum(ev(k) << int(k[1:]) for k in env if k.startswith("z"))


def match_ab(wires: set, ab: set):
    return set(w for w in wires if isinstance(w, BinOp) and set((w.a, w.b)) == ab)


def match_out(wires: set, out: str):
    return set(w for w in wires if w.out == out)


def label(p, i):
    return p + f"{i:02}"


def xy_labels(i):
    return {label(c, i) for c in "xy"}


def wire_parents(wire):
    if isinstance(wire, Constant):
        return set()
    elif isinstance(wire, BinOp):
        return set([wire.a, wire.b])
    else:
        raise ("bad wire " + wire)


def apply_swaps(wires, swaps):
    for s0, s1 in swaps:
        wires_new = set()
        for w in wires:
            if w.out == s0:
                wires_new.add(dataclasses.replace(w, out=s1))
            elif w.out == s1:
                wires_new.add(dataclasses.replace(w, out=s0))
            else:
                wires_new.add(w)
        wires = wires_new
    return wires


class TrackedException(Exception):
    def suspect_labels(self):
        return []


class FindChildError(TrackedException):
    def __init__(self, ab, cls, rank):
        self.ab = ab
        self.cls = cls
        self.rank = rank

    def __str__(self):
        return f"FindChildError(ab={self.ab}, cls={self.cls}, rank={self.rank})"

    def suspect_labels(self):
        return list(self.ab)


class ChildrenLengthError(TrackedException):
    def __init__(self, parent, expected, actual, rank):
        self.parent = parent
        self.expected = expected
        self.actual = actual
        self.rank = rank

    def __str__(self):
        return f"ChildrenLengthError(parent={self.parent}, expected={self.expected}, actual={self.actual}, rank={self.rank})"

    def suspect_labels(self):
        return [self.parent]


class WireNameError(TrackedException):
    def __init__(self, expected, actual, rank=""):
        assert isinstance(expected, str)
        assert isinstance(actual, str)
        self.expected = expected
        self.actual = actual
        self.rank = rank

    def __str__(self):
        return f"WireNameError(expected={self.expected}, actual={self.actual}, rank={self.rank})"

    def suspect_labels(self):
        return [self.expected, self.actual]


def find_child(wires: set, ab: set, cls: type):
    """Return either a wire whose inputs, as a set, equal ab and which is an instance of
    cls or return None.
    """
    matches = [w for w in wires if isinstance(w, cls) and set((w.a, w.b)) == ab]

    if len(matches) != 1:
        return None
    return matches[0]


def calc_defects(wires, swaps):
    wires = apply_swaps(wires, swaps)
    len_xy = int(max(wire.out for wire in wires)[1:])
    for i in range(len_xy):
        assert len(match_out(wires, label("z", i))) == 1
        assert len(match_ab(wires, xy_labels(i))) == 2
    # parents: outputs->inputs
    parents = {wire.out: wire_parents(wire) for wire in wires}
    # children: inputs->outputs
    children = defaultdict(set)

    defects = set()
    for out, parents in parents.items():
        for p in parents:
            children[p].add(out)
    for i in range(len_xy):
        x, y, z = label("x", i), label("y", i), label("z", i)
        if len(children[x]) != 2:
            defects.add(f"len(children[{x}]) != 2")
        if len(children[y]) != 2:
            defects.add(f"len(children[{y}]) != 2")
        if len(children[z]) != 0:
            defects.add(f"len(children[{z}]) != 0")

        if i == 0:
            if u := find_child(wires, {x, y}, And):
                u = u.out
            else:
                defects.add(f"u := find_child(wires, {x}, {y}, And):")

            if v := find_child(wires, {x, y}, Xor):
                v = v.out
            else:
                defects.add(f"v := find_child(wires, {x}, {y}, Xor):")

            c = u
        else:
            # full adder
            # u = x&y, v = x^y, w = v&c, z = v^c, C = u|w
            # xy
            # uvc data flows between adjacent /connected wires except uw
            # |wZ
            # C

            if not isinstance(c, str):
                pass

            u = v = w = Z = C = None

            if u := find_child(wires, {x, y}, And):
                u = u.out
            elif x and y:
                defects.add(FindChildError({x, y}, And, i))
            if v := find_child(wires, {x, y}, Xor):
                v = v.out
            elif x and y:
                defects.add(FindChildError({x, y}, Xor, i))
            if w := find_child(wires, {v, c}, And):
                w = w.out
            elif v and c:
                defects.add(FindChildError({v, c}, And, i))
            if Z := find_child(wires, {v, c}, Xor):
                Z = Z.out
            elif v and c:
                defects.add(FindChildError({v, c}, Xor, i))
            for parent, expected in [(u, 1), (v, 2), (w, 1)]:
                if parent is None:
                    continue
                if (actual := len(children[parent])) != expected:
                    defects.add(ChildrenLengthError(parent, expected, actual, i))
            if Z not in (z, None):
                defects.add(WireNameError(Z, z, i))
            if C := find_child(wires, {u, w}, Or):
                C = C.out
            elif u and w:
                defects.add(FindChildError({u, w}, Or, i))
            c = C
    return defects


def calc_suspect_swaps(candidate_swaps, defects):
    """Return suspect swaps"""
    suspect_labels = set(
        (label for defect in defects for label in defect.suspect_labels())
    )

    return [pair for pair in candidate_swaps if set(pair) & suspect_labels]


def calc_defects_score(defects):
    """lower is better"""
    return -min((defect.rank for defect in defects), default=100)


def run_part2b(wires):
    """A pretty brute force approach.  Could be made faster / simpler but there's a trade
    off between how general to make it and how much to tune to the specific problem.
    """
    swaps = []

    output_labels = [w.out for w in wires if not isinstance(w, Constant)]
    candidate_swaps = [
        (output_labels[i], output_labels[j])
        for i in range(len(output_labels))
        for j in range(i)
    ]

    defects = calc_defects(wires, swaps)

    print()
    while defects:
        print(f"{swaps=}")
        print(f"{defects=}")
        print(f"{calc_defects_score(defects)=}")

        for swap in calc_suspect_swaps(candidate_swaps, defects):
            if calc_defects_score(
                calc_defects(wires, swaps + [swap])
            ) < calc_defects_score(defects):
                break
        else:
            raise Exception("Could not find a swap to improve things")
        swaps.append(swap)
        defects = calc_defects(wires, swaps)

    print(f"{swaps=}")
    return ",".join(sorted(el for swap in swaps for el in swap))


def run(input_file, part, skip=False):
    if skip:
        return None

    sections = helpers.read_input_sections(input_file)

    processed_input = process_sections(sections)
    if part == 1:
        return run_part1(processed_input)
    else:
        return run_part2b(processed_input)
