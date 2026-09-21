// Benchmark: Bubble Sort
// Category: Sorting
// Algorithm: Bubble Sort - O(n^2)

using System;
using System.Collections.Generic;

class MainClass
{
    static void Main()
    {
        List<long> a = new List<long>();

        string input = Console.In.ReadToEnd();

        string[] parts =
            input.Split(
                new char[] { ' ', '\n', '\r', '\t' },
                StringSplitOptions.RemoveEmptyEntries
            );

        foreach (string part in parts)
        {
            a.Add(long.Parse(part));
        }

        int n = a.Count;

        for (int i = 0; i < n - 1; i++)
        {
            bool swapped = false;

            for (int j = 0; j < n - i - 1; j++)
            {
                if (a[j] > a[j + 1])
                {
                    long temp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = temp;

                    swapped = true;
                }
            }

            if (!swapped)
            {
                break;
            }
        }

        Console.WriteLine(n == 0 ? 0 : a[n - 1]);
    }
}