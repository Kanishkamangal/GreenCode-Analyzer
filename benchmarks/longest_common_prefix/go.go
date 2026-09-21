// Benchmark: Longest Common Prefix
// Category: Strings
// Algorithm: Vertical Scanning - O(total characters)

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
    ); err != nil {
        return
    }

    if n <= 0 {
        fmt.Fprintln(out)
        return
    }

    strings := make(
        []string,
        n,
    )

    for i := 0; i < n; i++ {
        fmt.Fscan(
            in,
            &strings[i],
        )
    }

    prefixLength := 0

    for position := 0;
        position < len(strings[0]);
        position++ {

        current :=
            strings[0][position]

        matches := true

        for i := 1; i < n; i++ {
            if position >= len(strings[i]) ||
                strings[i][position] != current {

                matches = false
                break
            }
        }

        if !matches {
            break
        }

        prefixLength++
    }

    fmt.Fprintln(
        out,
        strings[0][:prefixLength],
    )
}
