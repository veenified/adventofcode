from typing import List
from utils.utils import run_parts


testInput = "111221"

def look_and_say(input_str: str):
    curr_chr = ""
    curr_chr_cnt = 0
    result = ""
    for chr in input_str:
        if chr == curr_chr:
            curr_chr_cnt += 1
        else:
            result += f"{curr_chr_cnt}{curr_chr}"
            curr_chr = chr
            curr_chr_cnt = 1
    result += f"{curr_chr_cnt}{curr_chr}"
    return result[1:]

def part1(input_lines: List[str]):
    result = input_lines[0]
    for i in range(40):
        result = look_and_say(result)
    return len(result)

def part2(input_lines: List[str]):
    result = input_lines[0]
    for i in range(50):
        result = look_and_say(result)
    return len(result)

if __name__ == "__main__":
    # print(look_and_say(testInput))
    run_parts(part1, part2, 2015, 10)