// Benchmark: Shell Sort
// Category: Sorting
// Algorithm: Shell Sort - Gap-based

package main

import (
    "bufio"
    "fmt"
    "os"
)

func shellSort(
    a []int64,
) {
    n := len(a)

    for gap := n / 2; gap > 0; gap /= 2 {
        for i := gap; i < n; i++ {
            temp := a[i]
            j := i

            for j >= gap &&
                a[j-gap] > temp {
                a[j] = a[j-gap]
                j -= gap
            }

            a[j] = temp
        }
    }
}

func main() {
    in := bufio.NewReader(os.Stdin)
    out := bufio.NewWriter(os.Stdout)
    defer out.Flush()

    a := make([]int64, 0)
    var x int64

    for {
        _, err := fmt.Fscan(
            in,
            &x,
        )

        if err != nil {
            break
        }

        a = append(
            a,
            x,
        )
    }

    if len(a) > 0 {
        shellSort(a)
    }

    if len(a) == 0 {
        fmt.Fprintln(
            out,
            0,
        )
    } else {
        fmt.Fprintln(
            out,
            a[len(a)-1],
        )
    }
}
