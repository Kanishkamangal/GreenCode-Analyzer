#include <stdio.h>
#include <stdlib.h>

int main() {
    long long *a = NULL;
    int n = 0, capacity = 0;
    long long x;

    while (scanf("%lld", &x) == 1) {
        if (n == capacity) {
            capacity = capacity == 0 ? 16 : capacity * 2;
            long long *temp = realloc(a, capacity * sizeof(long long));
            if (temp == NULL) {
                free(a);
                return 1;
            }
            a = temp;
        }
        a[n++] = x;
    }

    for (int i = 0; i < n - 1; i++) {
        int minIndex = i;
        for (int j = i + 1; j < n; j++) {
            if (a[j] < a[minIndex])
                minIndex = j;
        }

        if (minIndex != i) {
            long long temp = a[i];
            a[i] = a[minIndex];
            a[minIndex] = temp;
        }
    }

    printf("%lld", n == 0 ? 0 : a[n - 1]);
    free(a);
    return 0;
}
