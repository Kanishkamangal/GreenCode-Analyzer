# Benchmark: Substring Search
# Category: Strings
# Algorithm: Naive Substring Search - O(n * m)

import sys


def substring_search(
    text,
    pattern,
):
    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0

    if m > n:
        return -1

    for i in range(
        n - m + 1
    ):
        j = 0

        while (
            j < m
            and text[i + j]
            == pattern[j]
        ):
            j += 1

        if j == m:
            return i

    return -1


values = (
    sys.stdin.buffer
    .read()
    .split()
)

if len(values) < 2:
    sys.exit(0)

text = values[0]
pattern = values[1]

print(
    substring_search(
        text,
        pattern,
    )
)
