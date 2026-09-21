// Benchmark: Counting Sort
// Category: Sorting
// Algorithm: Counting Sort - O(n + k)

import java.io.*;
import java.util.*;

public class Main {

    static void countingSort(
        long[] a
    ) {
        if (a.length <= 1) {
            return;
        }

        long minValue = a[0];
        long maxValue = a[0];

        for (long value : a) {
            if (value < minValue) {
                minValue = value;
            }

            if (value > maxValue) {
                maxValue = value;
            }
        }

        int range = (int)(
            maxValue - minValue + 1
        );

        long[] count =
            new long[range];

        for (long value : a) {
            count[
                (int)(value - minValue)
            ]++;
        }

        int index = 0;

        for (
            int i = 0;
            i < range;
            i++
        ) {
            while (count[i] > 0) {
                a[index++] =
                    i + minValue;

                count[i]--;
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

            while (st.hasMoreTokens()) {
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
            countingSort(a);
        }

        System.out.println(
            a.length == 0
                ? 0
                : a[a.length - 1]
        );
    }
}
