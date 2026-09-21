// Benchmark: Longest Palindromic Substring
// Category: Strings
// Algorithm: Expand Around Center - O(n^2)

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

        s = s.split("\\s+")[0];

        int n = s.length();
        int bestStart = 0;
        int bestLength = 1;

        for (
            int center = 0;
            center < n;
            center++
        ) {
            int left = center;
            int right = center;

            while (
                left >= 0 &&
                right < n &&
                s.charAt(left) ==
                s.charAt(right)
            ) {
                int length =
                    right - left + 1;

                if (length > bestLength) {
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
                s.charAt(left) ==
                s.charAt(right)
            ) {
                int length =
                    right - left + 1;

                if (length > bestLength) {
                    bestStart = left;
                    bestLength = length;
                }

                left--;
                right++;
            }
        }

        System.out.println(
            s.substring(
                bestStart,
                bestStart + bestLength
            )
        );
    }
}
