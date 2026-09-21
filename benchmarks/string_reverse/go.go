// Benchmark: String Reverse
// Category: Strings
// Algorithm: Two-Pointer String Reverse - O(n)

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

    chars := []byte(s)

    left := 0
    right := len(chars) - 1

    for left < right {
        temp := chars[left]
        chars[left] = chars[right]
        chars[right] = temp

        left++
        right--
    }

    fmt.Fprintln(
        out,
        string(chars),
    )
}
