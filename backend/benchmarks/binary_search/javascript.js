// Benchmark: Binary Search
// Category: Searching
// Algorithm: Binary Search - O(log n)

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

if (input.length === 0) {
    process.exit(0);
}

const values =
    input.split(/\s+/).map(Number);

let position = 0;

const n =
    values[position++];

const a =
    new Array(n);

for (let i = 0; i < n; i++) {
    a[i] =
        values[position++];
}

const target =
    values[position];

let left = 0;
let right = n - 1;
let result = -1;

while (left <= right) {
    const mid =
        left +
        Math.floor(
            (right - left) / 2
        );

    if (a[mid] === target) {
        result = mid;
        break;
    }

    if (a[mid] < target) {
        left = mid + 1;
    } else {
        right = mid - 1;
    }
}

console.log(result);
