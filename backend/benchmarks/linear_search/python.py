# Benchmark: Linear Search
# Category: Searching
# Algorithm: Linear Search - O(n)

import sys

values = [
    int(x)
    for x in sys.stdin.buffer
    .read()
    .split()
]

if not values:
    sys.exit(0)

position = 0

n = values[position]
position += 1

a = values[
    position:
    position + n
]

position += n

target = values[position]

result = -1

for i in range(n):
    if a[i] == target:
        result = i
        break

print(result)
