// Benchmark: Jump Search
// Category: Searching
// Algorithm: Jump Search - O(sqrt(n))

package main

import (
    "bufio"
    "fmt"
    "math"
    "os"
)

func jumpSearch(
    a []int64,
    target int64,
) int {
    n := len(a)

    if n == 0 {
        return -1
    }

    step := int(
        math.Sqrt(float64(n)),
    )

    if step < 1 {
        step = 1
    }

    previous := 0
    current := step

    for previous < n {
        end := current

        if end > n {
            end = n
        }

        if a[end-1] >= target {
            break
        }

        previous = current
        current += step

        if previous >= n {
            return -1
        }
    }

    end := current

    if end > n {
        end = n
    }

    for i := previous; i < end; i++ {
        if a[i] == target {
            return i
        }

        if a[i] > target {
            break
        }
    }

    return -1
}

func main() {
    in := bufio.NewReader(os.Stdin)
    out := bufio.NewWriter(os.Stdout)
    defer out.Flush()

    var n int

    if _, err := fmt.Fscan(
        in,
        &n,
    ); err != nil || n < 0 {
        return
    }

    a := make(
        []int64,
        n,
    )

    for i := 0; i < n; i++ {
        fmt.Fscan(
            in,
            &a[i],
        )
    }

    var target int64

    fmt.Fscan(
        in,
        &target,
    )

    result :=
        jumpSearch(
            a,
            target,
        )

    fmt.Fprintln(
        out,
        result,
    )
}
