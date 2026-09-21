// Benchmark: Merge Sort
// Category: Sorting
// Algorithm: Merge Sort - O(n log n)

import java.io.*;
import java.util.*;

public class Main {

    static void merge(
        long[] a,
        long[] temp,
        int left,
        int mid,
        int right
    ) {
        int i = left;
        int j = mid + 1;
        int k = left;

        while (i <= mid && j <= right) {
            if (a[i] <= a[j]) {
                temp[k++] = a[i++];
            } else {
                temp[k++] = a[j++];
            }
        }

        while (i <= mid) {
            temp[k++] = a[i++];
        }

        while (j <= right) {
            temp[k++] = a[j++];
        }

        for (i = left; i <= right; i++) {
            a[i] = temp[i];
        }
    }

    static void mergeSort(
        long[] a,
        long[] temp,
        int left,
        int right
    ) {
        if (left >= right) {
            return;
        }

        int mid = left + (right - left) / 2;

        mergeSort(a, temp, left, mid);
        mergeSort(a, temp, mid + 1, right);

        merge(a, temp, left, mid, right);
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
            long[] temp = new long[a.length];

            mergeSort(
                a,
                temp,
                0,
                a.length - 1
            );
        }

        System.out.println(
            a.length == 0 ? 0 : a[a.length - 1]
        );
    }
}
