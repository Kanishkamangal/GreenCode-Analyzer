// Benchmark: Bubble Sort
// Category: Sorting
// Algorithm: Bubble Sort - O(n^2)

#include <stdio.h>
#include <stdlib.h>

int main() {
    int n = 0;
    int capacity = 1024;

    long long *a = malloc(capacity * sizeof(long long));

    if (a == NULL) {
        return 1;
    }

    while (scanf("%lld", &a[n]) == 1) {
        n++;

        if (n == capacity) {
            capacity *= 2;

            long long *temp =
                realloc(a, capacity * sizeof(long long));

            if (temp == NULL) {
                free(a);
                return 1;
            }

            a = temp;
        }
    }

    for (int i = 0; i < n - 1; i++) {
        int swapped = 0;

        for (int j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) {
                long long temp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = temp;
                swapped = 1;
            }
        }

        if (!swapped) {
            break;
        }
    }

    printf("%lld\n", n > 0 ? a[n - 1] : 0);

    free(a);

    return 0;
}