// Benchmark: String Reverse
// Category: Strings
// Algorithm: Two-Pointer String Reverse - O(n)

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

    val chars =
        values[0].toCharArray()

    var left = 0
    var right =
        chars.size - 1

    while (left < right) {
        val temp = chars[left]

        chars[left] =
            chars[right]

        chars[right] =
            temp

        left++
        right--
    }

    println(
        chars.concatToString()
    )
}
