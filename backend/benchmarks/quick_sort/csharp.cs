// Benchmark: Quick Sort
// Category: Sorting
// Algorithm: Quick Sort - O(n log n) average

using System;
using System.Collections.Generic;

class Program
{
    static int Partition(
        List<long> a,
        int low,
        int high
    )
    {
        long pivot = a[high];
        int i = low - 1;

        for (int j = low; j < high; j++)
        {
            if (a[j] <= pivot)
            {
                i++;

                long temp = a[i];
                a[i] = a[j];
                a[j] = temp;
            }
        }

        long value = a[i + 1];
        a[i + 1] = a[high];
        a[high] = value;

        return i + 1;
    }

    static void QuickSort(
        List<long> a,
        int low,
        int high
    )
    {
        if (low < high)
        {
            int pivotIndex = Partition(
                a,
                low,
                high
            );

            QuickSort(
                a,
                low,
                pivotIndex - 1
            );

            QuickSort(
                a,
                pivotIndex + 1,
                high
            );
        }
    }

    static void Main()
    {
        string input = Console.In.ReadToEnd();

        string[] parts = input.Split(
            (char[])null,
            StringSplitOptions.RemoveEmptyEntries
        );

        List<long> a = new List<long>();

        foreach (string part in parts)
        {
            a.Add(long.Parse(part));
        }

        if (a.Count > 0)
        {
            QuickSort(
                a,
                0,
                a.Count - 1
            );
        }

        Console.WriteLine(
            a.Count == 0 ? 0 : a[a.Count - 1]
        );
    }
}
