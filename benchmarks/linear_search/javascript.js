// Benchmark: Linear Search
// Category: Searching
// Algorithm: Linear Search - O(n)

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

let result = -1;

for (let i = 0; i < n; i++) {
    if (a[i] === target) {
        result = i;
        break;
    }
}

console.log(result);
