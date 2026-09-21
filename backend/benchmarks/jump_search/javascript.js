// Benchmark: Jump Search
// Category: Searching
// Algorithm: Jump Search - O(sqrt(n))

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

function jumpSearch(
    a,
    target
) {
    const n = a.length;

    if (n === 0) {
        return -1;
    }

    const step = Math.max(
        1,
        Math.floor(Math.sqrt(n))
    );

    let previous = 0;
    let current = step;

    while (
        previous < n &&
        a[Math.min(current, n) - 1]
            < target
    ) {
        previous = current;
        current += step;

        if (previous >= n) {
            return -1;
        }
    }

    const end =
        Math.min(current, n);

    for (
        let i = previous;
        i < end;
        i++
    ) {
        if (a[i] === target) {
            return i;
        }

        if (a[i] > target) {
            break;
        }
    }

    return -1;
}

console.log(
    jumpSearch(
        a,
        target
    )
);
