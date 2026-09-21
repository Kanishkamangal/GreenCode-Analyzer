# Benchmark: Vowel or Consonant Check
# Category: Character
# Algorithm: Direct Character Check - O(1)

import sys

input_data = (
    sys.stdin
    .read()
    .strip()
)

if not input_data:
    sys.exit(0)

ch = input_data[0]

vowel = (
    ch == "a"
    or ch == "e"
    or ch == "i"
    or ch == "o"
    or ch == "u"
    or ch == "A"
    or ch == "E"
    or ch == "I"
    or ch == "O"
    or ch == "U"
)

print(
    1 if vowel else 0
)
