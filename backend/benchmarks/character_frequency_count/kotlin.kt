// Benchmark: Character Frequency Count
// Category: Character
// Algorithm: Linear Frequency Count - O(n)

fun main() {
    val values =
        generateSequence(::readLine)
            .flatMap {
                it.trim()
                    .split(Regex("\\s+"))
                    .asSequence()
            }
            .filter {
                it.isNotEmpty()
            }
            .toList()

    if (values.size < 2) {
        return
    }

    val s = values[0]
    val target = values[1][0]

    var count = 0L

    for (i in s.indices) {
        if (s[i] == target) {
            count++
        }
    }

    println(count)
}
