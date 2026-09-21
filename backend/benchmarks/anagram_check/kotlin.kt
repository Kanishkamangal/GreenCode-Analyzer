// Benchmark: Anagram Check
// Category: String
// Algorithm: Anagram Check - O(n)

fun main() {
    val tokens = generateSequence { readLine() }
        .flatMap { it.trim().split(Regex("\s+")).asSequence() }
        .filter { it.isNotEmpty() }
        .toList()

    if (tokens.size < 2) {
        println(0)
        return
    }

    val s1 = tokens[0]
    val s2 = tokens[1]

    if (s1.length != s2.length) {
        println(0)
        return
    }

    val count = HashMap<Char, Int>()

    for (c in s1)
        count[c] = (count[c] ?: 0) + 1

    for (c in s2)
        count[c] = (count[c] ?: 0) - 1

    println(if (count.values.all { it == 0 }) 1 else 0)
}
