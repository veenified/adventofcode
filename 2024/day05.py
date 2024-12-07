from math import floor
from dataclasses import dataclass

from utils.utils import run_parts


@dataclass
class Rule:
    before: str
    after: str

    def is_valid(self, sequence: list[str]) -> bool:
        if self.before not in sequence or self.after not in sequence:
            return True
        return sequence.index(self.before) < sequence.index(self.after)


def parse_input(input_lines: list[str]) -> tuple[list[Rule], list[list[str]]]:
    rules = []
    sequences = []
    
    for line in input_lines:
        if '|' in line:
            before, after = line.split('|')
            rules.append(Rule(before.strip(), after.strip()))
        elif ',' in line:
            sequences.append(line.strip().split(','))
    
    return rules, sequences


def is_valid_sequence(sequence: list[str], rules: list[Rule]) -> bool:
    return all(rule.is_valid(sequence) for rule in rules)


def get_middle_value(sequence: list[str]) -> int:
    return int(sequence[floor(len(sequence)/2)])


def part1(input_lines: list[str]) -> int:
    rules, sequences = parse_input(input_lines)
    return sum(
        get_middle_value(sequence) 
        for sequence in sequences 
        if is_valid_sequence(sequence, rules)
    )


def fix_sequence(sequence: list[str], rules: list[Rule]) -> list[str]:
    for rule in rules:
        if not rule.is_valid(sequence):
            after_index = sequence.index(rule.after)
            before_index = sequence.index(rule.before)
            if after_index < before_index:
                sequence[after_index], sequence[before_index] = sequence[before_index], sequence[after_index]
        if is_valid_sequence(sequence, rules):
            break
    if not is_valid_sequence(sequence, rules):
        sequence = fix_sequence(sequence, rules)
    return sequence


def part2(input_lines: list[str]) -> int:
    rules, sequences = parse_input(input_lines)

    # Fix each invalid sequence individually
    fixed_sequences = [
        fix_sequence(sequence, rules) 
        for sequence in sequences 
        if not is_valid_sequence(sequence, rules)
    ]
    return sum(
        get_middle_value(fixed_sequence) 
        for fixed_sequence in fixed_sequences 
    )


if __name__ == "__main__":
    test_input = """
    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    """
    
    # print(part1(test_input.strip().split('\n')))  # expect 143
    # print(part2(test_input.strip().split('\n')))  # expect 123
    run_parts(part1, part2, 2024, 5)
