# Benchmark: String Reverse
# Category: Strings
# Algorithm: Two-Pointer String Reverse - O(n)

import sys

values = (
    sys.stdin.buffer
    .read()
    .split()
)

if not values:
    sys.exit(0)

s = bytearray(values[0])

left = 0
right = len(s) - 1

while left < right:
    temp = s[left]

    s[left] = s[right]
    s[right] = temp

    left += 1
    right -= 1

sys.stdout.buffer.write(
    bytes(s) + b"\n"
)
