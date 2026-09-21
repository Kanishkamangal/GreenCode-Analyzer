// Benchmark: Character Frequency in String
// Category: Strings
// Algorithm: Linear Character Frequency Count - O(n)

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
    var target string

    if _, err := fmt.Fscan(
        in,
        &s,
    ); err != nil {
        return
    }

    if _, err := fmt.Fscan(
        in,
        &target,
    ); err != nil {
        return
    }

    if len(target) == 0 {
        return
    }

    var frequency int64 = 0

    for i := 0; i < len(s); i++ {
        if s[i] == target[0] {
            frequency++
        }
    }

    fmt.Fprintln(
        out,
        frequency,
    )
}
