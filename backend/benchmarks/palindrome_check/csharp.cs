// Benchmark: Palindrome Check
// Category: Strings
// Algorithm: Two-Pointer Palindrome Check - O(n)

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

        int left = 0;
        int right = s.Length - 1;

        bool palindrome = true;

        while (left < right)
        {
            if (s[left] != s[right])
            {
                palindrome = false;
                break;
            }

            left++;
            right--;
        }

        Console.WriteLine(
            palindrome ? 1 : 0
        );
    }
}
