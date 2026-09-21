// Benchmark: String Reverse
// Category: Strings
// Algorithm: Two-Pointer String Reverse - O(n)

import java.io.*;

public class Main {
    public static void main(
        String[] args
    ) throws Exception {

        BufferedReader br =
            new BufferedReader(
                new InputStreamReader(
                    System.in
                )
            );

        String s = br.readLine();

        if (s == null) {
            return;
        }

        s = s.trim();

        if (s.isEmpty()) {
            return;
        }

        s = s.split("\\s+")[0];

        char[] chars =
            s.toCharArray();

        int left = 0;
        int right =
            chars.length - 1;

        while (left < right) {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;

            left++;
            right--;
        }

        System.out.println(
            new String(chars)
        );
    }
}
