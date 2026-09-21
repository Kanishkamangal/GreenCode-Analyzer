# Benchmark: Heap Sort
# Category: Sorting
# Algorithm: Heap Sort - O(n log n)

import sys


def heapify(a, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if (
        left < n
        and a[left] > a[largest]
    ):
        largest = left

    if (
        right < n
        and a[right] > a[largest]
    ):
        largest = right

    if largest != i:
        a[i], a[largest] = (
            a[largest],
            a[i],
        )

        heapify(
            a,
            n,
            largest,
        )


def heap_sort(a):
    n = len(a)

    for i in range(
        n // 2 - 1,
        -1,
        -1,
    ):
        heapify(
            a,
            n,
            i,
        )

    for i in range(
        n - 1,
        0,
        -1,
    ):
        a[0], a[i] = (
            a[i],
            a[0],
        )

        heapify(
            a,
            i,
            0,
        )


a = [
    int(x)
    for x in sys.stdin.buffer
    .read()
    .split()
]

if a:
    heap_sort(a)

print(
    a[-1] if a else 0
)
