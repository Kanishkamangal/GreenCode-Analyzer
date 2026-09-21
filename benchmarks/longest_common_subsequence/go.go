// Benchmark: Longest Common Subsequence
// Category: Strings
// Algorithm: Dynamic Programming LCS - O(n * m)

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

    var first string
    var second string

    if _, err := fmt.Fscan(
        in,
        &first,
    ); err != nil {
        return
    }

    if _, err := fmt.Fscan(
        in,
        &second,
    ); err != nil {
        return
    }

    n := len(first)
    m := len(second)

    previous :=
        make([]int, m+1)

    current :=
        make([]int, m+1)

    for i := 1; i <= n; i++ {
        current[0] = 0

        for j := 1; j <= m; j++ {
            if first[i-1] ==
                second[j-1] {

                current[j] =
                    previous[j-1] + 1
            } else {
                if previous[j] >
                    current[j-1] {

                    current[j] =
                        previous[j]
                } else {
                    current[j] =
                        current[j-1]
                }
            }
        }

        previous, current =
            current, previous
    }

    fmt.Fprintln(
        out,
        previous[m],
    )
}
