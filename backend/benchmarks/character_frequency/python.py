# Benchmark: Character Frequency in String
# Category: Strings
# Algorithm: Linear Character Frequency Count - O(n)

import sys

values = (
    sys.stdin.buffer
    .read()
    .split()
)

if len(values) < 2:
    sys.exit(0)

s = values[0]
target = values[1][0]

frequency = 0

for ch in s:
    if ch == target:
        frequency += 1

print(
    frequency
)
