import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(
            new InputStreamReader(System.in)
        );

        ArrayList<Long> a = new ArrayList<>();
        String line;

        while ((line = br.readLine()) != null) {
            StringTokenizer st = new StringTokenizer(line);

            while (st.hasMoreTokens()) {
                a.add(
                    Long.parseLong(st.nextToken())
                );
            }
        }

        int n = a.size();

        for (int i = 1; i < n; i++) {
            long key = a.get(i);
            int j = i - 1;

            while (
                j >= 0 &&
                a.get(j) > key
            ) {
                a.set(
                    j + 1,
                    a.get(j)
                );

                j--;
            }

            a.set(j + 1, key);
        }

        System.out.print(
            n == 0 ? 0 : a.get(n - 1)
        );
    }
}
