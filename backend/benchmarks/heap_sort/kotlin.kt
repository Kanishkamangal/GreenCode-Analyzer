// Benchmark: Heap Sort
// Category: Sorting
// Algorithm: Heap Sort - O(n log n)

fun heapify(
    a: MutableList<Long>,
    n: Int,
    i: Int
) {
    var largest = i
    val left = 2 * i + 1
    val right = 2 * i + 2

    if (
        left < n &&
        a[left] > a[largest]
    ) {
        largest = left
    }

    if (
        right < n &&
        a[right] > a[largest]
    ) {
        largest = right
    }

    if (largest != i) {
        val temp = a[i]
        a[i] = a[largest]
        a[largest] = temp

        heapify(
            a,
            n,
            largest
        )
    }
}

fun heapSort(
    a: MutableList<Long>
) {
    val n = a.size

    for (
        i in (n / 2 - 1) downTo 0
    ) {
        heapify(
            a,
            n,
            i
        )
    }

    for (
        i in (n - 1) downTo 1
    ) {
        val temp = a[0]
        a[0] = a[i]
        a[i] = temp

        heapify(
            a,
            i,
            0
        )
    }
}

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
            .map {
                it.toLong()
            }
            .toMutableList()

    if (input.isNotEmpty()) {
        heapSort(input)
    }

    println(
        if (input.isEmpty())
            0
        else
            input[input.size - 1]
    )
}
