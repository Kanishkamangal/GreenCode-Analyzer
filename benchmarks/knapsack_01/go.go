// Benchmark: 0/1 Knapsack
// Category: Dynamic Programming
// Algorithm: 0/1 Knapsack - O(n * capacity)

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

    var n, capacity int

    if _, err := fmt.Fscan(
        in,
        &n,
        &capacity,
    ); err != nil {
        return
    }

    if n < 0 || capacity < 0 {
        return
    }

    weights := make([]int, n)
    values := make([]int64, n)

    for i := 0; i < n; i++ {
        if _, err := fmt.Fscan(
            in,
            &weights[i],
        ); err != nil {
            return
        }
    }

    for i := 0; i < n; i++ {
        if _, err := fmt.Fscan(
            in,
            &values[i],
        ); err != nil {
            return
        }
    }

    dp := make(
        []int64,
        capacity+1,
    )

    for i := 0; i < n; i++ {
        weight := weights[i]
        value := values[i]

        if weight <= 0 {
            continue
        }

        for c := capacity; c >= weight; c-- {
            candidate :=
                dp[c-weight] + value

            if candidate > dp[c] {
                dp[c] = candidate
            }
        }
    }

    fmt.Fprintln(
        out,
        dp[capacity],
    )
}
