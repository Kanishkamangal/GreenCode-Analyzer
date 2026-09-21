# Benchmark: Radix Sort
# Category: Sorting
# Algorithm: LSD Radix Sort - O(d * (n + b))

import sys


def radix_sort_non_negative(a):
    if len(a) <= 1:
        return

    max_value = max(a)
    exp = 1

    while max_value // exp > 0:
        output = [0] * len(a)
        count = [0] * 10

        for value in a:
            digit = (
                value // exp
            ) % 10

            count[digit] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(
            len(a) - 1,
            -1,
            -1,
        ):
            digit = (
                a[i] // exp
            ) % 10

            count[digit] -= 1

            output[
                count[digit]
            ] = a[i]

        for i in range(len(a)):
            a[i] = output[i]

        exp *= 10


def radix_sort(a):
    negative = []
    positive = []

    for value in a:
        if value < 0:
            negative.append(-value)
        else:
            positive.append(value)

    radix_sort_non_negative(
        negative
    )

    radix_sort_non_negative(
        positive
    )

    index = 0

    for i in range(
        len(negative) - 1,
        -1,
        -1,
    ):
        a[index] = -negative[i]
        index += 1

    for value in positive:
        a[index] = value
        index += 1


a = [
    int(x)
    for x in sys.stdin.buffer
    .read()
    .split()
]

if a:
    radix_sort(a)

print(
    a[-1] if a else 0
)
