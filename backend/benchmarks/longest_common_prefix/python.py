# Benchmark: Longest Common Prefix
# Category: Strings
# Algorithm: Vertical Scanning - O(total characters)

import sys

values = (
    sys.stdin.buffer
    .read()
    .split()
)

if not values:
    sys.exit(0)

input_position = 0

n = int(
    values[input_position]
)

input_position += 1

if n <= 0:
    print()
    sys.exit(0)

strings = values[
    input_position:
    input_position + n
]

prefix_length = 0

for position in range(
    len(strings[0])
):
    current = strings[0][position]

    matches = True

    for i in range(1, n):
        if (
            position >= len(strings[i])
            or strings[i][position]
            != current
        ):
            matches = False
            break

    if not matches:
        break

    prefix_length += 1

sys.stdout.buffer.write(
    strings[0][:prefix_length]
    + b"\n"
)
