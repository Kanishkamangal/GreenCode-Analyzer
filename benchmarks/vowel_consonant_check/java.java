// Benchmark: Vowel or Consonant Check
// Category: Character
// Algorithm: Direct Character Check - O(1)

import java.io.*;

public class Main {
    public static void main(
        String[] args
    ) throws Exception {

        BufferedReader br =
            new BufferedReader(
                new InputStreamReader(
                    System.in
                )
            );

        String input = br.readLine();

        if (input == null) {
            return;
        }

        input = input.trim();

        if (input.isEmpty()) {
            return;
        }

        char ch = input.charAt(0);

        boolean vowel =
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

        System.out.println(
            vowel ? 1 : 0
        );
    }
}
