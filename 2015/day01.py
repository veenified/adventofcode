from collections import Counter
import timeit
from utils.utils import run_parts


def part1(input_lines: list[str]):
    instructions = input_lines[0]
    counter = Counter(instructions)
    return counter.get("(") - counter.get(")")


def part2(input_lines: list[str]):
    location = 0
    instructions = input_lines[0]
    for i, item in enumerate(instructions, start=1):
        if item == "(":
            location += 1
        else:
            location -= 1
        if location < 0:
            return i
    raise ValueError("Never went negative!")


if __name__ == "__main__":
    run_parts(part1, part2, 2015, 1)
