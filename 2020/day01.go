package main

import (
	"fmt"

	"github.com/veenified/adventofcode/utils"
)

var input = utils.Input(2020, 1)
var inputInts = utils.ExtractInts(input)

func main() {
outer:
	for _, i := range inputInts {
		for _, j := range inputInts {
			if i+j == 2020 {
				fmt.Println(fmt.Sprintf("Part 1: %v", i*j))
				break outer
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
