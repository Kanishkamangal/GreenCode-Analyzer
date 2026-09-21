// Benchmark: 0/1 Knapsack
// Category: Dynamic Programming
// Algorithm: 0/1 Knapsack - O(n * capacity)

const fs = require("fs");

const tokens = fs
    .readFileSync(0, "utf8")
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map(Number);

if (tokens.length < 2)
    process.exit(0);

const n = tokens[0];
const capacity = tokens[1];

if (
    n < 0 ||
    capacity < 0 ||
    tokens.length < 2 + 2 * n
) {
    process.exit(0);
}

const weights =
    tokens.slice(2, 2 + n);

const values =
    tokens.slice(2 + n, 2 + 2 * n);

const dp =
    new Array(capacity + 1).fill(0);

for (let i = 0; i < n; i++) {
    const weight = weights[i];
    const value = values[i];

    if (weight <= 0)
        continue;

    for (
        let c = capacity;
        c >= weight;
        c--
    ) {
        const candidate =
            dp[c - weight] + value;

        if (candidate > dp[c])
            dp[c] = candidate;
    }
}

console.log(dp[capacity]);
