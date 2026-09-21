// Benchmark: Radix Sort
// Category: Sorting
// Algorithm: LSD Radix Sort - O(d * (n + b))

using System;
using System.Collections.Generic;

class Program
{
    static void RadixSortNonNegative(
        List<ulong> a
    )
    {
        if (a.Count <= 1)
        {
            return;
        }

        ulong maxValue = a[0];

        foreach (ulong value in a)
        {
            if (value > maxValue)
            {
                maxValue = value;
            }
        }

        ulong[] output =
            new ulong[a.Count];

        for (
            ulong exp = 1;
            maxValue / exp > 0;
        )
        {
            int[] count = new int[10];

            foreach (ulong value in a)
            {
                int digit =
                    (int)((value / exp) % 10);

                count[digit]++;
            }

            for (int i = 1; i < 10; i++)
            {
                count[i] += count[i - 1];
            }

            for (
                int i = a.Count - 1;
                i >= 0;
                i--
            )
            {
                int digit =
                    (int)((a[i] / exp) % 10);

                output[
                    --count[digit]
                ] = a[i];
            }

            for (
                int i = 0;
                i < a.Count;
                i++
            )
            {
                a[i] = output[i];
            }

            if (exp > maxValue / 10)
            {
                break;
            }

            exp *= 10;
        }
    }

    static void RadixSort(
        List<long> a
    )
    {
        List<ulong> negative =
            new List<ulong>();

        List<ulong> positive =
            new List<ulong>();

        foreach (long value in a)
        {
            if (value < 0)
            {
                negative.Add(
                    (ulong)(-(value + 1)) + 1
                );
            }
            else
            {
                positive.Add(
                    (ulong)value
                );
            }
        }

        RadixSortNonNegative(negative);
        RadixSortNonNegative(positive);

        int index = 0;

        for (
            int i = negative.Count - 1;
            i >= 0;
            i--
        )
        {
            a[index++] =
                -(long)negative[i];
        }

        foreach (ulong value in positive)
        {
            a[index++] =
                (long)value;
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
            RadixSort(a);
        }

        Console.WriteLine(
            a.Count == 0
                ? 0
                : a[a.Count - 1]
        );
    }
}
