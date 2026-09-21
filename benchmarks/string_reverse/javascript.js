// Benchmark: String Reverse
// Category: Strings
// Algorithm: Two-Pointer String Reverse - O(n)

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

if (input.length === 0) {
    process.exit(0);
}

const s =
    input.split(/\s+/)[0];

const chars =
    s.split("");

let left = 0;
let right =
    chars.length - 1;

while (left < right) {
    const temp =
        chars[left];

    chars[left] =
        chars[right];

    chars[right] =
        temp;

    left++;
    right--;
}

console.log(
    chars.join("")
);
