// Benchmark: Longest Common Prefix
// Category: Strings
// Algorithm: Vertical Scanning - O(total characters)

const fs = require("fs");

const input = fs
    .readFileSync(0, "utf8")
    .trim();

if (input.length === 0) {
    process.exit(0);
}

const values =
    input.split(/\s+/);

let inputPosition = 0;

const n =
    Number(values[inputPosition++]);

if (n <= 0) {
    console.log("");
    process.exit(0);
}

const strings =
    new Array(n);

for (let i = 0; i < n; i++) {
    strings[i] =
        values[inputPosition++];
}

let prefixLength = 0;

for (
    let position = 0;
    position < strings[0].length;
    position++
) {
    const current =
        strings[0][position];

    let matches = true;

    for (let i = 1; i < n; i++) {
        if (
            position >= strings[i].length ||
            strings[i][position] !== current
        ) {
            matches = false;
            break;
        }
    }

    if (!matches) {
        break;
    }

    prefixLength++;
}

let result = "";

for (
    let i = 0;
    i < prefixLength;
    i++
) {
    result += strings[0][i];
}

console.log(result);
