// Benchmark: Shell Sort
// Category: Sorting
// Algorithm: Shell Sort - Gap-based

using System;
using System.Collections.Generic;

class Program
{
    static void ShellSort(
        List<long> a
    )
    {
        int n = a.Count;

        for (
            int gap = n / 2;
            gap > 0;
            gap /= 2
        )
        {
            for (
                int i = gap;
                i < n;
                i++
            )
            {
                long temp = a[i];
                int j = i;

                while (
                    j >= gap &&
                    a[j - gap] > temp
                )
                {
                    a[j] = a[j - gap];
                    j -= gap;
                }

                a[j] = temp;
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
            ShellSort(a);
        }

        Console.WriteLine(
            a.Count == 0
                ? 0
                : a[a.Count - 1]
        );
    }
}
