package day02

import (
	"bufio"
	"fmt"
	"os"
	"reflect"
	"testing"
)

func Test_part1(t *testing.T) {
	tests := []struct {
		filename string
		result   int
	}{
		{
			filename: "input02.sample.txt",
			result:   8,
		},
	}

	for _, test := range tests {
		t.Run(test.filename, func(t *testing.T) {
			file, err := os.Open(test.filename)
			if err != nil {
				panic(err)
			}
			defer file.Close()
			scanner := bufio.NewScanner(file)

			got := part1(scanner)
			want := test.result
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func Test_main(t *testing.T) {
	file, err := os.Open("input02.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	got := part1(scanner)
	fmt.Println("\n============\nResult:", got)
}
