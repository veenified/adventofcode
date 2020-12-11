package main

import "lukechampine.com/advent/utils"

func day03() {
	var testInput = `..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#`

	var input = testInput
	input = utils.Input(2020, 3)

	utils.Println(countTreesHit(3, 1, input))
	utils.Println(countTreesHit(1, 1, input) *
		countTreesHit(3, 1, input) *
		countTreesHit(5, 1, input) *
		countTreesHit(7, 1, input) *
		countTreesHit(1, 2, input))
}

func countTreesHit(dx, dy int, input string) (n int) {
	var lines = utils.Lines(input)
	var maxX = len(lines[0])

	x, y := 0, 0
	for y < len(lines) {
		if lines[y][x] == '#' {
			n++
		}
		x = (x + dx) % maxX
		y += dy
	}
	return
}
