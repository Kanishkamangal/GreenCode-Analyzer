// Benchmark: Character Frequency in String
// Category: Strings
// Algorithm: Linear Character Frequency Count - O(n)

#include <stdio.h>

int main() {
    char s[1000005];
    char target;

    if (
        scanf(
            "%1000000s",
            s
        ) != 1
    ) {
        return 1;
    }

    if (
        scanf(
            " %c",
            &target
        ) != 1
    ) {
        return 1;
    }

    long long frequency = 0;

    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == target) {
            frequency++;
        }
    }

    printf(
        "%lld\n",
        frequency
    );

    return 0;
}
