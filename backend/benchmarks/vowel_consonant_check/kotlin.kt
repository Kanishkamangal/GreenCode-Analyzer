// Benchmark: Vowel or Consonant Check
// Category: Character
// Algorithm: Direct Character Check - O(1)

fun main() {
    val input =
        generateSequence(::readLine)
            .joinToString("")
            .trim()

    if (input.isEmpty()) {
        return
    }

    val ch = input[0]

    val vowel =
        ch == 'a' ||
        ch == 'e' ||
        ch == 'i' ||
        ch == 'o' ||
        ch == 'u' ||
        ch == 'A' ||
        ch == 'E' ||
        ch == 'I' ||
        ch == 'O' ||
        ch == 'U'

    println(
        if (vowel) 1 else 0
    )
}
