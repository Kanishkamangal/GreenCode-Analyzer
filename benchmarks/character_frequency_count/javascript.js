// Benchmark: Character Frequency Count
// Category: Character
// Algorithm: Linear Frequency Count - O(n)

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

if (input.length === 0) {
    process.exit(0);
}

const values =
    input.split(/\s+/);

if (values.length < 2) {
    process.exit(0);
}

const s = values[0];
const target = values[1][0];

let count = 0;

for (let i = 0; i < s.length; i++) {
    if (s[i] === target) {
        count++;
    }
}

console.log(count);
