package main

import (
	"fmt"
	"strings"

	"github.com/veenified/adventofcode/utils"
)

type policy struct {
	Lowerbound, Upperbound int
	Character              byte
	Password               string
}

func day02() {
	var testInput = `1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc`

	var input = testInput
	input = utils.Input(2020, 2)

	var policies []policy
	utils.Parse(&policies, "%d-%d %c: %s", input)

	fmt.Println(utils.Count(0, len(policies), func(i int) bool {
		p := policies[i]
		n := strings.Count(p.Password, string(p.Character))
		return n >= p.Lowerbound && n <= p.Upperbound
	}))

	fmt.Println(utils.Count(0, len(policies), func(i int) bool {
		p := policies[i]
		return (p.Password[p.Lowerbound-1] == p.Character) != /* XOR */ (p.Password[p.Upperbound-1] == p.Character)
	}))
}
