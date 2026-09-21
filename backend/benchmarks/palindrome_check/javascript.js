// Benchmark: Palindrome Check
// Category: Strings
// Algorithm: Two-Pointer Palindrome Check - O(n)

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

if (input.length === 0) {
    process.exit(0);
}

const s =
    input.split(/\s+/)[0];

let left = 0;
let right = s.length - 1;
let palindrome = true;

while (left < right) {
    if (s[left] !== s[right]) {
        palindrome = false;
        break;
    }

    left++;
    right--;
}

console.log(
    palindrome ? 1 : 0
);
