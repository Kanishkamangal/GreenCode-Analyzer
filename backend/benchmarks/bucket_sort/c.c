// Benchmark: Bucket Sort
// Category: Sorting
// Algorithm: Bucket Sort - O(n + k) average

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct {
    long long *data;
    int size;
    int capacity;
} Bucket;

void insertBucket(
    Bucket *bucket,
    long long value
) {
    if (bucket->size == bucket->capacity) {
        bucket->capacity =
            bucket->capacity == 0
                ? 4
                : bucket->capacity * 2;

        long long *newData = realloc(
            bucket->data,
            bucket->capacity * sizeof(long long)
        );

        if (newData == NULL) {
            return;
        }

        bucket->data = newData;
    }

    bucket->data[bucket->size++] = value;
}

void insertionSort(
    long long a[],
    int n
) {
    for (int i = 1; i < n; i++) {
        long long key = a[i];
        int j = i - 1;

        while (
            j >= 0 &&
            a[j] > key
        ) {
            a[j + 1] = a[j];
            j--;
        }

        a[j + 1] = key;
    }
}

void bucketSort(
    long long a[],
    int n
) {
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

    if (minValue == maxValue) {
        return;
    }

    int bucketCount =
        (int)sqrt((double)n);

    if (bucketCount < 1) {
        bucketCount = 1;
    }

    Bucket *buckets = calloc(
        bucketCount,
        sizeof(Bucket)
    );

    if (buckets == NULL) {
        return;
    }

    unsigned long long range =
        (unsigned long long)(
            maxValue - minValue
        ) + 1ULL;

    for (int i = 0; i < n; i++) {
        unsigned long long offset =
            (unsigned long long)(
                a[i] - minValue
            );

        int index = (int)(
            (offset * bucketCount) /
            range
        );

        if (index >= bucketCount) {
            index = bucketCount - 1;
        }

        insertBucket(
            &buckets[index],
            a[i]
        );
    }

    int position = 0;

    for (
        int i = 0;
        i < bucketCount;
        i++
    ) {
        insertionSort(
            buckets[i].data,
            buckets[i].size
        );

        for (
            int j = 0;
            j < buckets[i].size;
            j++
        ) {
            a[position++] =
                buckets[i].data[j];
        }

        free(buckets[i].data);
    }

    free(buckets);
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
        bucketSort(a, n);
    }

    printf(
        "%lld\n",
        n == 0 ? 0 : a[n - 1]
    );

    free(a);

    return 0;
}
