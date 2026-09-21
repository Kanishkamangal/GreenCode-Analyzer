// Benchmark: Linear Search
// Category: Searching
// Algorithm: Linear Search - O(n)

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

    result := -1

    for i := 0; i < n; i++ {
        if a[i] == target {
            result = i
            break
        }
    }

    fmt.Fprintln(
        out,
        result,
    )
}
