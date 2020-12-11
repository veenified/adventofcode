package main

import (
	"fmt"

	"github.com/veenified/adventofcode/utils"
)

func day01() {
	var testInput = `1721
	979
	366
	299
	675
	1456`

	var input = testInput
	input = utils.Input(2020, 1)
	var inputInts = utils.ExtractInts(input)

out:
	for _, i := range inputInts {
		for _, j := range inputInts {
			if i+j == 2020 {
				fmt.Println(fmt.Sprintf("Part 1: %v", i*j))
				break out
			}
		}
	}
	for _, i := range inputInts {
		for _, j := range inputInts {
			for _, k := range inputInts {
				if i+j+k == 2020 {
					fmt.Println(fmt.Sprintf("Part 2: %v", i*j*k))
					return
				}
			}
		}
	}
}
