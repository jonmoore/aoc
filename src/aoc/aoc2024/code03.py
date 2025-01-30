from aoc.helpers import read_input_sections
import re


def run(input_file, part):
    sections = read_input_sections(input_file)
    assert len(sections) in (1, 2)
    contents = "".join(sections[(part - 1) % len(sections)])
    if part == 1:
        matches = re.findall(r"mul\(([0-9]+),([0-9]+)\)", contents)
        return sum(int(m[0]) * int(m[1]) for m in matches)
    else:
        matches = re.finditer(
            r"(?P<cmd1>mul)\((?P<a>[0-9]+),(?P<b>[0-9]+)\)|(?P<cmd2>do)\(\)|(?P<cmd3>don't)\(\)",
            contents,
        )

        adding = True
        total = 0
        for match in matches:
            cmd = match["cmd1"] or match["cmd2"] or match["cmd3"]

            match cmd:
                case "mul":
                    if adding:
                        total += int(match["a"]) * int(match["b"])
                case "do":
                    adding = True
                case "don't":
                    adding = False

        return total
