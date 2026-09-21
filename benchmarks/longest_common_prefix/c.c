// Benchmark: Longest Common Prefix
// Category: Strings
// Algorithm: Vertical Scanning - O(total characters)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 1000005

int main() {
    int n;

    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("\n");
        return 0;
    }

    char **strings =
        malloc(n * sizeof(char *));

    if (strings == NULL) {
        return 1;
    }

    for (int i = 0; i < n; i++) {
        strings[i] =
            malloc(MAX_LEN);

        if (strings[i] == NULL) {
            for (int j = 0; j < i; j++) {
                free(strings[j]);
            }

            free(strings);
            return 1;
        }

        if (
            scanf(
                "%1000000s",
                strings[i]
            ) != 1
        ) {
            for (int j = 0; j <= i; j++) {
                free(strings[j]);
            }

            free(strings);
            return 1;
        }
    }

    int prefixLength = 0;
    int firstLength =
        (int)strlen(strings[0]);

    for (
        int position = 0;
        position < firstLength;
        position++
    ) {
        char current =
            strings[0][position];

        int matches = 1;

        for (int i = 1; i < n; i++) {
            if (
                position >=
                    (int)strlen(strings[i]) ||
                strings[i][position] != current
            ) {
                matches = 0;
                break;
            }
        }

        if (!matches) {
            break;
        }

        prefixLength++;
    }

    for (
        int i = 0;
        i < prefixLength;
        i++
    ) {
        putchar(strings[0][i]);
    }

    putchar('\n');

    for (int i = 0; i < n; i++) {
        free(strings[i]);
    }

    free(strings);

    return 0;
}
