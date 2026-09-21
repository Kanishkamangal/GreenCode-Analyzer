// Benchmark: 0/1 Knapsack
// Category: Dynamic Programming
// Algorithm: 0/1 Knapsack - O(n * capacity)

fun main() {
    val tokens = generateSequence { readLine() }
        .flatMap {
            it.trim()
                .split(Regex("\\s+"))
                .asSequence()
        }
        .filter { it.isNotEmpty() }
        .toList()

    if (tokens.size < 2)
        return

    var index = 0

    val n =
        tokens[index++].toInt()

    val capacity =
        tokens[index++].toInt()

    if (
        n < 0 ||
        capacity < 0 ||
        tokens.size < 2 + 2 * n
    )
        return

    val weights =
        IntArray(n)

    val values =
        LongArray(n)

    for (i in 0 until n)
        weights[i] =
            tokens[index++].toInt()

    for (i in 0 until n)
        values[i] =
            tokens[index++].toLong()

    val dp =
        LongArray(capacity + 1)

    for (i in 0 until n) {
        val weight = weights[i]
        val value = values[i]

        if (weight <= 0)
            continue

        for (c in capacity downTo weight) {
            val candidate =
                dp[c - weight] + value

            if (candidate > dp[c])
                dp[c] = candidate
        }
    }

    println(dp[capacity])
}
