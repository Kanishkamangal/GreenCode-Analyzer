// Benchmark: Character Frequency Count
// Category: Character
// Algorithm: Linear Frequency Count - O(n)

import java.io.*;
import java.util.*;

public class Main {
    public static void main(
        String[] args
    ) throws Exception {

        BufferedReader br =
            new BufferedReader(
                new InputStreamReader(System.in)
            );

        StringBuilder input =
            new StringBuilder();

        String line;

        while ((line = br.readLine()) != null) {
            input.append(line).append(' ');
        }

        StringTokenizer st =
            new StringTokenizer(
                input.toString()
            );

        if (!st.hasMoreTokens()) {
            return;
        }

        String s =
            st.nextToken();

        if (!st.hasMoreTokens()) {
            return;
        }

        char target =
            st.nextToken().charAt(0);

        long count = 0;

        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == target) {
                count++;
            }
        }

        System.out.println(count);
    }
}
