# Benchmark: Counting Sort
# Category: Sorting
# Algorithm: Counting Sort - O(n + k)

import sys


def counting_sort(a):
    if len(a) <= 1:
        return

    min_value = min(a)
    max_value = max(a)

    value_range = (
        max_value - min_value + 1
    )

    count = [0] * value_range

    for value in a:
        count[
            value - min_value
        ] += 1

    index = 0

    for i in range(value_range):
        while count[i] > 0:
            a[index] = (
                i + min_value
            )

            index += 1
            count[i] -= 1


a = [
    int(x)
    for x in sys.stdin.buffer
    .read()
    .split()
]

if a:
    counting_sort(a)

print(
    a[-1] if a else 0
)
