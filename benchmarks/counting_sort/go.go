// Benchmark: Counting Sort
// Category: Sorting
// Algorithm: Counting Sort - O(n + k)

package main

import (
    "bufio"
    "fmt"
    "os"
)

func countingSort(
    a []int64,
) {
    if len(a) <= 1 {
        return
    }

    minValue := a[0]
    maxValue := a[0]

    for _, value := range a {
        if value < minValue {
            minValue = value
        }

        if value > maxValue {
            maxValue = value
        }
    }

    size := int(
        maxValue - minValue + 1,
    )

    count := make(
        []int,
        size,
    )

    for _, value := range a {
        count[
            int(value-minValue)
        ]++
    }

    index := 0

    for i := 0; i < size; i++ {
        for count[i] > 0 {
            a[index] =
                int64(i) + minValue

            index++
            count[i]--
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
        countingSort(a)
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
