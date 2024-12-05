from utils.utils import run_parts

WORD = "XMAS"

DIRECTIONS = [
    (0, -1),  # Vertical (N)
    (1, -1),  # Diagonal (NE)
    (1, 0),  # Horizontal (E)
    (1, 1),  # Diagonal (SE)
    (0, 1),  # Vertical (S)
    (-1, 1),  # Diagonal (SW)
    (-1, 0),  # Horizontal (W)
    (-1, -1),  # Diagonal (NW)
]

test_input = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def check_word(x, y, direction, grid):
    for i in range(len(WORD)):
        nx, ny = x + i * direction[0], y + i * direction[1]
        if (
            nx < 0
            or ny < 0
            or nx >= len(grid[0])
            or ny >= len(grid)
            or grid[ny][nx] != WORD[i]
        ):
            return False
    return True


def part1(input_lines: list[str]):
    # create word grid
    grid = [line.strip() for line in input_lines]
    # count the number of occurences of "XMAS"
    count = 0
    for row in range(len(input_lines[0])):
        for col in range(len(input_lines)):
            for dx, dy in DIRECTIONS:
                if check_word(row, col, (dx, dy), grid):
                    count += 1
    return count


def part2(input_lines: list[str]):
    # create word grid
    grid = [line.strip() for line in input_lines]
    # count the number of occurences of "X-MAS"
    x_mas_amount = 0
    for x in range(1, len(grid) - 1):  # Don't start at the horizontal edges
        for y in range(1, len(grid[0]) - 1):  # Don't start at the vertical edges
            if (
                grid[x][y] == "A"
                and {grid[x - 1][y - 1], grid[x + 1][y + 1]} == {"M", "S"}
                and {grid[x + 1][y - 1], grid[x - 1][y + 1]} == {"M", "S"}
            ):
                x_mas_amount += 1
    return x_mas_amount


if __name__ == "__main__":
    # print(part1(test_input.strip().split('\n'))) # expect 18
    # print(part2(test_input.strip().split('\n'))) # expect 9
    run_parts(part1, part2, 2024, 4)
