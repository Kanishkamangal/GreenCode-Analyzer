// Benchmark: Longest Palindromic Substring
// Category: Strings
// Algorithm: Expand Around Center - O(n^2)

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

if (input.length === 0) {
    process.exit(0);
}

const s =
    input.split(/\s+/)[0];

const n = s.length;

let bestStart = 0;
let bestLength = 1;

for (
    let center = 0;
    center < n;
    center++
) {
    let left = center;
    let right = center;

    while (
        left >= 0 &&
        right < n &&
        s[left] === s[right]
    ) {
        const length =
            right - left + 1;

        if (length > bestLength) {
            bestStart = left;
            bestLength = length;
        }

        left--;
        right++;
    }

    left = center;
    right = center + 1;

    while (
        left >= 0 &&
        right < n &&
        s[left] === s[right]
    ) {
        const length =
            right - left + 1;

        if (length > bestLength) {
            bestStart = left;
            bestLength = length;
        }

        left--;
        right++;
    }
}

let result = "";

for (
    let i = bestStart;
    i < bestStart + bestLength;
    i++
) {
    result += s[i];
}

console.log(result);
