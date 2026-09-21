// Benchmark: Quick Sort
// Category: Sorting
// Algorithm: Quick Sort - O(n log n) average

fun partition(
    a: MutableList<Long>,
    low: Int,
    high: Int
): Int {
    val pivot = a[high]
    var i = low - 1

    for (j in low until high) {
        if (a[j] <= pivot) {
            i++

            val temp = a[i]
            a[i] = a[j]
            a[j] = temp
        }
    }

    val temp = a[i + 1]
    a[i + 1] = a[high]
    a[high] = temp

    return i + 1
}

fun quickSort(
    a: MutableList<Long>,
    low: Int,
    high: Int
) {
    if (low < high) {
        val pivotIndex = partition(
            a,
            low,
            high
        )

        quickSort(
            a,
            low,
            pivotIndex - 1
        )

        quickSort(
            a,
            pivotIndex + 1,
            high
        )
    }
}

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

    if (input.isNotEmpty()) {
        quickSort(
            input,
            0,
            input.size - 1
        )
    }

    println(
        if (input.isEmpty())
            0
        else
            input[input.size - 1]
    )
}
