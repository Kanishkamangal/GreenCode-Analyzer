// Benchmark: Bucket Sort
// Category: Sorting
// Algorithm: Bucket Sort - O(n + k) average

using System;
using System.Collections.Generic;

class Program
{
    static void InsertionSort(
        List<long> bucket
    )
    {
        for (
            int i = 1;
            i < bucket.Count;
            i++
        )
        {
            long key = bucket[i];
            int j = i - 1;

            while (
                j >= 0 &&
                bucket[j] > key
            )
            {
                bucket[j + 1] =
                    bucket[j];

                j--;
            }

            bucket[j + 1] = key;
        }
    }

    static void BucketSort(
        List<long> a
    )
    {
        int n = a.Count;

        if (n <= 1)
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

        if (minValue == maxValue)
        {
            return;
        }

        int bucketCount = Math.Max(
            1,
            (int)Math.Sqrt(n)
        );

        List<long>[] buckets =
            new List<long>[bucketCount];

        for (
            int i = 0;
            i < bucketCount;
            i++
        )
        {
            buckets[i] =
                new List<long>();
        }

        decimal range =
            (decimal)maxValue -
            (decimal)minValue + 1m;

        foreach (long value in a)
        {
            decimal offset =
                (decimal)value -
                (decimal)minValue;

            int index = (int)(
                offset * bucketCount /
                range
            );

            if (index >= bucketCount)
            {
                index =
                    bucketCount - 1;
            }

            buckets[index].Add(value);
        }

        int position = 0;

        foreach (
            List<long> bucket in buckets
        )
        {
            InsertionSort(bucket);

            foreach (
                long value in bucket
            )
            {
                a[position++] = value;
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
            BucketSort(a);
        }

        Console.WriteLine(
            a.Count == 0
                ? 0
                : a[a.Count - 1]
        );
    }
}
