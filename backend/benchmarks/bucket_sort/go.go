// Benchmark: Bucket Sort
// Category: Sorting
// Algorithm: Bucket Sort - O(n + k) average

package main

import (
    "bufio"
    "fmt"
    "math"
    "os"
)

func insertionSort(
    bucket []int64,
) {
    for i := 1; i < len(bucket); i++ {
        key := bucket[i]
        j := i - 1

        for j >= 0 &&
            bucket[j] > key {
            bucket[j+1] =
                bucket[j]

            j--
        }

        bucket[j+1] = key
    }
}

func bucketSort(
    a []int64,
) {
    n := len(a)

    if n <= 1 {
        return
    }

    minValue := a[0]
    maxValue := a[0]

    for _, value := range a {
        if value < minValue {
            minValue = value
        }

        if value > maxValue {
            maxValue = value
        }
    }

    if minValue == maxValue {
        return
    }

    bucketCount := int(
        math.Sqrt(float64(n)),
    )

    if bucketCount < 1 {
        bucketCount = 1
    }

    buckets := make(
        [][]int64,
        bucketCount,
    )

    valueRange :=
        float64(maxValue) -
            float64(minValue) + 1.0

    for _, value := range a {
        offset :=
            float64(value) -
                float64(minValue)

        index := int(
            offset *
                float64(bucketCount) /
                valueRange,
        )

        if index >= bucketCount {
            index =
                bucketCount - 1
        }

        buckets[index] = append(
            buckets[index],
            value,
        )
    }

    position := 0

    for i := 0; i < bucketCount; i++ {
        insertionSort(
            buckets[i],
        )

        for _, value :=
            range buckets[i] {
            a[position] = value
            position++
        }
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
        bucketSort(a)
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
