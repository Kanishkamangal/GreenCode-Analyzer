// Benchmark: Character Frequency Count
// Category: Character
// Algorithm: Linear Frequency Count - O(n)

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

        string s = values[0];
        char target = values[1][0];

        long count = 0;

        for (int i = 0; i < s.Length; i++)
        {
            if (s[i] == target)
            {
                count++;
            }
        }

        Console.WriteLine(count);
    }
}
