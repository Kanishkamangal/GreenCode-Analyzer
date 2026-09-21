// Benchmark: Vowel or Consonant Check
// Category: Character
// Algorithm: Direct Character Check - O(1)

#include <stdio.h>

int main() {
    char ch;

    if (scanf(" %c", &ch) != 1) {
        return 1;
    }

    int vowel =
        ch == 'a' ||
        ch == 'e' ||
        ch == 'i' ||
        ch == 'o' ||
        ch == 'u' ||
        ch == 'A' ||
        ch == 'E' ||
        ch == 'I' ||
        ch == 'O' ||
        ch == 'U';

    printf("%d\n", vowel ? 1 : 0);

    return 0;
}
