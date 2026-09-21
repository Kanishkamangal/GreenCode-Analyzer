// Benchmark: Substring Search
// Category: Strings
// Algorithm: Naive Substring Search - O(n * m)

#include <stdio.h>
#include <string.h>

int substringSearch(
    const char text[],
    const char pattern[]
) {
    int n = (int)strlen(text);
    int m = (int)strlen(pattern);

    if (m == 0) {
        return 0;
    }

    if (m > n) {
        return -1;
    }

    for (int i = 0; i <= n - m; i++) {
        int j = 0;

        while (
            j < m &&
            text[i + j] == pattern[j]
        ) {
            j++;
        }

        if (j == m) {
            return i;
        }
    }

    return -1;
}

int main() {
    char text[1000005];
    char pattern[1000005];

    if (
        scanf(
            "%1000000s",
            text
        ) != 1
    ) {
        return 1;
    }

    if (
        scanf(
            "%1000000s",
            pattern
        ) != 1
    ) {
        return 1;
    }

    printf(
        "%d\n",
        substringSearch(
            text,
            pattern
        )
    );

    return 0;
}
