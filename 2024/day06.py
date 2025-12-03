from dataclasses import dataclass

    
@dataclass
class Player:
    x: int
    y: int
    direction: str

    def turn_right(self) -> None:
        self.direction = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}[self.direction]


@dataclass
class Grid:
    grid: list[list[str]]
    player: Player

    def __init__(self, input: list[str]) -> None:
        grid = []
        for y, line in enumerate(input):
            new_line = list(line)
            for x, char in enumerate(line):
                if char in ('^', 'v', '<', '>'):
                    new_line[x] = 'X'
                    self.player = Player(
                        x=x,
                        y=y, 
                        direction={'v': 'S', '^': 'N', '<': 'W', '>': 'E'}[char]
                    )
            grid.append(new_line)
        self.grid = grid

    def is_obstacle(self, x: int, y: int) -> bool:
        return self.grid[y][x] == '#'
    
    def is_off_grid(self, x: int, y: int) -> bool:
        return x < 0 or x >= len(self.grid[0]) or y < 0 or y >= len(self.grid)
    
    def mark_visited(self, x: int, y: int) -> None:
        self.grid[y][x] = 'X'

    def move_player(self, direction: str) -> None:
        if direction == 'N':
            self.player.y -= 1
        elif direction == 'S':
            self.player.y += 1
        elif direction == 'E':
            self.player.x += 1
        elif direction == 'W':
            self.player.x -= 1
        self.mark_visited(self.player.x, self.player.y)

    def next_move_not_off_grid(self, direction: str) -> bool:
        next_x = self.player.x
        next_y = self.player.y
        if direction == 'N':
            next_y -= 1
        elif direction == 'S':
            next_y += 1
        elif direction == 'E':
            next_x += 1
        elif direction == 'W':
            next_x -= 1
        return not self.is_off_grid(next_x, next_y)
    
    def move_player_until_obstacle(self, direction: str) -> None:
        while self.valid_next_move(direction):
            self.move_player(direction)

    def valid_next_move(self, direction: str) -> bool:
        next_x = self.player.x
        next_y = self.player.y
        if direction == 'N':
            next_y -= 1
        elif direction == 'S':
            next_y += 1
        elif direction == 'E':
            next_x += 1
        elif direction == 'W':
            next_x -= 1
        return not self.is_obstacle(next_x, next_y) and not self.is_off_grid(next_x, next_y)
    
    def print_grid(self) -> None:
        for row in self.grid:
            print(''.join(row))

# TODO: Complete part1 of 2024/day06.py
def part1(input_lines: list[str]) -> int:
    grid = Grid(input_lines)
    while grid.next_move_not_off_grid(grid.player.direction):
        while grid.valid_next_move(grid.player.direction):
            grid.move_player(grid.player.direction)
            print(f"Moved {grid.player.direction} to {grid.player.x}, {grid.player.y}")
            grid.print_grid()
            input("Press Enter to continue...")
        grid.player.turn_right()

    # count the number of visited cells
    visit_count = 0
    for row in grid.grid:
        for cell in row:
            if cell == 'X':
                visit_count += 1
    # grid.print_grid()
    return visit_count

def part2(input_lines: list[str]) -> int:
    pass

if __name__ == "__main__":
    test_input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
    
    print(part1(test_input.strip().split('\n')))  # expect 41
    # print(part2(test_input.strip().split('\n')))  # expect ?
    # run_parts(part1, part2, 2024, 6)
