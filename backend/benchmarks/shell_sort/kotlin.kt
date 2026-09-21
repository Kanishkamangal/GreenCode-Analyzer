// Benchmark: Shell Sort
// Category: Sorting
// Algorithm: Shell Sort - Gap-based

fun shellSort(
    a: MutableList<Long>
) {
    val n = a.size
    var gap = n / 2

    while (gap > 0) {
        for (
            i in gap until n
        ) {
            val temp = a[i]
            var j = i

            while (
                j >= gap &&
                a[j - gap] > temp
            ) {
                a[j] = a[j - gap]
                j -= gap
            }

            a[j] = temp
        }

        gap /= 2
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
        shellSort(input)
    }

    println(
        if (input.isEmpty())
            0
        else
            input[input.size - 1]
    )
}
