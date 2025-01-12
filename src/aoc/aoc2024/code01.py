from collections import Counter


def transpose(iterables):
    return zip(*iterables)


def run(input_file, part):
    assert part in (1, 2)
    assert part in (1, 2)

    if part == 1:
        pairs = [map(int, line.split()) for line in input_file]
        sorted_pairs = transpose(map(sorted, transpose(pairs)))
        total_dist = sum(abs(left - right) for left, right in sorted_pairs)
        return total_dist
    else:
        pairs = [tuple(map(int, line.split())) for line in input_file]
        left, right = transpose(pairs)
        counts = Counter(right)
        score = sum(el * counts[el] for el in left)
        return score
