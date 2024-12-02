from typing import List

from utils.utils import run_parts

def has_increasing_straight(password: str):
    for i in range(len(password) - 2):
        if ord(password[i]) + 1 == ord(password[i+1]) and ord(password[i]) + 2 == ord(password[i+2]):
            return True
    return False

def has_forbidden_letters(password: str):
    return "i" in password or "o" in password or "l" in password

def has_two_distinct_pairs(password: str):
    pair_count = 0
    prev_pair = ""
    for i in range(len(password) - 1):
        if password[i] == password[i+1]:
            # If the previous pair is the same as the current pair, skip, as they must distinct pairs
            if prev_pair == password[i]:
                continue
            prev_pair = password[i]
            pair_count += 1
    return pair_count >= 2

def is_valid_password(password: str):
    return has_increasing_straight(password) and not has_forbidden_letters(password) and has_two_distinct_pairs(password)


def increment_password(password: str):
    password = list(password)
    for i in range(len(password) - 1, -1, -1):
        if password[i] == "z":
            password[i] = "a"
        else:
            password[i] = chr(ord(password[i]) + 1)
            break
    return "".join(password)

def next_password(password: str):
    while not is_valid_password(password):
        password = increment_password(password)
    return password


def part1(input_lines: List[str]):
    print(f"Original Password: {input_lines[0]}")
    return next_password(input_lines[0])

def part2(input_lines: List[str]):
    return next_password(increment_password(next_password(input_lines[0])))

if __name__ == "__main__":
    # print(part1(["abcdefgh"]))
    run_parts(part1, part2, 2015, 11)
