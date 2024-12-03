import re
from typing import List

from utils.utils import run_parts


test_input_1 = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""
test_input_2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

def parse_out_mul_pairs(input_lines: List[str], parse_conditional: bool = False):
    # parse out a list of every mul(x{1,3},y{1,3}) using regex
    result = []
    # conditional flag is sustained through multiple mul(x,y) pairs, including newlines, until a new conditional is encountered
    conditional = True
    for line in input_lines:
        # Find all mul(x,y) patterns where x and y are 1-3 digits
        matches = re.findall(r'(?:(do\(\)|don\'t\(\)).*?)?mul\((\d{1,3}),(\d{1,3})\)', line)
        print(matches)
        # if parse_conditional, then we need to include a conditional flag (c) in the result
        if parse_conditional:
            for c, x, y in matches:
                if c == "don't()":
                    conditional = False
                elif c == "do()":
                    conditional = True
                result.extend([(conditional, int(x), int(y))])
        else:
            result.extend([(int(x), int(y)) for _, x, y in matches])
    return result

def part1(input_lines: List[str]):

    # parse out a list of every mul(x{1,3},y{1,3}) using regex
    result = parse_out_mul_pairs(input_lines)
    # then multiply them together and add them together
    total = 0
    for x, y in result:
        total += x * y
    # then return the result
    return total

def part2(input_lines: List[str]):
    # parse out a list of every mul(x{1,3},y{1,3}) using regex
    result = parse_out_mul_pairs(input_lines, parse_conditional=True)
    print(result)
    # then multiply them together and add them together
    total = 0
    for c, x, y in result:
        if c:
            total += x * y
    # then return the result
    return total

if __name__ == "__main__":
    # print(part1(test_input_1.strip().split('\n'))) # expect 161 (2*4 + 5*5 + 11*8 + 8*5)
    # print(part2(test_input_2.strip().split('\n'))) # expect 48 (2*4 + 8*5)
    run_parts(part1, part2, 2024, 3)
