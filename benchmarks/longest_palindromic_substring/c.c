// Benchmark: Longest Palindromic Substring
// Category: Strings
// Algorithm: Expand Around Center - O(n^2)

#include <stdio.h>
#include <string.h>

int main() {
    char s[1000005];

    if (scanf("%1000000s", s) != 1) {
        return 1;
    }

    int n = (int)strlen(s);
    int bestStart = 0;
    int bestLength = 1;

    for (int center = 0; center < n; center++) {
        int left = center;
        int right = center;

        while (
            left >= 0 &&
            right < n &&
            s[left] == s[right]
        ) {
            int length = right - left + 1;

            if (length > bestLength) {
                bestStart = left;
                bestLength = length;
            }

            left--;
            right++;
        }

        left = center;
        right = center + 1;

        while (
            left >= 0 &&
            right < n &&
            s[left] == s[right]
        ) {
            int length = right - left + 1;

            if (length > bestLength) {
                bestStart = left;
                bestLength = length;
            }

            left--;
            right++;
        }
    }

    for (
        int i = bestStart;
        i < bestStart + bestLength;
        i++
    ) {
        putchar(s[i]);
    }

    putchar('\n');

    return 0;
}
