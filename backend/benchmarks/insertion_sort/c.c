#include <stdio.h>
#include <stdlib.h>

int main() {
    long long *a = NULL;
    int n = 0, capacity = 0;
    long long x;

    while (scanf("%lld", &x) == 1) {
        if (n == capacity) {
            capacity = capacity == 0 ? 16 : capacity * 2;

            long long *temp = realloc(
                a,
                capacity * sizeof(long long)
            );

            if (temp == NULL) {
                free(a);
                return 1;
            }

            a = temp;
        }

        a[n++] = x;
    }

    for (int i = 1; i < n; i++) {
        long long key = a[i];
        int j = i - 1;

        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            j--;
        }

        a[j + 1] = key;
    }

    printf("%lld", n == 0 ? 0 : a[n - 1]);

    free(a);
    return 0;
}
