// Benchmark: Longest Common Prefix
// Category: Strings
// Algorithm: Vertical Scanning - O(total characters)

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

        int n =
            Integer.parseInt(
                st.nextToken()
            );

        if (n <= 0) {
            System.out.println();
            return;
        }

        String[] strings =
            new String[n];

        for (int i = 0; i < n; i++) {
            strings[i] =
                st.nextToken();
        }

        int prefixLength = 0;

        for (
            int position = 0;
            position < strings[0].length();
            position++
        ) {
            char current =
                strings[0].charAt(position);

            boolean matches = true;

            for (int i = 1; i < n; i++) {
                if (
                    position >=
                        strings[i].length() ||
                    strings[i].charAt(position)
                        != current
                ) {
                    matches = false;
                    break;
                }
            }

            if (!matches) {
                break;
            }

            prefixLength++;
        }

        System.out.println(
            strings[0].substring(
                0,
                prefixLength
            )
        );
    }
}
