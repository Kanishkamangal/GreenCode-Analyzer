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

            while (st.hasMoreTokens())
                a.add(Long.parseLong(st.nextToken()));
        }

        int n = a.size();

        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;

            for (int j = i + 1; j < n; j++) {
                if (a.get(j) < a.get(minIndex))
                    minIndex = j;
            }

            if (minIndex != i) {
                long temp = a.get(i);
                a.set(i, a.get(minIndex));
                a.set(minIndex, temp);
            }
        }

        System.out.print(n == 0 ? 0 : a.get(n - 1));
    }
}
