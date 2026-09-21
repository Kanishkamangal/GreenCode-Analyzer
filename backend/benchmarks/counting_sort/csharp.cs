// Benchmark: Counting Sort
// Category: Sorting
// Algorithm: Counting Sort - O(n + k)

using System;
using System.Collections.Generic;

class Program
{
    static void CountingSort(
        List<long> a
    )
    {
        if (a.Count <= 1)
        {
            return;
        }

        long minValue = a[0];
        long maxValue = a[0];

        foreach (long value in a)
        {
            if (value < minValue)
            {
                minValue = value;
            }

            if (value > maxValue)
            {
                maxValue = value;
            }
        }

        long range =
            maxValue - minValue + 1;

        long[] count =
            new long[(int)range];

        foreach (long value in a)
        {
            count[
                (int)(value - minValue)
            ]++;
        }

        int index = 0;

        for (
            int i = 0;
            i < count.Length;
            i++
        )
        {
            while (count[i] > 0)
            {
                a[index++] =
                    i + minValue;

                count[i]--;
            }
        }
    }

    static void Main()
    {
        string input =
            Console.In.ReadToEnd();

        string[] parts = input.Split(
            (char[])null,
            StringSplitOptions.RemoveEmptyEntries
        );

        List<long> a =
            new List<long>();

        foreach (string part in parts)
        {
            a.Add(
                long.Parse(part)
            );
        }

        if (a.Count > 0)
        {
            CountingSort(a);
        }

        Console.WriteLine(
            a.Count == 0
                ? 0
                : a[a.Count - 1]
        );
    }
}
