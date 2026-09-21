// Benchmark: Longest Common Subsequence
// Category: Strings
// Algorithm: Dynamic Programming LCS - O(n * m)

import java.io.*;
import java.util.*;

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

        StringBuilder input =
            new StringBuilder();

        String line;

        while (
            (line = br.readLine()) != null
        ) {
            input.append(line)
                 .append(' ');
        }

        StringTokenizer st =
            new StringTokenizer(
                input.toString()
            );

        if (!st.hasMoreTokens()) {
            return;
        }

        String first =
            st.nextToken();

        if (!st.hasMoreTokens()) {
            return;
        }

        String second =
            st.nextToken();

        int n = first.length();
        int m = second.length();

        int[] previous =
            new int[m + 1];

        int[] current =
            new int[m + 1];

        for (int i = 1; i <= n; i++) {
            current[0] = 0;

            for (int j = 1; j <= m; j++) {
                if (
                    first.charAt(i - 1) ==
                    second.charAt(j - 1)
                ) {
                    current[j] =
                        previous[j - 1] + 1;
                } else {
                    current[j] =
                        Math.max(
                            previous[j],
                            current[j - 1]
                        );
                }
            }

            int[] temp = previous;
            previous = current;
            current = temp;
        }

        System.out.println(
            previous[m]
        );
    }
}
