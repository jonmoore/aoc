def is_monotonic(lis):
    return lis == sorted(lis) or lis == sorted(lis, reverse=True)


def is_delta_safe(lis):
    return all(abs(lis[i + 1] - lis[i]) in {1, 2, 3} for i in range(len(lis) - 1))


def is_safe(lis):
    return is_monotonic(lis) and is_delta_safe(lis)


def is_one_safe(lis):
    if is_safe(lis):
        return True
    for i in range(len(lis)):
        if is_safe(lis[:i] + lis[i + 1 :]):
            return True
    return False


def run(input_file, part):
    assert part in (1, 2)
    if part == 1:
        lists = [list(map(int, line.split())) for line in input_file]
        return sum(is_monotonic(lis) and is_delta_safe(lis) for lis in lists)
    else:
        lists = [list(map(int, line.split())) for line in input_file]
        return sum(is_one_safe(lis) for lis in lists)
