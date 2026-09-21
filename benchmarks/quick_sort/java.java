// Benchmark: Quick Sort
// Category: Sorting
// Algorithm: Quick Sort - O(n log n) average

import java.io.*;
import java.util.*;

public class Main {

    static int partition(
        long[] a,
        int low,
        int high
    ) {
        long pivot = a[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (a[j] <= pivot) {
                i++;

                long temp = a[i];
                a[i] = a[j];
                a[j] = temp;
            }
        }

        long temp = a[i + 1];
        a[i + 1] = a[high];
        a[high] = temp;

        return i + 1;
    }

    static void quickSort(
        long[] a,
        int low,
        int high
    ) {
        if (low < high) {
            int pivotIndex = partition(
                a,
                low,
                high
            );

            quickSort(
                a,
                low,
                pivotIndex - 1
            );

            quickSort(
                a,
                pivotIndex + 1,
                high
            );
        }
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(
            new InputStreamReader(System.in)
        );

        ArrayList<Long> values = new ArrayList<>();
        String line;

        while ((line = br.readLine()) != null) {
            StringTokenizer st = new StringTokenizer(line);

            while (st.hasMoreTokens()) {
                values.add(
                    Long.parseLong(st.nextToken())
                );
            }
        }

        long[] a = new long[values.size()];

        for (int i = 0; i < values.size(); i++) {
            a[i] = values.get(i);
        }

        if (a.length > 0) {
            quickSort(
                a,
                0,
                a.length - 1
            );
        }

        System.out.println(
            a.length == 0 ? 0 : a[a.length - 1]
        );
    }
}
