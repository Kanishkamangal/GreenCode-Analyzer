// Benchmark: Quick Sort
// Category: Sorting
// Algorithm: Quick Sort - O(n log n) average

#include <stdio.h>
#include <stdlib.h>

void swapValues(long long *a, long long *b) {
    long long temp = *a;
    *a = *b;
    *b = temp;
}

int partition(long long a[], int low, int high) {
    long long pivot = a[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (a[j] <= pivot) {
            i++;
            swapValues(&a[i], &a[j]);
        }
    }

    swapValues(&a[i + 1], &a[high]);

    return i + 1;
}

void quickSort(long long a[], int low, int high) {
    if (low < high) {
        int pivotIndex = partition(a, low, high);

        quickSort(a, low, pivotIndex - 1);
        quickSort(a, pivotIndex + 1, high);
    }
}

int main() {
    long long *a = NULL;
    int n = 0;
    int capacity = 0;
    long long x;

    while (scanf("%lld", &x) == 1) {
        if (n == capacity) {
            capacity = capacity == 0 ? 16 : capacity * 2;

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
        quickSort(a, 0, n - 1);
    }

    printf("%lld\n", n == 0 ? 0 : a[n - 1]);

    free(a);

    return 0;
}
