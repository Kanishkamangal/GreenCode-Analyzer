// Benchmark: Substring Search
// Category: Strings
// Algorithm: Naive Substring Search - O(n * m)

import java.io.*;
import java.util.*;

public class Main {

    static int substringSearch(
        String text,
        String pattern
    ) {
        int n = text.length();
        int m = pattern.length();

        if (m == 0) {
            return 0;
        }

        if (m > n) {
            return -1;
        }

        for (
            int i = 0;
            i <= n - m;
            i++
        ) {
            int j = 0;

            while (
                j < m &&
                text.charAt(i + j) ==
                pattern.charAt(j)
            ) {
                j++;
            }

            if (j == m) {
                return i;
            }
        }

        return -1;
    }

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

        if (
            !st.hasMoreTokens()
        ) {
            return;
        }

        String text =
            st.nextToken();

        if (
            !st.hasMoreTokens()
        ) {
            return;
        }

        String pattern =
            st.nextToken();

        System.out.println(
            substringSearch(
                text,
                pattern
            )
        );
    }
}
