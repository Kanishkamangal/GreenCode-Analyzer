// Benchmark: Jump Search
// Category: Searching
// Algorithm: Jump Search - O(sqrt(n))

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int jumpSearch(
    long long a[],
    int n,
    long long target
) {
    if (n == 0) {
        return -1;
    }

    int step = (int)sqrt((double)n);

    if (step < 1) {
        step = 1;
    }

    int previous = 0;
    int current = step;

    while (
        previous < n &&
        a[(current < n ? current : n) - 1] < target
    ) {
        previous = current;
        current += step;

        if (previous >= n) {
            return -1;
        }
    }

    int end =
        current < n
            ? current
            : n;

    for (
        int i = previous;
        i < end;
        i++
    ) {
        if (a[i] == target) {
            return i;
        }

        if (a[i] > target) {
            break;
        }
    }

    return -1;
}

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

    int result =
        jumpSearch(
            a,
            n,
            target
        );

    printf("%d\n", result);

    free(a);

    return 0;
}
