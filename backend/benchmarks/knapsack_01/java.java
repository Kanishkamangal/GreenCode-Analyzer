// Benchmark: 0/1 Knapsack
// Category: Dynamic Programming
// Algorithm: 0/1 Knapsack - O(n * capacity)

import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args)
        throws Exception {

        BufferedInputStream in =
            new BufferedInputStream(System.in);

        Scanner sc = new Scanner(in);

        if (!sc.hasNextInt())
            return;

        int n = sc.nextInt();
        int capacity = sc.nextInt();

        if (n < 0 || capacity < 0)
            return;

        int[] weights = new int[n];
        long[] values = new long[n];

        for (int i = 0; i < n; i++)
            weights[i] = sc.nextInt();

        for (int i = 0; i < n; i++)
            values[i] = sc.nextLong();

        long[] dp =
            new long[capacity + 1];

        for (int i = 0; i < n; i++) {
            int weight = weights[i];
            long value = values[i];

            if (weight <= 0)
                continue;

            for (
                int c = capacity;
                c >= weight;
                c--
            ) {
                long candidate =
                    dp[c - weight] + value;

                if (candidate > dp[c])
                    dp[c] = candidate;
            }
        }

        System.out.println(dp[capacity]);
    }
}
