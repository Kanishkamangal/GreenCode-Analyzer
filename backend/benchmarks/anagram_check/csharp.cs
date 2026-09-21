// Benchmark: Anagram Check
// Category: String
// Algorithm: Anagram Check - O(n)

using System;
using System.Collections.Generic;

public class Program
{
    public static void Main()
    {
        string input = Console.In.ReadToEnd();
        string[] tokens = input.Split(
            (char[])null,
            StringSplitOptions.RemoveEmptyEntries
        );

        if (tokens.Length < 2)
        {
            Console.WriteLine(0);
            return;
        }

        string s1 = tokens[0];
        string s2 = tokens[1];

        if (s1.Length != s2.Length)
        {
            Console.WriteLine(0);
            return;
        }

        var count = new Dictionary<char, int>();

        foreach (char c in s1)
        {
            if (!count.ContainsKey(c))
                count[c] = 0;

            count[c]++;
        }

        foreach (char c in s2)
        {
            if (!count.ContainsKey(c))
                count[c] = 0;

            count[c]--;
        }

        foreach (int value in count.Values)
        {
            if (value != 0)
            {
                Console.WriteLine(0);
                return;
            }
        }

        Console.WriteLine(1);
    }
}
