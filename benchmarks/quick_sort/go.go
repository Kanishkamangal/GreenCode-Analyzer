// Benchmark: Quick Sort
// Category: Sorting
// Algorithm: Quick Sort - O(n log n) average

package main

import (
    "bufio"
    "fmt"
    "os"
)

func partition(
    a []int64,
    low int,
    high int,
) int {
    pivot := a[high]
    i := low - 1

    for j := low; j < high; j++ {
        if a[j] <= pivot {
            i++
            a[i], a[j] = a[j], a[i]
        }
    }

    a[i+1], a[high] = a[high], a[i+1]

    return i + 1
}

func quickSort(
    a []int64,
    low int,
    high int,
) {
    if low < high {
        pivotIndex := partition(
            a,
            low,
            high,
        )

        quickSort(
            a,
            low,
            pivotIndex-1,
        )

        quickSort(
            a,
            pivotIndex+1,
            high,
        )
    }
}

func main() {
    in := bufio.NewReader(os.Stdin)
    out := bufio.NewWriter(os.Stdout)
    defer out.Flush()

    a := make([]int64, 0)
    var x int64

    for {
        _, err := fmt.Fscan(in, &x)

        if err != nil {
            break
        }

        a = append(a, x)
    }

    if len(a) > 0 {
        quickSort(
            a,
            0,
            len(a)-1,
        )
    }

    if len(a) == 0 {
        fmt.Fprintln(out, 0)
    } else {
        fmt.Fprintln(out, a[len(a)-1])
    }
}
