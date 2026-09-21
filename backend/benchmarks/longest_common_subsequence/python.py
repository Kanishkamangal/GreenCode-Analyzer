# Benchmark: Longest Common Subsequence
# Category: Strings
# Algorithm: Dynamic Programming LCS - O(n * m)

import sys

values = (
    sys.stdin.buffer
    .read()
    .split()
)

if len(values) < 2:
    sys.exit(0)

first = values[0]
second = values[1]

n = len(first)
m = len(second)

previous = [0] * (m + 1)
current = [0] * (m + 1)

for i in range(1, n + 1):
    current[0] = 0

    for j in range(1, m + 1):
        if (
            first[i - 1] ==
            second[j - 1]
        ):
            current[j] = (
                previous[j - 1] + 1
            )
        else:
            current[j] = max(
                previous[j],
                current[j - 1],
            )

    previous, current = (
        current,
        previous,
    )

print(
    previous[m]
)
