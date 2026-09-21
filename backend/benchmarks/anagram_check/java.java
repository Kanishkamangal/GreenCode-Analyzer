// Benchmark: Anagram Check
// Category: String
// Algorithm: Anagram Check - O(n)

import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();

        if (line == null) {
            System.out.println(0);
            return;
        }

        StringTokenizer st = new StringTokenizer(line);

        if (st.countTokens() < 2) {
            System.out.println(0);
            return;
        }

        String s1 = st.nextToken();
        String s2 = st.nextToken();

        if (s1.length() != s2.length()) {
            System.out.println(0);
            return;
        }

        int[] count = new int[65536];

        for (int i = 0; i < s1.length(); i++)
            count[s1.charAt(i)]++;

        for (int i = 0; i < s2.length(); i++)
            count[s2.charAt(i)]--;

        for (int value : count) {
            if (value != 0) {
                System.out.println(0);
                return;
            }
        }

        System.out.println(1);
    }
}
