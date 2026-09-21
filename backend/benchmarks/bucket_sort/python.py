# Benchmark: Bucket Sort
# Category: Sorting
# Algorithm: Bucket Sort - O(n + k) average

import sys
import math


def insertion_sort(bucket):
    for i in range(
        1,
        len(bucket),
    ):
        key = bucket[i]
        j = i - 1

        while (
            j >= 0
            and bucket[j] > key
        ):
            bucket[j + 1] = bucket[j]
            j -= 1

        bucket[j + 1] = key


def bucket_sort(a):
    n = len(a)

    if n <= 1:
        return

    min_value = min(a)
    max_value = max(a)

    if min_value == max_value:
        return

    bucket_count = max(
        1,
        math.isqrt(n),
    )

    buckets = [
        []
        for _ in range(bucket_count)
    ]

    value_range = (
        max_value -
        min_value +
        1
    )

    for value in a:
        index = (
            (value - min_value) *
            bucket_count //
            value_range
        )

        if index >= bucket_count:
            index = bucket_count - 1

        buckets[index].append(value)

    position = 0

    for bucket in buckets:
        insertion_sort(bucket)

        for value in bucket:
            a[position] = value
            position += 1


a = [
    int(x)
    for x in sys.stdin.buffer
    .read()
    .split()
]

if a:
    bucket_sort(a)

print(
    a[-1] if a else 0
)
