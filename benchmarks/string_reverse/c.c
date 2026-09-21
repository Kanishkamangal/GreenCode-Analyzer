// Benchmark: String Reverse
// Category: Strings
// Algorithm: Two-Pointer String Reverse - O(n)

#include <stdio.h>
#include <string.h>

int main() {
    char s[1000005];

    if (scanf("%1000000s", s) != 1) {
        return 1;
    }

    int left = 0;
    int right = (int)strlen(s) - 1;

    while (left < right) {
        char temp = s[left];
        s[left] = s[right];
        s[right] = temp;

        left++;
        right--;
    }

    printf("%s\n", s);

    return 0;
}
