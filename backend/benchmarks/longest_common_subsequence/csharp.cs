// Benchmark: Longest Common Subsequence
// Category: Strings
// Algorithm: Dynamic Programming LCS - O(n * m)

using System;

class Program
{
    static void Main()
    {
        string input =
            Console.In.ReadToEnd();

        string[] values = input.Split(
            (char[])null,
            StringSplitOptions.RemoveEmptyEntries
        );

        if (values.Length < 2)
        {
            return;
        }

        string first = values[0];
        string second = values[1];

        int n = first.Length;
        int m = second.Length;

        int[] previous =
            new int[m + 1];

        int[] current =
            new int[m + 1];

        for (int i = 1; i <= n; i++)
        {
            current[0] = 0;

            for (int j = 1; j <= m; j++)
            {
                if (
                    first[i - 1] ==
                    second[j - 1]
                )
                {
                    current[j] =
                        previous[j - 1] + 1;
                }
                else
                {
                    current[j] =
                        Math.Max(
                            previous[j],
                            current[j - 1]
                        );
                }
            }

            int[] temp = previous;
            previous = current;
            current = temp;
        }

        Console.WriteLine(
            previous[m]
        );
    }
}
