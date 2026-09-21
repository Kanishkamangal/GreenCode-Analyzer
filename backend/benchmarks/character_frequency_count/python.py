# Benchmark: Character Frequency Count
# Category: Character
# Algorithm: Linear Frequency Count - O(n)

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

count = 0

for ch in s:
    if ch == target:
        count += 1

print(count)
