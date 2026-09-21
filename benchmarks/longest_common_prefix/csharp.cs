// Benchmark: Longest Common Prefix
// Category: Strings
// Algorithm: Vertical Scanning - O(total characters)

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

        if (values.Length == 0)
        {
            return;
        }

        int position = 0;

        int n =
            int.Parse(
                values[position++]
            );

        if (n <= 0)
        {
            Console.WriteLine("");
            return;
        }

        string[] strings =
            new string[n];

        for (int i = 0; i < n; i++)
        {
            strings[i] =
                values[position++];
        }

        int prefixLength = 0;

        for (
            int index = 0;
            index < strings[0].Length;
            index++
        )
        {
            char current =
                strings[0][index];

            bool matches = true;

            for (int i = 1; i < n; i++)
            {
                if (
                    index >= strings[i].Length ||
                    strings[i][index] != current
                )
                {
                    matches = false;
                    break;
                }
            }

            if (!matches)
            {
                break;
            }

            prefixLength++;
        }

        Console.WriteLine(
            strings[0].Substring(
                0,
                prefixLength
            )
        );
    }
}
