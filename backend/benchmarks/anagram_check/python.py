# Benchmark: Anagram Check
# Category: String
# Algorithm: Anagram Check - O(n)

import sys

tokens = sys.stdin.read().split()

if len(tokens) < 2:
    print(0)
    raise SystemExit

s1, s2 = tokens[0], tokens[1]

if len(s1) != len(s2):
    print(0)
    raise SystemExit

count = {}

for ch in s1:
    count[ch] = count.get(ch, 0) + 1

for ch in s2:
    count[ch] = count.get(ch, 0) - 1

print(1 if all(value == 0 for value in count.values()) else 0)
