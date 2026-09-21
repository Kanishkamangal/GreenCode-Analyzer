// Benchmark: Longest Palindromic Substring
// Category: Strings
// Algorithm: Expand Around Center - O(n^2)

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

    if (values.isEmpty()) {
        return
    }

    val s = values[0]

    val n = s.length
    var bestStart = 0
    var bestLength = 1

    for (center in 0 until n) {
        var left = center
        var right = center

        while (
            left >= 0 &&
            right < n &&
            s[left] == s[right]
        ) {
            val length =
                right - left + 1

            if (length > bestLength) {
                bestStart = left
                bestLength = length
            }

            left--
            right++
        }

        left = center
        right = center + 1

        while (
            left >= 0 &&
            right < n &&
            s[left] == s[right]
        ) {
            val length =
                right - left + 1

            if (length > bestLength) {
                bestStart = left
                bestLength = length
            }

            left--
            right++
        }
    }

    println(
        s.substring(
            bestStart,
            bestStart + bestLength
        )
    )
}
