// Benchmark: Substring Search
// Category: Strings
// Algorithm: Naive Substring Search - O(n * m)

const fs = require("fs");

const input = fs
    .readFileSync(
        0,
        "utf8"
    )
    .trim();

const parts =
    input.split(/\s+/);

if (
    input.length === 0 ||
    parts.length < 2
) {
    process.exit(0);
}

const text = parts[0];
const pattern = parts[1];

function substringSearch(
    text,
    pattern
) {
    const n = text.length;
    const m = pattern.length;

    if (m === 0) {
        return 0;
    }

    if (m > n) {
        return -1;
    }

    for (
        let i = 0;
        i <= n - m;
        i++
    ) {
        let j = 0;

        while (
            j < m &&
            text[i + j] ===
            pattern[j]
        ) {
            j++;
        }

        if (j === m) {
            return i;
        }
    }

    return -1;
}

console.log(
    substringSearch(
        text,
        pattern
    )
);
