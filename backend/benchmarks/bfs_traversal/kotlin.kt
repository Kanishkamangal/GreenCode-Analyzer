// Benchmark: BFS Traversal
// Category: Graph
// Algorithm: Breadth First Search - O(V + E)

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

    val n = tokens[index++].toInt()
    val m = tokens[index++].toInt()

    if (n <= 0 || m < 0)
        return

    val adj =
        Array(n) { mutableListOf<Int>() }

    repeat(m) {
        if (index + 1 >= tokens.size)
            return

        val u = tokens[index++].toInt()
        val v = tokens[index++].toInt()

        if (
            u in 0 until n &&
            v in 0 until n
        ) {
            adj[u].add(v)
            adj[v].add(u)
        }
    }

    if (index >= tokens.size)
        return

    val source = tokens[index].toInt()

    if (source !in 0 until n)
        return

    val visited = BooleanArray(n)
    val queue = ArrayDeque<Int>()
    val result = mutableListOf<Int>()

    visited[source] = true
    queue.addLast(source)

    while (queue.isNotEmpty()) {
        val node = queue.removeFirst()

        result.add(node)

        for (next in adj[node]) {
            if (!visited[next]) {
                visited[next] = true
                queue.addLast(next)
            }
        }
    }

    println(result.joinToString(" "))
}
