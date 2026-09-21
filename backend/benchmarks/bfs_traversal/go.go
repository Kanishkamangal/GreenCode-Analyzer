// Benchmark: BFS Traversal
// Category: Graph
// Algorithm: Breadth First Search - O(V + E)

package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    in := bufio.NewReader(os.Stdin)
    out := bufio.NewWriter(os.Stdout)
    defer out.Flush()

    var n, m int

    if _, err := fmt.Fscan(in, &n, &m); err != nil {
        return
    }

    if n <= 0 || m < 0 {
        return
    }

    adj := make([][]int, n)

    for i := 0; i < m; i++ {
        var u, v int

        if _, err := fmt.Fscan(in, &u, &v); err != nil {
            return
        }

        if u >= 0 && u < n &&
            v >= 0 && v < n {
            adj[u] = append(adj[u], v)
            adj[v] = append(adj[v], u)
        }
    }

    var source int

    if _, err := fmt.Fscan(in, &source); err != nil {
        return
    }

    if source < 0 || source >= n {
        return
    }

    visited := make([]bool, n)
    queue := make([]int, 0, n)

    visited[source] = true
    queue = append(queue, source)

    result := make([]int, 0, n)

    for front := 0; front < len(queue); front++ {
        node := queue[front]
        result = append(result, node)

        for _, next := range adj[node] {
            if !visited[next] {
                visited[next] = true
                queue = append(queue, next)
            }
        }
    }

    for i, node := range result {
        if i > 0 {
            fmt.Fprint(out, " ")
        }

        fmt.Fprint(out, node)
    }

    fmt.Fprintln(out)
}
