// Benchmark: Radix Sort
// Category: Sorting
// Algorithm: LSD Radix Sort - O(d * (n + b))

import java.io.*;
import java.util.*;

public class Main {

    static void radixSortNonNegative(
        long[] a
    ) {
        if (a.length <= 1) {
            return;
        }

        long maxValue = a[0];

        for (long value : a) {
            if (value > maxValue) {
                maxValue = value;
            }
        }

        long[] output =
            new long[a.length];

        for (
            long exp = 1;
            maxValue / exp > 0;
        ) {
            int[] count = new int[10];

            for (long value : a) {
                int digit =
                    (int)((value / exp) % 10);

                count[digit]++;
            }

            for (int i = 1; i < 10; i++) {
                count[i] += count[i - 1];
            }

            for (
                int i = a.length - 1;
                i >= 0;
                i--
            ) {
                int digit =
                    (int)((a[i] / exp) % 10);

                output[
                    --count[digit]
                ] = a[i];
            }

            System.arraycopy(
                output,
                0,
                a,
                0,
                a.length
            );

            if (exp > maxValue / 10) {
                break;
            }

            exp *= 10;
        }
    }

    static void radixSort(
        long[] a
    ) {
        ArrayList<Long> negative =
            new ArrayList<>();

        ArrayList<Long> positive =
            new ArrayList<>();

        for (long value : a) {
            if (value < 0) {
                negative.add(-value);
            } else {
                positive.add(value);
            }
        }

        long[] neg =
            new long[negative.size()];

        long[] pos =
            new long[positive.size()];

        for (
            int i = 0;
            i < negative.size();
            i++
        ) {
            neg[i] = negative.get(i);
        }

        for (
            int i = 0;
            i < positive.size();
            i++
        ) {
            pos[i] = positive.get(i);
        }

        radixSortNonNegative(neg);
        radixSortNonNegative(pos);

        int index = 0;

        for (
            int i = neg.length - 1;
            i >= 0;
            i--
        ) {
            a[index++] = -neg[i];
        }

        for (long value : pos) {
            a[index++] = value;
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
            radixSort(a);
        }

        System.out.println(
            a.length == 0
                ? 0
                : a[a.length - 1]
        );
    }
}
