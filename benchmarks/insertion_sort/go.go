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

    a := make([]int64, 0)

    var x int64

    for {
        _, err := fmt.Fscan(in, &x)

        if err != nil {
            break
        }

        a = append(a, x)
    }

    n := len(a)

    for i := 1; i < n; i++ {
        key := a[i]
        j := i - 1

        for j >= 0 && a[j] > key {
            a[j+1] = a[j]
            j--
        }

        a[j+1] = key
    }

    if n == 0 {
        fmt.Fprint(out, 0)
    } else {
        fmt.Fprint(out, a[n-1])
    }
}
