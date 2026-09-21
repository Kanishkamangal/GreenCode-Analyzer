// Benchmark: Merge Sort
// Category: Sorting
// Algorithm: Merge Sort - O(n log n)

using System;
using System.Collections.Generic;

class Program
{
    static void Merge(
        List<long> a,
        long[] temp,
        int left,
        int mid,
        int right
    )
    {
        int i = left;
        int j = mid + 1;
        int k = left;

        while (i <= mid && j <= right)
        {
            if (a[i] <= a[j])
            {
                temp[k++] = a[i++];
            }
            else
            {
                temp[k++] = a[j++];
            }
        }

        while (i <= mid)
        {
            temp[k++] = a[i++];
        }

        while (j <= right)
        {
            temp[k++] = a[j++];
        }

        for (i = left; i <= right; i++)
        {
            a[i] = temp[i];
        }
    }

    static void MergeSort(
        List<long> a,
        long[] temp,
        int left,
        int right
    )
    {
        if (left >= right)
        {
            return;
        }

        int mid = left + (right - left) / 2;

        MergeSort(a, temp, left, mid);
        MergeSort(a, temp, mid + 1, right);
        Merge(a, temp, left, mid, right);
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
            long[] temp = new long[a.Count];

            MergeSort(
                a,
                temp,
                0,
                a.Count - 1
            );
        }

        Console.WriteLine(
            a.Count == 0 ? 0 : a[a.Count - 1]
        );
    }
}
