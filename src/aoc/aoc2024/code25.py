import re

import aoc.helpers as helpers


def calc_run(s):
    run = 0
    for letter in s:
        if letter == "#":
            run += 1
        else:
            break
    return run


def process_sections(sections):
    keys = []
    locks = []

    for section in sections:
        if re.fullmatch("#+", section[0]):
            lock = []
            for s in helpers.transpose(section):
                lock.append(calc_run(s) - 1)
            locks.append(tuple(lock))
        elif re.fullmatch("#+", section[-1]):
            key = []
            for s in helpers.transpose(section):
                key.append(calc_run(reversed(s)) - 1)
            keys.append(tuple(key))
        else:
            raise ValueError("Unexpected section " + section)
    return locks, keys


def fits(lock, key):
    return all(
        lock_height + key_height <= 5 for lock_height, key_height in zip(lock, key)
    )


def run_part1(locks, keys):
    matches = set()
    for lock in locks:
        for key in keys:
            if fits(lock, key):
                matches.add((lock, key))
    return len(matches)


def run_part2(processed_input):
    return None


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)

    processed_input = process_sections(sections)
    if part == 1:
        return run_part1(*processed_input)
    else:
        return None
