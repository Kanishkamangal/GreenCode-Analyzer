// Benchmark: Substring Search
// Category: Strings
// Algorithm: Naive Substring Search - O(n * m)

package main

import (
    "bufio"
    "fmt"
    "os"
)

func substringSearch(
    text string,
    pattern string,
) int {
    n := len(text)
    m := len(pattern)

    if m == 0 {
        return 0
    }

    if m > n {
        return -1
    }

    for i := 0; i <= n-m; i++ {
        j := 0

        for j < m &&
            text[i+j] == pattern[j] {
            j++
        }

        if j == m {
            return i
        }
    }

    return -1
}

func main() {
    in := bufio.NewReader(os.Stdin)
    out := bufio.NewWriter(os.Stdout)
    defer out.Flush()

    var text string
    var pattern string

    if _, err := fmt.Fscan(
        in,
        &text,
    ); err != nil {
        return
    }

    if _, err := fmt.Fscan(
        in,
        &pattern,
    ); err != nil {
        return
    }

    fmt.Fprintln(
        out,
        substringSearch(
            text,
            pattern,
        ),
    )
}
