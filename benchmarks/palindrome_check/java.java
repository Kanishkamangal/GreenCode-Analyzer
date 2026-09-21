// Benchmark: Palindrome Check
// Category: Strings
// Algorithm: Two-Pointer Palindrome Check - O(n)

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

        String s = br.readLine();

        if (s == null) {
            return;
        }

        s = s.trim();

        if (s.isEmpty()) {
            return;
        }

        String[] parts =
            s.split("\\s+");

        s = parts[0];

        int left = 0;
        int right = s.length() - 1;

        boolean palindrome = true;

        while (left < right) {
            if (
                s.charAt(left) !=
                s.charAt(right)
            ) {
                palindrome = false;
                break;
            }

            left++;
            right--;
        }

        System.out.println(
            palindrome ? 1 : 0
        );
    }
}
