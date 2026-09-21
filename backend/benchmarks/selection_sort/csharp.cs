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
            a.Add(long.Parse(part));

        int n = a.Count;

        for (int i = 0; i < n - 1; i++)
        {
            int minIndex = i;

            for (int j = i + 1; j < n; j++)
            {
                if (a[j] < a[minIndex])
                    minIndex = j;
            }

            if (minIndex != i)
            {
                long temp = a[i];
                a[i] = a[minIndex];
                a[minIndex] = temp;
            }
        }

        Console.Write(n == 0 ? 0 : a[n - 1]);
    }
}
