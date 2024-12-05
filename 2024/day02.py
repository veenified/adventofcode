from utils.utils import run_parts


test_input = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def check_adjacent_diff(report_list: list[int]):
    for i in range(len(report_list) - 1):
        diff = abs(report_list[i] - report_list[i + 1])
        if diff < 1 or diff > 3:
            return False
    return True


def is_list_valid(report_list: list[int]) -> bool:
    # Check if list is monotonic
    is_increasing = all(
        report_list[i] <= report_list[i + 1] for i in range(len(report_list) - 1)
    )
    is_decreasing = all(
        report_list[i] >= report_list[i + 1] for i in range(len(report_list) - 1)
    )

    if not (is_increasing or is_decreasing):
        return False

    return check_adjacent_diff(report_list)


def determine_safe_count(input_lines: list[str], dampener_available: bool = False):
    safe_count = 0
    for line in input_lines:
        report_list = list(map(int, line.split()))

        # Check original list
        if is_list_valid(report_list):
            print(f"{report_list} is safe")
            safe_count += 1
            continue

        # If dampener available, try removing one number at a time
        if dampener_available:
            for i in range(len(report_list)):
                modified_list = report_list[:i] + report_list[i + 1 :]
                if is_list_valid(modified_list):
                    print(f"{modified_list} is safe (after removing {report_list[i]})")
                    safe_count += 1
                    break

    return safe_count


def part1(input_lines: list[str]):
    return determine_safe_count(input_lines)


def part2(input_lines: list[str]):
    return determine_safe_count(input_lines, True)


if __name__ == "__main__":
    # print(part1(test_input.strip().split('\n')))  # should return 2 safe
    # print(part2(test_input.strip().split('\n')))  # should return 4 safe
    run_parts(part1, part2, 2024, 2)
