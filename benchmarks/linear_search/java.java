// Benchmark: Linear Search
// Category: Searching
// Algorithm: Linear Search - O(n)

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

        long[] a =
            new long[n];

        for (int i = 0; i < n; i++) {
            a[i] =
                Long.parseLong(
                    st.nextToken()
                );
        }

        long target =
            Long.parseLong(
                st.nextToken()
            );

        int result = -1;

        for (int i = 0; i < n; i++) {
            if (a[i] == target) {
                result = i;
                break;
            }
        }

        System.out.println(result);
    }
}
