// Benchmark: Merge Sort
// Category: Sorting
// Algorithm: Merge Sort - O(n log n)

fun merge(
    a: MutableList<Long>,
    temp: LongArray,
    left: Int,
    mid: Int,
    right: Int
) {
    var i = left
    var j = mid + 1
    var k = left

    while (i <= mid && j <= right) {
        if (a[i] <= a[j]) {
            temp[k++] = a[i++]
        } else {
            temp[k++] = a[j++]
        }
    }

    while (i <= mid) {
        temp[k++] = a[i++]
    }

    while (j <= right) {
        temp[k++] = a[j++]
    }

    for (index in left..right) {
        a[index] = temp[index]
    }
}

fun mergeSort(
    a: MutableList<Long>,
    temp: LongArray,
    left: Int,
    right: Int
) {
    if (left >= right) {
        return
    }

    val mid = left + (right - left) / 2

    mergeSort(a, temp, left, mid)
    mergeSort(a, temp, mid + 1, right)

    merge(a, temp, left, mid, right)
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
        val temp = LongArray(input.size)

        mergeSort(
            input,
            temp,
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
