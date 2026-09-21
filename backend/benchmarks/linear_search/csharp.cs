// Benchmark: Linear Search
// Category: Searching
// Algorithm: Linear Search - O(n)

using System;

class Program
{
    static void Main()
    {
        string input =
            Console.In.ReadToEnd();

        string[] parts = input.Split(
            (char[])null,
            StringSplitOptions.RemoveEmptyEntries
        );

        if (parts.Length == 0)
        {
            return;
        }

        int position = 0;

        int n =
            int.Parse(parts[position++]);

        long[] a =
            new long[n];

        for (int i = 0; i < n; i++)
        {
            a[i] =
                long.Parse(
                    parts[position++]
                );
        }

        long target =
            long.Parse(
                parts[position]
            );

        int result = -1;

        for (int i = 0; i < n; i++)
        {
            if (a[i] == target)
            {
                result = i;
                break;
            }
        }

        Console.WriteLine(result);
    }
}
