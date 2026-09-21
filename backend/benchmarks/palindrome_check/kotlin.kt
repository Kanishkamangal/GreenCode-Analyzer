// Benchmark: Palindrome Check
// Category: Strings
// Algorithm: Two-Pointer Palindrome Check - O(n)

fun main() {
    val input =
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

    if (input.isEmpty()) {
        return
    }

    val s = input[0]

    var left = 0
    var right = s.length - 1
    var palindrome = true

    while (left < right) {
        if (s[left] != s[right]) {
            palindrome = false
            break
        }

        left++
        right--
    }

    println(
        if (palindrome) 1 else 0
    )
}
