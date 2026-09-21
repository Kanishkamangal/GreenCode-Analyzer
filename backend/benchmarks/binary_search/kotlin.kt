// Benchmark: Binary Search
// Category: Searching
// Algorithm: Binary Search - O(log n)

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

    var left = 0
    var right = n - 1
    var result = -1

    while (left <= right) {
        val mid =
            left + (right - left) / 2

        if (a[mid] == target) {
            result = mid
            break
        }

        if (a[mid] < target) {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }

    println(result)
}
