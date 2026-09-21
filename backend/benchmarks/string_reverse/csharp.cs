// Benchmark: String Reverse
// Category: Strings
// Algorithm: Two-Pointer String Reverse - O(n)

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

        char[] chars =
            s.ToCharArray();

        int left = 0;
        int right =
            chars.Length - 1;

        while (left < right)
        {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;

            left++;
            right--;
        }

        Console.WriteLine(
            new string(chars)
        );
    }
}
