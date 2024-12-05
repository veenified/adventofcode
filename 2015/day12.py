import json
import re
from utils.utils import run_parts

test_input = """
[1,2,3]
{"a":2,"b":4}
[[[3]]]
{"a":{"b":4},"c":-1}
{"a":[-1,1]}
[-1,{"a":1}]
[]
{}
"""


def filter_red_objects(data):
    if isinstance(data, dict):
        if "red" in data.values():
            return 0
        return sum(filter_red_objects(v) for v in data.values())
    elif isinstance(data, list):
        return sum(filter_red_objects(v) for v in data)
    elif isinstance(data, int):
        return data
    return 0


def part1(input_lines: list[str]):
    test_input_lines = test_input.split("\n")
    # extract all numbers from the input
    numbers = [int(num) for line in input_lines for num in re.findall(r"-?\d+", line)]
    return sum(numbers)


def part2(input_lines: list[str]):
    # parse the input as json
    json_data = json.loads(input_lines[0])

    # filter out all the red objects and sum the remaining numbers
    return filter_red_objects(json_data)


if __name__ == "__main__":
    # for line in test_input.split("\n"):
    #     print(part1([line])) # 6, 6, 3, 3, 0, 0, 0, 0
    run_parts(part1, part2, 2015, 12)
