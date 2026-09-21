// Benchmark: Binary Search
// Category: Searching
// Algorithm: Binary Search - O(log n)

package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    in := bufio.NewReader(os.Stdin)
    out := bufio.NewWriter(os.Stdout)
    defer out.Flush()

    var n int

    if _, err := fmt.Fscan(
        in,
        &n,
    ); err != nil || n < 0 {
        return
    }

    a := make(
        []int64,
        n,
    )

    for i := 0; i < n; i++ {
        fmt.Fscan(
            in,
            &a[i],
        )
    }

    var target int64

    fmt.Fscan(
        in,
        &target,
    )

    left := 0
    right := n - 1
    result := -1

    for left <= right {
        mid :=
            left + (right-left)/2

        if a[mid] == target {
            result = mid
            break
        }

        if a[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }

    fmt.Fprintln(
        out,
        result,
    )
}
