// Benchmark: Merge Sort
// Category: Sorting
// Algorithm: Merge Sort - O(n log n)

package main

import (
    "bufio"
    "fmt"
    "os"
)

func merge(
    a []int64,
    temp []int64,
    left int,
    mid int,
    right int,
) {
    i := left
    j := mid + 1
    k := left

    for i <= mid && j <= right {
        if a[i] <= a[j] {
            temp[k] = a[i]
            i++
        } else {
            temp[k] = a[j]
            j++
        }
        k++
    }

    for i <= mid {
        temp[k] = a[i]
        i++
        k++
    }

    for j <= right {
        temp[k] = a[j]
        j++
        k++
    }

    for i = left; i <= right; i++ {
        a[i] = temp[i]
    }
}

func mergeSort(
    a []int64,
    temp []int64,
    left int,
    right int,
) {
    if left >= right {
        return
    }

    mid := left + (right-left)/2

    mergeSort(a, temp, left, mid)
    mergeSort(a, temp, mid+1, right)

    merge(a, temp, left, mid, right)
}

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

    if len(a) > 0 {
        temp := make([]int64, len(a))

        mergeSort(
            a,
            temp,
            0,
            len(a)-1,
        )
    }

    if len(a) == 0 {
        fmt.Fprintln(out, 0)
    } else {
        fmt.Fprintln(out, a[len(a)-1])
    }
}
