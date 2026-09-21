// Benchmark: Longest Common Subsequence
// Category: Strings
// Algorithm: Dynamic Programming LCS - O(n * m)

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
            .toList()

    if (values.size < 2) {
        return
    }

    val first = values[0]
    val second = values[1]

    val n = first.length
    val m = second.length

    var previous =
        IntArray(m + 1)

    var current =
        IntArray(m + 1)

    for (i in 1..n) {
        current[0] = 0

        for (j in 1..m) {
            if (
                first[i - 1] ==
                second[j - 1]
            ) {
                current[j] =
                    previous[j - 1] + 1
            } else {
                current[j] =
                    maxOf(
                        previous[j],
                        current[j - 1]
                    )
            }
        }

        val temp = previous
        previous = current
        current = temp
    }

    println(
        previous[m]
    )
}
