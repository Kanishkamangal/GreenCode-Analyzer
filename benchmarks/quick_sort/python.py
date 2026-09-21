# Benchmark: Quick Sort
# Category: Sorting
# Algorithm: Quick Sort - O(n log n) average

import sys


def partition(a, low, high):
    pivot = a[high]
    i = low - 1

    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]

    a[i + 1], a[high] = (
        a[high],
        a[i + 1],
    )

    return i + 1


def quick_sort(a, low, high):
    if low < high:
        pivot_index = partition(
            a,
            low,
            high,
        )

        quick_sort(
            a,
            low,
            pivot_index - 1,
        )

        quick_sort(
            a,
            pivot_index + 1,
            high,
        )


a = [
    int(x)
    for x in sys.stdin.buffer.read().split()
]

if a:
    quick_sort(
        a,
        0,
        len(a) - 1,
    )

print(
    a[-1] if a else 0
)
