from hashlib import md5
import timeit
from utils.utils import run_parts


def match_md5_zeroes(key, count=5):
    for i in range(10_000_000):
        this_md5 = md5(key)
        number = str(i).encode("utf-8")
        this_md5.update(number)
        digest = this_md5.hexdigest()
        if digest[slice(0, count)] == "0" * count:
            return i
    raise ValueError("Could not find a match")


def part1(input_lines: list[str]):
    key = input_lines[0].encode("utf-8")
    return match_md5_zeroes(key, count=5)


def part2(input_lines: list[str]):
    key = input_lines[0].encode("utf-8")
    return match_md5_zeroes(key, count=6)


if __name__ == "__main__":
    run_parts(part1, part2, 2015, 4)
