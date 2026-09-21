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

    for i := 0; i < n-1; i++ {
        minIndex := i

        for j := i + 1; j < n; j++ {
            if a[j] < a[minIndex] {
                minIndex = j
            }
        }

        if minIndex != i {
            a[i], a[minIndex] = a[minIndex], a[i]
        }
    }

    if n == 0 {
        fmt.Fprint(out, 0)
    } else {
        fmt.Fprint(out, a[n-1])
    }
}
