// Benchmark: Longest Palindromic Substring
// Category: Strings
// Algorithm: Expand Around Center - O(n^2)

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

    var s string

    if _, err := fmt.Fscan(
        in,
        &s,
    ); err != nil {
        return
    }

    n := len(s)
    bestStart := 0
    bestLength := 1

    for center := 0; center < n; center++ {
        left := center
        right := center

        for left >= 0 &&
            right < n &&
            s[left] == s[right] {

            length :=
                right - left + 1

            if length > bestLength {
                bestStart = left
                bestLength = length
            }

            left--
            right++
        }

        left = center
        right = center + 1

        for left >= 0 &&
            right < n &&
            s[left] == s[right] {

            length :=
                right - left + 1

            if length > bestLength {
                bestStart = left
                bestLength = length
            }

            left--
            right++
        }
    }

    fmt.Fprintln(
        out,
        s[bestStart:bestStart+bestLength],
    )
}
