// Benchmark: Bubble Sort
// Category: Sorting
// Algorithm: Bubble Sort - O(n^2)

import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        ArrayList<Long> a = new ArrayList<>();

        String line;

        while ((line = br.readLine()) != null) {
            String[] parts = line.trim().split("\\s+");

            for (String p : parts) {
                if (!p.isEmpty())
                    a.add(Long.parseLong(p));
            }
        }

        for (int i = 0; i < a.size() - 1; i++) {
            boolean swapped = false;

            for (int j = 0; j < a.size() - i - 1; j++) {
                if (a.get(j) > a.get(j + 1)) {
                    long temp = a.get(j);
                    a.set(j, a.get(j + 1));
                    a.set(j + 1, temp);
                    swapped = true;
                }
            }

            if (!swapped) break;
        }

        System.out.println(a.isEmpty() ? 0 : a.get(a.size() - 1));
    }
}