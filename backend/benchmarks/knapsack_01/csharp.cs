// Benchmark: 0/1 Knapsack
// Category: Dynamic Programming
// Algorithm: 0/1 Knapsack - O(n * capacity)

using System;

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

        int n =
            int.Parse(tokens[index++]);

        int capacity =
            int.Parse(tokens[index++]);

        if (
            n < 0 ||
            capacity < 0 ||
            tokens.Length < 2 + 2 * n
        )
            return;

        int[] weights =
            new int[n];

        long[] values =
            new long[n];

        for (int i = 0; i < n; i++)
            weights[i] =
                int.Parse(tokens[index++]);

        for (int i = 0; i < n; i++)
            values[i] =
                long.Parse(tokens[index++]);

        long[] dp =
            new long[capacity + 1];

        for (int i = 0; i < n; i++)
        {
            int weight = weights[i];
            long value = values[i];

            if (weight <= 0)
                continue;

            for (
                int c = capacity;
                c >= weight;
                c--
            )
            {
                long candidate =
                    dp[c - weight] + value;

                if (candidate > dp[c])
                    dp[c] = candidate;
            }
        }

        Console.WriteLine(
            dp[capacity]
        );
    }
}
