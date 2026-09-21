// Benchmark: Substring Search
// Category: Strings
// Algorithm: Naive Substring Search - O(n * m)

using System;

class Program
{
    static int SubstringSearch(
        string text,
        string pattern
    )
    {
        int n = text.Length;
        int m = pattern.Length;

        if (m == 0)
        {
            return 0;
        }

        if (m > n)
        {
            return -1;
        }

        for (
            int i = 0;
            i <= n - m;
            i++
        )
        {
            int j = 0;

            while (
                j < m &&
                text[i + j] ==
                pattern[j]
            )
            {
                j++;
            }

            if (j == m)
            {
                return i;
            }
        }

        return -1;
    }

    static void Main()
    {
        string input =
            Console.In.ReadToEnd();

        string[] parts = input.Split(
            (char[])null,
            StringSplitOptions.RemoveEmptyEntries
        );

        if (parts.Length < 2)
        {
            return;
        }

        string text = parts[0];
        string pattern = parts[1];

        Console.WriteLine(
            SubstringSearch(
                text,
                pattern
            )
        );
    }
}
