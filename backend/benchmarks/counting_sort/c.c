// Benchmark: Counting Sort
// Category: Sorting
// Algorithm: Counting Sort - O(n + k)

#include <stdio.h>
#include <stdlib.h>

void countingSort(long long a[], int n) {
    if (n <= 1) {
        return;
    }

    long long minValue = a[0];
    long long maxValue = a[0];

    for (int i = 1; i < n; i++) {
        if (a[i] < minValue) {
            minValue = a[i];
        }

        if (a[i] > maxValue) {
            maxValue = a[i];
        }
    }

    size_t range =
        (size_t)(maxValue - minValue + 1);

    size_t *count = calloc(
        range,
        sizeof(size_t)
    );

    if (count == NULL) {
        return;
    }

    for (int i = 0; i < n; i++) {
        count[a[i] - minValue]++;
    }

    int index = 0;

    for (size_t i = 0; i < range; i++) {
        while (count[i] > 0) {
            a[index++] =
                (long long)i + minValue;

            count[i]--;
        }
    }

    free(count);
}

int main() {
    long long *a = NULL;
    int n = 0;
    int capacity = 0;
    long long x;

    while (scanf("%lld", &x) == 1) {
        if (n == capacity) {
            capacity =
                capacity == 0
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
        countingSort(a, n);
    }

    printf(
        "%lld\n",
        n == 0 ? 0 : a[n - 1]
    );

    free(a);

    return 0;
}
