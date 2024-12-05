from utils.utils import run_parts


testInput = """
""
"abc"
"aaa\\"aaa"
"\\x27"
"""


def part1(input_lines: list[str]):
    # Count the difference between code representation and memory representation
    total_code_chars = 0  # Total characters in code strings
    total_memory_chars = 0  # Total characters in memory after escaping

    for line in input_lines:
        # Add length of original string including quotes
        total_code_chars += len(line)

        # Remove surrounding quotes and process escape sequences
        string_content = line[1:-1]
        it = iter(string_content)
        memory_string = ""

        try:
            while char := next(it):
                if char == "\\":
                    escape_char = next(it)
                    if escape_char == "x":
                        # Handle hex escape sequence (\x27 etc)
                        hex_code = next(it) + next(it)  # Skip the two hex digits
                        memory_string += "X"  # Represents one decoded character
                    else:
                        # Handle simple escape sequences (\\ or \")
                        memory_string += escape_char
                else:
                    memory_string += char

        except StopIteration:
            pass

        total_memory_chars += len(memory_string)

    # Return difference between code representation and memory representation
    return total_code_chars - total_memory_chars


def part2(input_lines: list[str]):
    # Count difference between original string length and escaped string length
    original_length = 0  # Length of original strings
    escaped_length = 0  # Length after escaping special characters

    for line in input_lines:
        original_length += len(line)

        for ch in line:
            if ch == "\\":
                # Each backslash needs to be escaped with another backslash (\\)
                escaped_length += 2
            elif ch == '"':
                # Each quote needs to be escaped with a backslash (\")
                escaped_length += 2
            else:
                # Regular characters just copy over as-is
                escaped_length += 1

        # Add 2 for the new surrounding quotes needed for each string
        escaped_length += 2

    # Return difference between escaped and original lengths
    return escaped_length - original_length


if __name__ == "__main__":
    # print(part1(testInput.split('\n')))
    run_parts(part1, part2, 2015, 8)
