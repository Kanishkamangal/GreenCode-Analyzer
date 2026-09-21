// Benchmark: Anagram Check
// Category: String
// Algorithm: Anagram Check - O(n)

#include <stdio.h>
#include <string.h>

int main() {
    char s1[1000001], s2[1000001];

    if (scanf("%1000000s %1000000s", s1, s2) != 2) {
        printf("0\n");
        return 0;
    }

    if (strlen(s1) != strlen(s2)) {
        printf("0\n");
        return 0;
    }

    long long count[256] = {0};

    for (int i = 0; s1[i]; i++)
        count[(unsigned char)s1[i]]++;

    for (int i = 0; s2[i]; i++)
        count[(unsigned char)s2[i]]--;

    for (int i = 0; i < 256; i++) {
        if (count[i] != 0) {
            printf("0\n");
            return 0;
        }
    }

    printf("1\n");
    return 0;
}
