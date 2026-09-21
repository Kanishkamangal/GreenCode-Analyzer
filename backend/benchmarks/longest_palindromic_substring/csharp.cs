// Benchmark: Longest Palindromic Substring
// Category: Strings
// Algorithm: Expand Around Center - O(n^2)

using System;

class Program
{
    static void Main()
    {
        string input =
            Console.In.ReadToEnd().Trim();

        if (input.Length == 0)
        {
            return;
        }

        string s =
            input.Split(
                (char[])null,
                StringSplitOptions.RemoveEmptyEntries
            )[0];

        int n = s.Length;
        int bestStart = 0;
        int bestLength = 1;

        for (
            int center = 0;
            center < n;
            center++
        )
        {
            int left = center;
            int right = center;

            while (
                left >= 0 &&
                right < n &&
                s[left] == s[right]
            )
            {
                int length =
                    right - left + 1;

                if (length > bestLength)
                {
                    bestStart = left;
                    bestLength = length;
                }

                left--;
                right++;
            }

            left = center;
            right = center + 1;

            while (
                left >= 0 &&
                right < n &&
                s[left] == s[right]
            )
            {
                int length =
                    right - left + 1;

                if (length > bestLength)
                {
                    bestStart = left;
                    bestLength = length;
                }

                left--;
                right++;
            }
        }

        Console.WriteLine(
            s.Substring(
                bestStart,
                bestLength
            )
        );
    }
}
