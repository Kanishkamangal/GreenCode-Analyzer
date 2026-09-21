// Benchmark: Shell Sort
// Category: Sorting
// Algorithm: Shell Sort - Gap-based

#include <stdio.h>
#include <stdlib.h>

void shellSort(
    long long a[],
    int n
) {
    for (
        int gap = n / 2;
        gap > 0;
        gap /= 2
    ) {
        for (
            int i = gap;
            i < n;
            i++
        ) {
            long long temp = a[i];
            int j = i;

            while (
                j >= gap &&
                a[j - gap] > temp
            ) {
                a[j] = a[j - gap];
                j -= gap;
            }

            a[j] = temp;
        }
    }
}

int main() {
    long long *a = NULL;
    int n = 0;
    int capacity = 0;
    long long x;

    while (scanf("%lld", &x) == 1) {
        if (n == capacity) {
            capacity = capacity == 0
                ? 16
                : capacity * 2;

            long long *newArray = realloc(
                a,
                capacity * sizeof(long long)
            );

            if (newArray == NULL) {
                free(a);
                return 1;
            }

            a = newArray;
        }

        a[n++] = x;
    }

    if (n > 0) {
        shellSort(
            a,
            n
        );
    }

    printf(
        "%lld\n",
        n == 0 ? 0 : a[n - 1]
    );

    free(a);

    return 0;
}
