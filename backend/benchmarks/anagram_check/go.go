// Benchmark: Anagram Check
// Category: String
// Algorithm: Anagram Check - O(n)

package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    in := bufio.NewReader(os.Stdin)

    var s1, s2 string

    if _, err := fmt.Fscan(in, &s1, &s2); err != nil {
        fmt.Println(0)
        return
    }

    if len(s1) != len(s2) {
        fmt.Println(0)
        return
    }

    count := make(map[byte]int)

    for i := 0; i < len(s1); i++ {
        count[s1[i]]++
    }

    for i := 0; i < len(s2); i++ {
        count[s2[i]]--
    }

    for _, value := range count {
        if value != 0 {
            fmt.Println(0)
            return
        }
    }

    fmt.Println(1)
}
