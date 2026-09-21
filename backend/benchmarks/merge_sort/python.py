# Benchmark: Merge Sort
# Category: Sorting
# Algorithm: Merge Sort - O(n log n)

import sys


def merge(a, temp, left, mid, right):
    i = left
    j = mid + 1
    k = left

    while i <= mid and j <= right:
        if a[i] <= a[j]:
            temp[k] = a[i]
            i += 1
        else:
            temp[k] = a[j]
            j += 1

        k += 1

    while i <= mid:
        temp[k] = a[i]
        i += 1
        k += 1

    while j <= right:
        temp[k] = a[j]
        j += 1
        k += 1

    for index in range(left, right + 1):
        a[index] = temp[index]


def merge_sort(a, temp, left, right):
    if left >= right:
        return

    mid = left + (right - left) // 2

    merge_sort(a, temp, left, mid)
    merge_sort(a, temp, mid + 1, right)

    merge(a, temp, left, mid, right)


a = [
    int(x)
    for x in sys.stdin.buffer.read().split()
]

if a:
    temp = [0] * len(a)

    merge_sort(
        a,
        temp,
        0,
        len(a) - 1
    )

print(
    a[-1] if a else 0
)
