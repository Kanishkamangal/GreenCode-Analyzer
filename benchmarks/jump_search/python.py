# Benchmark: Jump Search
# Category: Searching
# Algorithm: Jump Search - O(sqrt(n))

import sys
import math


def jump_search(a, target):
    n = len(a)

    if n == 0:
        return -1

    step = max(
        1,
        math.isqrt(n),
    )

    previous = 0
    current = step

    while (
        previous < n
        and a[min(current, n) - 1]
        < target
    ):
        previous = current
        current += step

        if previous >= n:
            return -1

    end = min(
        current,
        n,
    )

    for i in range(
        previous,
        end,
    ):
        if a[i] == target:
            return i

        if a[i] > target:
            break

    return -1


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

print(
    jump_search(
        a,
        target,
    )
)
