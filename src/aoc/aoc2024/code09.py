from dataclasses import dataclass
import itertools
import aoc.helpers as helpers


@dataclass
class Segment:
    segment_type: str
    length: int
    file_id: int | None


def compute_blocks(segments):
    blocks = []
    for segment in segments:
        blocks.extend([segment.file_id] * segment.length)
    return blocks


def compute_block_intervals(segments):
    return list(
        itertools.pairwise(
            itertools.accumulate(
                segments, lambda total, segment: total + segment.length, initial=0
            )
        )
    )


def compute_checksum(blocks):
    return sum(i * val for i, val in enumerate(blocks) if val)


def run_part1(segments):
    blocks = compute_blocks(segments)

    lpos = 0
    rpos = len(blocks) - 1
    occupied = sum(
        segment.length for segment in segments if segment.segment_type == "file"
    )
    while rpos > occupied - 1:
        while blocks[lpos] is not None:
            lpos += 1
        while blocks[rpos] is None:
            rpos -= 1
        blocks[lpos], blocks[rpos] = blocks[rpos], blocks[lpos]
        lpos += 1
        rpos -= 1

    return compute_checksum(blocks)


def compute_free_indices(free_intervals, indices=None):
    # return a dict d st d[l_] is the index in free_intervals of the first interval of
    # length >= l_
    MAX_LENGTH = 10
    if indices is None:
        indices = {length: 0 for length in range(1, MAX_LENGTH)}

    new_indices = dict()
    for length in indices:
        if length > 1:
            i = max(new_indices[length - 1], indices[length])
        else:
            i = indices[length]
        while i < len(free_intervals):
            interval = free_intervals[i]
            if interval[1] - interval[0] >= length:
                new_indices[length] = i
                break
            i += 1
        if length not in new_indices:
            break
    return new_indices


def run_part2(segments):
    # segments - list of segments, from the start of the file
    # blocks - the file blocks laid out as a list
    blocks = compute_blocks(segments)
    block_intervals = compute_block_intervals(segments)

    segment_intervals = list(zip(segments, block_intervals))

    file_segments, file_intervals = list(
        zip(*((s, i) for (s, i) in segment_intervals if s.segment_type == "file"))
    )

    free_intervals = [i for (s, i) in segment_intervals if s.segment_type == "free"]
    free_indices = compute_free_indices(free_intervals)

    for i in range(len(file_segments)):
        file_length = file_segments[-i - 1].length
        file_interval = file_intervals[-i - 1]

        if (free_index := free_indices.get(file_length, None)) is None:
            continue

        if (free_interval := free_intervals[free_index]) >= file_interval:
            continue

        file_slice = slice(*file_interval)
        free_slice = slice(*free_interval)
        rep_slice = slice(free_slice.start, free_slice.start + file_length)

        # move the blocks
        blocks[rep_slice], blocks[file_slice] = blocks[file_slice], blocks[rep_slice]

        # update free information
        free_intervals[free_index] = (rep_slice.stop, free_slice.stop)
        free_indices = compute_free_indices(free_intervals, free_indices)

    return compute_checksum(blocks)


def run(input_file, part):
    sections = helpers.read_input_sections(input_file)
    spec = sections[0][0].strip()
    segments = []
    for i, length in enumerate(map(int, spec)):
        if i % 2 == 0:
            segments.append(Segment("file", length, i // 2))
        else:
            segments.append(Segment("free", length, None))
    if part == 1:
        return run_part1(segments)
    else:
        return run_part2(segments)
