fun main() {
    val input = generateSequence(::readLine)
        .flatMap {
            it.trim()
                .split(Regex("\\s+"))
                .asSequence()
        }
        .filter {
            it.isNotEmpty()
        }
        .map {
            it.toLong()
        }
        .toMutableList()

    val n = input.size

    for (i in 1 until n) {
        val key = input[i]
        var j = i - 1

        while (
            j >= 0 &&
            input[j] > key
        ) {
            input[j + 1] = input[j]
            j--
        }

        input[j + 1] = key
    }

    print(
        if (input.isEmpty())
            0
        else
            input[input.size - 1]
    )
}
