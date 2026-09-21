// Benchmark: BFS Traversal
// Category: Graph
// Algorithm: Breadth First Search - O(V + E)

import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(
            new BufferedInputStream(System.in)
        );

        if (!sc.hasNextInt())
            return;

        int n = sc.nextInt();
        int m = sc.nextInt();

        if (n <= 0 || m < 0)
            return;

        ArrayList<Integer>[] adj =
            new ArrayList[n];

        for (int i = 0; i < n; i++)
            adj[i] = new ArrayList<>();

        for (int i = 0; i < m; i++) {
            int u = sc.nextInt();
            int v = sc.nextInt();

            if (u >= 0 && u < n &&
                v >= 0 && v < n) {
                adj[u].add(v);
                adj[v].add(u);
            }
        }

        if (!sc.hasNextInt())
            return;

        int source = sc.nextInt();

        if (source < 0 || source >= n)
            return;

        boolean[] visited = new boolean[n];
        ArrayDeque<Integer> queue =
            new ArrayDeque<>();

        visited[source] = true;
        queue.add(source);

        StringBuilder result =
            new StringBuilder();

        while (!queue.isEmpty()) {
            int node = queue.remove();

            if (result.length() > 0)
                result.append(' ');

            result.append(node);

            for (int next : adj[node]) {
                if (!visited[next]) {
                    visited[next] = true;
                    queue.add(next);
                }
            }
        }

        System.out.println(result);
    }
}
