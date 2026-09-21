# Benchmark: Shell Sort
# Category: Sorting
# Algorithm: Shell Sort - Gap-based

import sys


def shell_sort(a):
    n = len(a)
    gap = n // 2

    while gap > 0:
        for i in range(
            gap,
            n,
        ):
            temp = a[i]
            j = i

            while (
                j >= gap
                and a[j - gap] > temp
            ):
                a[j] = a[j - gap]
                j -= gap

            a[j] = temp

        gap //= 2


a = [
    int(x)
    for x in sys.stdin.buffer
    .read()
    .split()
]

if a:
    shell_sort(a)

print(
    a[-1] if a else 0
)
