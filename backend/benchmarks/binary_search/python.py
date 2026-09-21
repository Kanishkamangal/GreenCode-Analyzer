# Benchmark: Binary Search
# Category: Searching
# Algorithm: Binary Search - O(log n)

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

left = 0
right = n - 1
result = -1

while left <= right:
    mid = (
        left +
        (right - left) // 2
    )

    if a[mid] == target:
        result = mid
        break

    if a[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

print(result)
