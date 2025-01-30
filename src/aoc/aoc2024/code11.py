from collections import Counter

import aoc.helpers as helpers


def process_sections(sections) -> list[int]:
    return [int(s) for s in sections[0][0].split()]


def new_layout(old_layout: list[int]) -> list[int]:
    for stone in old_layout:
        if stone == 0:
            yield 1
        elif len(str(stone)) % 2 == 0:
            st = str(stone)
            len1 = (len(st) + 1) // 2
            yield int(st[:len1])
            yield int(st[len1:])
        else:
            yield stone * 2024


def next_counter(old_counter: Counter) -> Counter[int]:
    new_counter = Counter()
    for stone, count in old_counter.items():
        for new_stone in new_layout([stone]):
            new_counter[new_stone] += count
    return new_counter


def length_after(layout, n_blinks) -> int:
    counter = Counter(layout)
    for _ in range(n_blinks):
        counter = next_counter(counter)
    return counter.total()


def run_part1(layout):
    return length_after(layout, n_blinks=25)


def run_part2(layout):
    return length_after(layout, n_blinks=75)


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    layout = process_sections(sections)

    if part == 1:
        return run_part1(layout)
    else:
        return run_part2(layout)
