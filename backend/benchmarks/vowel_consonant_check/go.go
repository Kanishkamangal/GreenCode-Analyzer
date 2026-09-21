// Benchmark: Vowel or Consonant Check
// Category: Character
// Algorithm: Direct Character Check - O(1)

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

    var ch string

    if _, err := fmt.Fscan(
        in,
        &ch,
    ); err != nil || len(ch) == 0 {
        return
    }

    c := ch[0]

    vowel :=
        c == 'a' ||
            c == 'e' ||
            c == 'i' ||
            c == 'o' ||
            c == 'u' ||
            c == 'A' ||
            c == 'E' ||
            c == 'I' ||
            c == 'O' ||
            c == 'U'

    if vowel {
        fmt.Fprintln(out, 1)
    } else {
        fmt.Fprintln(out, 0)
    }
}
