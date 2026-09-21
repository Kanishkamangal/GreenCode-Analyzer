# Benchmark: Longest Palindromic Substring
# Category: Strings
# Algorithm: Expand Around Center - O(n^2)

import sys

values = (
    sys.stdin.buffer
    .read()
    .split()
)

if not values:
    sys.exit(0)

s = values[0]

n = len(s)
best_start = 0
best_length = 1

for center in range(n):
    left = center
    right = center

    while (
        left >= 0
        and right < n
        and s[left] == s[right]
    ):
        length = right - left + 1

        if length > best_length:
            best_start = left
            best_length = length

        left -= 1
        right += 1

    left = center
    right = center + 1

    while (
        left >= 0
        and right < n
        and s[left] == s[right]
    ):
        length = right - left + 1

        if length > best_length:
            best_start = left
            best_length = length

        left -= 1
        right += 1

sys.stdout.buffer.write(
    s[
        best_start:
        best_start + best_length
    ] + b"\n"
)
