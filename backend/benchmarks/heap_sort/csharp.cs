// Benchmark: Heap Sort
// Category: Sorting
// Algorithm: Heap Sort - O(n log n)

using System;
using System.Collections.Generic;

class Program
{
    static void Heapify(
        List<long> a,
        int n,
        int i
    )
    {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (
            left < n &&
            a[left] > a[largest]
        )
        {
            largest = left;
        }

        if (
            right < n &&
            a[right] > a[largest]
        )
        {
            largest = right;
        }

        if (largest != i)
        {
            long temp = a[i];
            a[i] = a[largest];
            a[largest] = temp;

            Heapify(
                a,
                n,
                largest
            );
        }
    }

    static void HeapSort(
        List<long> a
    )
    {
        int n = a.Count;

        for (
            int i = n / 2 - 1;
            i >= 0;
            i--
        )
        {
            Heapify(
                a,
                n,
                i
            );
        }

        for (
            int i = n - 1;
            i > 0;
            i--
        )
        {
            long temp = a[0];
            a[0] = a[i];
            a[i] = temp;

            Heapify(
                a,
                i,
                0
            );
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
            HeapSort(a);
        }

        Console.WriteLine(
            a.Count == 0
                ? 0
                : a[a.Count - 1]
        );
    }
}
