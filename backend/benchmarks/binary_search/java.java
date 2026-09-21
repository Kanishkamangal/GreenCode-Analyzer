// Benchmark: Binary Search
// Category: Searching
// Algorithm: Binary Search - O(log n)

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

        int left = 0;
        int right = n - 1;
        int result = -1;

        while (left <= right) {
            int mid =
                left + (right - left) / 2;

            if (a[mid] == target) {
                result = mid;
                break;
            }

            if (a[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        System.out.println(result);
    }
}
