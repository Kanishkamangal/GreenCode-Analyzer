# Benchmark: Palindrome Check
# Category: Strings
# Algorithm: Two-Pointer Palindrome Check - O(n)

import sys

values = (
    sys.stdin.buffer
    .read()
    .split()
)

if not values:
    sys.exit(0)

s = values[0]

left = 0
right = len(s) - 1
palindrome = True

while left < right:
    if s[left] != s[right]:
        palindrome = False
        break

    left += 1
    right -= 1

print(
    1 if palindrome else 0
)
