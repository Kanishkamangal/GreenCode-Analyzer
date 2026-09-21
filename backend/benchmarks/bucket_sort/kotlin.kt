// Benchmark: Bucket Sort
// Category: Sorting
// Algorithm: Bucket Sort - O(n + k) average

import kotlin.math.sqrt

fun insertionSort(
    bucket: MutableList<Long>
) {
    for (
        i in 1 until bucket.size
    ) {
        val key = bucket[i]
        var j = i - 1

        while (
            j >= 0 &&
            bucket[j] > key
        ) {
            bucket[j + 1] =
                bucket[j]

            j--
        }

        bucket[j + 1] = key
    }
}

fun bucketSort(
    a: MutableList<Long>
) {
    val n = a.size

    if (n <= 1) {
        return
    }

    var minValue = a[0]
    var maxValue = a[0]

    for (value in a) {
        if (value < minValue) {
            minValue = value
        }

        if (value > maxValue) {
            maxValue = value
        }
    }

    if (minValue == maxValue) {
        return
    }

    val bucketCount =
        maxOf(
            1,
            sqrt(n.toDouble())
                .toInt()
        )

    val buckets =
        MutableList(bucketCount) {
            mutableListOf<Long>()
        }

    val range =
        maxValue.toDouble() -
        minValue.toDouble() + 1.0

    for (value in a) {
        val offset =
            value.toDouble() -
            minValue.toDouble()

        var index = (
            offset *
            bucketCount /
            range
        ).toInt()

        if (index >= bucketCount) {
            index =
                bucketCount - 1
        }

        buckets[index].add(value)
    }

    var position = 0

    for (bucket in buckets) {
        insertionSort(bucket)

        for (value in bucket) {
            a[position++] = value
        }
    }
}

fun main() {
    val input =
        generateSequence(::readLine)
            .flatMap {
                it.trim()
                    .split(
                        Regex("\\s+")
                    )
                    .asSequence()
            }
            .filter {
                it.isNotEmpty()
            }
            .map {
                it.toLong()
            }
            .toMutableList()

    if (input.isNotEmpty()) {
        bucketSort(input)
    }

    println(
        if (input.isEmpty())
            0
        else
            input[input.size - 1]
    )
}
