// Benchmark: Substring Search
// Category: Strings
// Algorithm: Naive Substring Search - O(n * m)

fun substringSearch(
    text: String,
    pattern: String
): Int {
    val n = text.length
    val m = pattern.length

    if (m == 0) {
        return 0
    }

    if (m > n) {
        return -1
    }

    for (i in 0..n - m) {
        var j = 0

        while (
            j < m &&
            text[i + j] ==
            pattern[j]
        ) {
            j++
        }

        if (j == m) {
            return i
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
            .toList()

    if (values.size < 2) {
        return
    }

    val text = values[0]
    val pattern = values[1]

    println(
        substringSearch(
            text,
            pattern
        )
    )
}
