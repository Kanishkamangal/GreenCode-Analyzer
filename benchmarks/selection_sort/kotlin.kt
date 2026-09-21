fun main() {
    val input = generateSequence(::readLine)
        .flatMap { it.trim().split(Regex("\\s+")).asSequence() }
        .filter { it.isNotEmpty() }
        .map { it.toLong() }
        .toMutableList()

    val n = input.size

    for (i in 0 until maxOf(0, n - 1)) {
        var minIndex = i

        for (j in i + 1 until n) {
            if (input[j] < input[minIndex])
                minIndex = j
        }

        if (minIndex != i) {
            val temp = input[i]
            input[i] = input[minIndex]
            input[minIndex] = temp
        }
    }

    print(if (input.isEmpty()) 0 else input[input.size - 1])
}
