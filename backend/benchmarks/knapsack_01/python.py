# Benchmark: 0/1 Knapsack
# Category: Dynamic Programming
# Algorithm: 0/1 Knapsack - O(n * capacity)

import sys

tokens = list(
    map(
        int,
        sys.stdin.buffer.read().split()
    )
)

if len(tokens) < 2:
    raise SystemExit

n = tokens[0]
capacity = tokens[1]

if n < 0 or capacity < 0:
    raise SystemExit

if len(tokens) < 2 + 2 * n:
    raise SystemExit

weights = tokens[2:2 + n]
values = tokens[2 + n:2 + 2 * n]

dp = [0] * (capacity + 1)

for weight, value in zip(weights, values):
    if weight <= 0:
        continue

    for c in range(
        capacity,
        weight - 1,
        -1
    ):
        candidate = (
            dp[c - weight] + value
        )

        if candidate > dp[c]:
            dp[c] = candidate

print(dp[capacity])
