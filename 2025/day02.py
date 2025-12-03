from typing import Callable
from utils.utils import get_input, run_parts


test_input = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""
def run_input_through_func(input_lines: list[str], func: Callable[int]) -> int:
    total_sum = 0
    
    for line in input_lines:
        # Parse ranges: "first-last,first-last,..."
        ranges = line.split(',')
        for range_str in ranges:
            start, end = map(int, range_str.split('-'))
            # Check each number in the range
            for num in range(start, end + 1):
                if func(num):
                    total_sum += num
    
    return total_sum

def part1(input_lines: list[str]):
    def is_invalid_id(num: int) -> bool:
        """Check if a number is made up of a sequence of digits repeated twice."""
        num_str = str(num)
        # Must have even number of digits
        if len(num_str) % 2 != 0:
            return False
        # Split in half and check if both halves are the same
        mid = len(num_str) // 2
        return num_str[:mid] == num_str[mid:]
    
    return run_input_through_func(input_lines, is_invalid_id)


def part2(input_lines: list[str]):
    def is_invalid_id(num: int) -> bool:
        """Check if a number is made up of a sequence of digits repeated at least twice."""
        num_str = str(num)
        num_len = len(num_str)
        
        # Try all possible segment lengths from 1 to num_len//2
        # (we need at least 2 segments, so segment length can't exceed half the total length)
        for segment_len in range(1, num_len // 2 + 1):
            # Check if the number length is divisible by segment length
            if num_len % segment_len != 0:
                continue
            
            # Extract all segments
            num_segments = num_len // segment_len
            segments = [num_str[i * segment_len:(i + 1) * segment_len] 
                       for i in range(num_segments)]
            
            # Check if all segments are the same (and we have at least 2 segments)
            if num_segments >= 2 and all(seg == segments[0] for seg in segments):
                return True
        
        return False
    
    return run_input_through_func(input_lines, is_invalid_id)


if __name__ == "__main__":
    # print(part1(test_input.strip().split('\n')))  # Test with test input
    # print(part2(test_input.strip().split('\n')))  # Test with test input
    run_parts(part1, part2, 2025, 2)
