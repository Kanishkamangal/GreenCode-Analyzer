// Benchmark: Radix Sort
// Category: Sorting
// Algorithm: LSD Radix Sort - O(d * (n + b))

package main

import (
    "bufio"
    "fmt"
    "os"
)

func radixSortNonNegative(
    a []uint64,
) {
    if len(a) <= 1 {
        return
    }

    maxValue := a[0]

    for _, value := range a {
        if value > maxValue {
            maxValue = value
        }
    }

    output := make(
        []uint64,
        len(a),
    )

    for exp := uint64(1); maxValue/exp > 0; {
        count := make([]int, 10)

        for _, value := range a {
            digit := (value / exp) % 10
            count[digit]++
        }

        for i := 1; i < 10; i++ {
            count[i] += count[i-1]
        }

        for i := len(a) - 1; i >= 0; i-- {
            digit := (a[i] / exp) % 10

            count[digit]--

            output[
                count[digit]
            ] = a[i]
        }

        copy(a, output)

        if exp > maxValue/10 {
            break
        }

        exp *= 10
    }
}

func radixSort(
    a []int64,
) {
    negative := make(
        []uint64,
        0,
    )

    positive := make(
        []uint64,
        0,
    )

    for _, value := range a {
        if value < 0 {
            negative = append(
                negative,
                uint64(-(value+1))+1,
            )
        } else {
            positive = append(
                positive,
                uint64(value),
            )
        }
    }

    radixSortNonNegative(negative)
    radixSortNonNegative(positive)

    index := 0

    for i := len(negative) - 1; i >= 0; i-- {
        a[index] =
            -int64(negative[i])

        index++
    }

    for _, value := range positive {
        a[index] =
            int64(value)

        index++
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
        radixSort(a)
    }

    if len(a) == 0 {
        fmt.Fprintln(out, 0)
    } else {
        fmt.Fprintln(
            out,
            a[len(a)-1],
        )
    }
}
