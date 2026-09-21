// Benchmark: Binary Search
// Category: Searching
// Algorithm: Binary Search - O(log n)

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

        int left = 0;
        int right = n - 1;
        int result = -1;

        while (left <= right)
        {
            int mid =
                left + (right - left) / 2;

            if (a[mid] == target)
            {
                result = mid;
                break;
            }

            if (a[mid] < target)
            {
                left = mid + 1;
            }
            else
            {
                right = mid - 1;
            }
        }

        Console.WriteLine(result);
    }
}
