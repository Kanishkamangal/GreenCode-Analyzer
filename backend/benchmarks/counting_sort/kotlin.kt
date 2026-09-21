// Benchmark: Counting Sort
// Category: Sorting
// Algorithm: Counting Sort - O(n + k)

fun countingSort(
    a: MutableList<Long>
) {
    if (a.size <= 1) {
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

    val range =
        (maxValue - minValue + 1)
            .toInt()

    val count =
        LongArray(range)

    for (value in a) {
        count[
            (value - minValue)
                .toInt()
        ]++
    }

    var index = 0

    for (i in 0 until range) {
        while (count[i] > 0) {
            a[index++] =
                i.toLong() + minValue

            count[i]--
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
        countingSort(input)
    }

    println(
        if (input.isEmpty())
            0
        else
            input[input.size - 1]
    )
}
