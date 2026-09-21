// Benchmark: Heap Sort
// Category: Sorting
// Algorithm: Heap Sort - O(n log n)

import java.io.*;
import java.util.*;

public class Main {

    static void heapify(
        long[] a,
        int n,
        int i
    ) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (
            left < n &&
            a[left] > a[largest]
        ) {
            largest = left;
        }

        if (
            right < n &&
            a[right] > a[largest]
        ) {
            largest = right;
        }

        if (largest != i) {
            long temp = a[i];
            a[i] = a[largest];
            a[largest] = temp;

            heapify(
                a,
                n,
                largest
            );
        }
    }

    static void heapSort(
        long[] a
    ) {
        int n = a.length;

        for (
            int i = n / 2 - 1;
            i >= 0;
            i--
        ) {
            heapify(
                a,
                n,
                i
            );
        }

        for (
            int i = n - 1;
            i > 0;
            i--
        ) {
            long temp = a[0];
            a[0] = a[i];
            a[i] = temp;

            heapify(
                a,
                i,
                0
            );
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
            heapSort(a);
        }

        System.out.println(
            a.length == 0
                ? 0
                : a[a.length - 1]
        );
    }
}
