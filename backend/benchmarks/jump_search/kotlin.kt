// Benchmark: Jump Search
// Category: Searching
// Algorithm: Jump Search - O(sqrt(n))

import kotlin.math.sqrt

fun jumpSearch(
    a: LongArray,
    target: Long
): Int {
    val n = a.size

    if (n == 0) {
        return -1
    }

    val step =
        maxOf(
            1,
            sqrt(n.toDouble())
                .toInt()
        )

    var previous = 0
    var current = step

    while (
        previous < n &&
        a[minOf(current, n) - 1]
            < target
    ) {
        previous = current
        current += step

        if (previous >= n) {
            return -1
        }
    }

    val end =
        minOf(current, n)

    for (
        i in previous until end
    ) {
        if (a[i] == target) {
            return i
        }

        if (a[i] > target) {
            break
        }
    }

    return -1
}

fun main() {
    val values =
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
            .toList()

    if (values.isEmpty()) {
        return
    }

    var position = 0

    val n =
        values[position++]
            .toInt()

    val a =
        LongArray(n)

    for (i in 0 until n) {
        a[i] =
            values[position++]
    }

    val target =
        values[position]

    println(
        jumpSearch(
            a,
            target
        )
    )
}
