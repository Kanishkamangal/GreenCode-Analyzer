// Benchmark: Bubble Sort
// Category: Sorting
// Algorithm: Bubble Sort - O(n^2)

import java.io.*;
import java.util.*;

public class Main {

    public static void main(String[] args) throws Exception {

        BufferedReader br =
            new BufferedReader(new InputStreamReader(System.in));

        ArrayList<Long> list = new ArrayList<>();

        String line;

        while ((line = br.readLine()) != null) {
            String[] parts = line.trim().split("\\s+");

            for (String part : parts) {
                if (!part.isEmpty()) {
                    list.add(Long.parseLong(part));
                }
            }
        }

        long[] a = new long[list.size()];

        for (int i = 0; i < list.size(); i++) {
            a[i] = list.get(i);
        }

        for (int i = 0; i < a.length - 1; i++) {

            boolean swapped = false;

            for (int j = 0; j < a.length - i - 1; j++) {

                if (a[j] > a[j + 1]) {

                    long temp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = temp;

                    swapped = true;
                }
            }

            if (!swapped) {
                break;
            }
        }

        System.out.println(a.length == 0 ? 0 : a[a.length - 1]);
    }
}