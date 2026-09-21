// Benchmark: Radix Sort
// Category: Sorting
// Algorithm: LSD Radix Sort - O(d * (n + b))

#include <stdio.h>
#include <stdlib.h>

void radixSortNonNegative(
    unsigned long long a[],
    int n
) {
    if (n <= 1) {
        return;
    }

    unsigned long long maxValue = a[0];

    for (int i = 1; i < n; i++) {
        if (a[i] > maxValue) {
            maxValue = a[i];
        }
    }

    unsigned long long *output = malloc(
        n * sizeof(unsigned long long)
    );

    if (output == NULL) {
        return;
    }

    for (
        unsigned long long exp = 1;
        maxValue / exp > 0;
    ) {
        int count[10] = {0};

        for (int i = 0; i < n; i++) {
            int digit =
                (int)((a[i] / exp) % 10);

            count[digit]++;
        }

        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        for (int i = n - 1; i >= 0; i--) {
            int digit =
                (int)((a[i] / exp) % 10);

            output[
                --count[digit]
            ] = a[i];
        }

        for (int i = 0; i < n; i++) {
            a[i] = output[i];
        }

        if (exp > maxValue / 10) {
            break;
        }

        exp *= 10;
    }

    free(output);
}

void radixSort(
    long long a[],
    int n
) {
    if (n <= 1) {
        return;
    }

    unsigned long long *negative = malloc(
        n * sizeof(unsigned long long)
    );

    unsigned long long *positive = malloc(
        n * sizeof(unsigned long long)
    );

    if (
        negative == NULL ||
        positive == NULL
    ) {
        free(negative);
        free(positive);
        return;
    }

    int negativeCount = 0;
    int positiveCount = 0;

    for (int i = 0; i < n; i++) {
        if (a[i] < 0) {
            negative[negativeCount++] =
                0ULL - (unsigned long long)a[i];
        } else {
            positive[positiveCount++] =
                (unsigned long long)a[i];
        }
    }

    radixSortNonNegative(
        negative,
        negativeCount
    );

    radixSortNonNegative(
        positive,
        positiveCount
    );

    int index = 0;

    for (
        int i = negativeCount - 1;
        i >= 0;
        i--
    ) {
        a[index++] =
            -(long long)negative[i];
    }

    for (
        int i = 0;
        i < positiveCount;
        i++
    ) {
        a[index++] =
            (long long)positive[i];
    }

    free(negative);
    free(positive);
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
        radixSort(a, n);
    }

    printf(
        "%lld\n",
        n == 0 ? 0 : a[n - 1]
    );

    free(a);

    return 0;
}
