package day02

import (
	"bufio"
	"regexp"
	"strconv"
	"strings"
)

func part1(scanner *bufio.Scanner) int {
	result := 0
	for scanner.Scan() {
		line := scanner.Text()
		// fmt.Println(line)
		result += process_part1(line)
	}
	return result

}

func process_part1(data string) int {
	// Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
	re := regexp.MustCompile(`Game (\d+):(.*)`)
	found := re.FindStringSubmatch(data)
	index, _ := strconv.Atoi(found[1])
	subsets := found[2]
	d := map[string]int{
		"red": 0, "green": 0, "blue": 0,
	}
	for _, v := range strings.Split(strings.TrimSpace(subsets), ";") {
		for _, c := range strings.Split(strings.TrimSpace(v), ",") {
			cubes := strings.Split(strings.TrimSpace(c), " ")
			value, _ := strconv.Atoi(cubes[0])
			color := cubes[1]
			d[color] = max(value, d[color])
		}
	}
	if d["red"] <= 12 && d["green"] <= 13 && d["blue"] <= 14 {
		return index
	}

	return 0
}
