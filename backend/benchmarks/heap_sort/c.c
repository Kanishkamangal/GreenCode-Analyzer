// Benchmark: Heap Sort
// Category: Sorting
// Algorithm: Heap Sort - O(n log n)

#include <stdio.h>
#include <stdlib.h>

void swapValues(long long *a, long long *b) {
    long long temp = *a;
    *a = *b;
    *b = temp;
}

void heapify(
    long long a[],
    int n,
    int i
) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && a[left] > a[largest]) {
        largest = left;
    }

    if (right < n && a[right] > a[largest]) {
        largest = right;
    }

    if (largest != i) {
        swapValues(
            &a[i],
            &a[largest]
        );

        heapify(
            a,
            n,
            largest
        );
    }
}

void heapSort(
    long long a[],
    int n
) {
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(
            a,
            n,
            i
        );
    }

    for (int i = n - 1; i > 0; i--) {
        swapValues(
            &a[0],
            &a[i]
        );

        heapify(
            a,
            i,
            0
        );
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
        heapSort(
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
