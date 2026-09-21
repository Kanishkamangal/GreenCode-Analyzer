// Benchmark: Radix Sort
// Category: Sorting
// Algorithm: LSD Radix Sort - O(d * (n + b))

fun radixSortNonNegative(
    a: MutableList<Long>
) {
    if (a.size <= 1) {
        return
    }

    var maxValue = a[0]

    for (value in a) {
        if (value > maxValue) {
            maxValue = value
        }
    }

    val output =
        LongArray(a.size)

    var exp = 1L

    while (maxValue / exp > 0) {
        val count = IntArray(10)

        for (value in a) {
            val digit =
                ((value / exp) % 10)
                    .toInt()

            count[digit]++
        }

        for (i in 1 until 10) {
            count[i] += count[i - 1]
        }

        for (
            i in a.size - 1 downTo 0
        ) {
            val digit =
                ((a[i] / exp) % 10)
                    .toInt()

            output[
                --count[digit]
            ] = a[i]
        }

        for (i in a.indices) {
            a[i] = output[i]
        }

        if (exp > maxValue / 10) {
            break
        }

        exp *= 10
    }
}

fun radixSort(
    a: MutableList<Long>
) {
    val negative =
        mutableListOf<Long>()

    val positive =
        mutableListOf<Long>()

    for (value in a) {
        if (value < 0) {
            negative.add(-value)
        } else {
            positive.add(value)
        }
    }

    radixSortNonNegative(negative)
    radixSortNonNegative(positive)

    var index = 0

    for (
        i in negative.size - 1 downTo 0
    ) {
        a[index++] = -negative[i]
    }

    for (value in positive) {
        a[index++] = value
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
        radixSort(input)
    }

    println(
        if (input.isEmpty())
            0
        else
            input[input.size - 1]
    )
}
