// Benchmark: Palindrome Check
// Category: Strings
// Algorithm: Two-Pointer Palindrome Check - O(n)

#include <stdio.h>
#include <string.h>

int main() {
    char s[1000005];

    if (scanf("%1000000s", s) != 1) {
        return 1;
    }

    int left = 0;
    int right = (int)strlen(s) - 1;
    int palindrome = 1;

    while (left < right) {
        if (s[left] != s[right]) {
            palindrome = 0;
            break;
        }

        left++;
        right--;
    }

    printf("%d\n", palindrome);

    return 0;
}
