// Benchmark: BFS Traversal
// Category: Graph
// Algorithm: Breadth First Search - O(V + E)

using System;
using System.Collections.Generic;

public class Program
{
    public static void Main()
    {
        string[] tokens = Console.In
            .ReadToEnd()
            .Split(
                (char[])null,
                StringSplitOptions.RemoveEmptyEntries
            );

        if (tokens.Length < 2)
            return;

        int index = 0;

        int n = int.Parse(tokens[index++]);
        int m = int.Parse(tokens[index++]);

        if (n <= 0 || m < 0)
            return;

        List<int>[] adj =
            new List<int>[n];

        for (int i = 0; i < n; i++)
            adj[i] = new List<int>();

        for (int i = 0; i < m; i++)
        {
            if (index + 1 >= tokens.Length)
                return;

            int u = int.Parse(tokens[index++]);
            int v = int.Parse(tokens[index++]);

            if (
                u >= 0 && u < n &&
                v >= 0 && v < n
            )
            {
                adj[u].Add(v);
                adj[v].Add(u);
            }
        }

        if (index >= tokens.Length)
            return;

        int source =
            int.Parse(tokens[index]);

        if (source < 0 || source >= n)
            return;

        bool[] visited = new bool[n];
        Queue<int> queue = new Queue<int>();
        List<int> result = new List<int>();

        visited[source] = true;
        queue.Enqueue(source);

        while (queue.Count > 0)
        {
            int node = queue.Dequeue();

            result.Add(node);

            foreach (int next in adj[node])
            {
                if (!visited[next])
                {
                    visited[next] = true;
                    queue.Enqueue(next);
                }
            }
        }

        Console.WriteLine(
            string.Join(" ", result)
        );
    }
}
