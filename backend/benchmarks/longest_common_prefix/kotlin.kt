// Benchmark: Longest Common Prefix
// Category: Strings
// Algorithm: Vertical Scanning - O(total characters)

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

    var inputPosition = 0

    val n =
        values[inputPosition++]
            .toInt()

    if (n <= 0) {
        println("")
        return
    }

    val strings =
        Array(n) {
            values[inputPosition++]
        }

    var prefixLength = 0

    for (
        position in strings[0].indices
    ) {
        val current =
            strings[0][position]

        var matches = true

        for (i in 1 until n) {
            if (
                position >=
                    strings[i].length ||
                strings[i][position] != current
            ) {
                matches = false
                break
            }
        }

        if (!matches) {
            break
        }

        prefixLength++
    }

    println(
        strings[0].substring(
            0,
            prefixLength
        )
    )
}
