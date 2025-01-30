def transpose(matrix):
    return list(zip(*matrix))


def convert_to_string(chars):
    return "".join(chars)


def generate_diagonal_strings(starts, increment, n_rows, n_cols, data):
    max_len = max(n_rows, n_cols)
    strings = []
    for start_row, start_col in starts:
        chars = []
        for i in range(max_len):
            row, col = start_row + i * increment[0], start_col + i * increment[1]
            if 0 <= row < n_rows and 0 <= col < n_cols:
                chars.append(data[row][col])
            else:
                break
        strings.append("".join(chars))
    return strings


def count_patterns(patterns, strings):
    return sum(string.count(pattern) for pattern in patterns for string in strings)


def match_patterns(patterns, submatrix):
    return sum(
        all(pattern[r][c] in (submatrix[r][c], ".") for r in range(3) for c in range(3))
        for pattern in patterns
    )


def get_submatrix(matrix, start_row, start_col):
    return [[matrix[start_row + r][start_col + c] for c in range(3)] for r in range(3)]


def calculate_matches(rows, patterns):
    n_rows, n_cols = len(rows), len(rows[0])
    return sum(
        match_patterns(patterns, get_submatrix(rows, r, c))
        for r in range(n_rows - 2)
        for c in range(n_cols - 2)
    )


def run(input_file, part):
    if part == 1:
        rows = [list(line.strip()) for line in input_file]

        patterns = ["XMAS", "SAMX"]
        n_rows, n_cols = len(rows), len(rows[0])

        row_strings = [convert_to_string(row) for row in rows]
        col_strings = [convert_to_string(col) for col in transpose(rows)]

        forward_diagonal_starts = [(r, 0) for r in range(1, n_rows)] + [
            (0, c) for c in range(n_cols)
        ]
        backward_diagonal_starts = [(0, c) for c in range(n_cols)] + [
            (r, n_cols - 1) for r in range(1, n_rows)
        ]

        forward_strings = generate_diagonal_strings(
            forward_diagonal_starts, (1, 1), n_rows, n_cols, rows
        )
        backward_strings = generate_diagonal_strings(
            backward_diagonal_starts, (1, -1), n_rows, n_cols, rows
        )

        all_strings = row_strings + col_strings + forward_strings + backward_strings

        return count_patterns(patterns, all_strings)
    else:
        rows = [list(line.strip()) for line in input_file]

        patterns = [
            ["M.S", ".A.", "M.S"],
            ["M.M", ".A.", "S.S"],
            ["S.M", ".A.", "S.M"],
            ["S.S", ".A.", "M.M"],
        ]

        count_matches = calculate_matches(rows, patterns)
        return count_matches
