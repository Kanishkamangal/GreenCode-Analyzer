// Benchmark: Jump Search
// Category: Searching
// Algorithm: Jump Search - O(sqrt(n))

using System;

class Program
{
    static int JumpSearch(
        long[] a,
        long target
    )
    {
        int n = a.Length;

        if (n == 0)
        {
            return -1;
        }

        int step = Math.Max(
            1,
            (int)Math.Sqrt(n)
        );

        int previous = 0;
        int current = step;

        while (
            previous < n &&
            a[Math.Min(current, n) - 1]
                < target
        )
        {
            previous = current;
            current += step;

            if (previous >= n)
            {
                return -1;
            }
        }

        int end =
            Math.Min(current, n);

        for (
            int i = previous;
            i < end;
            i++
        )
        {
            if (a[i] == target)
            {
                return i;
            }

            if (a[i] > target)
            {
                break;
            }
        }

        return -1;
    }

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
            int.Parse(
                parts[position++]
            );

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

        Console.WriteLine(
            JumpSearch(
                a,
                target
            )
        );
    }
}
