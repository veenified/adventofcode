from utils.utils import run_parts


test_input = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def part1(input_lines: list[str]):
    # Create a data structure that starts at 50 and acts as a circular buffer,
    # moving left and right based on the instructions.
    # If the dialSetting is 0, increment the zeroCount.
    dial_setting = 50
    zero_count = 0
    for line in input_lines:
        if line.startswith("L"):
            dial_setting = (dial_setting - int(line.split("L")[1])) % 100
            if dial_setting == 0:
                zero_count += 1
        elif line.startswith("R"):
            dial_setting = (dial_setting + int(line.split("R")[1])) % 100
            if dial_setting == 0:
                zero_count += 1
    return zero_count


def part2(input_lines: list[str]):
    # Part 2 (password method 0x434C49434B)
    # Count the number of times a 0 dialSetting is passed during moves
    dial_setting = 50
    zero_count = 0
    for line in input_lines:
        start_setting = dial_setting
        if line.startswith("L"):
            move_amount = int(line.split("L")[1])
            # When moving left, count how many times we pass through position 0
            # If moveAmount > startSetting, we wrap and pass through 0 at least once
            # Plus once for each additional full 100 we go past
            if move_amount > start_setting:
                zero_count += 1 + (move_amount - start_setting - 1) // 100
            dial_setting = (dial_setting - move_amount) % 100
        elif line.startswith("R"):
            move_amount = int(line.split("R")[1])
            # When moving right, count how many times we pass through position 0
            # We pass through 0 when we're at position 0 during the move
            # Count: floor((startSetting + moveAmount - 1) / 100) - floor((startSetting - 1) / 100)
            zero_count += (start_setting + move_amount - 1) // 100 - (start_setting - 1) // 100
            dial_setting = (dial_setting + move_amount) % 100
    return zero_count


if __name__ == "__main__":
    # print(part1(test_input.strip().split('\n')))  # Test with test input
    # print(part2(test_input.strip().split('\n')))  # Test with test input
    run_parts(part1, part2, 2025, 1)
