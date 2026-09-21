// Benchmark: Linear Search
// Category: Searching
// Algorithm: Linear Search - O(n)

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

    var result = -1

    for (i in 0 until n) {
        if (a[i] == target) {
            result = i
            break
        }
    }

    println(result)
}
