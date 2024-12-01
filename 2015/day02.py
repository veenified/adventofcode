import timeit
from typing import List
from utils.utils import run_parts

def part1(input_lines: List[str]):
    total_sq_ft = 0
    for line in input_lines:
        a, b, c = sorted(int(i) for i in line.split("x"))
        total_sq_ft += 3 * a * b + 2 * a * c + 2 * b * c
    return total_sq_ft


def part2(input_lines: List[str]):
    total_ft = 0
    for line in input_lines:
        a, b, c = sorted(int(i) for i in line.split("x"))
        total_ft += 2 * a + 2 * b + a * b * c
    return total_ft

if __name__ == "__main__":
    run_parts(part1, part2, 2015, 2)