// Benchmark: Longest Common Subsequence
// Category: Strings
// Algorithm: Dynamic Programming LCS - O(n * m)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char first[100005];
    char second[100005];

    if (scanf("%100000s", first) != 1) {
        return 1;
    }

    if (scanf("%100000s", second) != 1) {
        return 1;
    }

    int n = (int)strlen(first);
    int m = (int)strlen(second);

    int *previous =
        calloc(m + 1, sizeof(int));

    int *current =
        calloc(m + 1, sizeof(int));

    if (
        previous == NULL ||
        current == NULL
    ) {
        free(previous);
        free(current);
        return 1;
    }

    for (int i = 1; i <= n; i++) {
        current[0] = 0;

        for (int j = 1; j <= m; j++) {
            if (
                first[i - 1] ==
                second[j - 1]
            ) {
                current[j] =
                    previous[j - 1] + 1;
            } else {
                current[j] =
                    previous[j] > current[j - 1]
                        ? previous[j]
                        : current[j - 1];
            }
        }

        int *temp = previous;
        previous = current;
        current = temp;
    }

    printf("%d\n", previous[m]);

    free(previous);
    free(current);

    return 0;
}
