// Benchmark: Longest Common Subsequence
// Category: Strings
// Algorithm: Dynamic Programming LCS - O(n * m)

const fs = require("fs");

const input = fs
    .readFileSync(
        0,
        "utf8"
    )
    .trim();

if (input.length === 0) {
    process.exit(0);
}

const values =
    input.split(/\s+/);

if (values.length < 2) {
    process.exit(0);
}

const first = values[0];
const second = values[1];

const n = first.length;
const m = second.length;

let previous =
    new Array(m + 1).fill(0);

let current =
    new Array(m + 1).fill(0);

for (let i = 1; i <= n; i++) {
    current[0] = 0;

    for (let j = 1; j <= m; j++) {
        if (
            first[i - 1] ===
            second[j - 1]
        ) {
            current[j] =
                previous[j - 1] + 1;
        } else {
            current[j] =
                Math.max(
                    previous[j],
                    current[j - 1]
                );
        }
    }

    const temp = previous;
    previous = current;
    current = temp;
}

console.log(
    previous[m]
);
