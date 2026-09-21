// Benchmark: Anagram Check
// Category: String
// Algorithm: Anagram Check - O(n)

const fs = require("fs");

const tokens = fs.readFileSync(0, "utf8").trim().split(/\s+/);

if (tokens.length < 2) {
    console.log(0);
    process.exit(0);
}

const s1 = tokens[0];
const s2 = tokens[1];

if (s1.length !== s2.length) {
    console.log(0);
    process.exit(0);
}

const count = new Map();

for (const ch of s1)
    count.set(ch, (count.get(ch) || 0) + 1);

for (const ch of s2)
    count.set(ch, (count.get(ch) || 0) - 1);

let valid = true;

for (const value of count.values()) {
    if (value !== 0) {
        valid = false;
        break;
    }
}

console.log(valid ? 1 : 0);
