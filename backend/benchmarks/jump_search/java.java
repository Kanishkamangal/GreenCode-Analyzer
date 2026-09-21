// Benchmark: Jump Search
// Category: Searching
// Algorithm: Jump Search - O(sqrt(n))

import java.io.*;
import java.util.*;

public class Main {

    static int jumpSearch(
        long[] a,
        long target
    ) {
        int n = a.length;

        if (n == 0) {
            return -1;
        }

        int step = Math.max(
            1,
            (int)Math.sqrt(n)
        );

        int previous = 0;
        int current = step;

        while (
            previous < n &&
            a[Math.min(current, n) - 1]
                < target
        ) {
            previous = current;
            current += step;

            if (previous >= n) {
                return -1;
            }
        }

        int end =
            Math.min(current, n);

        for (
            int i = previous;
            i < end;
            i++
        ) {
            if (a[i] == target) {
                return i;
            }

            if (a[i] > target) {
                break;
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

        System.out.println(
            jumpSearch(
                a,
                target
            )
        );
    }
}
