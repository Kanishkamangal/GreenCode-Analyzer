// Benchmark: 0/1 Knapsack
// Category: Dynamic Programming
// Algorithm: 0/1 Knapsack - O(n * capacity)

#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, capacity;

    if (scanf("%d %d", &n, &capacity) != 2 ||
        n < 0 || capacity < 0) {
        return 0;
    }

    int *weights =
        (int *)malloc((size_t)n * sizeof(int));

    long long *values =
        (long long *)malloc((size_t)n * sizeof(long long));

    for (int i = 0; i < n; i++) {
        if (scanf("%d", &weights[i]) != 1) {
            free(weights);
            free(values);
            return 0;
        }
    }

    for (int i = 0; i < n; i++) {
        if (scanf("%lld", &values[i]) != 1) {
            free(weights);
            free(values);
            return 0;
        }
    }

    long long *dp =
        (long long *)calloc(
            (size_t)capacity + 1,
            sizeof(long long)
        );

    for (int i = 0; i < n; i++) {
        int weight = weights[i];
        long long value = values[i];

        if (weight <= 0)
            continue;

        for (int c = capacity; c >= weight; c--) {
            long long candidate =
                dp[c - weight] + value;

            if (candidate > dp[c])
                dp[c] = candidate;
        }
    }

    printf("%lld\n", dp[capacity]);

    free(weights);
    free(values);
    free(dp);

    return 0;
}
