using System;
using System.Collections.Generic;

class Program
{
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

        int n = a.Count;

        for (int i = 1; i < n; i++)
        {
            long key = a[i];
            int j = i - 1;

            while (j >= 0 && a[j] > key)
            {
                a[j + 1] = a[j];
                j--;
            }

            a[j + 1] = key;
        }

        Console.Write(
            n == 0 ? 0 : a[n - 1]
        );
    }
}
