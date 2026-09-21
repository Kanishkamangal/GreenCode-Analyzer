// Benchmark: Heap Sort
// Category: Sorting
// Algorithm: Heap Sort - O(n log n)

package main

import (
    "bufio"
    "fmt"
    "os"
)

func heapify(
    a []int64,
    n int,
    i int,
) {
    largest := i
    left := 2*i + 1
    right := 2*i + 2

    if left < n &&
        a[left] > a[largest] {
        largest = left
    }

    if right < n &&
        a[right] > a[largest] {
        largest = right
    }

    if largest != i {
        a[i], a[largest] =
            a[largest], a[i]

        heapify(
            a,
            n,
            largest,
        )
    }
}

func heapSort(
    a []int64,
) {
    n := len(a)

    for i := n/2 - 1; i >= 0; i-- {
        heapify(
            a,
            n,
            i,
        )
    }

    for i := n - 1; i > 0; i-- {
        a[0], a[i] =
            a[i], a[0]

        heapify(
            a,
            i,
            0,
        )
    }
}

func main() {
    in := bufio.NewReader(os.Stdin)
    out := bufio.NewWriter(os.Stdout)
    defer out.Flush()

    a := make([]int64, 0)
    var x int64

    for {
        _, err := fmt.Fscan(
            in,
            &x,
        )

        if err != nil {
            break
        }

        a = append(
            a,
            x,
        )
    }

    if len(a) > 0 {
        heapSort(a)
    }

    if len(a) == 0 {
        fmt.Fprintln(
            out,
            0,
        )
    } else {
        fmt.Fprintln(
            out,
            a[len(a)-1],
        )
    }
}
