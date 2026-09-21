// Benchmark: Binary Search
// Category: Searching
// Algorithm: Binary Search - O(log n)

#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    if (scanf("%d", &n) != 1 || n < 0) {
        return 1;
    }

    long long *a = NULL;

    if (n > 0) {
        a = malloc(
            n * sizeof(long long)
        );

        if (a == NULL) {
            return 1;
        }
    }

    for (int i = 0; i < n; i++) {
        if (scanf("%lld", &a[i]) != 1) {
            free(a);
            return 1;
        }
    }

    long long target;

    if (scanf("%lld", &target) != 1) {
        free(a);
        return 1;
    }

    int left = 0;
    int right = n - 1;
    int result = -1;

    while (left <= right) {
        int mid =
            left + (right - left) / 2;

        if (a[mid] == target) {
            result = mid;
            break;
        }

        if (a[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    printf("%d\n", result);

    free(a);

    return 0;
}
