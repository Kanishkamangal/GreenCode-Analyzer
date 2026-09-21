// Benchmark: Vowel or Consonant Check
// Category: Character
// Algorithm: Direct Character Check - O(1)

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

        char ch = input[0];

        bool vowel =
            ch == 'a' ||
            ch == 'e' ||
            ch == 'i' ||
            ch == 'o' ||
            ch == 'u' ||
            ch == 'A' ||
            ch == 'E' ||
            ch == 'I' ||
            ch == 'O' ||
            ch == 'U';

        Console.WriteLine(
            vowel ? 1 : 0
        );
    }
}
