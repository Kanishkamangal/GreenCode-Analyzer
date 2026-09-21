// Benchmark: Shell Sort
// Category: Sorting
// Algorithm: Shell Sort - Gap-based

import java.io.*;
import java.util.*;

public class Main {

    static void shellSort(
        long[] a
    ) {
        int n = a.length;

        for (
            int gap = n / 2;
            gap > 0;
            gap /= 2
        ) {
            for (
                int i = gap;
                i < n;
                i++
            ) {
                long temp = a[i];
                int j = i;

                while (
                    j >= gap &&
                    a[j - gap] > temp
                ) {
                    a[j] = a[j - gap];
                    j -= gap;
                }

                a[j] = temp;
            }
        }
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

        ArrayList<Long> values =
            new ArrayList<>();

        String line;

        while (
            (line = br.readLine()) != null
        ) {
            StringTokenizer st =
                new StringTokenizer(line);

            while (
                st.hasMoreTokens()
            ) {
                values.add(
                    Long.parseLong(
                        st.nextToken()
                    )
                );
            }
        }

        long[] a =
            new long[values.size()];

        for (
            int i = 0;
            i < values.size();
            i++
        ) {
            a[i] = values.get(i);
        }

        if (a.length > 0) {
            shellSort(a);
        }

        System.out.println(
            a.length == 0
                ? 0
                : a[a.length - 1]
        );
    }
}
