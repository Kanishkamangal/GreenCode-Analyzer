// Benchmark: Bucket Sort
// Category: Sorting
// Algorithm: Bucket Sort - O(n + k) average

import java.io.*;
import java.util.*;

public class Main {

    static void insertionSort(
        ArrayList<Long> bucket
    ) {
        for (
            int i = 1;
            i < bucket.size();
            i++
        ) {
            long key = bucket.get(i);
            int j = i - 1;

            while (
                j >= 0 &&
                bucket.get(j) > key
            ) {
                bucket.set(
                    j + 1,
                    bucket.get(j)
                );

                j--;
            }

            bucket.set(
                j + 1,
                key
            );
        }
    }

    static void bucketSort(
        long[] a
    ) {
        int n = a.length;

        if (n <= 1) {
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

        if (minValue == maxValue) {
            return;
        }

        int bucketCount = Math.max(
            1,
            (int)Math.sqrt(n)
        );

        ArrayList<ArrayList<Long>>
            buckets = new ArrayList<>();

        for (
            int i = 0;
            i < bucketCount;
            i++
        ) {
            buckets.add(
                new ArrayList<>()
            );
        }

        double range =
            (double)maxValue -
            (double)minValue + 1.0;

        for (long value : a) {
            double offset =
                (double)value -
                (double)minValue;

            int index = (int)(
                offset *
                bucketCount /
                range
            );

            if (index >= bucketCount) {
                index =
                    bucketCount - 1;
            }

            buckets.get(index)
                .add(value);
        }

        int position = 0;

        for (
            ArrayList<Long> bucket :
            buckets
        ) {
            insertionSort(bucket);

            for (long value : bucket) {
                a[position++] = value;
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
            bucketSort(a);
        }

        System.out.println(
            a.length == 0
                ? 0
                : a[a.length - 1]
        );
    }
}
