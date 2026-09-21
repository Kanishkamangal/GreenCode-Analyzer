// Benchmark: Palindrome Check
// Category: Strings
// Algorithm: Two-Pointer Palindrome Check - O(n)

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

    left := 0
    right := len(s) - 1
    palindrome := true

    for left < right {
        if s[left] != s[right] {
            palindrome = false
            break
        }

        left++
        right--
    }

    if palindrome {
        fmt.Fprintln(out, 1)
    } else {
        fmt.Fprintln(out, 0)
    }
}
