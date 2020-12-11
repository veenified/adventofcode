package main

import (
	"fmt"
	"strings"

	"github.com/veenified/adventofcode/utils"
)

var testInput = `1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc`

type policy struct {
	Lowerbound, Upperbound int
	Character              byte
	Password               string
}

var day02Input = utils.Input(2020, 2)

func day02() {
	var policies []policy
	utils.Parse(&policies, "%d-%d %c: %s", day02Input)

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
