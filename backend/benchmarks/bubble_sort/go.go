// Benchmark: Bubble Sort
// Category: Sorting
// Algorithm: Bubble Sort - O(n^2)

package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {

	in := bufio.NewReader(os.Stdin)

	var a []int64

	for {
		var x int64

		_, err := fmt.Fscan(in, &x)

		if err != nil {
			break
		}

		a = append(a, x)
	}

	n := len(a)

	for i := 0; i < n-1; i++ {

		swapped := false

		for j := 0; j < n-i-1; j++ {

			if a[j] > a[j+1] {

				a[j], a[j+1] = a[j+1], a[j]

				swapped = true
			}
		}

		if !swapped {
			break
		}
	}

	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	if n == 0 {
		fmt.Fprintln(out, 0)
	} else {
		fmt.Fprintln(out, a[n-1])
	}
}