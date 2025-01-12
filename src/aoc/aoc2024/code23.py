from collections import defaultdict

import aoc.helpers as helpers


def process_sections(sections):
    edges = sections[0]
    return [tuple(edge.split("-")) for edge in edges]


def create_neighbors(edges):
    neighbors = defaultdict(set)
    for f, t in edges:
        neighbors[f].add(t)
        neighbors[t].add(f)
    return neighbors


def expand(tuples, neighbors):
    new_tuples = set()
    for tup in tuples:
        neighbor_sets = [neighbors[n] for n in tup]
        common_neighbors = set.intersection(*neighbor_sets)
        for n in common_neighbors:
            new_tuples.add(tuple(sorted((*tup, n))))
    return new_tuples


def run_part1(edges):
    neighbors = create_neighbors(edges)
    triples = expand(edges, neighbors)
    triples = set(
        triple for triple in triples if any(item.startswith("t") for item in triple)
    )
    return len(triples)


def run_part2(edges):
    neighbors = create_neighbors(edges)
    tuples = edges
    while True:
        new_tuples = expand(tuples, neighbors)
        print(f"{len(new_tuples)=}")
        if not new_tuples:
            break
        tuples = new_tuples
    assert len(tuples) == 1
    return ",".join(tuples.pop())


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    processed_input = process_sections(sections)
    if part == 1:
        return run_part1(processed_input)
    else:
        return run_part2(processed_input)
