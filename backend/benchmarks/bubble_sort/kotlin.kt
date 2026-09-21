// Benchmark: Bubble Sort
// Category: Sorting
// Algorithm: Bubble Sort - O(n^2)

import java.io.BufferedReader
import java.io.InputStreamReader
import java.util.StringTokenizer

fun main() {

    val br = BufferedReader(InputStreamReader(System.`in`))

    val a = ArrayList<Long>()

    var line: String?

    while (true) {

        line = br.readLine()

        if (line == null) {
            break
        }

        val st = StringTokenizer(line)

        while (st.hasMoreTokens()) {
            a.add(st.nextToken().toLong())
        }
    }

    val n = a.size

    for (i in 0 until maxOf(0, n - 1)) {

        var swapped = false

        for (j in 0 until n - i - 1) {

            if (a[j] > a[j + 1]) {

                val temp = a[j]
                a[j] = a[j + 1]
                a[j + 1] = temp

                swapped = true
            }
        }

        if (!swapped) {
            break
        }
    }

    println(if (n == 0) 0 else a[n - 1])
}